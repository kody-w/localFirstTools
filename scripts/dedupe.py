#!/usr/bin/env python3
"""Phase 1: collapse byte-identical HTML duplicates across gallery roots.

For each hash-group with >1 file:
  - pick the canonical location via reorg_common.canonical_score
  - for every non-canonical file, replace it with a redirect stub and add
    an entry to data/redirects.json

Never touches files already in data/redirects.json (they are already stubs).
Never deletes the canonical copy. Idempotent.

Usage:
    python3 scripts/dedupe.py --dry-run
    python3 scripts/dedupe.py
"""

from __future__ import annotations

import argparse
import json
import sys
from collections import defaultdict
from pathlib import Path

from reorg_common import (
    REPO_ROOT,
    iter_gallery_html,
    pick_canonical,
    sha256,
)
from build_redirects import render_stub

REDIRECTS_JSON = REPO_ROOT / "data" / "redirects.json"
LOG_JSONL = REPO_ROOT / "scripts" / "reorg_log.jsonl"

# A stub is small and its hash is stable per (source, target) pair. We skip
# files whose content already looks like a stub so reruns are idempotent.
STUB_MARKER = '<meta http-equiv="refresh"'


def load_redirects() -> dict[str, str]:
    if not REDIRECTS_JSON.exists():
        return {}
    return json.loads(REDIRECTS_JSON.read_text())


def save_redirects(d: dict[str, str]) -> None:
    REDIRECTS_JSON.parent.mkdir(parents=True, exist_ok=True)
    REDIRECTS_JSON.write_text(json.dumps(dict(sorted(d.items())), indent=2) + "\n")


def looks_like_stub(abs_path: Path) -> bool:
    try:
        # stubs are tiny; read first 2KB only
        with open(abs_path, "rb") as f:
            head = f.read(2048)
        return STUB_MARKER.encode() in head
    except OSError:
        return False


def log(event: dict) -> None:
    LOG_JSONL.parent.mkdir(parents=True, exist_ok=True)
    with open(LOG_JSONL, "a") as f:
        f.write(json.dumps(event) + "\n")


def main(dry_run: bool) -> int:
    redirects = load_redirects()
    already_stubbed = set(redirects.keys())

    # 1. Hash every gallery HTML (skipping known stubs)
    by_hash: dict[str, list[Path]] = defaultdict(list)
    hashed = 0
    skipped_stubs = 0
    for rel in iter_gallery_html():
        abs_p = REPO_ROOT / rel
        if str(rel) in already_stubbed:
            skipped_stubs += 1
            continue
        if looks_like_stub(abs_p):
            skipped_stubs += 1
            continue
        try:
            by_hash[sha256(abs_p)].append(rel)
            hashed += 1
        except OSError as e:
            print(f"warn: cannot hash {rel}: {e}", file=sys.stderr)

    # 2. For each group >1, pick canonical, stub rest
    groups = [(h, paths) for h, paths in by_hash.items() if len(paths) > 1]
    print(f"hashed: {hashed}; skipped stubs: {skipped_stubs}; dup groups: {len(groups)}")

    dup_file_count = sum(len(paths) - 1 for _, paths in groups)
    print(f"files that will become stubs: {dup_file_count}")

    if dry_run:
        # print a sample
        for h, paths in sorted(groups, key=lambda g: -len(g[1]))[:10]:
            canon = pick_canonical(paths)
            others = [p for p in paths if p != canon]
            print(f"  hash {h[:8]}  canon={canon}  stubs={len(others)}  (e.g. {others[0]})")
        return 0

    made = 0
    bytes_freed = 0
    for h, paths in groups:
        canon = pick_canonical(paths)
        canon_abs = REPO_ROOT / canon
        for other in paths:
            if other == canon:
                continue
            other_abs = REPO_ROOT / other
            try:
                before = other_abs.stat().st_size
            except OSError:
                before = 0
            # write stub
            stub_content = render_stub(str(other), str(canon))
            other_abs.write_text(stub_content)
            redirects[str(other)] = str(canon)
            after = len(stub_content.encode())
            bytes_freed += max(0, before - after)
            made += 1
            log({"phase": 1, "action": "stub", "src": str(other), "canonical": str(canon), "bytes_saved": before - after})

    save_redirects(redirects)

    print(f"\nphase 1 complete")
    print(f"  stubs written: {made}")
    print(f"  bytes freed: {bytes_freed:,} (~{bytes_freed/1024/1024:.1f} MiB)")
    print(f"  redirects.json entries: {len(redirects)}")
    return 0


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--dry-run", action="store_true")
    args = p.parse_args()
    sys.exit(main(dry_run=args.dry_run))
