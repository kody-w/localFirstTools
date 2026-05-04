"""
Structured chunking for long prompts (Step 01).

This module parses Markdown-like text into semantic chunks with:
- Stable IDs derived from content and section path
- Hierarchical parent/child relations via heading structure
- Token counts via a pluggable tokenizer interface
- Must-keep tagging and protected spans (inline code, key requirements)
- Basic reference extraction (Markdown links)

No external dependencies; safe, minimal, and modular.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Callable, Iterable, List, Optional, Sequence, Tuple
import hashlib
import re


# ----------------------------- Tokenization -----------------------------


class Tokenizer:
    """Interface for token counting.

    Implementations should provide a deterministic token count for text. This
    default approximates GPT-style tokenization conservatively (~4 chars/token).
    Replace with a real tokenizer (e.g., tiktoken) by injecting a custom
    instance where needed.
    """

    def count(self, text: str) -> int:
        # Conservative estimate: 1 token ~ 4 characters, min 1.
        # This errs on the side of over-counting to keep budgets safe.
        n = max(1, round(len(text) / 4))
        return n


# ----------------------------- Data Models ------------------------------


@dataclass(frozen=True)
class Span:
    """A protected span within a chunk's text.

    start/end are 0-based, end-exclusive indices.
    """

    start: int
    end: int
    label: str


@dataclass(frozen=True)
class Reference:
    """A lightweight reference extracted from a chunk.

    kind examples: "link", "code", "anchor".
    value: the referenced value (e.g., URL for links).
    text: the display text (e.g., link text), if applicable.
    """

    kind: str
    value: str
    text: Optional[str] = None


ChunkType = str  # e.g., "heading", "paragraph", "list", "code", "table"


@dataclass
class Chunk:
    """A semantic unit of the source document.

    IDs are stable for unchanged content within the same section path.
    """

    id: str
    type: ChunkType
    text: str
    token_count: int
    heading_path: List[str] = field(default_factory=list)
    level: Optional[int] = None  # Only for headings (1-6)
    parent_id: Optional[str] = None
    children: List[str] = field(default_factory=list)
    must_keep: bool = False
    protected_spans: List[Span] = field(default_factory=list)
    references: List[Reference] = field(default_factory=list)
    meta: dict = field(default_factory=dict)


# ----------------------------- Chunker Core -----------------------------


_RE_HEADING = re.compile(r"^(#{1,6})\s+(.+?)\s*$")
_RE_FENCE = re.compile(r"^(```|~~~)(.*)$")
_RE_LIST = re.compile(r"^(\s*)([-*+] |\d+\. )\s*(.*)$")
_RE_TABLE = re.compile(r"^\s*\|.*\|\s*$")
_RE_INLINE_CODE = re.compile(r"`([^`]+)`")
_RE_MD_LINK = re.compile(r"\[([^\]]+)\]\(([^)]+)\)")
_RE_REQ_KEYWORDS = re.compile(
    r"\b(MUST|SHALL|DO NOT|NEVER|REQUIRED|CONSTRAINTS?)\b",
    flags=re.IGNORECASE,
)
_RE_APIISH = re.compile(r"https?://|/v\d+/|\{[^}]+\}|\"\s*:\s*\"")


def _slugify(text: str) -> str:
    s = re.sub(r"[^a-zA-Z0-9\s-]", "", text).strip().lower()
    s = re.sub(r"\s+", "-", s)
    return s or "section"


def _norm(text: str) -> str:
    return re.sub(r"\s+", " ", text.strip())


def _stable_id(kind: str, path: Sequence[str], text: str, suffix: str = "") -> str:
    hasher = hashlib.sha1()
    path_str = "/".join(_slugify(p) for p in path)
    payload = f"{kind}|{path_str}|{_norm(text)}|{suffix}".encode("utf-8")
    hasher.update(payload)
    return f"{kind[:1]}_{hasher.hexdigest()[:10]}"


def _extract_inline_protections(text: str) -> Tuple[List[Span], List[Reference]]:
    spans: List[Span] = []
    refs: List[Reference] = []

    # Inline code spans
    for m in _RE_INLINE_CODE.finditer(text):
        spans.append(Span(start=m.start(0), end=m.end(0), label="inline_code"))
        refs.append(Reference(kind="code", value=m.group(1)))

    # Markdown links
    for m in _RE_MD_LINK.finditer(text):
        spans.append(Span(start=m.start(0), end=m.end(0), label="link"))
        refs.append(Reference(kind="link", value=m.group(2), text=m.group(1)))

    # Hard requirements keywords
    for m in _RE_REQ_KEYWORDS.finditer(text):
        spans.append(Span(start=m.start(0), end=m.end(0), label="requirement"))

    return spans, refs


def _is_table_line(line: str) -> bool:
    # Basic table row detection and the separator line (---|---)
    if _RE_TABLE.match(line):
        return True
    if re.match(r"^\s*:?[-]{3,}\s*(\|\s*:?[-]{3,}\s*)+$", line):
        return True
    return False


class MarkdownChunker:
    """Markdown-aware chunker producing semantic chunks.

    Rules:
    - Headings establish hierarchy and parentage
    - Code fences are atomic (never split)
    - Lists stay grouped as a single chunk per contiguous block
    - Paragraphs are separated by blank lines
    - Tables are grouped as contiguous table blocks
    - Chunks carry: stable id, token count, must-keep flags, protected spans
    """

    def __init__(self, tokenizer: Optional[Tokenizer] = None) -> None:
        self.tokenizer = tokenizer or Tokenizer()

    def chunk(self, text: str) -> List[Chunk]:
        lines = text.splitlines()
        chunks: List[Chunk] = []

        # Track heading stack: list of (level, heading_text, chunk_id)
        heading_stack: List[Tuple[int, str, str]] = []

        def current_path() -> List[str]:
            return [h[1] for h in heading_stack]

        def current_parent_id() -> Optional[str]:
            return heading_stack[-1][2] if heading_stack else None

        def push_heading(level: int, title: str) -> Chunk:
            # Pop until the stack top has lower level than the new heading
            while heading_stack and heading_stack[-1][0] >= level:
                heading_stack.pop()

            path_before = current_path()
            cid = _stable_id("heading", path_before + [title], title)
            ch = Chunk(
                id=cid,
                type="heading",
                text=title.strip(),
                token_count=self.tokenizer.count(title),
                heading_path=path_before,
                level=level,
                parent_id=current_parent_id(),
                must_keep=self._heading_must_keep(title),
            )
            chunks.append(ch)
            # Link as child to parent if present
            if ch.parent_id:
                self._append_child(chunks, ch.parent_id, ch.id)

            heading_stack.append((level, title.strip(), ch.id))
            return ch

        i = 0
        para_buf: List[str] = []

        def flush_paragraph():
            if not para_buf:
                return
            body = "\n".join(para_buf).strip("\n")
            para_buf.clear()
            if not body.strip():
                return
            path = current_path()
            cid = _stable_id("paragraph", path, body)
            spans, refs = _extract_inline_protections(body)
            must_keep = bool(_RE_REQ_KEYWORDS.search(body) or _RE_APIISH.search(body))
            ch = Chunk(
                id=cid,
                type="paragraph",
                text=body,
                token_count=self.tokenizer.count(body),
                heading_path=path,
                parent_id=current_parent_id(),
                must_keep=must_keep,
                protected_spans=spans,
                references=refs,
            )
            chunks.append(ch)
            if ch.parent_id:
                self._append_child(chunks, ch.parent_id, ch.id)

        while i < len(lines):
            line = lines[i]

            # Heading
            m_h = _RE_HEADING.match(line)
            if m_h:
                flush_paragraph()
                level = len(m_h.group(1))
                title = m_h.group(2)
                push_heading(level, title)
                i += 1
                continue

            # Code fence block
            m_f = _RE_FENCE.match(line)
            if m_f:
                flush_paragraph()
                fence = m_f.group(1)
                lang = m_f.group(2).strip() or None
                i += 1
                code_lines: List[str] = []
                while i < len(lines):
                    if lines[i].startswith(fence):
                        i += 1
                        break
                    code_lines.append(lines[i])
                    i += 1
                code_text = "\n".join(code_lines)
                path = current_path()
                cid = _stable_id("code", path, code_text or "<empty>", suffix=lang or "")
                ch = Chunk(
                    id=cid,
                    type="code",
                    text=code_text,
                    token_count=self.tokenizer.count(code_text),
                    heading_path=path,
                    parent_id=current_parent_id(),
                    must_keep=True,  # never drop code by default
                    meta={"lang": lang} if lang else {},
                )
                chunks.append(ch)
                if ch.parent_id:
                    self._append_child(chunks, ch.parent_id, ch.id)
                continue

            # Table block
            if _is_table_line(line):
                flush_paragraph()
                table_lines = [line]
                i += 1
                while i < len(lines) and _is_table_line(lines[i]):
                    table_lines.append(lines[i])
                    i += 1
                tbl = "\n".join(table_lines)
                path = current_path()
                cid = _stable_id("table", path, tbl)
                spans, refs = _extract_inline_protections(tbl)
                ch = Chunk(
                    id=cid,
                    type="table",
                    text=tbl,
                    token_count=self.tokenizer.count(tbl),
                    heading_path=path,
                    parent_id=current_parent_id(),
                    must_keep=True,  # tables often encode structure; protect by default
                    protected_spans=spans,
                    references=refs,
                )
                chunks.append(ch)
                if ch.parent_id:
                    self._append_child(chunks, ch.parent_id, ch.id)
                continue

            # List block
            m_l = _RE_LIST.match(line)
            if m_l:
                flush_paragraph()
                list_lines = [line]
                i += 1
                while i < len(lines) and (_RE_LIST.match(lines[i]) or lines[i].strip() == ""):
                    # Keep blank lines inside lists (for wrapped items)
                    if lines[i].strip() == "":
                        list_lines.append(lines[i])
                        i += 1
                        continue
                    list_lines.append(lines[i])
                    i += 1
                lst = "\n".join(list_lines)
                path = current_path()
                cid = _stable_id("list", path, lst)
                spans, refs = _extract_inline_protections(lst)
                must_keep = bool(_RE_REQ_KEYWORDS.search(lst) or _RE_APIISH.search(lst))
                ch = Chunk(
                    id=cid,
                    type="list",
                    text=lst,
                    token_count=self.tokenizer.count(lst),
                    heading_path=path,
                    parent_id=current_parent_id(),
                    must_keep=must_keep,
                    protected_spans=spans,
                    references=refs,
                )
                chunks.append(ch)
                if ch.parent_id:
                    self._append_child(chunks, ch.parent_id, ch.id)
                continue

            # Blank line => paragraph boundary
            if line.strip() == "":
                flush_paragraph()
                i += 1
                continue

            # Default: paragraph accumulation
            para_buf.append(line)
            i += 1

        # Flush trailing paragraph
        flush_paragraph()

        return chunks

    # -------------------------- Helpers --------------------------

    @staticmethod
    def _append_child(chunks: List[Chunk], parent_id: str, child_id: str) -> None:
        for ch in reversed(chunks):  # reverse to find parent faster in recent items
            if ch.id == parent_id:
                ch.children.append(child_id)
                return

    @staticmethod
    def _heading_must_keep(title: str) -> bool:
        key_terms = (
            "requirement",
            "requirements",
            "constraint",
            "constraints",
            "api",
            "schema",
            "contract",
            "definition",
            "definitions",
            "rules",
            "protocol",
            "interface",
            "spec",
            "specification",
            "security",
            "compliance",
        )
        t = title.strip().lower()
        return any(k in t for k in key_terms)


# ----------------------------- Utilities -----------------------------


def total_tokens(chunks: Iterable[Chunk]) -> int:
    """Compute total token count of all chunks."""
    return sum(c.token_count for c in chunks)


__all__ = [
    "Tokenizer",
    "Span",
    "Reference",
    "Chunk",
    "MarkdownChunker",
    "total_tokens",
]

