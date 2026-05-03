#!/usr/bin/env python3
"""App-Forge Bridge — local HTTP service that scaffolds self-contained HTML
applications from natural-language prompts using built-in templates.

No network access required at forge time. No LLM calls.

Endpoints:
    POST /forge   {"prompt": "..."}
                  -> streamed text/html (a single complete HTML document)
                     header X-Forge-Template names the template that was used.
    POST /save    {"category": "...", "filename": "...", "html": "..."}
                  -> {"ok": true, "path": "apps/<cat>/<file>.html",
                      "created": true|false}

Run:
    python3 scripts/forge-bridge.py

The server binds to 127.0.0.1:7711 only. CORS-permissive so localhost pages
served on any port can talk to it.
"""

import html as html_mod
import json
import os
import re
import sys
import time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

HOST = "127.0.0.1"
PORT = 7711

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))

# Categories that exist under apps/ in the repo. Saving outside this list is
# refused.
ALLOWED_CATEGORIES = {
    "games", "productivity", "business", "development", "media",
    "education", "ai-tools", "health", "utilities",
    "p2p-world", "quantum-worlds", "index-variants",
}

# Filename must be a single segment, lowercase, hyphenated, ending in .html.
FILENAME_RE = re.compile(r"^[a-z0-9][a-z0-9-]*\.html$")
SLUG_STRIP_RE = re.compile(r"[^a-z0-9-]+")

# ---------------------------------------------------------------------------
# Theme palettes. Keys are matched by detect_theme() against the prompt.
# ---------------------------------------------------------------------------
THEMES = {
    "vampire":   {"bg": "#0d0608", "panel": "#1a0c10", "fg": "#f3e2e2",
                  "muted": "#a47d7d", "accent": "#b51d2a", "accent2": "#3a0a12",
                  "ring": "#e84a5f"},
    "neon":      {"bg": "#06061a", "panel": "#0e0e2a", "fg": "#e6f7ff",
                  "muted": "#7d8aa8", "accent": "#ff2bd6", "accent2": "#22e6ff",
                  "ring": "#22e6ff"},
    "cyberpunk": {"bg": "#06061a", "panel": "#0e0e2a", "fg": "#e6f7ff",
                  "muted": "#7d8aa8", "accent": "#ff2bd6", "accent2": "#22e6ff",
                  "ring": "#22e6ff"},
    "forest":    {"bg": "#0d1a10", "panel": "#143a22", "fg": "#e8f3e6",
                  "muted": "#9ab8a0", "accent": "#3fbf6e", "accent2": "#1f6b3a",
                  "ring": "#7ee29b"},
    "ocean":     {"bg": "#06121f", "panel": "#0e2238", "fg": "#e6f1fb",
                  "muted": "#9ab1c8", "accent": "#2ba9e8", "accent2": "#0c4f7a",
                  "ring": "#5fd4ff"},
    "sunset":    {"bg": "#1a0a0e", "panel": "#2a1014", "fg": "#fbe9d8",
                  "muted": "#c69a7a", "accent": "#ff7a3a", "accent2": "#b53a3a",
                  "ring": "#ffb073"},
    "pastel":    {"bg": "#fff7f9", "panel": "#ffeef4", "fg": "#3a2a32",
                  "muted": "#9a8a90", "accent": "#ff7eb6", "accent2": "#7ec4ff",
                  "ring": "#ff7eb6"},
    "minimal":   {"bg": "#fafafa", "panel": "#ffffff", "fg": "#1a1a1a",
                  "muted": "#6a6a6a", "accent": "#1a1a1a", "accent2": "#9a9a9a",
                  "ring": "#1a1a1a"},
    "dark":      {"bg": "#0e0e10", "panel": "#16161c", "fg": "#e6e6ee",
                  "muted": "#8a8aa0", "accent": "#7c5bff", "accent2": "#22c3ff",
                  "ring": "#9c80ff"},
    "default":   {"bg": "#0e0e10", "panel": "#16161c", "fg": "#e6e6ee",
                  "muted": "#8a8aa0", "accent": "#7c5bff", "accent2": "#22c3ff",
                  "ring": "#9c80ff"},
}

# Keyword groups that pick a specific theme.
THEME_SYNONYMS = {
    "vampire":   ["vampire", "blood", "gothic", "dracula", "coffin"],
    "neon":      ["neon", "cyber", "cyberpunk", "synthwave", "retrowave"],
    "forest":    ["forest", "nature", "leaf", "garden", "jungle", "moss"],
    "ocean":     ["ocean", "sea", "aqua", "marine", "water", "wave", "beach"],
    "sunset":    ["sunset", "fire", "ember", "lava", "warm", "autumn"],
    "pastel":    ["pastel", "soft", "kawaii", "candy", "cute"],
    "minimal":   ["minimal", "monochrome", "mono", "simple", "clean"],
    "dark":      ["dark", "night", "shadow", "midnight", "stealth"],
}

# Template selection. First template whose keyword matches wins.
TEMPLATE_KEYWORDS = [
    ("timer",      ["timer", "pomodoro", "stopwatch", "countdown", "clock", "alarm"]),
    ("calculator", ["calculator", "calc", "compute"]),
    ("drawing",    ["drawing", "draw", "paint", "sketch", "canvas", "doodle"]),
    ("chat",       ["chat", "messenger", "messaging", "journal", "diary", "log"]),
    ("dashboard",  ["dashboard", "stats", "metrics", "tracker", "kpi", "widgets"]),
    ("game",       ["game", "arcade", "shooter", "clicker", "puzzle", "play"]),
    ("list",       ["list", "todo", "to-do", "tasks", "task", "checklist", "notes"]),
]
SUPPORTED_TEMPLATES = [name for name, _ in TEMPLATE_KEYWORDS]

FILLER = {"a", "an", "the", "of", "for", "with", "and", "or", "to",
          "my", "our", "your", "i", "want", "need", "make", "build", "create"}


def detect_template(prompt: str) -> str:
    p = prompt.lower()
    for name, words in TEMPLATE_KEYWORDS:
        for w in words:
            if re.search(rf"\b{re.escape(w)}\b", p):
                return name
    return "list"


def detect_theme(prompt: str):
    p = prompt.lower()
    for name in THEMES:
        if name == "default":
            continue
        if re.search(rf"\b{re.escape(name)}\b", p):
            return name, THEMES[name]
    for name, syns in THEME_SYNONYMS.items():
        for s in syns:
            if re.search(rf"\b{re.escape(s)}\b", p):
                return name, THEMES[name]
    return "default", THEMES["default"]


