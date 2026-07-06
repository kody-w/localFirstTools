# LocalFirst Protocol — v1

**An open standard for server-free, offline-first, interoperable web tools.**
Maintained by [@kody-w](https://github.com/kody-w) · canonical home: `kody-w.github.io/localFirstTools`

Any single-file HTML app that follows this protocol automatically interoperates with the
other **2885+ tools** in [LocalFirst Tools](https://kody-w.github.io/localFirstTools/landgrab/hq.html):
they share one browser event bus, one portable identity, one achievement/leaderboard layer,
and one harvestable telemetry format — with **no server, no build step, and no tracking.**

## Principles
1. **One file.** A tool is a single, self-contained `.html` that runs by opening it.
2. **Local-first.** All state lives in the browser (`localStorage`). Works fully offline.
3. **No server.** Interop happens over `BroadcastChannel` + `localStorage`, never a backend.
4. **Interoperable.** Tools speak a shared message bus so they can compose.
5. **Agent-legible.** The whole corpus is published as machine-readable data (`index.json`, `llms.txt`, MCP).

## The bus
Every conformant tool exposes / consumes a global event bus. Include the reference runtime:

```html
<script src="https://kody-w.github.io/localFirstTools/landgrab/lib/localfirst.js"></script>
```

```js
LocalFirst.bus.publish('score', { game: 'snake4', score: 420 });
LocalFirst.bus.subscribe('score', (p) => console.log(p.handle, 'scored', p.score));
LocalFirst.bus.history('score', 20);        // last 20 messages on a channel
```

A bus **message** is:

```json
{ "__lf": 1, "channel": "score", "payload": { }, "ts": 1730000000000, "from": "lf-ab12cd" }
```

### Reserved channels
| channel | payload | meaning |
|---|---|---|
| `score` | `{ game, score, client, handle }` | a run finished with a score (drives cross-app leaderboards) |
| `achievement` | `{ id, by, handle }` | a badge was unlocked |
| `telemetry` | `{ type, data }` | an app event, appended to the local harvestable log |
| `presence` | `{ app, handle, ts }` | "I'm here now" heartbeat |
| `embed` | `{ tool, host }` | a tool was embedded on another site |

Tools MAY define their own channels; keep names lowercase-kebab.

## Identity, achievements, telemetry
- **Identity** — `LocalFirst.identity` = a stable `{ id, handle }` generated once and reused across every tool.
- **Achievements** — `LocalFirst.achievements.unlock('first-win')` — persisted, broadcast, and shown in the global profile.
- **Telemetry** — `LocalFirst.telemetry.record('event', {...})` appends to a local log; `LocalFirst.telemetry.export()` returns it as JSON you can harvest into a public dataset.

## Discovery (for agents & crawlers)
- Catalog: `https://kody-w.github.io/localFirstTools/landgrab/index.json`
- LLM manifest: `https://kody-w.github.io/localFirstTools/llms.txt`
- MCP tools: `https://kody-w.github.io/localFirstTools/landgrab/mcp/tools.json`
- Training corpus: `https://kody-w.github.io/localFirstTools/landgrab/corpus/corpus.jsonl`

Validate a message against [`protocol/localfirst.schema.json`](protocol/localfirst.schema.json) or the
[interactive validator](protocol/validate.html).

## Conformance
A tool is **LocalFirst-conformant** if it: (a) is a single self-contained HTML file, (b) persists its
own state locally, (c) requires no server to function, and (d) — if it emits scores/achievements/telemetry —
uses the reserved channels above. Conformant tools are tagged `bus` in the catalog.

_MIT licensed. Fork it, ship compatible tools, and they'll speak to the whole ecosystem._
