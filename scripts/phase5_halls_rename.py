#!/usr/bin/env python3
"""Phase 5: rename Exhibition_Halls/ -> exhibitions/ with kebab-case hall names.

Why pragmatic: a prior partial reorg had moved many apps FROM apps/ INTO
Exhibition_Halls/. Wholesale reversal would churn ~600 files. Instead we:

  1. Rename top dir + hall subdirs to repo convention (lowercase-kebab).
     git mv preserves history.
  2. Add redirect entries Exhibition_Halls/<Old_Hall>/<file> -> exhibitions/<new-hall>/<file>.
  3. Rewrite every redirect TARGET in data/redirects.json that pointed
     into Exhibition_Halls/*, so stubs now land on the new path.
  4. Write redirect stubs at the old Exhibition_Halls/<Hall>/<file>
     paths so case-sensitive deep links still resolve.

Inner files are NOT moved — they stay under exhibitions/<hall>/ as the
Hall's curated content. Later phases (future work) can fold them into
apps/<cat>/ if desired.
"""

from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
from pathlib import Path

from reorg_common import REPO_ROOT
from build_redirects import render_stub

REDIRECTS_JSON = REPO_ROOT / "data" / "redirects.json"
OLD_TOP = "Exhibition_Halls"
NEW_TOP = "exhibitions"

HALL_RENAME = {
    "AI_Research": "ai-research",
    "Educational_Center": "educational-center",
    "Productivity_Suite": "productivity-suite",
    "Simulation_Lab": "simulation-lab",
    "Sound_Studio": "sound-studio",
    "The_Arcade": "the-arcade",
    "Visual_Arts": "visual-arts",
}


def load_redirects() -> dict[str, str]:
    return json.loads(REDIRECTS_JSON.read_text()) if REDIRECTS_JSON.exists() else {}


def save_redirects(d: dict[str, str]) -> None:
    REDIRECTS_JSON.write_text(json.dumps(dict(sorted(d.items())), indent=2) + "\n")


def translate(old_path: str) -> str | None:
    """Translate an Exhibition_Halls/<Hall>/<rest> path to the new form."""
    parts = old_path.split("/")
    if len(parts) < 2:
        return None
    if parts[0] != OLD_TOP:
        return None
    new_hall = HALL_RENAME.get(parts[1])
    if not new_hall:
        return None
    return "/".join([NEW_TOP, new_hall] + parts[2:])


def main(dry_run: bool) -> int:
    redirects = load_redirects()

    old_top_abs = REPO_ROOT / OLD_TOP
    new_top_abs = REPO_ROOT / NEW_TOP

    if not old_top_abs.is_dir():
        print(f"{OLD_TOP}/ not present; nothing to do")
        return 0

    # 1. Compute list of every file currently under Exhibition_Halls (pre-move)
    old_files: list[str] = []
    for dirpath, dirnames, filenames in Path(old_top_abs).walk() if hasattr(Path, "walk") else []:
        pass
    # fallback walker (Path.walk is 3.12+)
    import os
    old_files = []
    for dirpath, dirnames, filenames in os.walk(old_top_abs):
        for fn in filenames:
            rel = Path(dirpath, fn).relative_to(REPO_ROOT)
            old_files.append(str(rel).replace("\\", "/"))

    print(f"  Exhibition_Halls files to relocate: {len(old_files)}")

    # Compute the new path for each
    mapping: dict[str, str] = {}
    for old in old_files:
        new = translate(old)
        if new is None:
            # Files directly under Exhibition_Halls/ (no hall subdir) -> exhibitions/
            parts = old.split("/")
            if len(parts) >= 2 and parts[0] == OLD_TOP:
                new = "/".join([NEW_TOP] + parts[1:])
            else:
                continue
        mapping[old] = new

    if dry_run:
        print(f"  sample mappings:")
        for k, v in list(mapping.items())[:6]:
            print(f"    {k} -> {v}")
        print(f"  total file mappings: {len(mapping)}")
        print(f"  redirect-target rewrites (Exhibition_Halls/* in redirects.json):")
        rewrites = sum(1 for t in redirects.values() if t.startswith(OLD_TOP + "/"))
        print(f"    {rewrites}")
        return 0

    # 2. Move files with git mv when inside a git tree; fallback to shutil.move.
    new_top_abs.mkdir(parents=True, exist_ok=True)
    moved = 0
    for old, new in mapping.items():
        src = REPO_ROOT / old
        dst = REPO_ROOT / new
        dst.parent.mkdir(parents=True, exist_ok=True)
        if dst.exists():
            # target collision — shouldn't happen since exhibitions/ is new,
            # but be safe.
            continue
        try:
            subprocess.run(
                ["git", "mv", "-k", str(src.relative_to(REPO_ROOT)), str(dst.relative_to(REPO_ROOT))],
                cwd=REPO_ROOT,
                check=True,
                capture_output=True,
            )
        except subprocess.CalledProcessError:
            shutil.move(str(src), str(dst))
        moved += 1

    # 3. Write redirect stubs at every old Exhibition_Halls/<path> and
    #    register in data/redirects.json.
    for old, new in mapping.items():
        old_abs = REPO_ROOT / old
        old_abs.parent.mkdir(parents=True, exist_ok=True)
        if old.endswith(".html"):
            old_abs.write_text(render_stub(old, new))
        elif old.endswith(".json"):
            # Duplicate the bytes so XHR consumers still work.
            shutil.copy2(REPO_ROOT / new, old_abs)
        else:
            # Other assets — copy bytes
            shutil.copy2(REPO_ROOT / new, old_abs)
        redirects[old] = new

    # 4. Rewrite every redirect target that was Exhibition_Halls/*
    rewritten_targets = 0
    for k, v in list(redirects.items()):
        if v.startswith(OLD_TOP + "/"):
            new_target = translate(v)
            if new_target:
                redirects[k] = new_target
                rewritten_targets += 1

    # 5. Now regenerate all redirect stubs so their href math reflects
    #    the new layout (some stubs used to point within Exhibition_Halls
    #    with relative hrefs; rel math needs to follow the move).
    from build_redirects import render_stub as _render_stub
    stubs_rewritten = 0
    for stub_rel, target_rel in redirects.items():
        stub_abs = REPO_ROOT / stub_rel
        if stub_rel.endswith(".html") and stub_abs.is_file():
            # Rewrite only if it's our stub (detect by our title marker)
            try:
                head = stub_abs.read_text()[:400]
            except OSError:
                continue
            if "Moved —" in head or "<meta http-equiv=\"refresh\"" in head:
                stub_abs.write_text(_render_stub(stub_rel, target_rel))
                stubs_rewritten += 1

    save_redirects(redirects)

    print(f"\nphase 5 — Exhibition_Halls -> exhibitions/")
    print(f"  files moved: {moved}")
    print(f"  stubs written at old Exhibition_Halls paths: {sum(1 for k in mapping if k.endswith('.html'))}")
    print(f"  redirect-target rewrites: {rewritten_targets}")
    print(f"  stubs regenerated: {stubs_rewritten}")
    print(f"  redirects.json entries: {len(redirects)}")
    return 0


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--dry-run", action="store_true")
    args = p.parse_args()
    sys.exit(main(dry_run=args.dry_run))
