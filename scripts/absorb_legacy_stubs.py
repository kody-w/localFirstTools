#!/usr/bin/env python3
"""Absorb pre-existing redirect-stub HTML files into data/redirects.json.

Before this reorg, someone manually wrote ~341 HTML files containing a
<meta http-equiv="refresh"> pointing to a moved location. Those stubs
work, but they're not registered in our redirects.json, they use an older
template, and they use relative paths that weren't normalized.

This script:
  1. Walks the gallery looking for files that LOOK like hand-written stubs
     (small, contain meta-refresh, don't match our current stub template)
  2. Parses the target out of their meta-refresh or JS
  3. Resolves the target relative to the stub's location
  4. Verifies the target file actually exists
  5. Adds {stub_path: target_path} to data/redirects.json
  6. Rewrites the stub with our current template

Result: a single unified redirect mechanism.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

from reorg_common import REPO_ROOT, iter_gallery_html
from build_redirects import render_stub, STUB_TEMPLATE

REDIRECTS_JSON = REPO_ROOT / "data" / "redirects.json"

# Markers for our canonical stub template — files with these are already ours.
OURS_MARKERS = [
    b"<title>Moved \xe2\x80\x94 Local First Tools</title>",
]

REFRESH_RE = re.compile(
    rb'<meta\s+http-equiv=["\']refresh["\']\s+content=["\']\s*\d+\s*;\s*url=([^"\']+)["\']',
    re.IGNORECASE,
)
JS_REPLACE_RE = re.compile(rb'location\.replace\(["\']([^"\']+)["\']')


def load_redirects() -> dict[str, str]:
    if not REDIRECTS_JSON.exists():
        return {}
    return json.loads(REDIRECTS_JSON.read_text())


def save_redirects(d: dict[str, str]) -> None:
    REDIRECTS_JSON.write_text(json.dumps(dict(sorted(d.items())), indent=2) + "\n")


def is_ours(head: bytes) -> bool:
    return any(m in head for m in OURS_MARKERS)


def looks_like_legacy_stub(head: bytes, size: int) -> bool:
    if size > 4096:
        return False
    if is_ours(head):
        return False
    return b"http-equiv" in head and b"refresh" in head


def parse_target(content: bytes) -> str | None:
    m = REFRESH_RE.search(content)
    if m:
        return m.group(1).decode("utf-8", errors="replace").strip()
    m = JS_REPLACE_RE.search(content)
    if m:
        return m.group(1).decode("utf-8", errors="replace").strip()
    return None


def main(dry_run: bool) -> int:
    redirects = load_redirects()
    before = len(redirects)

    absorbed = 0
    rewritten = 0
    skipped_no_target = 0
    skipped_target_missing = 0

    for rel in iter_gallery_html():
        abs_p = REPO_ROOT / rel
        try:
            size = abs_p.stat().st_size
            with open(abs_p, "rb") as f:
                head = f.read(4096)
        except OSError:
            continue

        if not looks_like_legacy_stub(head, size):
            continue

        raw_target = parse_target(head)
        if not raw_target:
            skipped_no_target += 1
            continue

        # Resolve target relative to the stub's directory, then normalize to
        # a repo-relative POSIX path.
        stub_dir = abs_p.parent
        target_abs = (stub_dir / raw_target).resolve()
        try:
            target_rel = target_abs.relative_to(REPO_ROOT.resolve())
        except ValueError:
            skipped_target_missing += 1
            continue
        target_rel_str = str(target_rel).replace("\\", "/")

        if not target_abs.exists():
            skipped_target_missing += 1
            continue

        src_str = str(rel).replace("\\", "/")

        if dry_run:
            absorbed += 1
            if absorbed <= 5:
                print(f"  would absorb: {src_str} -> {target_rel_str}")
            continue

        redirects[src_str] = target_rel_str
        # Rewrite with our template
        abs_p.write_text(render_stub(src_str, target_rel_str))
        absorbed += 1
        rewritten += 1

    if not dry_run:
        save_redirects(redirects)

    print(f"legacy stubs absorbed: {absorbed}")
    print(f"  rewritten to new template: {rewritten}")
    print(f"  skipped (no target parsed): {skipped_no_target}")
    print(f"  skipped (target missing):   {skipped_target_missing}")
    print(f"redirects.json: {before} -> {len(redirects)} entries")
    return 0


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--dry-run", action="store_true")
    args = p.parse_args()
    sys.exit(main(dry_run=args.dry_run))
