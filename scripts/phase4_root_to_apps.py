#!/usr/bin/env python3
"""Phase 4: move root-level HTML applications into apps/<category>/.

Categorization is a keyword-match on the filename stem against the
CATEGORY_KEYWORDS map. Unknown → apps/uncategorized/.

Protected files (index.html, 404.html, etc.) stay at root.
Already-stub files at root get their stub preserved; we only move the
ones that contain real content.

For each moved file:
  - move bytes to apps/<cat>/<name>.html
  - write an HTML redirect stub at the old root path
  - record old -> new in data/redirects.json
"""

from __future__ import annotations

import argparse
import json
import re
import shutil
import sys
from pathlib import Path

from reorg_common import REPO_ROOT, PROTECTED
from build_redirects import render_stub

REDIRECTS_JSON = REPO_ROOT / "data" / "redirects.json"
STUB_MARKER = '<meta http-equiv="refresh"'

# First-match-wins. Order matters — more specific keywords first.
CATEGORY_KEYWORDS: list[tuple[str, list[str]]] = [
    ("ai-tools", [
        "mcp", "claude", "gpt", "llm", "agentic", "agent-", "-agent", "agent_",
        "neural", "copilot", "ai-", "-ai", "chatbot", "chat-ai", "anthropic",
        "prompt-", "-prompt", "workshop", "wristai",
    ]),
    ("games", [
        "game", "snake", "poker", "chess", "pokemon", "pokedex", "cards",
        "card-", "dungeon", "quest", "rpg", "arcade", "zork", "blackjack",
        "solitaire", "monster", "adventure", "racing", "tetris", "pinball",
        "tron", "roblox", "nexus", "world-", "-world", "civ-", "colony",
        "balatro", "mario", "zelda", "pacman", "doom", "city-of", "citybuilder",
        "clicker", "idler", "dota", "hackathon", "minecraft", "fps", "shooter",
        "platformer", "runner", "puzzle", "sudoku", "crossword", "trivia",
        "quiz-game", "ctf", "dragon", "hero", "villain", "boss", "combat",
        "war-", "battle", "fighting", "tactical", "strategy-", "tabletop",
        "dnd", "wargame", "apex-protocol", "levi", "ecs-console", "evomon",
        "mmo", "mud", "roguelike", "retroplay", "skate", "tile-room",
    ]),
    ("development", [
        "terminal", "vm-", "docker", "debug", "compiler", "ide-", "editor",
        "git-", "deploy", "ci-", "api-", "rest-", "graphql", "javascript",
        "python", "code-", "-code", "repo-", "github", "linter", "markdown",
        "regex", "json-", "yaml-", "ast-", "linker", "assembler", "wasm",
        "typescript", "jsdom", "reverse-eng", "disassembler",
        "dev-", "devtools", "sql-", "database-", "gamedev",
        "kubernetes", "aws-", "azure-", "gcp-", "cloud-",
    ]),
    ("education", [
        "tutor", "learn", "teacher", "quiz", "trainer", "study", "flashcard",
        "tutorial", "lesson", "education", "school", "math-", "algebra",
        "physics-class", "chemistry-", "biology-", "history-", "geography",
        "language-", "spanish", "french", "german", "japanese", "chinese",
        "typing-", "speed-read", "reading-", "spelling", "grammar",
    ]),
    ("business", [
        "crm", "sales", "invoice", "presentation", "pitch", "dashboard",
        "executive", "ceo", "financial", "business", "slide-", "slides",
        "kanban", "roadmap", "okr", "kpi", "analytics", "report",
    ]),
    ("health", [
        "breath", "fitness", "exercise", "medit", "workout", "health",
        "wellness", "sleep", "yoga", "nutrition", "calorie",
    ]),
    ("media", [
        "audio-", "video-", "music", "song", "808", "synth", "drum-",
        "piano-", "beat-", "sampler", "sequencer", "daw-", "mixer",
        "equalizer", "recorder", "screen-record", "webcam", "photo-",
        "image-", "camera", "render", "midi", "mp3", "wav", "acoustic",
    ]),
    ("productivity", [
        "todo", "task", "note-", "notepad", "calendar", "timer", "tracker",
        "planner", "notes-", "memo", "doc-", "document-", "writer", "journal",
        "habit", "timezone", "pomodoro", "checklist", "outliner",
    ]),
    ("creative", [
        "art-", "canvas-", "paint", "draw", "design", "pattern", "fractal",
        "generative", "procedural", "creative", "svg-", "color-",
        "pixel-", "ascii-", "typograph", "palette", "gradient",
        "font-", "logo-", "emoji-", "sticker", "poet", "lyric",
        "symphony", "orchestra", "melody", "harmon", "tone-", "mandala",
    ]),
    ("simulations", [
        "simulator", "simulation", "cellular-autom", "automat-", "petri",
        "ecosystem", "evolution", "genetic-", "predator", "prey",
        "particle", "fluid-", "gas-", "wave-", "pendulum", "chaos",
        "lorenz", "mandelbrot", "sandpile", "boid", "flock",
    ]),
    ("quantum-worlds", [
        "quantum-", "reality-", "dimension", "multiverse", "timeline",
        "nexus-", "meta-", "abyssal", "ego-death", "consciousness",
        "philosophical", "metaphysics", "ontolog",
    ]),
    ("utilities", [
        "converter", "generator", "calculator", "clock", "countdown",
        "viewer", "explorer", "manager", "finder", "parser", "checker",
        "analyzer", "validator", "formatter", "encoder", "decoder",
        "hash-", "cipher", "qr-", "barcode", "url-", "diff-", "compare",
        "search-", "-tool", "os-", "emulator", "browser-", "filesystem",
        "file-", "download", "uploader", "backup", "compress", "archive-",
    ]),
]

