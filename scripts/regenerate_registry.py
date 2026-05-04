#!/usr/bin/env python3
"""
regenerate_registry.py — single source of truth for data/config/utility_apps_config.json

Walks `apps/**/*.html` (READ-ONLY — never moves files) and emits a fresh
registry that the gallery launcher (root index.html) consumes at runtime.

Per app, extracts metadata from the actual HTML in this priority order:
    title       <title> → first <h1> → humanized filename
    description <meta name="description"> → first <p> in body → category fallback
    tags        <meta name="keywords"> → category-based defaults
    icon        <meta name="icon"> → category-based default emoji

ID is path-based to GUARANTEE uniqueness:    id = f"{category}__{filename_stem}"
This prevents the silent overwrite bug in gallery-foryou.html's recommender
map when two apps share a filename across categories. The previous filename
in the registry stem is kept as `aliases` for any consumer that wants to
resolve old localStorage keys.

Usage:
    python3 scripts/regenerate_registry.py            # write registry
    python3 scripts/regenerate_registry.py --dry-run  # diff only, no write
    python3 scripts/regenerate_registry.py --check    # exit 1 if duplicate IDs

Replaces both `intelligent_organizer.py` (which dangerously re-shuffled files
based on filename guesses) and `organize_files.py`.
"""

from __future__ import annotations

import argparse
import html
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
APPS_DIR = REPO_ROOT / "apps"
REGISTRY_PATH = REPO_ROOT / "data" / "config" / "utility_apps_config.json"

CATEGORY_ICONS = {
    "ai-tools": "🤖",
    "business": "💼",
    "development": "🛠️",
    "education": "📚",
    "games": "🎮",
    "health": "💚",
    "index-variants": "🪞",
    "media": "🎨",
    "p2p-world": "🌐",
    "productivity": "✅",
    "quantum-worlds": "🌌",
    "utilities": "🧰",
}

CATEGORY_TAGS = {
    "ai-tools": ["ai", "agent"],
    "business": ["business"],
    "development": ["dev"],
    "education": ["learning"],
    "games": ["game"],
    "health": ["health"],
    "index-variants": ["gallery"],
    "media": ["media"],
    "p2p-world": ["p2p", "3d"],
    "productivity": ["productivity"],
    "quantum-worlds": ["3d", "world"],
    "utilities": ["utility"],
}

# Regex once, reused per file
TITLE_RE = re.compile(r"<title[^>]*>(.*?)</title>", re.IGNORECASE | re.DOTALL)
META_DESC_RE = re.compile(
    r'<meta[^>]+name=["\']description["\'][^>]+content=["\']([^"\']+)["\']',
    re.IGNORECASE,
)
META_KEYWORDS_RE = re.compile(
    r'<meta[^>]+name=["\'](?:keywords|tags)["\'][^>]+content=["\']([^"\']+)["\']',
    re.IGNORECASE,
)
META_ICON_RE = re.compile(
    r'<meta[^>]+name=["\']icon["\'][^>]+content=["\']([^"\']+)["\']',
    re.IGNORECASE,
)
H1_RE = re.compile(r"<h1[^>]*>(.*?)</h1>", re.IGNORECASE | re.DOTALL)
P_RE = re.compile(r"<p[^>]*>(.*?)</p>", re.IGNORECASE | re.DOTALL)
TAG_STRIP_RE = re.compile(r"<[^>]+>")

# Strip common site-suffix patterns from <title>
TITLE_SUFFIX_RE = re.compile(
    r"\s*[\|\u2014\u2013\-\u2022\u00b7]\s*"
    r"(localFirstTools|Local[\s-]?First[\s-]?Tools|"
    r"Vibe Coding Gallery|Gallery|Local-First|"
    r"a vibe coding experiment)\s*$",
    re.IGNORECASE,
)

MAX_DESC_LEN = 220


def humanize(stem: str) -> str:
    parts = re.split(r"[-_\s]+", stem)
    return " ".join(p.capitalize() if p.islower() else p for p in parts if p)


def clean_text(s: str) -> str:
    s = TAG_STRIP_RE.sub("", s)
    s = html.unescape(s)
    s = re.sub(r"\s+", " ", s).strip()
    return s


def truncate(s: str, n: int = MAX_DESC_LEN) -> str:
    if len(s) <= n:
        return s
    cut = s[: n - 1]
    last_space = cut.rfind(" ")
    if last_space > n * 0.6:
        cut = cut[:last_space]
    return cut.rstrip(",.;:") + "…"


def category_from_path(p: Path) -> str:
    rel = p.relative_to(APPS_DIR)
    return rel.parts[0] if len(rel.parts) > 1 else "uncategorized"


