#!/usr/bin/env python3
"""harvest_static_data.py — Static Data Covenant harvester (kody-w/RAR CONSTITUTION.md
Article XXIV) for kody-w/localFirstTools.

Several pages in this repo used to call the unauthenticated GitHub REST API
(api.github.com) directly from the visitor's browser to discover this repo's
own root contents, its recursive file tree, or the artifacts/ directory. That
means every page load spent part of the shared 60-req/hr-per-IP unauthenticated
GitHub API quota on data that only changes when someone pushes to this repo.

This script runs in CI (full checkout, not shallow) and writes committed JSON
snapshots in the SAME shape as the GitHub API responses they replace, so each
page's existing parsing code is untouched — only the fetch URL changes, from
api.github.com to a raw.githubusercontent.com read of these files.

Also writes empty snapshots (same shape) for three foreign-repo lookups these
pages point at, each independently confirmed NOT to exist as of this harvest —
verified against https://github.com/{owner}/{repo} directly (not just the API,
which rate-limits unauthenticated callers): kody-w/Copilot-Agent-365 (404),
kody-w/AI-Agent-Library (404), and the mcp-registry.html template's own
unfilled placeholder owner/repo. No live source to harvest from any of them;
writing empty keeps each page's existing "no results" / mock-data fallback UI
working while eliminating the runtime api.github.com call.

Writes:
  state/tree.json                        — git-trees API shape (recursive)
  state/root_contents.json               — contents API shape (repo root)
  state/artifacts_contents.json          — contents API shape (artifacts/)
  state/mcp_servers_contents.json        — contents API shape (empty; no servers/ dir exists)
  state/copilot_agent365_agents.json     — contents API shape (empty; repo 404s)
  state/copilot_agent365_commit_dates.json — {schema, files:{path:{added,updated}}} (empty; repo 404s)
  state/ai_agent_library_agents.json     — contents API shape (empty; repo 404s)
"""

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
STATE = ROOT / "state"
OWNER = "kody-w"
REPO = "localFirstTools"
BRANCH = "main"


def run(*args):
    return subprocess.run(args, cwd=ROOT, capture_output=True, text=True, check=True).stdout


def require_full_clone():
    shallow = run("git", "rev-parse", "--is-shallow-repository").strip()
    if shallow == "true":
        print("refusing to harvest from a shallow clone (need full history/tree) — use fetch-depth: 0")
        sys.exit(2)


def raw_url(path):
    return f"https://raw.githubusercontent.com/{OWNER}/{REPO}/{BRANCH}/{path}"


def build_tree_json():
    head = run("git", "rev-parse", "HEAD").strip()
    out = run("git", "ls-tree", "-r", "HEAD")
    tree = []
    for line in out.splitlines():
        meta, path = line.split("\t", 1)
        mode, typ, sha = meta.split()
        tree.append({"path": path, "mode": mode, "type": typ, "sha": sha})
    return {"sha": head, "url": "committed-by-ci", "tree": tree, "truncated": False}


def build_contents_json(dir_path):
    """Mirror GET /repos/{owner}/{repo}/contents/{dir_path}: an array of
    {name, path, sha, size, type, download_url, html_url, git_url, url} for
    the immediate children of dir_path (dir_path='' means repo root)."""
    prefix = f"{dir_path}/" if dir_path else ""
    out = run("git", "ls-tree", "HEAD", f"{prefix}" if prefix else ".")
    items = []
    for line in out.splitlines():
        meta, raw_name = line.split("\t", 1)
        mode, typ, sha = meta.split()
        # `git ls-tree HEAD <dir>/` already returns each entry's path prefixed
        # with <dir>/ — don't prepend prefix again (that double-prefixes).
        rel_path = raw_name
        name = raw_name.rsplit("/", 1)[-1]
        entry_type = "dir" if typ == "tree" else "file"
        size = 0
        if entry_type == "file":
            size = int(run("git", "cat-file", "-s", sha).strip())
        items.append({
            "name": name,
            "path": rel_path,
            "sha": sha,
            "size": size,
            "type": entry_type,
            "download_url": raw_url(rel_path) if entry_type == "file" else None,
            "html_url": f"https://github.com/{OWNER}/{REPO}/blob/{BRANCH}/{rel_path}" if entry_type == "file" else f"https://github.com/{OWNER}/{REPO}/tree/{BRANCH}/{rel_path}",
            "git_url": f"https://api.github.com/repos/{OWNER}/{REPO}/git/blobs/{sha}",
            "url": f"https://api.github.com/repos/{OWNER}/{REPO}/contents/{rel_path}?ref={BRANCH}",
        })
    return items


def main():
    require_full_clone()
    STATE.mkdir(parents=True, exist_ok=True)

    tree = build_tree_json()
    (STATE / "tree.json").write_text(json.dumps(tree, indent=0) + "\n")
    print(f"tree.json: {len(tree['tree'])} entries")

    root_contents = build_contents_json("")
    (STATE / "root_contents.json").write_text(json.dumps(root_contents, indent=1) + "\n")
    print(f"root_contents.json: {len(root_contents)} entries")

    artifacts_contents = build_contents_json("artifacts")
    (STATE / "artifacts_contents.json").write_text(json.dumps(artifacts_contents, indent=1) + "\n")
    print(f"artifacts_contents.json: {len(artifacts_contents)} entries")

    # Confirmed-nonexistent foreign lookups (verified directly against
    # https://github.com/{owner}/{repo}, which 404s with no rate limit to
    # confuse the result — see harvest notes above). No live source to
    # harvest from; committed as empty snapshots in the same response shape
    # so pages stop hitting the API while keeping their existing empty/
    # mock-data fallback UI.
    (STATE / "mcp_servers_contents.json").write_text(json.dumps([], indent=1) + "\n")
    (STATE / "copilot_agent365_agents.json").write_text(json.dumps([], indent=1) + "\n")
    (STATE / "copilot_agent365_commit_dates.json").write_text(
        json.dumps({"schema": "commit-dates/1", "files": {}}, indent=1) + "\n")
    (STATE / "ai_agent_library_agents.json").write_text(json.dumps([], indent=1) + "\n")
    print("wrote empty snapshots for confirmed-nonexistent foreign lookups (mcp servers, Copilot-Agent-365, AI-Agent-Library)")


if __name__ == "__main__":
    main()
