#!/usr/bin/env python3
"""
Apply portable improvement patterns to featured HTML apps.

Patterns (only added when MISSING — fully idempotent):
  1. <html lang="en"> — accessibility
  2. <meta charset="UTF-8"> — required
  3. <meta name="viewport" content="width=device-width, initial-scale=1.0"> — mobile
  4. <meta name="description"> — pulled from vibe_gallery_config.json if not boilerplate
  5. <meta name="keywords"> — pulled from registry tags
  6. <meta name="icon"> — pulled from registry icon
  7. Inline SVG favicon — silences /favicon.ico 404

Rules:
  - Skip stub-redirect files (< 2KB)
  - Skip if a closer-matching tag already exists
  - Never replace existing values; only insert when missing
  - Skip files that look like fragments (no <head>, no <html>)

Run:
  python3 scripts/apply_portable_patterns.py --dry-run      # preview
  python3 scripts/apply_portable_patterns.py                # apply
  python3 scripts/apply_portable_patterns.py --check        # exit 1 if any need patching
"""
import argparse
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

VIEWPORT_RE = re.compile(r'<meta[^>]*name=["\']?viewport["\']?', re.IGNORECASE)
CHARSET_RE = re.compile(r'<meta[^>]*charset', re.IGNORECASE)
DESCRIPTION_RE = re.compile(r'<meta[^>]*name=["\']?description["\']?', re.IGNORECASE)
KEYWORDS_RE = re.compile(r'<meta[^>]*name=["\']?keywords["\']?', re.IGNORECASE)
ICON_META_RE = re.compile(r'<meta[^>]*name=["\']?icon["\']?', re.IGNORECASE)
FAVICON_LINK_RE = re.compile(r'<link[^>]*rel=["\']?(shortcut\s+)?icon["\']?', re.IGNORECASE)
HTML_LANG_RE = re.compile(r'<html[^>]*\blang\s*=', re.IGNORECASE)
HTML_TAG_RE = re.compile(r'<html\b[^>]*>', re.IGNORECASE)
HEAD_OPEN_RE = re.compile(r'<head\b[^>]*>', re.IGNORECASE)
TITLE_RE = re.compile(r'<title>([^<]*)</title>', re.IGNORECASE | re.DOTALL)

# Stub-redirect detection
STUB_RE = re.compile(r'(http-equiv=["\']?refresh|location\.replace\()', re.IGNORECASE)

# Boilerplate descriptions we should ignore (auto-generated)
BOILERPLATE_RE = re.compile(
    r'^(A\s+\w+\s+application|Interactive\s+\w+\s+application|Self-contained|Browser-native|Local-first|Offline-first|Powerful)\b',
    re.IGNORECASE
)


def load_registry():
    """Load vibe_gallery_config.json, return {path: app_record}."""
    cfg_path = ROOT / 'vibe_gallery_config.json'
    if not cfg_path.exists():
        return {}
    with cfg_path.open() as f:
        cfg = json.load(f)
    by_path = {}
    for k, c in cfg.get('vibeGallery', {}).get('categories', {}).items():
        for app in c.get('apps', []):
            p = app.get('path', '').lstrip('./').lstrip('/')
            if p:
                by_path[p] = app
    return by_path


def insert_after(text, anchor_pattern, insert_block):
    """Insert insert_block right after the matched anchor_pattern."""
    m = anchor_pattern.search(text)
    if not m:
        return text, False
    pos = m.end()
    return text[:pos] + insert_block + text[pos:], True


def good_description(text):
    """Return text if it looks like a real description, else None."""
    if not text:
        return None
    text = text.strip()
    if len(text) < 20:
        return None
    if BOILERPLATE_RE.search(text):
        return None
    return text