def extract_metadata(path: Path) -> dict:
    try:
        text = path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        text = ""

    category = category_from_path(path)
    stem = path.stem

    # title
    title = ""
    m = TITLE_RE.search(text)
    if m:
        title = clean_text(m.group(1))
        title = TITLE_SUFFIX_RE.sub("", title).strip()
    if not title:
        m = H1_RE.search(text)
        if m:
            title = clean_text(m.group(1))
    if not title:
        title = humanize(stem)

    # description
    desc = ""
    m = META_DESC_RE.search(text)
    if m:
        desc = clean_text(m.group(1))
    if not desc:
        # First <p> in body that's substantial
        for m in P_RE.finditer(text):
            candidate = clean_text(m.group(1))
            if len(candidate) >= 30:
                desc = candidate
                break
    if not desc:
        cat_label = category.replace("-", " ")
        desc = f"Local-first {cat_label} app: {title}."
    desc = truncate(desc)

    # tags
    tags: list[str] = []
    m = META_KEYWORDS_RE.search(text)
    if m:
        tags = [t.strip().lower() for t in m.group(1).split(",") if t.strip()]
    if not tags:
        tags = list(CATEGORY_TAGS.get(category, [category]))
    tags = list(dict.fromkeys(tags))[:6]

    # icon
    icon = ""
    m = META_ICON_RE.search(text)
    if m:
        icon = m.group(1).strip()
    if not icon:
        icon = CATEGORY_ICONS.get(category, "✨")

    return {
        "title": title,
        "description": desc,
        "tags": tags,
        "icon": icon,
    }


def build_registry() -> dict:
    apps: list[dict] = []
    seen_ids: set[str] = set()

    for path in sorted(APPS_DIR.rglob("*.html")):
        # Skip files smaller than 200B (likely empty stubs / redirects)
        try:
            if path.stat().st_size < 200:
                continue
        except OSError:
            continue

        # Skip the apps/utilities/index_sorting.html redirect stub.
        if path.relative_to(REPO_ROOT) == Path("apps/utilities/index_sorting.html"):
            continue

        category = category_from_path(path)
        stem = path.stem
        new_id = f"{category}__{stem}"

        if new_id in seen_ids:
            print(f"WARN: duplicate id collision {new_id} — skipping {path}",
                  file=sys.stderr)
            continue
        seen_ids.add(new_id)

        meta = extract_metadata(path)
        rel_path = path.relative_to(REPO_ROOT).as_posix()

        apps.append({
            "id": new_id,
            "title": meta["title"],
            "description": meta["description"],
            "tags": meta["tags"],
            "path": f"./{rel_path}",
            "icon": meta["icon"],
            "category": category,
            "aliases": [stem] if stem != new_id else [],
        })

    apps.sort(key=lambda a: (a["category"], a["title"].lower()))

    return {
        "version": "3.1",
        "lastUpdated": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "generatedBy": "scripts/regenerate_registry.py v1.0",
        "apps": apps,
    }


def diff_summary(old: dict, new: dict) -> None:
    old_ids = {a["id"]: a for a in old.get("apps", [])}
    new_ids = {a["id"]: a for a in new.get("apps", [])}

    added = [i for i in new_ids if i not in old_ids]
    removed = [i for i in old_ids if i not in new_ids]

    weak_old = sum(
        1
        for a in old.get("apps", [])
        if a.get("description", "").startswith("A ")
        and a.get("description", "").endswith(" application")
    )
    weak_new = sum(
        1
        for a in new["apps"]
        if a.get("description", "").startswith("A ")
        and a.get("description", "").endswith(" application")
    )

    print(f"Apps:               {len(old_ids):3d} → {len(new_ids):3d}")
    print(f"  added:            {len(added)}")
    print(f"  removed:          {len(removed)}")
    print(f"Boilerplate descs:  {weak_old:3d} → {weak_new:3d}")
    print(f"Duplicate ids:      "
          f"{len(old.get('apps', [])) - len({a['id'] for a in old.get('apps', [])})} → "
          f"{len(new['apps']) - len({a['id'] for a in new['apps']})}")


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--dry-run", action="store_true",
                    help="print diff vs current registry, don't write")
    ap.add_argument("--check", action="store_true",
                    help="exit 1 if duplicate IDs would be produced")
    args = ap.parse_args()

    new_registry = build_registry()

    new_ids = [a["id"] for a in new_registry["apps"]]
    dup_count = len(new_ids) - len(set(new_ids))
    if dup_count > 0:
        print(f"FAIL: {dup_count} duplicate IDs", file=sys.stderr)
        return 1
    if args.check:
        print(f"OK: {len(new_ids)} unique IDs")
        return 0

    old_registry: dict = {}
    if REGISTRY_PATH.exists():
        old_registry = json.loads(REGISTRY_PATH.read_text())

    diff_summary(old_registry, new_registry)

    if args.dry_run:
        print("(--dry-run; no file written)")
        return 0

    REGISTRY_PATH.parent.mkdir(parents=True, exist_ok=True)
    REGISTRY_PATH.write_text(
        json.dumps(new_registry, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    print(f"Wrote {REGISTRY_PATH.relative_to(REPO_ROOT)} "
          f"({len(new_registry['apps'])} apps)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
