#!/usr/bin/env node
// vox-string.mjs — "the String" (rapp-neighborhood-protocol §5a-kite).
// A zero-dependency CDP driver: flies voxel-world.html tabs from a shell by
// evaluating expressions (vox.observe(), vox.act([...]), vox('kite'), ...)
// in the browser console. The CDP hop stays on-machine per the spec.
//
// Usage:
//   node vox-string.mjs list                          # list open tabs
//   node vox-string.mjs open "<url>"                  # open a new tab, prints its id
//   node vox-string.mjs eval <tabIdOrUrlSubstring> "<js expression>"
//   node vox-string.mjs close <tabId>
//   node vox-string.mjs activate <tabId>              # bring tab to front
//
// Chrome must be started with --remote-debugging-port (default 9222):
//   "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" \
//     --remote-debugging-port=9222 --user-data-dir=/tmp/vox-string-profile \
//     --disable-background-timer-throttling --disable-backgrounding-occluded-windows \
//     --disable-renderer-backgrounding "<url>"
//
// Env: VOX_CDP_PORT overrides the port.

const PORT = process.env.VOX_CDP_PORT || '9222';
const BASE = `http://127.0.0.1:${PORT}`;

async function listTabs() {
  const res = await fetch(`${BASE}/json/list`);
  if (!res.ok) throw new Error(`CDP list failed: ${res.status}`);
  return (await res.json()).filter(t => t.type === 'page');
}

async function findTab(idOrSubstr) {
  const tabs = await listTabs();
  const tab = tabs.find(t => t.id === idOrSubstr) ||
    tabs.find(t => (t.url || '').includes(idOrSubstr)) ||
    tabs.find(t => (t.title || '').includes(idOrSubstr));
  if (!tab) throw new Error(`No tab matching "${idOrSubstr}". Open tabs:\n` +
    tabs.map(t => `  ${t.id}  ${t.url}`).join('\n'));
  return tab;
}

function cdpEval(wsUrl, expression, timeoutMs = 30000) {
  return new Promise((resolve, reject) => {
    const ws = new WebSocket(wsUrl);
    const timer = setTimeout(() => { ws.close(); reject(new Error('CDP eval timeout')); }, timeoutMs);
    ws.onerror = e => { clearTimeout(timer); reject(new Error('CDP websocket error: ' + (e.message || ''))); };
    ws.onopen = () => {
      ws.send(JSON.stringify({
        id: 1, method: 'Runtime.evaluate',
        params: { expression, awaitPromise: true, returnByValue: true, userGesture: true },
      }));
    };
    ws.onmessage = ev => {
      const msg = JSON.parse(ev.data);
      if (msg.id !== 1) return;
      clearTimeout(timer); ws.close();
      if (msg.error) return reject(new Error('CDP error: ' + JSON.stringify(msg.error)));
      const r = msg.result;
      if (r.exceptionDetails) {
        return resolve({ ok: false, exception: r.exceptionDetails.text,
          detail: r.exceptionDetails.exception && r.exceptionDetails.exception.description });
      }
      resolve(r.result.value !== undefined ? r.result.value
        : { type: r.result.type, description: r.result.description });
    };
  });
}

const [cmd, ...args] = process.argv.slice(2);
try {
  if (cmd === 'list') {
    const tabs = await listTabs();
    console.log(JSON.stringify(tabs.map(t => ({ id: t.id, url: t.url, title: t.title })), null, 2));
  } else if (cmd === 'open') {
    const url = args[0];
    if (!url) throw new Error('usage: open <url>');
    let res = await fetch(`${BASE}/json/new?${encodeURIComponent(url)}`, { method: 'PUT' });
    if (!res.ok) res = await fetch(`${BASE}/json/new?${encodeURIComponent(url)}`); // older Chrome used GET
    if (!res.ok) throw new Error(`CDP open failed: ${res.status}`);
    const tab = await res.json();
    console.log(JSON.stringify({ id: tab.id, url: tab.url }));
  } else if (cmd === 'eval') {
    const [target, ...exprParts] = args;
    const expression = exprParts.join(' ');
    if (!target || !expression) throw new Error('usage: eval <tabIdOrUrlSubstring> "<expression>"');
    const tab = await findTab(target);
    const value = await cdpEval(tab.webSocketDebuggerUrl, expression);
    console.log(typeof value === 'string' ? value : JSON.stringify(value, null, 2));
  } else if (cmd === 'close') {
    const tab = await findTab(args[0]);
    await fetch(`${BASE}/json/close/${tab.id}`);
    console.log(JSON.stringify({ closed: tab.id }));
  } else if (cmd === 'activate') {
    const tab = await findTab(args[0]);
    await fetch(`${BASE}/json/activate/${tab.id}`);
    console.log(JSON.stringify({ activated: tab.id }));
  } else {
    console.log('usage: vox-string.mjs list | open <url> | eval <tab> "<expr>" | close <tab> | activate <tab>');
    process.exit(cmd ? 1 : 0);
  }
} catch (e) {
  console.error(JSON.stringify({ ok: false, error: e.message }));
  process.exit(1);
}