def make_title(prompt: str) -> str:
    cleaned = re.sub(r"[^\w\s-]", " ", prompt).strip()
    if not cleaned:
        return "Forged App"
    words = [w for w in cleaned.split() if w.lower() not in FILLER]
    if not words:
        words = cleaned.split()
    words = words[:6]
    return " ".join(w.capitalize() for w in words)


def make_app_name(title: str) -> str:
    slug = title.lower().replace(" ", "-")
    slug = SLUG_STRIP_RE.sub("", slug)
    slug = slug.strip("-") or "forged-app"
    return slug


def render_template(template_name: str, prompt: str):
    title = make_title(prompt)
    app_name = make_app_name(title)
    theme_name, theme = detect_theme(prompt)
    tpl = TEMPLATES[template_name]
    subs = {
        "__TITLE__": title,
        "__APP_NAME__": app_name,
        "__THEME__": theme_name,
        "__TEMPLATE__": template_name,
        "__PROMPT__": html_mod.escape(prompt),
        "__C_BG__": theme["bg"],
        "__C_PANEL__": theme["panel"],
        "__C_FG__": theme["fg"],
        "__C_MUTED__": theme["muted"],
        "__C_ACCENT__": theme["accent"],
        "__C_ACCENT2__": theme["accent2"],
        "__C_RING__": theme["ring"],
    }
    out = tpl
    for k, v in subs.items():
        out = out.replace(k, v)
    return out, theme_name


# ---------------------------------------------------------------------------
# Templates. Each is a complete self-contained HTML document with a
# data-controls bar, exportData/importData, localStorage keyed on APP_NAME,
# and responsive CSS. Tokens are __NAME__ — substituted before sending.
# ---------------------------------------------------------------------------

_BASE_HEAD_CSS = r"""
* { margin: 0; padding: 0; box-sizing: border-box; }
body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
       background: __C_BG__; color: __C_FG__; min-height: 100vh; padding: 72px 16px 24px;
       line-height: 1.45; }
.data-controls { position: fixed; top: 10px; right: 10px; z-index: 1000; display: flex; gap: 8px; }
.data-controls button { padding: 8px 14px; border: 1px solid __C_RING__;
       background: __C_PANEL__; color: __C_FG__; border-radius: 8px; cursor: pointer; font: inherit; }
.data-controls button:hover { background: __C_RING__; color: __C_BG__; }
header.app-head { max-width: 720px; margin: 0 auto 16px; padding: 0 4px; }
header.app-head h1 { font-size: clamp(1.4em, 4vw, 2em); }
header.app-head .sub { color: __C_MUTED__; font-size: .9em; margin-top: 4px; }
"""

_BASE_DATA_BAR = r"""
<div class="data-controls">
  <button onclick="exportData()" aria-label="Export data">Export</button>
  <button onclick="document.getElementById('importFile').click()" aria-label="Import data">Import</button>
  <input type="file" id="importFile" accept=".json" style="display:none" onchange="importData(event)">
</div>
"""

_BASE_DATA_JS = r"""
const APP_NAME = '__APP_NAME__';
let appData = JSON.parse(localStorage.getItem(APP_NAME) || 'null') || __INITIAL_DATA__;
function saveData() { localStorage.setItem(APP_NAME, JSON.stringify(appData)); }
function exportData() {
  const blob = new Blob([JSON.stringify(appData, null, 2)], {type:'application/json'});
  const url = URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url;
  a.download = APP_NAME + '-data-' + new Date().toISOString().split('T')[0] + '.json';
  document.body.appendChild(a); a.click(); a.remove();
  URL.revokeObjectURL(url);
}
function importData(ev) {
  const f = ev.target.files && ev.target.files[0]; if (!f) return;
  const r = new FileReader();
  r.onload = e => {
    try { appData = JSON.parse(e.target.result); saveData(); location.reload(); }
    catch (err) { alert('Invalid JSON file: ' + err.message); }
  };
  r.readAsText(f);
}
"""


def _build(body_html: str, scripts: str, extra_css: str = "",
           initial_data: str = "{}") -> str:
    return ("<!DOCTYPE html>\n"
            "<html lang=\"en\">\n<head>\n"
            "<meta charset=\"UTF-8\">\n"
            "<meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\">\n"
            "<title>__TITLE__</title>\n"
            "<style>" + _BASE_HEAD_CSS + extra_css + "</style>\n"
            "</head>\n<body>\n"
            + _BASE_DATA_BAR
            + "<header class=\"app-head\"><h1>__TITLE__</h1>"
              "<div class=\"sub\">__PROMPT__</div></header>\n"
            + body_html
            + "\n<script>\n"
            + _BASE_DATA_JS.replace("__INITIAL_DATA__", initial_data)
            + scripts
            + "\n</script>\n</body>\n</html>\n")


