# LocalFirst Tools — Corpus Datasheet

A clean, licensed, attributed dataset of **2885+ single-file, offline-first web tools** — ideal
for training/evaluating code models, studying single-file app design, or powering tool-discovery agents.

## Files
- [`corpus.jsonl`](corpus.jsonl) — one JSON object per tool: `{ id, title, category, tags, description, url, code_url, size, license, attribution }`.
- Full source of every tool is fetchable at its `code_url` (`raw.githubusercontent.com/.../main/<path>`).
- Machine-readable index: [`../index.json`](../index.json).

## What's in it
- **~2885 tools** across 33 categories (games, simulations, ai-tools, creative, productivity, utilities, education, business, health…).
- Each is a **self-contained HTML file** — no build, no server — so every row is a complete, runnable program.
- Metadata extracted from each file's `<title>`, meta description, and detected capabilities (`3d`, `bus`, `interactive`).

## Intended uses
- Training / fine-tuning code models on **complete, runnable, single-file programs**.
- Evaluating "prompt → working app" generation.
- Building tool-discovery / recommendation agents.

## Provenance & license
- Author: **kody-w** · Repo: `kody-w/localFirstTools` · License: **MIT**.
- Please retain the `attribution` field. Regenerated on every deploy by `landgrab/generate.mjs`.

## How to consume
```bash
curl -s https://kody-w.github.io/localFirstTools/landgrab/corpus/corpus.jsonl \
  | head -1 | jq .           # inspect one row
# fetch a tool's full source:
curl -s "$(curl -s .../corpus.jsonl | head -1 | jq -r .code_url)"
```
