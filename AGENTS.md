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

_Owned by @kody-w · MIT · zero-server · offline-first._