# ---------- timer ----------------------------------------------------------
TPL_TIMER = _build(
    body_html=r"""
<main class="app">
  <div class="modes" id="modes">
    <button data-mode="work" class="active" type="button">Focus</button>
    <button data-mode="short" type="button">Short break</button>
    <button data-mode="long" type="button">Long break</button>
  </div>
  <div class="dial" id="dial" aria-live="polite">25:00</div>
  <div class="actions">
    <button id="startBtn" class="primary" type="button">Start</button>
    <button id="resetBtn" class="ghost" type="button">Reset</button>
  </div>
  <div class="settings">
    <label>Focus (min)<input type="number" id="workMin" min="1" max="180" value="25"></label>
    <label>Short break (min)<input type="number" id="shortMin" min="1" max="60" value="5"></label>
    <label>Long break (min)<input type="number" id="longMin" min="1" max="120" value="15"></label>
    <label>Cycles before long<input type="number" id="cycles" min="1" max="12" value="4"></label>
  </div>
  <section class="history">
    <h3>Recent sessions</h3>
    <ul id="historyList"><li class="empty">No sessions yet.</li></ul>
  </section>
</main>
""",
    extra_css=r"""
.app { max-width: 540px; margin: 0 auto; background: __C_PANEL__;
       border: 1px solid __C_ACCENT2__; border-radius: 16px; padding: 28px;
       box-shadow: 0 12px 40px rgba(0,0,0,.3); }
.modes { display: flex; gap: 8px; justify-content: center; margin-bottom: 14px; flex-wrap: wrap; }
.modes button { padding: 8px 14px; border: 1px solid __C_ACCENT2__; background: transparent;
       color: __C_FG__; border-radius: 999px; cursor: pointer; font: inherit; }
.modes button.active { background: __C_ACCENT__; color: __C_BG__; border-color: __C_ACCENT__; }
.dial { font-variant-numeric: tabular-nums; font-size: clamp(56px, 14vw, 96px);
        text-align: center; padding: 18px 0; color: __C_ACCENT__; letter-spacing: 2px; }
.actions { display: flex; gap: 10px; justify-content: center; margin-bottom: 18px; flex-wrap: wrap; }
.actions .primary { padding: 12px 26px; border: 0; background: __C_ACCENT__; color: __C_BG__;
        border-radius: 10px; cursor: pointer; font: inherit; font-weight: 700; }
.actions .ghost { padding: 12px 22px; background: transparent; color: __C_FG__;
        border: 1px solid __C_ACCENT2__; border-radius: 10px; cursor: pointer; font: inherit; }
.settings { display: grid; grid-template-columns: repeat(2, 1fr); gap: 10px; margin: 16px 0; }
.settings label { display: flex; flex-direction: column; gap: 4px; font-size: .85em; color: __C_MUTED__; }
.settings input { padding: 8px; background: __C_BG__; color: __C_FG__;
        border: 1px solid __C_ACCENT2__; border-radius: 6px; font: inherit; }
.history { margin-top: 12px; max-height: 180px; overflow: auto;
        border-top: 1px solid __C_ACCENT2__; padding-top: 12px; }
.history h3 { font-size: .9em; color: __C_MUTED__; margin-bottom: 6px; }
.history ul { list-style: none; }
.history li { padding: 4px 0; font-size: .9em; border-bottom: 1px dashed __C_ACCENT2__; }
.history li.empty { color: __C_MUTED__; }
@media (max-width: 600px) { .app { padding: 18px; } .settings { grid-template-columns: 1fr; } }
""",
    initial_data='{"settings":{"workMin":25,"shortMin":5,"longMin":15,"cycles":4},"history":[],"cycleCount":0}',
    scripts=r"""
const dial = document.getElementById('dial');
const startBtn = document.getElementById('startBtn');
const resetBtn = document.getElementById('resetBtn');
const modes = document.getElementById('modes');
const inputs = {
  workMin: document.getElementById('workMin'),
  shortMin: document.getElementById('shortMin'),
  longMin: document.getElementById('longMin'),
  cycles: document.getElementById('cycles'),
};
let mode = 'work', remaining = 0, ticking = null;
for (const k of Object.keys(inputs)) {
  inputs[k].value = appData.settings[k];
  inputs[k].addEventListener('change', () => {
    appData.settings[k] = Math.max(1, parseInt(inputs[k].value, 10) || 1);
    saveData(); if (!ticking) setMode(mode);
  });
}
function fmt(s) { const m = Math.floor(s / 60), r = s % 60;
  return String(m).padStart(2, '0') + ':' + String(r).padStart(2, '0'); }
function setMode(m) {
  mode = m;
  for (const b of modes.children) b.classList.toggle('active', b.dataset.mode === m);
  const map = { work: 'workMin', short: 'shortMin', long: 'longMin' };
  remaining = appData.settings[map[m]] * 60;
  dial.textContent = fmt(remaining);
  document.title = fmt(remaining) + ' • __TITLE__';
}
modes.addEventListener('click', e => {
  const b = e.target.closest('button[data-mode]'); if (!b) return;
  stop(); setMode(b.dataset.mode);
});
function tick() {
  remaining--; dial.textContent = fmt(remaining);
  document.title = fmt(remaining) + ' • __TITLE__';
  if (remaining <= 0) { stop(); finish(); }
}
function start() {
  if (ticking) return;
  if (remaining <= 0) setMode(mode);
  startBtn.textContent = 'Pause';
  ticking = setInterval(tick, 1000);
}
function stop() {
  if (ticking) { clearInterval(ticking); ticking = null; }
  startBtn.textContent = 'Start';
}
function beep() {
  try {
    const ac = new (window.AudioContext || window.webkitAudioContext)();
    const o = ac.createOscillator(); o.frequency.value = 660;
    const g = ac.createGain(); g.gain.value = 0.12;
    o.connect(g); g.connect(ac.destination); o.start();
    setTimeout(() => { o.stop(); ac.close(); }, 250);
  } catch (e) { /* no audio */ }
}
function finish() {
  appData.history.unshift({ mode, at: new Date().toISOString() });
  appData.history = appData.history.slice(0, 30);
  if (mode === 'work') {
    appData.cycleCount = (appData.cycleCount || 0) + 1;
    setMode((appData.cycleCount % appData.settings.cycles === 0) ? 'long' : 'short');
  } else {
    setMode('work');
  }
  saveData(); renderHistory(); beep();
}
startBtn.addEventListener('click', () => { ticking ? stop() : start(); });
resetBtn.addEventListener('click', () => { stop(); setMode(mode); });
function renderHistory() {
  const ul = document.getElementById('historyList');
  if (!appData.history.length) {
    ul.innerHTML = '<li class="empty">No sessions yet.</li>'; return;
  }
  ul.innerHTML = appData.history.map(h => {
    const d = new Date(h.at);
    return '<li>' + h.mode + ' \u2022 ' + d.toLocaleString() + '</li>';
  }).join('');
}
setMode('work'); renderHistory();
""",
)


