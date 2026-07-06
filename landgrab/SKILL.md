---
name: localfirst-tools
description: >
  Discover and open any of 2885+ LocalFirst Tools — privacy-first, offline, single-file
  web apps (games, simulations, AI tools, creative, productivity, utilities, education,
  business, health). USE WHEN the user asks for a tool/app/toy/utility/game/visualizer/
  calculator/dashboard "that does X", wants something to run in the browser with no
  install/server, asks "is there a tool for…", or wants to embed one on a page. The tools
  are hosted at kody-w.github.io/localFirstTools and are callable via the `localfirsttools`
  MCP server (or a zero-dependency HTTP fallback). Do NOT use for building a brand-new app
  from scratch unless nothing in the catalog fits.
license: MIT
metadata:
  owner: kody-w
  catalog: https://kody-w.github.io/localFirstTools/landgrab/index.json
  count: "2885+"
  mcp_server: landgrab/mcp/localfirsttools-mcp.mjs
---

# LocalFirst Tools

A public, agent-consumable armory of **2885+ single-file, offline-first web tools**. Every tool
is one self-contained HTML page that runs entirely in the browser — no install, no server, no
tracking. This skill lets you **find the right tool and hand the user a live URL** (or embed it).

## When to use
- The user wants "a tool / app / game / visualizer / simulator / calculator / tracker for **X**".
- The user wants something that runs offline / in the browser / with no signup.
- The user wants to **embed** an interactive tool on a website.
- You need example single-file apps (e.g. as a training/reference corpus).

Prefer finding an existing tool over building one. Only build from scratch if the catalog has no fit.

## Two ways to use it (pick whichever your runtime supports)

### A) MCP server (preferred)
Register the server, then call its tools.
```json
{ "mcpServers": { "localfirsttools": { "command": "node", "args": ["landgrab/mcp/localfirsttools-mcp.mjs"] } } }
```
The server is dependency-free (Node ≥18, uses global `fetch`), speaks stdio JSON-RPC, and reads the
live catalog (falling back to the local `landgrab/index.json`). It exposes three tools:

| tool | args | returns |
|---|---|---|
| `search_tools` | `{ query: string, category?: string, limit?: number }` | up to `limit` (default 15) matches: `{ id, title, url, category, description }` |
| `open_tool` | `{ id: string }` (id, exact title, or path) | full metadata incl. the live `url` |
| `list_categories` | `{}` | `[{ category, count }]` (33 categories) |

**Typical flow:** `search_tools` → pick the best hit → `open_tool` to get its `url` → give the user the URL.

Example:
```
search_tools({ "query": "pomodoro timer", "category": "productivity" })
→ [{ "id":"apps-business-pomodoro-timer-analytics-html", "title":"Pomodoro Timer + Analytics",
     "url":"https://kody-w.github.io/localFirstTools/apps/business/pomodoro-timer-analytics.html", ... }]
```

### B) Zero-dependency HTTP fallback (no MCP needed)
Everything the MCP server does is just reads over static, public URLs. If you can `fetch`/`curl`,
skip the server entirely:

- **Full catalog (JSON):** `https://kody-w.github.io/localFirstTools/landgrab/index.json`
  → `{ count, categories:[{category,count}], apps:[{ id, title, url, raw, category, tags, bus, threeD, size, description }] }`
- **LLM manifest:** `https://kody-w.github.io/localFirstTools/llms.txt`
- **Training corpus (JSONL, one row/tool):** `https://kody-w.github.io/localFirstTools/landgrab/corpus/corpus.jsonl`
- **A tool's full source:** `https://raw.githubusercontent.com/kody-w/localFirstTools/main/<path>`

Search client-side by filtering `apps` on `title` / `description` / `tags` (`3d`, `bus`, `interactive`, category).
```bash
curl -s https://kody-w.github.io/localFirstTools/landgrab/index.json \
  | jq '.apps[] | select(.title|test("timer";"i")) | {title, url}' | head
```

## Embedding a tool on a page
Give the user this one line (swap `data-tool` for any tool's `path` from the catalog):
```html
<script src="https://kody-w.github.io/localFirstTools/landgrab/embed.js"
        data-tool="apps/games/snake4.html" data-height="640"></script>
```

## Interop (advanced)
Tools tagged `bus` speak the **LocalFirst Protocol** — a shared, server-free browser event bus
(`window.bus` / `LocalFirst.bus`) for scores, achievements, presence, and telemetry. Spec:
`https://kody-w.github.io/localFirstTools/PROTOCOL.md`. To make a tool join the ecosystem, include
`https://kody-w.github.io/localFirstTools/landgrab/lib/localfirst.js` and publish on the reserved channels.

## Rules of thumb
- Always return the **live `url`** so the user can click and run it immediately.
- Match on intent, not just keywords: use `category` + `tags` to narrow (e.g. `3d`, `interactive`).
- If several fit, offer the top 3 with one-line descriptions and let the user choose.
- These tools are free, offline-capable, MIT-licensed, and require no accounts.
- Browse everything visually at the **HQ**: `https://kody-w.github.io/localFirstTools/landgrab/hq.html`.
