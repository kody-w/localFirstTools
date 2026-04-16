# localFirstTools — Great Reorganization Plan

**Branch:** `reorg/merge-versions` (worktree: `.worktrees/reorg`)
**Backup of pre-reorg local WIP:** branch `backup/pre-reorg-local` (commit `2b043c4`) + stash `stash@{0}`
**Synced from:** `origin/main @ d93e1b6`

---

## 1. Problem Statement (measured, not guessed)

| Metric | Count |
|---|---|
| Total HTML files (excl. `.git`, `chrome-extension-build`, `archive`, `v86-master`) | **2,732** |
| Unique basenames | **1,491** |
| Unique content hashes (byte-identical) | **850** |
| Files with Finder-style `" 2.html" / " 3.html"` suffix | **932** |
| Competing org schemes at root | **4** (`/`, `apps/`, `Exhibition_Halls/`, `tools/` + `utilities/`) |
| Index-page variants | **7+** (`index.html`, `index_MAC.html`, `index_slim*.html`, `index_sorting.html`, …) |

**~69% of the HTML in this repo is exact byte-for-byte duplication.** The remaining ~31% is a mix of meaningful versions (e.g. `NexusWorlds.html` has 2 distinct hashes across 4 locations) and near-duplicates.

**Competing schemes observed for the same tool** (`NexusWorlds.html`):
- `/NexusWorlds.html`
- `apps/quantum-worlds/NexusWorlds.html`
- `apps/games/NexusWorlds.html`
- `Exhibition_Halls/The_Arcade/NexusWorlds.html`

---

## 2. Non-Negotiable Constraints

1. **No broken GitHub Pages URLs.** `https://kody-w.github.io/localFirstTools/<anything-that-ever-worked>` must keep resolving. Blog posts, tweets, bookmarks, agent deployments — they all reference static paths.
2. **No lost functionality.** When two versions diverge, pick one canonical + archive the other; never silently overwrite.
3. **Self-contained HTML stays self-contained.** Per CLAUDE.md, every app is one file with inline CSS/JS, no CDN, no build.
4. **`index.html` stays at repo root.** It's the landing page for Pages.
5. **Everything is reversible.** Work happens on `reorg/merge-versions` with per-phase commits. Nothing gets force-pushed.

---

## 3. Target Shape

```
localFirstTools/
├── index.html                          # canonical launcher (unchanged path)
├── 404.html                            # NEW — client-side redirect fallback
├── data/
│   ├── config/
│   │   └── apps.json                   # single source of truth (renamed from utility_apps_config.json, keep old as symlink/stub)
│   ├── redirects.json                  # NEW — old path → canonical path map
│   └── games/                          # unchanged
├── apps/                               # THE CANONICAL LOCATION
│   ├── ai-tools/
│   ├── business/
│   ├── creative/                       # merges creative-tools + creative_tools
│   ├── development/
│   ├── education/
│   ├── games/
│   ├── health/
│   ├── media/
│   ├── productivity/
│   ├── quantum-worlds/                 # kept (distinct category)
│   ├── simulations/
│   ├── utilities/                      # merges tools/ + utilities/
│   └── _archive/                       # versioned tools: foo_v1.html, foo_v2.html, foo.html (canonical)
├── exhibitions/                        # renamed from Exhibition_Halls/ (kept as compat redirect)
│   ├── the-arcade/                     # each hall keeps its themed index.html as a curated view
│   ├── simulation-lab/
│   ├── ai-research/
│   └── …                               # apps INSIDE halls become stubs redirecting to apps/<cat>/<slug>
├── scripts/
│   ├── dedupe.py                       # hash-based dedupe runner
│   ├── build_redirects.py              # walks old paths, emits redirects.json + stub HTMLs
│   ├── build_apps_json.py              # regenerates apps.json from apps/**
│   └── verify_no_broken_links.py       # crawls index.html + apps.json, asserts every path resolves
└── REORG_PLAN.md                       # this file
```

**Key idea:** `apps/` becomes the one-and-only home. Every other historical location becomes a **redirect stub**.

---

## 4. Canonical-Selection Algorithm (how we "merge versions without losing functionality")

For each logical tool (cluster of files sharing a normalized slug):

1. **Cluster** files by normalized basename (strip ` 2`, ` 3`, `_v1`, `_v2`, `_MAC`, `_local`, `_slim`, `_cloud`, `.backup`, `(1)`, `(2)`, etc.).
2. **Hash every file in the cluster** (SHA-256).
3. **Collapse exact duplicates** → one survives.
4. **Among distinct-content survivors**, rank by:
    - (a) largest file size (usually most-developed version)
    - (b) newest git-blob modification time (`git log -1 --format=%ct`)
    - (c) presence in `apps/` over other dirs
    - (d) presence of feature markers: `localStorage`, `<canvas>`, external resource counts