def patch_file(path: Path, registry_entry, dry_run: bool):
    """Apply patterns to one file. Return list of (pattern_name, applied: bool)."""
    raw = path.read_bytes()
    if len(raw) < 2000:
        return [('skip', 'stub or tiny')]
    try:
        text = raw.decode('utf-8')
    except UnicodeDecodeError:
        try:
            text = raw.decode('latin-1')
        except Exception:
            return [('skip', 'undecodable')]

    if STUB_RE.search(text[:1000]):
        return [('skip', 'stub-redirect')]
    if not HTML_TAG_RE.search(text):
        return [('skip', 'no <html>')]
    if not HEAD_OPEN_RE.search(text):
        return [('skip', 'no <head>')]

    changes = []
    new_text = text

    # 1. <html lang="en">
    if not HTML_LANG_RE.search(new_text):
        new_text, ok = (lambda t: HTML_TAG_RE.sub(
            lambda m: m.group(0).replace('<html', '<html lang="en"', 1) if 'lang=' not in m.group(0) else m.group(0),
            t, count=1
        ), True)[0](new_text), True
        if 'lang="en"' in new_text:
            changes.append(('html-lang', True))

    # All other patches insert inside <head>. Build the block to inject after <head>.
    inserts = []

    if not CHARSET_RE.search(new_text):
        inserts.append('<meta charset="UTF-8">')

    if not VIEWPORT_RE.search(new_text):
        inserts.append('<meta name="viewport" content="width=device-width, initial-scale=1.0">')

    if not DESCRIPTION_RE.search(new_text) and registry_entry:
        d = good_description(registry_entry.get('description'))
        if d:
            d_safe = d.replace('"', '&quot;')[:300]
            inserts.append(f'<meta name="description" content="{d_safe}">')

    if not KEYWORDS_RE.search(new_text) and registry_entry:
        tags = registry_entry.get('tags') or []
        if tags:
            tags_str = ','.join(str(t) for t in tags[:8])
            inserts.append(f'<meta name="keywords" content="{tags_str}">')

    if not ICON_META_RE.search(new_text) and registry_entry:
        icon = registry_entry.get('icon')
        if icon:
            inserts.append(f'<meta name="icon" content="{icon}">')

    if not FAVICON_LINK_RE.search(new_text):
        # Pick emoji: registry icon, else category emoji, else generic
        emoji = '🛠️'
        if registry_entry:
            emoji = registry_entry.get('icon') or _category_emoji(registry_entry.get('category', '')) or '🛠️'
        # Strip variation selector from emoji to avoid encoding hassle
        emoji_clean = emoji.replace('\ufe0f', '')
        # SVG-emoji favicon
        svg = (
            f"<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'>"
            f"<text y='.9em' font-size='90'>{emoji_clean}</text>"
            f"</svg>"
        )
        # URL-encode minimally
        svg_enc = svg.replace('<', '%3C').replace('>', '%3E').replace('"', '%22')
        inserts.append(f'<link rel="icon" href="data:image/svg+xml,{svg_enc}">')

    if inserts:
        block = '\n    ' + '\n    '.join(inserts)
        m = HEAD_OPEN_RE.search(new_text)
        if m:
            pos = m.end()
            new_text = new_text[:pos] + block + new_text[pos:]
            for ins in inserts:
                tag = ins.split()[1] if len(ins.split()) > 1 else ins
                changes.append(('inserted', ins[:80]))

    if new_text != text:
        if not dry_run:
            path.write_text(new_text, encoding='utf-8')
        changes.append(('TOTAL_DIFF', len(new_text) - len(text)))

    return changes


CATEGORY_EMOJI = {
    'games_puzzles': '🎮',
    '3d_immersive': '🎨',
    'audio_music': '🎵',
    'experimental_ai': '🤖',
    'creative_tools': '🛠️',
    'generative_art': '✨',
    'particle_physics': '⚛️',
    'educational_tools': '📚',
    'visual_art': '🎨',
}


def _category_emoji(cat):
    return CATEGORY_EMOJI.get(cat, '🛠️')


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--dry-run', action='store_true')
    ap.add_argument('--check', action='store_true')
    ap.add_argument('--featured-only', action='store_true', default=True,
                    help='Only patch featured=true apps (default)')
    ap.add_argument('--all', action='store_true',
                    help='Patch ALL apps in registry (overrides --featured-only)')
    ap.add_argument('--limit', type=int, default=None)
    args = ap.parse_args()

    registry = load_registry()
    if not registry:
        print('No registry found.')
        return 1

    if args.all:
        apps = list(registry.values())
    else:
        apps = [a for a in registry.values() if a.get('featured')]

    if args.limit:
        apps = apps[:args.limit]

    print(f'targeting {len(apps)} apps ({"all" if args.all else "featured-only"})')
    if args.dry_run:
        print('  --dry-run: no files will be written')

    summary = {'patched': 0, 'skipped': 0, 'no-changes': 0, 'errors': 0, 'total-diff-bytes': 0}
    skip_reasons = {}
    for app in apps:
        rel = app.get('path', '').lstrip('./').lstrip('/')
        full = ROOT / rel
        if not full.exists():
            summary['skipped'] += 1
            skip_reasons['missing'] = skip_reasons.get('missing', 0) + 1
            continue
        try:
            changes = patch_file(full, app, args.dry_run)
        except Exception as e:
            print(f'  ERROR  {rel}: {e}')
            summary['errors'] += 1
            continue
        if changes and changes[0][0] == 'skip':
            summary['skipped'] += 1
            skip_reasons[changes[0][1]] = skip_reasons.get(changes[0][1], 0) + 1
            continue
        if not changes:
            summary['no-changes'] += 1
            continue
        # Has actual changes
        summary['patched'] += 1
        diff = next((c[1] for c in changes if c[0] == 'TOTAL_DIFF'), 0)
        summary['total-diff-bytes'] += diff

    print()
    print('=== SUMMARY ===')
    print(f'  patched:      {summary["patched"]}')
    print(f'  no-changes:   {summary["no-changes"]} (already complete)')
    print(f'  skipped:      {summary["skipped"]}')
    for r, n in sorted(skip_reasons.items(), key=lambda x: -x[1]):
        print(f'    - {r}: {n}')
    print(f'  errors:       {summary["errors"]}')
    print(f'  total bytes:  {summary["total-diff-bytes"]:+}')

    if args.check and summary['patched'] > 0:
        return 1
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
