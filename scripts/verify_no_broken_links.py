#!/usr/bin/env python3
"""Verify that every path referenced by the gallery resolves to either
an existing file OR a redirect stub whose target exists.

Sources of truth checked:
  - data/config/utility_apps_config.json   (all apps[*].path)
  - data/redirects.json                    (all keys + all values must resolve)

Exits 0 on success, 1 on any broken reference.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

from reorg_common import REPO_ROOT

APPS_JSON = REPO_ROOT / "data" / "config" / "utility_apps_config.json"
REDIRECTS_JSON = REPO_ROOT / "data" / "redirects.json"


def load_apps_paths() -> list[str]:
    if not APPS_JSON.exists():
        return []
    data = json.loads(APPS_JSON.read_text())
    paths = []
    for app in data.get("apps", []):
        p = app.get("path", "")
        if p.startswith("./"):
            p = p[2:]
        if p:
            paths.append(p)
    return paths


def load_redirects() -> dict[str, str]:
    if not REDIRECTS_JSON.exists():
        return {}
    return json.loads(REDIRECTS_JSON.read_text())


def resolves(rel_path: str, redirects: dict[str, str]) -> tuple[bool, str]:
    """Return (ok, reason). Follows redirects transitively (max 8 hops)."""
    seen = set()
    cur = rel_path
    for _ in range(8):
        if cur in seen:
            return False, f"redirect cycle via {cur}"
        seen.add(cur)
        if (REPO_ROOT / cur).exists():
            return True, "file"
        if cur in redirects:
            cur = redirects[cur]
            continue
        return False, f"missing (no file, no redirect): {cur}"
    return False, f"redirect chain too long from {rel_path}"


def main() -> int:
    redirects = load_redirects()
    app_paths = load_apps_paths()

    print(f"verifying {len(app_paths)} app paths + {len(redirects)} redirect entries ...")

    broken = []

    # 1. Every app path in config must resolve
    for p in app_paths:
        ok, why = resolves(p, redirects)
        if not ok:
            broken.append(("apps.json", p, why))

    # 2. Every redirect target must exist (follows chain)
    for src, dst in redirects.items():
        ok, why = resolves(dst, redirects)
        if not ok:
            broken.append(("redirects.json target", f"{src} -> {dst}", why))
        # And the source path should NOT have a real file (if it does, the
        # stub hasn't been written yet — that's handled by build_redirects).

    if broken:
        print(f"\nFAIL: {len(broken)} broken reference(s)")
        for origin, path, why in broken[:25]:
            print(f"  [{origin}] {path}  ({why})")
        if len(broken) > 25:
            print(f"  ... and {len(broken)-25} more")
        return 1

    print("OK: all references resolve")
    return 0


if __name__ == "__main__":
    sys.exit(main())