# ---------- list (todo / checklist) ---------------------------------------
TPL_LIST = _build(
    body_html=r"""
<main class="app">
  <form id="addForm" class="add">
    <input type="text" id="newItem" placeholder="What needs doing?" autocomplete="off" required>
    <button type="submit">Add</button>
  </form>
  <div class="filters">
    <button data-filter="all" class="active" type="button">All</button>
    <button data-filter="open" type="button">Open</button>
    <button data-filter="done" type="button">Done</button>
    <span class="grow"></span>
    <button id="clearDone" class="ghost" type="button">Clear done</button>
  </div>
  <ul id="items" class="items"></ul>
  <p class="counter" id="counter"></p>
</main>
""",
    extra_css=r"""
.app { max-width: 640px; margin: 0 auto; background: __C_PANEL__;
       border: 1px solid __C_ACCENT2__; border-radius: 14px; padding: 20px; }
.add { display: flex; gap: 8px; margin-bottom: 12px; }
.add input { flex: 1; padding: 12px; border: 1px solid __C_ACCENT2__; background: __C_BG__;
       color: __C_FG__; border-radius: 10px; font: inherit; }
.add button { padding: 12px 20px; background: __C_ACCENT__; color: __C_BG__;
       border: 0; border-radius: 10px; cursor: pointer; font: inherit; font-weight: 700; }
.filters { display: flex; gap: 8px; margin-bottom: 10px; align-items: center; flex-wrap: wrap; }
.filters button { padding: 6px 12px; border: 1px solid __C_ACCENT2__; background: transparent;
       color: __C_FG__; border-radius: 999px; cursor: pointer; font: inherit; }
.filters button.active { background: __C_ACCENT__; color: __C_BG__; border-color: __C_ACCENT__; }
.filters .ghost { background: transparent; }
.filters .grow { flex: 1; }
.items { list-style: none; }
.items li { display: flex; align-items: center; gap: 10px; padding: 10px;
       border-bottom: 1px dashed __C_ACCENT2__; }
.items li.done .text { opacity: .55; text-decoration: line-through; }
.items input[type=checkbox] { width: 20px; height: 20px; accent-color: __C_ACCENT__; }
.items .text { flex: 1; word-break: break-word; }
.items .del { background: transparent; color: __C_MUTED__; border: 0; cursor: pointer;
       font: inherit; padding: 4px 8px; border-radius: 6px; }
.items .del:hover { color: __C_ACCENT__; background: __C_BG__; }
.counter { color: __C_MUTED__; font-size: .85em; margin-top: 10px; text-align: center; }
""",
    initial_data='{"items":[],"filter":"all"}',
    scripts=r"""
const list = document.getElementById('items');
const counter = document.getElementById('counter');
const filtersEl = document.querySelector('.filters');
function uid() { return 'i-' + Date.now() + '-' + Math.random().toString(36).slice(2, 7); }
function render() {
  const items = appData.items.filter(it =>
    appData.filter === 'all' ? true :
    appData.filter === 'done' ? it.done : !it.done);
  list.innerHTML = items.map(it =>
    '<li data-id="' + it.id + '"' + (it.done ? ' class="done"' : '') + '>'
    + '<input type="checkbox"' + (it.done ? ' checked' : '') + '>'
    + '<span class="text"></span>'
    + '<button class="del" type="button" aria-label="Delete">×</button>'
    + '</li>').join('');
  // safe text injection
  for (const li of list.children) {
    const id = li.dataset.id;
    const it = appData.items.find(x => x.id === id);
    li.querySelector('.text').textContent = it.text;
  }
  for (const b of filtersEl.querySelectorAll('button[data-filter]'))
    b.classList.toggle('active', b.dataset.filter === appData.filter);
  const open = appData.items.filter(i => !i.done).length;
  counter.textContent = open + ' open • ' + appData.items.length + ' total';
}
document.getElementById('addForm').addEventListener('submit', e => {
  e.preventDefault();
  const i = document.getElementById('newItem');
  const t = i.value.trim(); if (!t) return;
  appData.items.unshift({ id: uid(), text: t, done: false, ts: Date.now() });
  i.value = ''; saveData(); render();
});
list.addEventListener('change', e => {
  if (e.target.type !== 'checkbox') return;
  const id = e.target.closest('li').dataset.id;
  const it = appData.items.find(x => x.id === id); if (!it) return;
  it.done = e.target.checked; saveData(); render();
});
list.addEventListener('click', e => {
  if (!e.target.classList.contains('del')) return;
  const id = e.target.closest('li').dataset.id;
  appData.items = appData.items.filter(x => x.id !== id); saveData(); render();
});
filtersEl.addEventListener('click', e => {
  const f = e.target.dataset.filter; if (!f) return;
  appData.filter = f; saveData(); render();
});
document.getElementById('clearDone').addEventListener('click', () => {
  appData.items = appData.items.filter(x => !x.done); saveData(); render();
});
render();
""",
)


# ---------- calculator ----------------------------------------------------
TPL_CALCULATOR = _build(
    body_html=r"""
<main class="app">
  <div class="screen" id="screen" aria-live="polite">0</div>
  <div class="expr" id="expr">&nbsp;</div>
  <div class="keys">
    <button data-k="C" class="op">C</button>
    <button data-k="±" class="op">±</button>
    <button data-k="%" class="op">%</button>
    <button data-k="/" class="op">÷</button>
    <button data-k="7">7</button><button data-k="8">8</button><button data-k="9">9</button>
    <button data-k="*" class="op">×</button>
    <button data-k="4">4</button><button data-k="5">5</button><button data-k="6">6</button>
    <button data-k="-" class="op">−</button>
    <button data-k="1">1</button><button data-k="2">2</button><button data-k="3">3</button>
    <button data-k="+" class="op">+</button>
    <button data-k="0" class="zero">0</button>
    <button data-k=".">.</button>
    <button data-k="=" class="eq">=</button>
  </div>
  <section class="history">
    <h3>History</h3>
    <ul id="historyList"><li class="empty">No calculations yet.</li></ul>
  </section>
</main>
""",
    extra_css=r"""
.app { max-width: 360px; margin: 0 auto; background: __C_PANEL__;
       border: 1px solid __C_ACCENT2__; border-radius: 18px; padding: 18px; }
.screen { font-variant-numeric: tabular-nums; font-size: clamp(36px, 9vw, 56px);
       text-align: right; padding: 14px 8px 0; color: __C_FG__; word-break: break-all; }
.expr { text-align: right; color: __C_MUTED__; font-size: .9em; min-height: 1.2em;
       padding: 4px 8px 12px; }
.keys { display: grid; grid-template-columns: repeat(4, 1fr); gap: 8px; }
.keys button { padding: 16px 0; background: __C_BG__; color: __C_FG__;
       border: 1px solid __C_ACCENT2__; border-radius: 10px; cursor: pointer;
       font: inherit; font-size: 1.1em; }
.keys button:hover { border-color: __C_RING__; }
.keys button.op { color: __C_ACCENT__; }
.keys button.eq { background: __C_ACCENT__; color: __C_BG__; border-color: __C_ACCENT__;
       grid-column: span 1; font-weight: 700; }
.keys button.zero { grid-column: span 2; }
.history { margin-top: 16px; max-height: 160px; overflow: auto;
       border-top: 1px solid __C_ACCENT2__; padding-top: 10px; }
.history h3 { font-size: .85em; color: __C_MUTED__; margin-bottom: 6px; }
.history ul { list-style: none; font-variant-numeric: tabular-nums; font-size: .9em; }
.history li { padding: 4px 0; border-bottom: 1px dashed __C_ACCENT2__; }
.history li.empty { color: __C_MUTED__; }
""",
    initial_data='{"history":[]}',
    scripts=r"""
const screen = document.getElementById('screen');
const exprEl = document.getElementById('expr');
let acc = null, op = null, cur = '0', justEvaled = false;
function show() { screen.textContent = cur; exprEl.innerHTML = (acc !== null ? (fmt(acc) + ' ' + (op || '')) : '&nbsp;'); }
function fmt(n) { const s = Number(n).toString(); return s.length > 14 ? Number(n).toExponential(8) : s; }
function input(d) {
  if (justEvaled) { cur = '0'; justEvaled = false; }
  if (d === '.') { if (!cur.includes('.')) cur += '.'; }
  else { cur = cur === '0' ? d : cur + d; }
  if (cur.length > 16) cur = cur.slice(0, 16);
  show();
}
function setOp(o) {
  if (op && !justEvaled) compute();
  acc = parseFloat(cur); op = o; cur = '0'; justEvaled = false; show();
}
function compute() {
  const b = parseFloat(cur);
  if (acc === null || op === null) { acc = b; show(); return; }
  let r = acc;
  if (op === '+') r = acc + b;
  else if (op === '-') r = acc - b;
  else if (op === '*') r = acc * b;
  else if (op === '/') r = b === 0 ? NaN : acc / b;
  appData.history.unshift({ a: acc, b, op, r, at: Date.now() });
  appData.history = appData.history.slice(0, 30);
  saveData(); renderHistory();
  acc = null; op = null; cur = String(r); justEvaled = true;
  show();
}
document.querySelector('.keys').addEventListener('click', e => {
  const b = e.target.closest('button'); if (!b) return;
  const k = b.dataset.k;
  if (/^[0-9.]$/.test(k)) input(k);
  else if (k === 'C') { acc = null; op = null; cur = '0'; justEvaled = false; show(); }
  else if (k === '±') { cur = (parseFloat(cur) * -1).toString(); show(); }
  else if (k === '%') { cur = (parseFloat(cur) / 100).toString(); show(); }
  else if (k === '=') compute();
  else setOp(k);
});
document.addEventListener('keydown', e => {
  const m = { 'Enter': '=', '=': '=', 'Escape': 'C', 'Backspace': 'C',
              '+': '+', '-': '-', '*': '*', '/': '/' };
  if (/^[0-9.]$/.test(e.key)) { input(e.key); e.preventDefault(); }
  else if (m[e.key]) {
    const k = m[e.key];
    if (k === '=') compute();
    else if (k === 'C') { acc = null; op = null; cur = '0'; justEvaled = false; show(); }
    else setOp(k);
    e.preventDefault();
  }
});
function renderHistory() {
  const ul = document.getElementById('historyList');
  if (!appData.history.length) { ul.innerHTML = '<li class="empty">No calculations yet.</li>'; return; }
  const map = { '+': '+', '-': '−', '*': '×', '/': '÷' };
  ul.innerHTML = appData.history.map(h =>
    '<li>' + fmt(h.a) + ' ' + map[h.op] + ' ' + fmt(h.b) + ' = ' + fmt(h.r) + '</li>').join('');
}
renderHistory(); show();
""",
)


