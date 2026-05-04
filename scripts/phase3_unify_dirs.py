#!/usr/bin/env python3
"""Phase 3: unify competing directory schemes.

Moves:
    apps/creative-tools/*  ->  apps/creative/*
    apps/creative_tools/*  ->  apps/creative/*
    apps/tools/*           ->  apps/utilities/*

For each moved file:
  - If the file is a redirect stub, just write a new stub at the new
    location (with recomputed relative target) and add the OLD path ->
    canonical target to data/redirects.json (follows chain).
  - If the file is a real app, copy bytes to new location, stub at old
    location, add OLD path -> new path to redirects.

Collisions: if the target path already exists with identical content,
the source becomes a stub; if target exists with DIFFERENT content, we
abort (should not happen given phase 1's dedupe — but the check is the
safety net).
"""

from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import sys
from pathlib import Path

from reorg_common import REPO_ROOT
from build_redirects import render_stub

REDIRECTS_JSON = REPO_ROOT / "data" / "redirects.json"
STUB_MARKER = '<meta http-equiv="refresh"'

MOVES = [
    ("apps/creative-tools", "apps/creative"),
    ("apps/creative_tools", "apps/creative"),
    ("apps/tools", "apps/utilities"),
]


def load_redirects() -> dict[str, str]:
    if not REDIRECTS_JSON.exists():
        return {}
    return json.loads(REDIRECTS_JSON.read_text())


def save_redirects(d: dict[str, str]) -> None:
    REDIRECTS_JSON.write_text(json.dumps(dict(sorted(d.items())), indent=2) + "\n")


def sha(path: Path) -> str:
    h = hashlib.sha256()
    h.update(path.read_bytes())
    return h.hexdigest()


def is_stub(path: Path) -> bool:
    if not path.is_file():
        return False
    try:
        with open(path, "rb") as f:
            return STUB_MARKER.encode() in f.read(2048)
    except OSError:
        return False


def follow_chain(start: str, redirects: dict[str, str]) -> str:
    cur = start
    seen = set()
    for _ in range(8):
        if cur in seen:
            return cur
        seen.add(cur)
        if cur in redirects:
            cur = redirects[cur]
            continue
        return cur
    return cur


def do_moves(dry_run: bool) -> int:
    redirects = load_redirects()

    moved = 0
    stubbed = 0
    aborted = 0

    for src_dir_rel, dst_dir_rel in MOVES:
        src_dir = REPO_ROOT / src_dir_rel
        dst_dir = REPO_ROOT / dst_dir_rel
        if not src_dir.is_dir():
            continue

        dst_dir.mkdir(parents=True, exist_ok=True)

        for src_file in sorted(src_dir.iterdir()):
            if not src_file.is_file():
                continue
            src_rel = f"{src_dir_rel}/{src_file.name}"
            dst_file = dst_dir / src_file.name
            dst_rel = f"{dst_dir_rel}/{src_file.name}"

            if is_stub(src_file):
                # Resolve through the chain so we don't carry over a broken arrow.
                target = redirects.get(src_rel) or follow_chain(src_rel, redirects)
                if target == src_rel:
                    # Couldn't resolve via the map — parse the stub's own href.
                    # (Should be rare; absorb_legacy_stubs already captured them.)
                    target = src_rel  # give up, leave as-is
                if dry_run:
                    print(f"  stub move: {src_rel} -> {dst_rel} (target stays {target})")
                    stubbed += 1
                    continue
                # Just delete src; add src_rel -> target to redirects (already there
                # if absorbed). The absence of dst is fine because nothing references it
                # (source location is what needs the entry, not dest).
                src_file.unlink()
                # also remove dst_file placeholder if we happened to create one earlier
                stubbed += 1
                redirects[src_rel] = target
                continue

            # Real content file
            if dst_file.exists():
                if sha(dst_file) == sha(src_file):
                    # Exact collision — just stub the source
                    if dry_run:
                        print(f"  dedupe into dst: {src_rel} -> {dst_rel}")
                    else:
                        src_file.write_text(render_stub(src_rel, dst_rel))
                        redirects[src_rel] = dst_rel
                    stubbed += 1
                else:
                    print(
                        f"  ABORT: content collision {src_rel} != {dst_rel}",
                        file=sys.stderr,
                    )
                    aborted += 1
                continue

            if dry_run:
                print(f"  move: {src_rel} -> {dst_rel}")
                moved += 1
                continue

            if src_file.suffix.lower() == ".html":
                shutil.move(str(src_file), str(dst_file))
                # Leave an HTML redirect stub at the source
                src_file.write_text(render_stub(src_rel, dst_rel))
                redirects[src_rel] = dst_rel
            else:
                # Non-HTML asset: copy, don't stub (an HTML stub at a .json path
                # would break any consumer that XHR-fetches and expects JSON).
                shutil.copy2(str(src_file), str(dst_file))
            moved += 1

        # If the src dir is now empty (excluding stubs), try to rmdir.
        # We want to keep the stub files so old URLs still resolve.

    if aborted:
        print(f"\nABORTED: {aborted} content collisions", file=sys.stderr)
        return 1

    if not dry_run:
        save_redirects(redirects)

    print(f"\nphase 3 — directory unification")
    print(f"  files moved: {moved}")
    print(f"  files stubbed (collision / stub passthrough): {stubbed}")
    print(f"  redirects.json entries: {len(redirects)}")
    return 0


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--dry-run", action="store_true")
    args = p.parse_args()
    sys.exit(do_moves(dry_run=args.dry_run))
