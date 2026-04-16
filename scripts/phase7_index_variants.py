#!/usr/bin/env python3
"""Phase 7: consolidate index* HTML variants.

Rule:
  - index.html stays at root (canonical launcher)
  - every other index*.html at root moves to apps/index-variants/
  - if the name already exists at apps/index-variants/ with same content,
    just stub the source
  - if different content, append a short hash to the variant filename
    so both survive (version preservation)
"""

from __future__ import annotations

import argparse
import json
import shutil
import sys
from pathlib import Path

from reorg_common import REPO_ROOT, sha256
from build_redirects import render_stub

REDIRECTS_JSON = REPO_ROOT / "data" / "redirects.json"
VARIANTS_DIR = REPO_ROOT / "apps" / "index-variants"


def load_redirects() -> dict[str, str]:
    return json.loads(REDIRECTS_JSON.read_text()) if REDIRECTS_JSON.exists() else {}


def save_redirects(d: dict[str, str]) -> None:
    REDIRECTS_JSON.write_text(json.dumps(dict(sorted(d.items())), indent=2) + "\n")


def main(dry_run: bool) -> int:
    redirects = load_redirects()
    VARIANTS_DIR.mkdir(parents=True, exist_ok=True)

    moved = 0
    stubbed_dupe = 0
    renamed_variants = 0

    for f in sorted(REPO_ROOT.glob("index*.html")):
        if f.name.lower() == "index.html":
            continue
        src_rel = f.name

        dst = VARIANTS_DIR / f.name
        dst_rel = f"apps/index-variants/{f.name}"

        if dst.exists():
            # Compare content
            if sha256(dst) == sha256(f):
                # exact dup — source becomes stub
                if dry_run:
                    stubbed_dupe += 1
                else:
                    f.write_text(render_stub(src_rel, dst_rel))
                    redirects[src_rel] = dst_rel
                    stubbed_dupe += 1
            else:
                # collision with different content — rename with hash suffix
                short = sha256(f)[:8]
                stem = f.stem
                new_name = f"{stem}__{short}.html"
                dst2 = VARIANTS_DIR / new_name
                dst2_rel = f"apps/index-variants/{new_name}"
                if dry_run:
                    renamed_variants += 1
                else:
                    shutil.move(str(f), str(dst2))
                    f.write_text(render_stub(src_rel, dst2_rel))
                    redirects[src_rel] = dst2_rel
                    renamed_variants += 1
            continue

        # target free — plain move
        if dry_run:
            moved += 1
            continue
        shutil.move(str(f), str(dst))
        f.write_text(render_stub(src_rel, dst_rel))
        redirects[src_rel] = dst_rel
        moved += 1

    if not dry_run:
        save_redirects(redirects)

    print(f"phase 7 — index variants")
    print(f"  moved to apps/index-variants/: {moved}")
    print(f"  stubbed (exact dup of existing variant): {stubbed_dupe}")
    print(f"  renamed-and-moved (content collision):   {renamed_variants}")
    print(f"  redirects.json entries: {len(redirects)}")
    return 0


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--dry-run", action="store_true")
    args = p.parse_args()
    sys.exit(main(dry_run=args.dry_run))
