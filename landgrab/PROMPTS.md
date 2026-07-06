# Prompt pack — grow the empire (#10)

Copy-paste prompts to expand LocalFirst Tools autonomously. Every new tool should be a single
self-contained HTML file, get harness-verified, deploy to the repo, and auto-register in the
public index (`node landgrab/generate.mjs`).

### Build + register a new tool
> "Build a single-file, offline-first HTML tool that ____. It must run with no server and store
> state in localStorage. Include the LocalFirst runtime
> (`https://kody-w.github.io/localFirstTools/landgrab/lib/localfirst.js`) and emit a `score`/
> `achievement`/`telemetry` where it makes sense. Write a headless Playwright check that proves it
> works, iterate until green, drop it in `apps/<category>/`, run `node landgrab/generate.mjs`, and
> deploy to `main` via a fresh worktree off `origin/main`."

### Mine gaps, then fill them
> "Read `landgrab/index.json`, cluster the 2885 tools by category, find the 5 highest-value gaps a
> local-first tool could fill, then build + verify + deploy + register one tool for each."

### Upgrade an existing tool to the protocol
> "Take `apps/<path>.html`, add the LocalFirst runtime, wire its wins/scores onto the reserved bus
> channels so it joins cross-app leaderboards + achievements, keep it single-file, verify, redeploy."

### Auto-curate the front page
> "From `landgrab/index.json`, generate a fresh 'featured' set (best 3D + bus tools per category) and
> update the HQ's featured rail. Keep it deterministic so the diff is reviewable."

Rules: single file · no server · localStorage state · re-run the generator so the index/llms.txt/
sitemap/MCP/corpus stay live · deploy off `origin/main` (never clobber local WIP).
