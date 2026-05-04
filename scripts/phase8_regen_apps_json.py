#!/usr/bin/env python3
"""Phase 8: regenerate data/config/utility_apps_config.json from apps/**.

Walks apps/<cat>/<name>.html for every cat except _archive and
index-variants, skips redirect stubs, and emits an apps.json entry per
real app file.

Preserves metadata (title, description, tags, icon) from the existing
config when a path survives; auto-generates sensible defaults for new
entries.
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import re
import sys
from pathlib import Path

from reorg_common import REPO_ROOT

CONFIG = REPO_ROOT / "data" / "config" / "utility_apps_config.json"
STUB_MARKER = b'<meta http-equiv="refresh"'

EXCLUDE_CATS = {"_archive", "index-variants"}

CATEGORY_ICONS = {
    "ai-tools": "\U0001f916",
    "games": "\U0001f3ae",
    "development": "\U0001f4bb",
    "education": "\U0001f4da",
    "business": "\U0001f4bc",
    "health": "\U0001f331",
    "media": "\U0001f3a5",
    "productivity": "\u2705",
    "creative": "\U0001f3a8",
    "simulations": "\U0001f52c",
    "quantum-worlds": "\U0001f300",
    "utilities": "\U0001f527",
    "uncategorized": "\U0001f4e6",
}


def is_stub(p: Path) -> bool:
    try:
        with open(p, "rb") as f:
            return STUB_MARKER in f.read(2048)
    except OSError:
        return False


def title_from_name(stem: str) -> str:
    s = re.sub(r"[_\-]+", " ", stem).strip()
    return " ".join(w.capitalize() for w in s.split())


def load_existing() -> dict[str, dict]:
    if not CONFIG.exists():
        return {}
    d = json.loads(CONFIG.read_text())
    return {a.get("path", "").lstrip("./"): a for a in d.get("apps", [])}


def main(dry_run: bool) -> int:
    existing_by_path = load_existing()
    apps_dir = REPO_ROOT / "apps"

    entries = []
    seen_ids: set[str] = set()

    for cat_dir in sorted(p for p in apps_dir.iterdir() if p.is_dir()):
        cat = cat_dir.name
        if cat in EXCLUDE_CATS:
            continue
        icon = CATEGORY_ICONS.get(cat, "\U0001f4e6")
        for f in sorted(cat_dir.glob("*.html")):
            if is_stub(f):
                continue
            rel = f.relative_to(REPO_ROOT).as_posix()
            path_key_dot = f"./{rel}"
            old = existing_by_path.get(rel) or existing_by_path.get(path_key_dot.lstrip("./"))

            if old:
                entry = dict(old)
                entry["path"] = path_key_dot
                entry["tags"] = old.get("tags") or [cat.replace("-", " ")]
                entry.setdefault("icon", icon)
            else:
                slug = re.sub(r"[^a-z0-9-]+", "-", f.stem.lower()).strip("-")
                entry = {
                    "id": slug,
                    "title": title_from_name(f.stem),
                    "description": f"A {cat.replace('-', ' ')} application",
                    "tags": [cat.replace("-", " ")],
                    "path": path_key_dot,
                    "icon": icon,
                }

            # de-dup ids
            base_id = entry["id"]
            n = 2
            while entry["id"] in seen_ids:
                entry["id"] = f"{base_id}-{n}"
                n += 1
            seen_ids.add(entry["id"])

            entries.append(entry)

    out = {
        "version": "2.1",
        "lastUpdated": dt.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ"),
        "apps": entries,
    }

    if dry_run:
        print(f"apps found: {len(entries)}")
        for e in entries[:8]:
            print(f"  {e['id']:40s} {e['path']}")
        return 0

    CONFIG.write_text(json.dumps(out, indent=2, ensure_ascii=False) + "\n")
    print(f"apps.json regenerated: {len(entries)} entries")
    return 0


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--dry-run", action="store_true")
    args = p.parse_args()
    sys.exit(main(dry_run=args.dry_run))