# ---------- drawing -------------------------------------------------------
TPL_DRAWING = _build(
    body_html=r"""
<main class="app">
  <div class="toolbar">
    <label>Color <input type="color" id="colorIn" value="__C_ACCENT__"></label>
    <label>Size <input type="range" id="sizeIn" min="1" max="40" value="6"></label>
    <button id="undoBtn" type="button" class="ghost">Undo</button>
    <button id="clearBtn" type="button" class="ghost">Clear</button>
    <button id="pngBtn" type="button">Save PNG</button>
  </div>
  <canvas id="board" width="900" height="540" aria-label="Drawing canvas"></canvas>
  <p class="hint">Click and drag to draw. Touch supported. Strokes saved to localStorage.</p>
</main>
""",
    extra_css=r"""
.app { max-width: 960px; margin: 0 auto; }
.toolbar { display: flex; gap: 10px; align-items: center; margin-bottom: 10px; flex-wrap: wrap;
       background: __C_PANEL__; border: 1px solid __C_ACCENT2__; border-radius: 10px; padding: 10px; }
.toolbar label { display: flex; gap: 6px; align-items: center; color: __C_MUTED__; font-size: .9em; }
.toolbar input[type=color] { width: 36px; height: 32px; border: 0; background: transparent; cursor: pointer; }
.toolbar input[type=range] { width: 140px; }
.toolbar button { padding: 8px 14px; background: __C_ACCENT__; color: __C_BG__;
       border: 0; border-radius: 8px; cursor: pointer; font: inherit; font-weight: 600; }
.toolbar button.ghost { background: transparent; color: __C_FG__; border: 1px solid __C_ACCENT2__; }
canvas { width: 100%; height: auto; aspect-ratio: 5/3; background: white;
       border: 1px solid __C_ACCENT2__; border-radius: 10px; display: block; touch-action: none; }
.hint { color: __C_MUTED__; font-size: .85em; margin-top: 8px; }
""",
    initial_data='{"strokes":[]}',
    scripts=r"""
const canvas = document.getElementById('board');
const ctx = canvas.getContext('2d');
const colorIn = document.getElementById('colorIn');
const sizeIn = document.getElementById('sizeIn');
let drawing = false, current = null;
function redraw() {
  ctx.fillStyle = '#ffffff';
  ctx.fillRect(0, 0, canvas.width, canvas.height);
  for (const s of appData.strokes) drawStroke(s);
}
function drawStroke(s) {
  if (!s.points.length) return;
  ctx.lineCap = 'round'; ctx.lineJoin = 'round';
  ctx.strokeStyle = s.color; ctx.lineWidth = s.size;
  ctx.beginPath();
  ctx.moveTo(s.points[0].x, s.points[0].y);
  for (let i = 1; i < s.points.length; i++) ctx.lineTo(s.points[i].x, s.points[i].y);
  ctx.stroke();
}
function pos(e) {
  const r = canvas.getBoundingClientRect();
  const t = e.touches ? e.touches[0] : e;
  return { x: (t.clientX - r.left) * (canvas.width / r.width),
           y: (t.clientY - r.top) * (canvas.height / r.height) };
}
function start(e) { drawing = true; current = { color: colorIn.value, size: parseInt(sizeIn.value, 10), points: [pos(e)] };
  appData.strokes.push(current); e.preventDefault(); }
function move(e) { if (!drawing) return; current.points.push(pos(e));
  drawStroke({ color: current.color, size: current.size, points: current.points.slice(-2) });
  e.preventDefault(); }
function end() { if (!drawing) return; drawing = false; saveData(); }
canvas.addEventListener('mousedown', start);
canvas.addEventListener('mousemove', move);
window.addEventListener('mouseup', end);
canvas.addEventListener('touchstart', start, { passive: false });
canvas.addEventListener('touchmove', move, { passive: false });
canvas.addEventListener('touchend', end);
document.getElementById('undoBtn').addEventListener('click', () => {
  appData.strokes.pop(); saveData(); redraw();
});
document.getElementById('clearBtn').addEventListener('click', () => {
  if (!confirm('Clear the canvas?')) return;
  appData.strokes = []; saveData(); redraw();
});
document.getElementById('pngBtn').addEventListener('click', () => {
  canvas.toBlob(b => {
    const url = URL.createObjectURL(b);
    const a = document.createElement('a');
    a.href = url; a.download = APP_NAME + '-' + Date.now() + '.png';
    document.body.appendChild(a); a.click(); a.remove();
    URL.revokeObjectURL(url);
  });
});
redraw();
""",
)


