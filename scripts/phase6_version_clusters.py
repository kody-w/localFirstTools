#!/usr/bin/env python3
"""Phase 6: resolve version clusters — files sharing a normalized stem
but differing in content.

Walks apps/** (and root-level real files) clustering by normalized stem.
For each cluster with >1 distinct SHA-256:
  - canonical = the file ranked best by (size desc, mtime desc)
  - losers    = moved to apps/_archive/<cat>/<slug>__<shortsha>.html
  - old path of each loser gets a redirect stub pointing at the canonical

Rationale: after phases 1-5, any remaining divergent content represents
real versioning (features added, UI rewrites, etc.). The largest file
is a reasonable default for "most-developed" and the archive preserves
every other version reachable by URL.
"""

from __future__ import annotations

import argparse
import json
import re
import shutil
import sys
from collections import defaultdict
from pathlib import Path

from reorg_common import REPO_ROOT, sha256, _FINDER_DUP_RE, _COPY_RE
from build_redirects import render_stub

REDIRECTS_JSON = REPO_ROOT / "data" / "redirects.json"
STUB_MARKER = '<meta http-equiv="refresh"'
ARCHIVE_ROOT = REPO_ROOT / "apps" / "_archive"


def normalize_stem(stem: str) -> str:
    s = stem.lower()
    # strip Finder suffix
    s = _FINDER_DUP_RE.sub("", s)
    # strip version suffix (_v1, -v2, _2, -3)
    s = re.sub(r"[_\- ]v?\d+$", "", s)
    # strip "copy", "backup", etc.
    s = _COPY_RE.sub("", s)
    # collapse separators
    s = re.sub(r"[\s_\-]+", "-", s).strip("-")
    return s


def is_stub(abs_path: Path) -> bool:
    try:
        with open(abs_path, "rb") as f:
            return STUB_MARKER.encode() in f.read(2048)
    except OSError:
        return False


def load_redirects() -> dict[str, str]:
    return json.loads(REDIRECTS_JSON.read_text()) if REDIRECTS_JSON.exists() else {}


def save_redirects(d: dict[str, str]) -> None:
    REDIRECTS_JSON.write_text(json.dumps(dict(sorted(d.items())), indent=2) + "\n")


def candidate_paths() -> list[Path]:
    """Real (non-stub) HTML files that are candidates for version-cluster
    resolution: everything under apps/ (EXCEPT apps/_archive) plus
    real root-level files that aren't index/404 variants."""
    out = []
    apps_dir = REPO_ROOT / "apps"
    for p in apps_dir.rglob("*.html"):
        if "_archive" in p.parts:
            continue
        if is_stub(p):
            continue
        out.append(p)
    for p in REPO_ROOT.glob("*.html"):
        if re.match(r"^(index|404)", p.name, re.I):
            continue
        if is_stub(p):
            continue
        out.append(p)
    return out


def rank_canonical(paths: list[Path]) -> Path:
    def key(p: Path):
        try:
            st = p.stat()
        except OSError:
            return (0, 0)
        return (-st.st_size, -int(st.st_mtime))
    return sorted(paths, key=key)[0]


def main(dry_run: bool) -> int:
    redirects = load_redirects()

    paths = candidate_paths()
    print(f"candidates (real, non-archive): {len(paths)}")

    # Group by normalized stem
    groups: dict[str, list[Path]] = defaultdict(list)
    for p in paths:
        groups[normalize_stem(p.stem)].append(p)

    # Filter: clusters of size >= 2 with >= 2 distinct hashes
    clusters = []
    for stem, members in groups.items():
        if len(members) < 2:
            continue
        # compute hashes
        by_hash: dict[str, list[Path]] = defaultdict(list)
        for m in members:
            try:
                by_hash[sha256(m)].append(m)
            except OSError:
                pass
        if len(by_hash) < 2:
            continue
        clusters.append((stem, by_hash))

    print(f"version clusters: {len(clusters)}")

    to_archive = 0
    archived_bytes = 0

    for stem, by_hash in clusters:
        # Pick one representative per hash (the best-ranked one),
        # then choose the overall canonical from representatives.
        reps = {h: rank_canonical(members) for h, members in by_hash.items()}
        canonical = rank_canonical(list(reps.values()))
        canonical_hash = sha256(canonical)

        for h, members in by_hash.items():
            if h == canonical_hash:
                # Within canonical's hash group, keep the canonical, and stub
                # any other byte-identical siblings to it (phase 1 residual).
                for m in members:
                    if m == canonical:
                        continue
                    m_rel = str(m.relative_to(REPO_ROOT))
                    c_rel = str(canonical.relative_to(REPO_ROOT))
                    if m_rel == c_rel:
                        continue
                    if dry_run:
                        continue
                    m.write_text(render_stub(m_rel, c_rel))
                    redirects[m_rel] = c_rel
                continue

            # Loser hash group — every member goes to archive, each gets
            # a stub redirecting to canonical.
            for m in members:
                m_rel = str(m.relative_to(REPO_ROOT))
                c_rel = str(canonical.relative_to(REPO_ROOT))

                # Pick a category for the archive. If the loser lived under
                # apps/<cat>/, preserve <cat>. Otherwise use a default.
                parts = m.parts
                if "apps" in parts:
                    try:
                        ai = parts.index("apps")
                        cat = parts[ai + 1] if ai + 1 < len(parts) else "misc"
                    except ValueError:
                        cat = "misc"
                else:
                    cat = "misc"

                short = h[:8]
                archive_name = f"{stem}__{short}.html"
                archive_rel = f"apps/_archive/{cat}/{archive_name}"
                archive_abs = REPO_ROOT / archive_rel
                archive_abs.parent.mkdir(parents=True, exist_ok=True)

                if dry_run:
                    to_archive += 1
                    continue

                # Move bytes to archive (if archive path already exists,
                # it means another member of the same hash group already
                # got there; just skip the move, still stub this path).
                try:
                    size = m.stat().st_size
                except OSError:
                    size = 0
                if not archive_abs.exists():
                    shutil.move(str(m), str(archive_abs))
                else:
                    # second member of same hash group — delete, archive has it
                    m.unlink()

                # stub at the old path pointing at the canonical
                m.parent.mkdir(parents=True, exist_ok=True)
                m.write_text(render_stub(m_rel, c_rel))
                redirects[m_rel] = c_rel

                # Also register the archive path so the verifier knows
                # it's reachable (it's a real file; no redirect needed).
                to_archive += 1
                archived_bytes += size

    if not dry_run:
        save_redirects(redirects)

    print(f"\nphase 6 — version clusters")
    print(f"  {'would-archive' if dry_run else 'archived'}: {to_archive}")
    print(f"  bytes moved to archive: {archived_bytes:,} ({archived_bytes/1024/1024:.1f} MiB)")
    print(f"  redirects.json entries: {len(redirects)}")
    return 0


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--dry-run", action="store_true")
    args = p.parse_args()
    sys.exit(main(dry_run=args.dry_run))
