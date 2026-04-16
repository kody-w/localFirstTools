"""Shared helpers for the reorg scripts (dedupe / build_redirects / verify)."""

from __future__ import annotations

import hashlib
import os
import re
from dataclasses import dataclass
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent

# Directories to ignore entirely — vendored, archived, or not part of the live site.
EXCLUDE_DIRS = {
    ".git",
    ".worktrees",
    "node_modules",
    "chrome-extension-build",
    "archive",
    "v86-master",
    "desktop-app",
    "edgeAddons",
    "notes",
    "vibe_templates",
}

# Top-level directories whose HTML files are considered "gallery content"
# and are candidates for dedupe / redirect stubs.
GALLERY_ROOTS = {"", "apps", "Exhibition_Halls", "tools", "utilities", "creative-tools", "creative_tools"}

# Paths we protect — never delete, never stub over.
PROTECTED = {
    "index.html",
    "404.html",
    "README.md",
}


def is_excluded(path: Path) -> bool:
    parts = set(path.parts)
    return bool(parts & EXCLUDE_DIRS)


def iter_gallery_html(root: Path = REPO_ROOT):
    """Yield every gallery-candidate .html path (relative to repo root)."""
    for dirpath, dirnames, filenames in os.walk(root):
        # prune
        dirnames[:] = [d for d in dirnames if d not in EXCLUDE_DIRS]
        rel_dir = Path(dirpath).relative_to(root)
        # skip files not under a gallery root
        top = rel_dir.parts[0] if rel_dir.parts else ""
        if top not in GALLERY_ROOTS:
            continue
        for fn in filenames:
            if not fn.endswith(".html"):
                continue
            rel = rel_dir / fn
            if str(rel) in PROTECTED:
                continue
            yield rel


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


_FINDER_DUP_RE = re.compile(r" \d+$")
_VERSION_SUFFIX_RE = re.compile(r"[_\- ]v?\d+$", re.IGNORECASE)
_COPY_RE = re.compile(r"(copy|backup|bak|\.orig)", re.IGNORECASE)


@dataclass(frozen=True, order=True)
class CanonScore:
    score: int
    path_str: str


def canonical_score(rel_path: Path) -> CanonScore:
    """Lower score = better canonical choice. Deterministic."""
    parts = rel_path.parts
    score = 0

    # Location tier
    if parts and parts[0] == "apps":
        score = 0
        if "_archive" in parts:
            score += 500
    elif len(parts) == 1:  # root-level
        score = 1000
    elif parts and parts[0] == "Exhibition_Halls":
        score = 2000
    else:
        score = 3000

    stem = rel_path.stem
    if _FINDER_DUP_RE.search(stem):
        score += 150
    if _COPY_RE.search(stem):
        score += 300
    if _VERSION_SUFFIX_RE.search(stem) and not _FINDER_DUP_RE.search(stem):
        score += 60
    if "." in stem:  # e.g. "foo.html.backup" glued on
        score += 50

    # Shorter wins as a tiebreaker
    score += len(str(rel_path))

    return CanonScore(score=score, path_str=str(rel_path))


def pick_canonical(rel_paths: list[Path]) -> Path:
    return min(rel_paths, key=canonical_score)


def rel_redirect_target(stub_path: Path, canonical_path: Path) -> str:
    """Relative href from stub location to canonical location.

    Both args are repo-relative Paths.
    """
    return os.path.relpath(canonical_path, start=stub_path.parent) or "."