# ---------- chat / journal ------------------------------------------------
TPL_CHAT = _build(
    body_html=r"""
<main class="app">
  <div class="thread" id="thread"></div>
  <form id="sendForm" class="send">
    <input type="text" id="msg" placeholder="Type a message…" autocomplete="off" required>
    <select id="who" aria-label="Sender">
      <option value="me">me</option>
      <option value="them">them</option>
    </select>
    <button type="submit">Send</button>
  </form>
</main>
""",
    extra_css=r"""
.app { max-width: 720px; margin: 0 auto; display: flex; flex-direction: column;
       background: __C_PANEL__; border: 1px solid __C_ACCENT2__; border-radius: 14px;
       overflow: hidden; height: min(72vh, 700px); }
.thread { flex: 1; overflow: auto; padding: 18px; display: flex; flex-direction: column; gap: 8px; }
.bubble { max-width: 78%; padding: 10px 14px; border-radius: 14px; word-break: break-word; }
.bubble.me { align-self: flex-end; background: __C_ACCENT__; color: __C_BG__;
       border-bottom-right-radius: 4px; }
.bubble.them { align-self: flex-start; background: __C_BG__; color: __C_FG__;
       border: 1px solid __C_ACCENT2__; border-bottom-left-radius: 4px; }
.bubble .ts { display: block; font-size: .7em; opacity: .65; margin-top: 4px; }
.send { display: flex; gap: 8px; padding: 10px; border-top: 1px solid __C_ACCENT2__;
       background: __C_PANEL__; }
.send input[type=text] { flex: 1; padding: 12px; border: 1px solid __C_ACCENT2__;
       background: __C_BG__; color: __C_FG__; border-radius: 10px; font: inherit; }
.send select { padding: 12px; border: 1px solid __C_ACCENT2__; background: __C_BG__;
       color: __C_FG__; border-radius: 10px; font: inherit; }
.send button { padding: 12px 20px; background: __C_ACCENT__; color: __C_BG__; border: 0;
       border-radius: 10px; cursor: pointer; font: inherit; font-weight: 700; }
""",
    initial_data='{"messages":[]}',
    scripts=r"""
const thread = document.getElementById('thread');
function render() {
  thread.innerHTML = appData.messages.map(m =>
    '<div class="bubble ' + (m.who === 'me' ? 'me' : 'them') + '">'
    + '<span class="text"></span>'
    + '<span class="ts">' + new Date(m.ts).toLocaleString() + '</span>'
    + '</div>').join('');
  // safe text
  const bubbles = thread.querySelectorAll('.bubble');
  for (let i = 0; i < bubbles.length; i++) {
    bubbles[i].querySelector('.text').textContent = appData.messages[i].text;
  }
  thread.scrollTop = thread.scrollHeight;
}
document.getElementById('sendForm').addEventListener('submit', e => {
  e.preventDefault();
  const t = document.getElementById('msg');
  const who = document.getElementById('who').value;
  const text = t.value.trim(); if (!text) return;
  appData.messages.push({ id: 'm-' + Date.now(), who, text, ts: Date.now() });
  appData.messages = appData.messages.slice(-500);
  t.value = ''; saveData(); render();
});
render();
""",
)


# ---------- dashboard -----------------------------------------------------
TPL_DASHBOARD = _build(
    body_html=r"""
<main class="app">
  <div class="toolbar">
    <button data-add="counter" type="button">+ Counter</button>
    <button data-add="number" type="button">+ Number</button>
    <button data-add="note" type="button">+ Note</button>
  </div>
  <div class="grid" id="grid"></div>
</main>
""",
    extra_css=r"""
.app { max-width: 1100px; margin: 0 auto; }
.toolbar { display: flex; gap: 8px; margin-bottom: 14px; flex-wrap: wrap; }
.toolbar button { padding: 10px 14px; background: __C_ACCENT__; color: __C_BG__;
       border: 0; border-radius: 8px; cursor: pointer; font: inherit; font-weight: 600; }
.grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(220px, 1fr));
       gap: 14px; }
.card { background: __C_PANEL__; border: 1px solid __C_ACCENT2__; border-radius: 14px;
       padding: 16px; position: relative; min-height: 130px; display: flex; flex-direction: column; }
.card .label { font-size: .8em; color: __C_MUTED__; text-transform: uppercase; letter-spacing: 1px; }
.card input.label-edit, .card .value-num { background: transparent; border: 0; color: __C_FG__;
       font: inherit; width: 100%; }
.card input.label-edit { font-size: .8em; color: __C_MUTED__; text-transform: uppercase; letter-spacing: 1px; }
.card .value-num { font-size: 2.4em; margin-top: 8px; padding: 4px 0;
       border-bottom: 1px dashed __C_ACCENT2__; }
.card textarea.note { width: 100%; flex: 1; min-height: 80px; background: transparent;
       border: 0; color: __C_FG__; font: inherit; resize: vertical; margin-top: 6px; }
.card .ctrls { display: flex; gap: 6px; margin-top: 10px; }
.card .ctrls button { flex: 1; padding: 6px; background: __C_BG__; color: __C_FG__;
       border: 1px solid __C_ACCENT2__; border-radius: 6px; cursor: pointer; font: inherit; }
.card .ctrls button.bump { color: __C_ACCENT__; }
.card .del { position: absolute; top: 6px; right: 8px; background: transparent;
       border: 0; color: __C_MUTED__; cursor: pointer; font-size: 1.2em; padding: 2px 8px; }
.card .del:hover { color: __C_ACCENT__; }
""",
    initial_data='{"cards":[{"id":"c-1","type":"counter","label":"Sample counter","value":0},{"id":"c-2","type":"note","label":"Notes","value":"Click any field to edit."}]}',
    scripts=r"""
const grid = document.getElementById('grid');
function uid() { return 'c-' + Date.now() + '-' + Math.random().toString(36).slice(2, 6); }
function render() {
  grid.innerHTML = appData.cards.map(c => cardHtml(c)).join('');
  bind();
}
function cardHtml(c) {
  const head = '<input class="label-edit" data-id="' + c.id + '" data-field="label" value="">';
  const del = '<button class="del" data-id="' + c.id + '" title="Delete">×</button>';
  if (c.type === 'note') {
    return '<div class="card">' + del + head
      + '<textarea class="note" data-id="' + c.id + '" data-field="value"></textarea>'
      + '</div>';
  }
  const ctrls = c.type === 'counter'
    ? '<div class="ctrls"><button class="bump" data-id="' + c.id + '" data-bump="-1" type="button">−1</button>'
      + '<button class="bump" data-id="' + c.id + '" data-bump="1" type="button">+1</button></div>'
    : '';
  return '<div class="card">' + del + head
    + '<input class="value-num" data-id="' + c.id + '" data-field="value" type="number" inputmode="decimal">'
    + ctrls + '</div>';
}
function bind() {
  for (const inp of grid.querySelectorAll('[data-field]')) {
    const c = appData.cards.find(x => x.id === inp.dataset.id);
    if (!c) continue;
    inp.value = c[inp.dataset.field] != null ? c[inp.dataset.field] : '';
    inp.addEventListener('input', () => {
      let v = inp.value;
      if (inp.dataset.field === 'value' && c.type !== 'note') v = parseFloat(v) || 0;
      c[inp.dataset.field] = v; saveData();
    });
  }
  for (const b of grid.querySelectorAll('button.bump')) {
    b.addEventListener('click', () => {
      const c = appData.cards.find(x => x.id === b.dataset.id); if (!c) return;
      c.value = (parseFloat(c.value) || 0) + parseInt(b.dataset.bump, 10);
      saveData(); render();
    });
  }
  for (const b of grid.querySelectorAll('button.del')) {
    b.addEventListener('click', () => {
      if (!confirm('Delete this card?')) return;
      appData.cards = appData.cards.filter(x => x.id !== b.dataset.id);
      saveData(); render();
    });
  }
}
document.querySelector('.toolbar').addEventListener('click', e => {
  const t = e.target.dataset.add; if (!t) return;
  const c = { id: uid(), type: t, label: t === 'note' ? 'New note' : 'New ' + t,
              value: t === 'note' ? '' : 0 };
  appData.cards.push(c); saveData(); render();
});
render();
""",
)