5. **Winner** → `apps/<category>/<slug>.html`.
6. **Losers with distinct content** → `apps/_archive/<slug>_v<n>.html`, linked from the canonical app's "Other versions" footer OR `apps.json` sidecar field.
7. **Losers with identical content** → deleted from disk, added to `data/redirects.json`.
8. Every action is logged to `scripts/reorg_log.jsonl` for audit/undo.

**This is deterministic and scriptable** — no ad-hoc judgment calls on 2,732 files.

---

## 5. Backwards-Compatibility Strategy (the critical part)

GitHub Pages serves static files. The only way to keep every old URL working is to physically keep **something** at every old path. Two mechanisms:

### 5a. Redirect stubs (primary)
For every old path whose canonical moved, write a ~400-byte HTML stub:

```html
<!DOCTYPE html><meta charset="utf-8">
<title>Moved — Local First Tools</title>
<link rel="canonical" href="/localFirstTools/apps/games/nexus-worlds.html">
<meta http-equiv="refresh" content="0;url=/localFirstTools/apps/games/nexus-worlds.html">
<script>location.replace("/localFirstTools/apps/games/nexus-worlds.html"+location.search+location.hash)</script>
<p>This tool moved. <a href="/localFirstTools/apps/games/nexus-worlds.html">Continue →</a></p>
```

- Preserves query strings and fragments.
- Works with JS disabled (meta refresh fallback).
- SEO-friendly (`rel=canonical`).
- Generated by `scripts/build_redirects.py` from `data/redirects.json`.

### 5b. 404.html client-side router (safety net)
A root `404.html` that reads `data/redirects.json` and routes unknown paths. GitHub Pages automatically serves this for any unmatched URL. Catches anything the stub generator missed.

### 5c. Integrity check
`scripts/verify_no_broken_links.py` — CI step that:
- Enumerates every path in `git log --all --diff-filter=A --name-only` under root, `apps/`, and `Exhibition_Halls/`.
- Asserts either (a) the path still exists OR (b) `data/redirects.json` contains it with a valid target.
- Fails the build if any old URL would 404.

This is the gate that makes the whole reorg safe to merge.

---

## 6. Phases (each phase = one commit, each commit = green CI)