CATEGORY_DIRS = [c for c, _ in CATEGORY_KEYWORDS] + ["uncategorized"]


def categorize(stem: str) -> str:
    # Normalize: lowercase, all separators -> '-', collapse runs
    s = stem.lower()
    s = re.sub(r"[_\s]+", "-", s)
    s = re.sub(r"-+", "-", s)
    s = f"-{s}-"  # sentinel so keyword matches at boundaries too
    for cat, kws in CATEGORY_KEYWORDS:
        for kw in kws:
            # Match keyword either with its dashes or bare
            kw_norm = kw if kw.startswith("-") or kw.endswith("-") else f"-{kw}-"
            if kw in s or kw_norm in s:
                return cat
    return "uncategorized"


def load_redirects() -> dict[str, str]:
    if not REDIRECTS_JSON.exists():
        return {}
    return json.loads(REDIRECTS_JSON.read_text())


def save_redirects(d: dict[str, str]) -> None:
    REDIRECTS_JSON.write_text(json.dumps(dict(sorted(d.items())), indent=2) + "\n")


def is_stub(abs_path: Path) -> bool:
    try:
        with open(abs_path, "rb") as f:
            return STUB_MARKER.encode() in f.read(2048)
    except OSError:
        return False


def main(dry_run: bool) -> int:
    redirects = load_redirects()

    # Protected patterns that must stay at root
    keep_at_root = set(PROTECTED) | {
        # index variants are handled by phase 7
        f.name for f in REPO_ROOT.iterdir()
        if f.is_file() and re.match(r"^(index|404)", f.name, re.I)
    }

    moved = 0
    stubbed = 0
    skipped_protected = 0
    category_counts: dict[str, int] = {}

    for f in sorted(REPO_ROOT.iterdir()):
        if not f.is_file():
            continue
        if f.suffix.lower() != ".html":
            continue
        if f.name in keep_at_root:
            skipped_protected += 1
            continue

        stem = f.stem
        cat = categorize(stem)
        category_counts[cat] = category_counts.get(cat, 0) + 1

        # Target name: same basename. Phase 6 handles version-cluster collisions.
        dst_dir = REPO_ROOT / "apps" / cat
        dst_dir.mkdir(parents=True, exist_ok=True)
        dst = dst_dir / f.name
        src_rel = f.name
        dst_rel = f"apps/{cat}/{f.name}"

        if is_stub(f):
            # Source is already a stub. Move the stub into its new home? No —
            # its reference is its old path, which should keep serving the
            # redirect. Easier: leave it where it is (it continues to work),
            # but record the dst mapping so apps.json regen finds nothing to
            # do for this file in either location.
            # Skip — pre-existing stubs at root are fine as-is.
            continue

        if dst.exists():
            # Collision. Defer to phase 6. Leave file alone at root for now.
            continue

        if dry_run:
            moved += 1
            continue

        shutil.move(str(f), str(dst))
        f.write_text(render_stub(src_rel, dst_rel))
        redirects[src_rel] = dst_rel
        moved += 1

    if not dry_run:
        save_redirects(redirects)

    print(f"phase 4 — root -> apps/<cat>/")
    print(f"  protected / kept at root: {skipped_protected}")
    print(f"  {'would-move' if dry_run else 'moved'}: {moved}")
    print(f"  category distribution:")
    for cat in sorted(category_counts, key=lambda c: -category_counts[c]):
        print(f"    {cat:20s} {category_counts[cat]}")
    print(f"  redirects.json entries: {len(redirects)}")
    return 0


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--dry-run", action="store_true")
    args = p.parse_args()
    sys.exit(main(dry_run=args.dry_run))
