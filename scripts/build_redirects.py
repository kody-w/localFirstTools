#!/usr/bin/env python3
"""Reads data/redirects.json and writes a small meta-refresh HTML stub at every
old path pointing to its canonical target. Idempotent. Safe to rerun.

Usage:
    python3 scripts/build_redirects.py            # write all stubs
    python3 scripts/build_redirects.py --check    # exit 1 if any stub is missing/wrong
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from reorg_common import REPO_ROOT, rel_redirect_target

REDIRECTS_JSON = REPO_ROOT / "data" / "redirects.json"

STUB_TEMPLATE = """<!DOCTYPE html>
<meta charset="utf-8">
<title>Moved — Local First Tools</title>
<link rel="canonical" href="{target_abs_hint}">
<meta http-equiv="refresh" content="0;url={target}">
<script>location.replace({target_js}+location.search+location.hash)</script>
<style>body{{font:14px/1.5 system-ui;max-width:40em;margin:3em auto;padding:0 1em;color:#333}}a{{color:#06c}}</style>
<p>This tool moved. <a href="{target}">Continue →</a></p>
"""


def load_redirects() -> dict[str, str]:
    if not REDIRECTS_JSON.exists():
        return {}
    return json.loads(REDIRECTS_JSON.read_text())


def render_stub(stub_rel: str, target_rel: str) -> str:
    stub_path = Path(stub_rel)
    target_path = Path(target_rel)
    rel = rel_redirect_target(stub_path, target_path)
    # Absolute hint is only a hint for SEO; we don't know the deploy prefix so
    # use a path-rooted form. Relative redirect is what actually runs.
    return STUB_TEMPLATE.format(
        target=rel,
        target_abs_hint="/" + target_rel,
        target_js=json.dumps(rel),
    )


def build(check_only: bool) -> int:
    redirects = load_redirects()
    missing = []
    wrote = 0
    for stub_rel, target_rel in sorted(redirects.items()):
        stub_abs = REPO_ROOT / stub_rel
        target_abs = REPO_ROOT / target_rel
        if not target_abs.exists():
            print(f"ERROR: redirect target missing: {stub_rel} -> {target_rel}", file=sys.stderr)
            missing.append(stub_rel)
            continue
        content = render_stub(stub_rel, target_rel)
        if check_only:
            if not stub_abs.exists() or stub_abs.read_text() != content:
                missing.append(stub_rel)
            continue
        stub_abs.parent.mkdir(parents=True, exist_ok=True)
        stub_abs.write_text(content)
        wrote += 1

    if check_only:
        if missing:
            print(f"{len(missing)} stub(s) missing or stale", file=sys.stderr)
            for m in missing[:10]:
                print(f"  {m}", file=sys.stderr)
            return 1
        print(f"OK: all {len(redirects)} redirect stubs present and current")
        return 0

    print(f"Wrote {wrote} redirect stub(s); {len(missing)} skipped due to missing targets")
    return 1 if missing else 0


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--check", action="store_true")
    args = p.parse_args()
    sys.exit(build(check_only=args.check))
