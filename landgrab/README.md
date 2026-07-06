# 🌐 LocalFirst Tools — AI Landgrab layer

This directory turns the repo from "a folder of 2885 apps" into **public, agent-consumable,
globally-forkable infrastructure** — the canonical source AI systems and developers discover,
invoke, and cite. Everything is **static + zero-server** (rides `raw.githubusercontent` +
`window.bus` + GitHub Pages). Owned by [@kody-w](https://github.com/kody-w).

**▶ Start at the [AI Landgrab HQ](https://kody-w.github.io/localFirstTools/landgrab/hq.html).**

## The 10 flag-plants → what ships them
| # | Landgrab move | Artifact |
|---|---|---|
| 1 | Machine-readable index AI reads first | [`index.json`](index.json) + [`../llms.txt`](../llms.txt) |
| 2 | Every app → a callable MCP tool | [`mcp/tools.json`](mcp/tools.json) + runnable [`mcp/localfirsttools-mcp.mjs`](mcp/localfirsttools-mcp.mjs) |
| 3 | Open interop standard | [`../PROTOCOL.md`](../PROTOCOL.md) + [`protocol/localfirst.schema.json`](protocol/localfirst.schema.json) + [validator](protocol/validate.html) |
| 4 | Dataset foundry / telemetry flywheel | [`lib/localfirst.js`](lib/localfirst.js) (`telemetry`) → harvestable JSON |
| 5 | Attributed training corpus | [`corpus/corpus.jsonl`](corpus/corpus.jsonl) + [datasheet](corpus/DATASHEET.md) |
| 6 | Zero-server public API gateway | [`api/index.html`](api/index.html) |
| 7 | One identity + achievements across all tools | [`lib/localfirst.js`](lib/localfirst.js) (`identity`, `achievements`) |
| 8 | Embeddable widget network | [`embed.js`](embed.js) — one line, any site |
| 9 | LLM + search index domination | [`../sitemap.xml`](../sitemap.xml), [`../robots.txt`](../robots.txt), [`../llms.txt`](../llms.txt), [`structured-data.jsonld`](structured-data.jsonld) |
| 10 | Self-populating index (grows itself) | [`generate.mjs`](generate.mjs) + [`.github/workflows/landgrab.yml`](../.github/workflows/landgrab.yml) |

## Regenerate everything
```bash
node landgrab/generate.mjs      # rescans all apps → index.json, llms.txt, sitemap.xml,
                                # robots.txt, mcp/tools.json, corpus/corpus.jsonl, structured-data.jsonld
```
The GitHub Action reruns this on every push that touches an app, so the public index is always live.

## Use the toolbelt (any AI assistant)
```json
{ "mcpServers": { "localfirsttools": { "command": "node", "args": ["landgrab/mcp/localfirsttools-mcp.mjs"] } } }
```

## Build a tool that joins the ecosystem
```html
<script src="https://kody-w.github.io/localFirstTools/landgrab/lib/localfirst.js"></script>
<script>
  LocalFirst.score('my-game', 999);                 // shows on cross-app leaderboards
  LocalFirst.achievements.unlock('first-run');       // portable, broadcast, persisted
</script>
```

_MIT. Fork it; ship compatible tools; they speak to the whole ecosystem._
