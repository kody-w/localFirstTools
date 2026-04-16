#!/usr/bin/env python3
"""Phase 2: collapse Finder-style near-duplicates.

Pairs `<basename> <n>.html` with `<basename>.html` (or lowest-numbered peer).
If their normalized content matches (whitespace/comments/date-strings
ignored), stub the numbered one to the base.

If content genuinely differs, this script LEAVES THEM — those are real
versions and get handled in phase 6.

Idempotent.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from collections import defaultdict
from pathlib import Path

from reorg_common import REPO_ROOT, iter_gallery_html, _FINDER_DUP_RE
from build_redirects import render_stub

REDIRECTS_JSON = REPO_ROOT / "data" / "redirects.json"
STUB_MARKER = '<meta http-equiv="refresh"'

_WS_RE = re.compile(rb"\s+")
_COMMENT_RE = re.compile(rb"<!--.*?-->", re.DOTALL)
_JS_COMMENT_RE = re.compile(rb"/\*.*?\*/", re.DOTALL)
_DATE_RE = re.compile(
    rb"\b(?:20\d{2}[-/]\d{2}[-/]\d{2}|\d{10,13})\b"
)  # ISO dates and unix timestamps


def normalize_hash(path: Path) -> str:
    data = path.read_bytes()
    data = _COMMENT_RE.sub(b"", data)
    data = _JS_COMMENT_RE.sub(b"", data)
    data = _DATE_RE.sub(b"DATE", data)
    data = _WS_RE.sub(b" ", data).strip()
    return hashlib.sha256(data).hexdigest()


def looks_like_stub(abs_path: Path) -> bool:
    try:
        with open(abs_path, "rb") as f:
            return STUB_MARKER.encode() in f.read(2048)
    except OSError:
        return False


def load_redirects() -> dict[str, str]:
    if not REDIRECTS_JSON.exists():
        return {}
    return json.loads(REDIRECTS_JSON.read_text())


def save_redirects(d: dict[str, str]) -> None:
    REDIRECTS_JSON.write_text(json.dumps(dict(sorted(d.items())), indent=2) + "\n")


def main(dry_run: bool) -> int:
    redirects = load_redirects()
    already_stubbed = set(redirects.keys())

    # Index every non-stub HTML by (directory, base stem without suffix)
    # so we can pair siblings.
    pairs: dict[tuple[str, str], list[Path]] = defaultdict(list)

    for rel in iter_gallery_html():
        if str(rel) in already_stubbed:
            continue
        abs_p = REPO_ROOT / rel
        if looks_like_stub(abs_p):
            continue
        stem = rel.stem
        m = _FINDER_DUP_RE.search(stem)
        if m:
            base_stem = stem[: m.start()]
        else:
            base_stem = stem
        key = (str(rel.parent), base_stem)
        pairs[key].append(rel)

    # Only act on keys with >1 sibling
    collapsed = 0
    skipped_diff = 0

    for (dirname, base), siblings in pairs.items():
        if len(siblings) < 2:
            continue

        # compute normalized hash for each
        hashed = {}
        for p in siblings:
            try:
                hashed[p] = normalize_hash(REPO_ROOT / p)
            except OSError:
                pass

        # group by normalized hash
        by_nh: dict[str, list[Path]] = defaultdict(list)
        for p, h in hashed.items():
            by_nh[h].append(p)

        for nh, group in by_nh.items():
            if len(group) < 2:
                continue
            # pick canonical: no Finder suffix if present, else lowest number
            def suffix_num(p: Path) -> int:
                m = _FINDER_DUP_RE.search(p.stem)
                return int(m.group(1)) if m else 0

            group_sorted = sorted(group, key=lambda p: (suffix_num(p), str(p)))
            canon = group_sorted[0]
            for other in group_sorted[1:]:
                if str(other) in redirects:
                    continue
                if dry_run:
                    collapsed += 1
                    if collapsed <= 8:
                        print(f"  would stub: {other}  ->  {canon}")
                    continue
                stub_content = render_stub(str(other), str(canon))
                (REPO_ROOT / other).write_text(stub_content)
                redirects[str(other)] = str(canon)
                collapsed += 1

        # If the group had siblings with different normalized hashes,
        # count them as skipped (real version divergence).
        distinct_nhs = {nh for nh in by_nh if len(by_nh[nh]) >= 1}
        if len(distinct_nhs) > 1:
            skipped_diff += sum(len(by_nh[nh]) for nh in by_nh) - max(
                len(by_nh[nh]) for nh in by_nh
            )

    if not dry_run:
        save_redirects(redirects)

    print(f"phase 2 — Finder near-dup collapse")
    print(f"  sibling groups considered: {sum(1 for s in pairs.values() if len(s) > 1)}")
    print(f"  near-dup stubs {'would-write' if dry_run else 'written'}: {collapsed}")
    print(f"  siblings deferred to phase 6 (real divergence): {skipped_diff}")
    print(f"  redirects.json entries: {len(redirects)}")
    return 0


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--dry-run", action="store_true")
    args = p.parse_args()
    sys.exit(main(dry_run=args.dry_run))