# ---------- game (target clicker) -----------------------------------------
TPL_GAME = _build(
    body_html=r"""
<main class="app">
  <div class="hud">
    <div><span class="label">Score</span><span id="score">0</span></div>
    <div><span class="label">Time</span><span id="time">30</span></div>
    <div><span class="label">Best</span><span id="best">0</span></div>
    <button id="startBtn" type="button">Start</button>
  </div>
  <div class="board" id="board" aria-label="Click the targets"></div>
  <p class="hint">Click or tap targets before they vanish. 30 seconds per round.</p>
</main>
""",
    extra_css=r"""
.app { max-width: 720px; margin: 0 auto; }
.hud { display: flex; align-items: center; gap: 14px; margin-bottom: 10px; flex-wrap: wrap;
       background: __C_PANEL__; border: 1px solid __C_ACCENT2__; border-radius: 10px; padding: 10px 14px; }
.hud div { display: flex; flex-direction: column; min-width: 64px; }
.hud .label { font-size: .7em; color: __C_MUTED__; text-transform: uppercase; letter-spacing: 1px; }
.hud div span:last-child { font-size: 1.4em; font-variant-numeric: tabular-nums; }
.hud button { margin-left: auto; padding: 10px 18px; background: __C_ACCENT__; color: __C_BG__;
       border: 0; border-radius: 8px; cursor: pointer; font: inherit; font-weight: 700; }
.board { position: relative; width: 100%; aspect-ratio: 4/3;
       background: __C_PANEL__; border: 1px solid __C_ACCENT2__; border-radius: 14px;
       overflow: hidden; touch-action: manipulation; }
.target { position: absolute; width: 56px; height: 56px; border-radius: 50%;
       background: radial-gradient(circle at 30% 30%, __C_ACCENT__, __C_ACCENT2__);
       cursor: pointer; box-shadow: 0 0 18px rgba(0,0,0,.4);
       transform: translate(-50%, -50%); animation: pop .3s ease-out; }
.target:hover { filter: brightness(1.15); }
@keyframes pop { from { transform: translate(-50%, -50%) scale(.2); opacity: 0; }
                 to   { transform: translate(-50%, -50%) scale(1);  opacity: 1; } }
.hint { color: __C_MUTED__; font-size: .85em; margin-top: 8px; text-align: center; }
""",
    initial_data='{"best":0,"plays":0}',
    scripts=r"""
const board = document.getElementById('board');
const scoreEl = document.getElementById('score');
const timeEl = document.getElementById('time');
const bestEl = document.getElementById('best');
const startBtn = document.getElementById('startBtn');
let score = 0, timeLeft = 30, gameOn = false, spawn = null, tick = null;
bestEl.textContent = appData.best || 0;
function rand(min, max) { return Math.random() * (max - min) + min; }
function spawnTarget() {
  if (!gameOn) return;
  const t = document.createElement('button');
  t.className = 'target'; t.type = 'button';
  const r = board.getBoundingClientRect();
  const pad = 32;
  t.style.left = rand(pad, r.width - pad) + 'px';
  t.style.top  = rand(pad, r.height - pad) + 'px';
  const life = 900 + Math.random() * 700;
  const dieTimer = setTimeout(() => { if (t.parentNode) t.remove(); }, life);
  t.addEventListener('click', () => {
    score++; scoreEl.textContent = score;
    clearTimeout(dieTimer); t.remove();
  });
  board.appendChild(t);
}
function start() {
  if (gameOn) return;
  gameOn = true; score = 0; timeLeft = 30;
  scoreEl.textContent = 0; timeEl.textContent = 30;
  board.innerHTML = '';
  startBtn.textContent = 'Playing…'; startBtn.disabled = true;
  spawn = setInterval(spawnTarget, 600);
  tick = setInterval(() => {
    timeLeft--; timeEl.textContent = timeLeft;
    if (timeLeft <= 0) end();
  }, 1000);
}
function end() {
  gameOn = false;
  clearInterval(spawn); clearInterval(tick); spawn = tick = null;
  board.innerHTML = '';
  startBtn.textContent = 'Play again';
  startBtn.disabled = false;
  appData.plays = (appData.plays || 0) + 1;
  if (score > (appData.best || 0)) { appData.best = score; bestEl.textContent = score; }
  saveData();
  setTimeout(() => alert('Final score: ' + score + (score === appData.best ? '  ★ new best!' : '')), 30);
}
startBtn.addEventListener('click', start);
""",
)