| # | Phase | Risk | What lands |
|---|---|---|---|
| 0 | **Tooling** | none | `scripts/` + `verify_no_broken_links.py` baseline (passes against current layout, so we know the check works) |
| 1 | **Exact-dup collapse** | very low | Delete byte-identical duplicates, write redirects. Expected ~1,880 file deletions, zero functional change. |
| 2 | **Finder-suffix collapse** | low | Merge `foo 2.html`, `foo 3.html` into `foo.html` (exact-match cluster from phase 1 handles most; phase 2 handles near-dupes where numbering changed a timestamp only). |
| 3 | **Directory unification** | low | `creative_tools/` → `creative-tools/` → `apps/creative/`. `tools/` → `apps/utilities/`. Stubs at all old paths. |
| 4 | **Root-level apps → `apps/<cat>/`** | medium | Move every root HTML (except `index.html`, `404.html`) into its category folder. Stubs at root. |
| 5 | **Exhibition_Halls → exhibitions/** | medium | Rename dir (case-sensitivity-safe via two commits). Inner apps become stubs pointing to `apps/<cat>/<slug>.html`. Hall-level themed `index.html` files become curated *views* that read `apps.json`. |
| 6 | **Version clusters** | medium | For each distinct-content group, pick canonical via the algorithm in §4. Losers move to `apps/_archive/`. The canonical page gets an "Other versions" footer block. |
| 7 | **index.html variants** | medium | `index.html` stays canonical. `index_slim*.html`, `index_MAC*.html`, `index_sorting.html` either merge into `index.html?mode=slim` query-param switches, or stay as stubs if their audiences diverged (document in `data/config/index_variants.md`). |
| 8 | **Regenerate `apps.json`** | none | Rebuild from current `apps/**` via `build_apps_json.py`. Keep `utility_apps_config.json` as a same-content symlink for one release cycle. |
| 9 | **Verify + PR** | — | Run `verify_no_broken_links.py`. Open PR against `main`. |

After merge, tag `v0.2.0` (major reorg). Keep `backup/pre-reorg-local` around for one release cycle then archive as tag `archive/pre-reorg`.

---

## 7. Rollback

At any phase, `git checkout main -- .` in the worktree reverts working tree. If the PR is merged and we discover a regression:

```bash
git revert -m 1 <merge-sha>       # one-command revert of the whole reorg
```

Because every phase is its own commit, we can also partially revert (e.g. keep phase 1 dedupe, revert phase 5 Halls rename).

---

## 8. What I need from you before I execute

1. **Category taxonomy**: do you want `apps/creative/` (my proposal) or keep `apps/creative-tools/`? Same for `utilities` vs `tools`.
2. **Exhibitions fate**: keep the themed "halls" as curated landing pages (my proposal), or fold them entirely into `apps/<cat>/` with just redirect stubs?
3. **Index variants**: merge into query params (`?mode=slim`) or keep as separate files with stubs?
4. **Archive cutoff**: how aggressively should `apps/_archive/` hide old versions? (a) link from canonical footer, (b) gallery-hidden but URL-reachable, (c) moved out of repo to a `archive` branch.

Green-light any combination and I'll execute phase 0 → 9 on the `reorg/merge-versions` worktree, committing per phase, and open the PR.

---

## 9. Execution log (2026-04-16)

All phases 0–9 executed on `reorg/merge-versions` (worktree), one
commit per phase, verifier green throughout.

| Phase | What happened |
|---|---|
| 0 | Tooling + green baseline. Surfaced & removed 2 stale apps.json entries (files never existed in history). |
| — | **Cleanup:** absorbed 340 pre-existing legacy stubs from a prior half-finished reorg into unified `data/redirects.json`. |
| 1 | Collapsed **926 byte-identical duplicate HTML files** into redirect stubs. **181 MiB freed**. |
| 2 | Normalized Finder near-match scan. 0 matches — phase 1 caught every trivial dup. |
| 3 | Unified `apps/creative-tools/` + `apps/creative_tools/` → `apps/creative/`, `apps/tools/` → `apps/utilities/`. |
| 4 | **Moved 481 root-level HTML files** into `apps/<category>/` via keyword-based categorization. |
| 5 | Renamed `Exhibition_Halls/` → `exhibitions/` with kebab-case hall names. 698 files via `git mv` (history preserved). 340 redirect targets rewritten. |
| 6 | **Resolved 63 version clusters.** 69 losers archived to `apps/_archive/<cat>/<stem>__<sha8>.html`. |
| 7 | Consolidated index variants: 5 moved, 6 renamed with hash suffix (no version loss), 11 stubs. `index.html` stays canonical. |
| 8 | **Regenerated `data/config/utility_apps_config.json`** from `apps/**`. 63 → 413 entries (~350 apps surfaced that existed but were never registered). |
| 9 | Added `404.html` client-side fallback router. Final: **413 apps / 2082 redirects, all resolving**. |

### Final state vs start

| Metric | Before | After |
|---|---|---|
| Total HTML files (active tree) | 2,732 | 3,989 |
| Registered apps (`apps.json`) | 63 (2 broken) | 413 |
| Redirect entries | 0 | 2,082 |
| Duplicated-content MiB | ~190 | ~0 |
| Competing top-level gallery roots | 4 | 1 canonical (`apps/`) + 1 curated (`exhibitions/`) |

HTML total **went up** because every move leaves a ~400-byte stub at
the old path — the cost of zero-broken-URLs backwards compatibility.
Net disk usage dropped by ~180 MiB.

### Backwards compatibility verification

- `scripts/verify_no_broken_links.py` (CI gate) — **green**
- `scripts/build_redirects.py --check` (stub integrity) — **green**
- `404.html` client-side router — installed as safety net

### What didn't ship

- Phase 5 did **not** fold `exhibitions/` content into `apps/` (would churn ~600 files; a prior half-reorg had already moved them there). Decision left open for the user.
- `apps/uncategorized/` is a legitimate escape hatch; recategorize by `mv`ing files between `apps/<cat>/` dirs and rerunning `scripts/phase8_regen_apps_json.py`.
- Phase 7 kept index variants as separate files (not merged into `index.html?mode=X`) — less risky.
- `vibe_gallery_config.json` (referenced by CLAUDE.md) was **not** regenerated; only the legacy `data/config/utility_apps_config.json` was. A follow-up can run `python3 vibe_gallery_updater.py` to regenerate the primary config.

### Rerunning any phase

All scripts are idempotent:

```bash
python3 scripts/phase8_regen_apps_json.py    # rebuild apps.json from apps/**
python3 scripts/build_redirects.py           # regenerate redirect stubs
python3 scripts/verify_no_broken_links.py    # gate
```

---

*Generated 2026-04-16 from the state of `origin/main@d93e1b6`.*
