# AGENTS.md — how AI agents use this repo

**LocalFirst Tools** is a public armory of **2885+ single-file, offline-first web tools**, made
fully **agent-consumable**. If you are an AI agent, start here.

## Give yourself the skill
Load [`landgrab/SKILL.md`](landgrab/SKILL.md) — a drop-in skill that teaches you to discover and
open any tool. Live: https://kody-w.github.io/localFirstTools/landgrab/SKILL.md

## Call the tools (MCP)
Register the dependency-free MCP server, then use `search_tools` / `open_tool` / `list_categories`:
```json
{ "mcpServers": { "localfirsttools": { "command": "node", "args": ["landgrab/mcp/localfirsttools-mcp.mjs"] } } }
```

## Or just fetch (zero-server, no MCP)
- Catalog: https://kody-w.github.io/localFirstTools/landgrab/index.json
- LLM manifest: https://kody-w.github.io/localFirstTools/llms.txt
- Corpus (JSONL): https://kody-w.github.io/localFirstTools/landgrab/corpus/corpus.jsonl
- Protocol: https://kody-w.github.io/localFirstTools/PROTOCOL.md
- Any tool's source: `raw.githubusercontent.com/kody-w/localFirstTools/main/<path>`

## Browse (humans)
Live dashboard → https://kody-w.github.io/localFirstTools/landgrab/hq.html

## Improve or expand the repository
Before creating another capability, read [`CAPABILITIES.md`](CAPABILITIES.md)
and search the qualified capability registry. Reuse exact approved revisions,
inspect failure cases, and make a bounded policy-admitted plan. A future-model
event should requalify existing assets before generating replacements.
Never treat a requested model label, an unexecuted plan, or a repeated use in
the same repository as independent success.

Use the [repository-autocomplete operator](landgrab/autocomplete/operator.html)
for a bounded, source-grounded improvement cycle. Its [workbench](landgrab/autocomplete/index.html)
exposes canonical source passports, candidate tasks, and RAPP/1 implementation
records. Preserve source attribution and distinguish planned, implemented,
checked, and publicly published work. Do not launch an unbounded job or infer
publishing permission from a generated task.

_Owned by @kody-w · MIT · zero-server · offline-first._