TEMPLATES = {
    "timer": TPL_TIMER,
    "list": TPL_LIST,
    "calculator": TPL_CALCULATOR,
    "drawing": TPL_DRAWING,
    "chat": TPL_CHAT,
    "dashboard": TPL_DASHBOARD,
    "game": TPL_GAME,
}


# ---------------------------------------------------------------------------
# HTTP handler
# ---------------------------------------------------------------------------
class Handler(BaseHTTPRequestHandler):
    protocol_version = "HTTP/1.1"

    def log_message(self, fmt, *args):
        sys.stderr.write("[forge-bridge] " + (fmt % args) + "\n")

    def _cors(self):
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.send_header("Access-Control-Expose-Headers", "X-Forge-Template")

    def do_OPTIONS(self):
        self.send_response(204)
        self._cors()
        self.send_header("Content-Length", "0")
        self.send_header("Connection", "close")
        self.end_headers()

    def do_GET(self):
        if self.path in ("/", "/health"):
            payload = {
                "ok": True,
                "service": "app-forge-bridge",
                "templates": SUPPORTED_TEMPLATES,
                "themes": [t for t in THEMES if t != "default"],
                "categories": sorted(ALLOWED_CATEGORIES),
            }
            self._send_json(200, payload)
        else:
            self._send_json(404, {"ok": False, "error": "not found"})

    def do_POST(self):
        if self.path == "/forge":
            self._handle_forge()
        elif self.path == "/save":
            self._handle_save()
        else:
            self._send_json(404, {"ok": False, "error": "not found"})

    # --- helpers ---------------------------------------------------------
    def _read_json(self):
        length = int(self.headers.get("Content-Length") or 0)
        raw = self.rfile.read(length) if length else b"{}"
        try:
            return json.loads(raw.decode("utf-8"))
        except Exception:
            return None

    def _send_json(self, status, payload):
        body = json.dumps(payload).encode("utf-8")
        self.send_response(status)
        self._cors()
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Connection", "close")
        self.end_headers()
        try:
            self.wfile.write(body)
        except (BrokenPipeError, ConnectionResetError):
            pass

    # --- routes ----------------------------------------------------------
    def _handle_forge(self):
        data = self._read_json()
        if not isinstance(data, dict):
            self._send_json(400, {"ok": False, "error": "invalid JSON body"})
            return
        prompt = (data.get("prompt") or "").strip()
        if not prompt:
            self._send_json(400, {"ok": False, "error": "prompt is required"})
            return
        template = detect_template(prompt)
        html_text, theme_name = render_template(template, prompt)
        payload = html_text.encode("utf-8")

        self.send_response(200)
        self._cors()
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("X-Forge-Template", template)
        self.send_header("X-Forge-Theme", theme_name)
        self.send_header("Cache-Control", "no-store")
        self.send_header("Transfer-Encoding", "chunked")
        self.send_header("Connection", "close")
        self.end_headers()

        chunk_size = 96
        try:
            for i in range(0, len(payload), chunk_size):
                chunk = payload[i:i + chunk_size]
                self.wfile.write(("%X\r\n" % len(chunk)).encode("ascii"))
                self.wfile.write(chunk)
                self.wfile.write(b"\r\n")
                self.wfile.flush()
                time.sleep(0.008)
            self.wfile.write(b"0\r\n\r\n")
            self.wfile.flush()
        except (BrokenPipeError, ConnectionResetError):
            pass

    def _handle_save(self):
        data = self._read_json()
        if not isinstance(data, dict):
            self._send_json(400, {"ok": False, "error": "invalid JSON body"})
            return
        category = (data.get("category") or "").strip()
        filename = (data.get("filename") or "").strip().lower()
        html_text = data.get("html") or ""

        if category not in ALLOWED_CATEGORIES:
            self._send_json(400, {
                "ok": False,
                "error": "unknown category '%s'" % category,
                "allowed": sorted(ALLOWED_CATEGORIES),
            })
            return
        if not filename.endswith(".html"):
            filename += ".html"
        if not FILENAME_RE.match(filename):
            self._send_json(400, {
                "ok": False,
                "error": "filename must match [a-z0-9][a-z0-9-]*\\.html"
            })
            return
        if not isinstance(html_text, str) or not html_text.strip():
            self._send_json(400, {"ok": False, "error": "html body is empty"})
            return

        target_dir = os.path.join(REPO_ROOT, "apps", category)
        os.makedirs(target_dir, exist_ok=True)
        target_path = os.path.normpath(os.path.join(target_dir, filename))
        # Defense-in-depth: ensure resolved path stays inside target_dir.
        if not target_path.startswith(os.path.abspath(target_dir) + os.sep):
            self._send_json(400, {"ok": False, "error": "invalid path"})
            return

        existed = os.path.exists(target_path)
        with open(target_path, "w", encoding="utf-8") as f:
            f.write(html_text)

        rel = os.path.relpath(target_path, REPO_ROOT).replace(os.sep, "/")
        self._send_json(200, {
            "ok": True,
            "path": rel,
            "created": not existed,
            "bytes": len(html_text.encode("utf-8")),
        })


def banner():
    bar = "=" * 64
    print(bar)
    print("  App-Forge Bridge")
    print(bar)
    print("  URL:        http://%s:%d" % (HOST, PORT))
    print("  Endpoints:  POST /forge   POST /save   GET /health")
    print("  Templates:  " + ", ".join(SUPPORTED_TEMPLATES))
    print("  Themes:     " + ", ".join(t for t in THEMES if t != "default"))
    print("  Repo root:  " + REPO_ROOT)
    print("  Categories: " + ", ".join(sorted(ALLOWED_CATEGORIES)))
    print(bar)
    print("  Open: apps/ai-tools/app-forge.html (served over HTTP)")
    print("  Stop: Ctrl+C")
    print(bar)


def main():
    banner()
    try:
        srv = ThreadingHTTPServer((HOST, PORT), Handler)
    except OSError as e:
        sys.stderr.write("[forge-bridge] failed to bind %s:%d -> %s\n" % (HOST, PORT, e))
        sys.exit(1)
    try:
        srv.serve_forever()
    except KeyboardInterrupt:
        print("\n[forge-bridge] shutting down")
    finally:
        srv.server_close()


if __name__ == "__main__":
    main()
