#!/usr/bin/env python3
"""Inventory committed HTML payloads and propose bounded, evidence-based maintenance.

No source is read from the working tree, executed, or fetched over the network.
The optional discovery catalogs and every HTML body come from one resolved commit.
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from datetime import datetime, timezone
import hashlib
from html.parser import HTMLParser
import json
import os
from pathlib import Path, PurePosixPath
import posixpath
import re
import subprocess
from urllib.parse import quote, unquote, urljoin, urlsplit, urlunsplit


SCHEMA = "localfirst-autocomplete-catalog/v1"
DEFAULT_REPOSITORY = "kody-w/localFirstTools"
METADATA_PATHS = ("vibe_gallery_config.json", "landgrab/index.json")
REGULAR_MODES = {"100644", "100755"}
PROVENANCE_DIRECTORIES = {
    "artifacts", "evidence", "frames", "generated", "receipts", "runs", "snapshots",
}


class CatalogError(ValueError):
    """An input cannot be inventoried without losing or misattributing evidence."""


@dataclass(frozen=True)
class TreeEntry:
    mode: str
    kind: str
    oid: str


@dataclass
class HtmlFacts:
    sha256: str
    size: int
    title: str
    description: str
    signals: dict
    refreshes: list
    base_href: str | None


@dataclass(frozen=True)
class Metadata:
    path: str
    catalog: str
    priority: int
    title: str = ""
    description: str = ""
    category: str = ""


@dataclass
class Redirect:
    target: str
    local_target: str | None
    reason: str | None = None


@dataclass(frozen=True)
class Resolution:
    destination: str | None
    reason: str | None = None
    failure_path: str | None = None
    cycle: tuple = ()


def _git_environment():
    environment = os.environ.copy()
    for key in (
        "GIT_DIR", "GIT_WORK_TREE", "GIT_COMMON_DIR", "GIT_INDEX_FILE",
        "GIT_OBJECT_DIRECTORY", "GIT_ALTERNATE_OBJECT_DIRECTORIES", "GIT_NAMESPACE",
    ):
        environment.pop(key, None)
    environment.update({
        "GIT_NO_LAZY_FETCH": "1", "GIT_ALLOW_PROTOCOL": "", "GIT_TERMINAL_PROMPT": "0",
    })
    return environment


def _git(repo_root, *args):
    try:
        result = subprocess.run(
            ["git", "--no-replace-objects", "-C", str(repo_root), *args],
            stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, check=False,
            env=_git_environment(),
        )
    except OSError as exc:
        raise CatalogError("Git could not be started; a local Git installation is required.") from exc
    if result.returncode:
        # Git diagnostics can include private filesystem paths or remote credentials.
        raise CatalogError(f"Git {args[0]} failed; check the repository and committed ref.")
    return result.stdout


def _snapshot(repo_root, ref):
    commit = _git(
        repo_root, "rev-parse", "--verify", "--end-of-options", f"{ref}^{{commit}}",
    ).decode("ascii").strip()
    tree = _git(repo_root, "rev-parse", "--verify", f"{commit}^{{tree}}").decode("ascii").strip()
    entries = {}
    for record in _git(repo_root, "ls-tree", "-r", "-z", "--full-tree", tree).split(b"\0"):
        if not record:
            continue
        header, path = record.split(b"\t", 1)
        mode, kind, oid = header.decode("ascii").split()
        entries[path.decode("utf-8", "surrogateescape")] = TreeEntry(mode, kind, oid)
    return commit, tree, entries


def _blobs(repo_root, object_ids):
    """Stream unique raw blobs through one process without a pipe-sized input deadlock."""
    ids = sorted(set(object_ids))
    if not ids:
        return
    try:
        process = subprocess.Popen(
            ["git", "--no-replace-objects", "-C", str(repo_root), "cat-file", "--batch"],
            stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL,
            env=_git_environment(),
        )
    except OSError as exc:
        raise CatalogError("Git cat-file could not be started.") from exc
    with process:
        try:
            for oid in ids:
                process.stdin.write(oid.encode("ascii") + b"\n")
                process.stdin.flush()
                header = process.stdout.readline().split()
                if len(header) != 3 or header[0] != oid.encode("ascii") or header[1] != b"blob":
                    raise CatalogError("Git cat-file did not return the requested committed blob.")
                size = int(header[2])
                data = process.stdout.read(size)
                if len(data) != size or process.stdout.read(1) != b"\n":
                    raise CatalogError("Git cat-file returned an incomplete committed blob.")
                yield oid, data
            process.stdin.close()
            if process.wait():
                raise CatalogError("Git cat-file failed while reading the committed tree.")
        except (OSError, ValueError) as exc:
            if isinstance(exc, CatalogError):
                raise
            raise CatalogError("Git cat-file could not read the committed blobs.") from exc


def _is_html(path):
    return PurePosixPath(path).suffix.lower() in {".html", ".htm"}


def _is_provenance(path):
    parts = path.split("/")
    return (
        len(parts) >= 4 and parts[:2] == ["landgrab", "autocomplete"]
        and parts[2] in PROVENANCE_DIRECTORIES
    )


def _role(path):
    parts = {part.lower() for part in PurePosixPath(path).parts[:-1]}
    name = PurePosixPath(path).name.lower()
    if parts & {
        "vendor", "vendors", "node_modules", "third_party", "third-party", "bundled",
        "dist", "build", "coverage", "generated", "templates", "template", "fixtures",
    } or name in {"template.html", "template.htm"} or name.endswith("-template.html"):
        return "artifact"
    if parts & {"archive", "archives", "archived", "backup", "backups", "legacy"}:
        return "archive"
    if parts & {"docs", "documentation"} or name in {"readme.html", "guide.html"}:
        return "documentation"
    if (
        path == "index.html" or path.startswith("landgrab/")
        or name in {"gallery.html", "vibe_gallery.html"}
    ):
        return "operational"
    return "app_candidate"


def _path_rank(path):
    lower = path.lower()
    if lower.startswith("v2/apps/"):
        location = 0
    elif lower.startswith("apps/"):
        location = 1
    elif "exhibitions/" in lower or "exhibition_halls/" in lower:
        location = 2
    else:
        location = 3
    roles = {"app_candidate": 0, "operational": 1, "documentation": 2, "archive": 3, "artifact": 4}
    return roles[_role(path)], location, path.casefold(), path


class _HtmlParser(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.title_parts = []
        self.in_title = False
        self.description = ""
        self.refreshes = []
        self.base_href = None
        self.external_scripts = False
        self.template_depth = 0

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == "template":
            self.template_depth += 1
        if self.template_depth:
            return
        if tag == "title":
            self.in_title = True
        elif tag == "base" and self.base_href is None and "href" in attrs:
            self.base_href = attrs["href"] or ""
        elif tag == "script":
            src = (attrs.get("src") or "").strip()
            if re.match(r"(?i)^(?:https?://|//)", src):
                self.external_scripts = True
        elif tag == "meta":
            if (attrs.get("http-equiv") or "").strip().lower() == "refresh":
                self.refreshes.append(attrs.get("content"))
            if (attrs.get("name") or "").strip().lower() == "description" and not self.description:
                self.description = " ".join((attrs.get("content") or "").split())

    def handle_endtag(self, tag):
        if tag == "template" and self.template_depth:
            self.template_depth -= 1
        if tag == "title":
            self.in_title = False

    def handle_data(self, data):
        if self.in_title and not self.template_depth:
            self.title_parts.append(data)


def _html_facts(data):
    text = data.decode("utf-8-sig", errors="replace")
    parser = _HtmlParser()
    parser.feed(text)
    parser.close()
    return HtmlFacts(
        sha256=hashlib.sha256(data).hexdigest(),
        size=len(data),
        title=" ".join("".join(parser.title_parts).split()),
        description=parser.description,
        signals={
            "local_persistence": bool(re.search(r"\b(?:localStorage|sessionStorage|indexedDB)\b", text)),
            "external_scripts": parser.external_scripts,
            "import_export_mentions": bool(re.search(r"\b(?:import|export)\b", text, flags=re.I)),
        },
        refreshes=parser.refreshes,
        base_href=parser.base_href,
    )


def _refresh_target(content):
    if content is None:
        return "", "malformed_refresh"
    match = re.fullmatch(r"\s*\d+(?:\.\d+)?\s*(?:[;,]\s*(.*))?", content, flags=re.S)
    if not match:
        return content, "malformed_refresh"
    target = match.group(1) or ""
    target = re.sub(r"(?i)^url\s*=\s*", "", target).strip()
    if target.startswith(("'", '"')):
        if len(target) < 2 or target[-1] != target[0]:
            return target, "malformed_refresh"
        target = target[1:-1]
    return target, None


def _repository(full_name, site_url):
    if not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9_.-]*/[A-Za-z0-9][A-Za-z0-9_.-]*", full_name):
        raise CatalogError("Repository must be an explicit GitHub owner/name, not a URL or local path.")
    owner, name = full_name.split("/")
    site_url = site_url or f"https://{owner}.github.io/{name}/"
    try:
        parsed = urlsplit(site_url)
        if (
            parsed.scheme not in {"https", "http"} or not parsed.hostname
            or parsed.username is not None or parsed.password is not None
            or parsed.query or parsed.fragment or "\\" in site_url
        ):
            raise ValueError
        parsed.port
        prefix = unquote(parsed.path, errors="strict")
        if posixpath.normpath("/" + prefix.lstrip("/")).rstrip("/") != prefix.rstrip("/"):
            raise ValueError
    except (ValueError, UnicodeError) as exc:
        raise CatalogError("Site URL must be an HTTP(S) base URL without credentials, query, or fragment.") from exc
    return {
        "full_name": full_name,
        "url": f"https://github.com/{full_name}",
        "site_url": site_url.rstrip("/") + "/",
    }


def _public_target(target):
    """Do not reproduce URL userinfo in generated public records."""
    try:
        parsed = urlsplit(target)
        if parsed.username is not None or parsed.password is not None:
            return urlunsplit(parsed._replace(netloc=parsed.netloc.rsplit("@", 1)[-1]))
    except ValueError:
        return "[invalid URL]"
    return target


def _quote_path(path):
    return quote(path, safe="/", errors="surrogateescape")


def _nondefault_port(parsed):
    port = parsed.port
    return None if port == {"http": 80, "https": 443}.get(parsed.scheme) else port


def _local_target(source_path, target, base_href, site_url, entries):
    try:
        page_url = site_url + _quote_path(source_path)
        base_url = urljoin(page_url, base_href) if base_href is not None else page_url
        # A refresh without a URL reloads this document, not its <base> URL.
        absolute = urljoin(base_url, target) if target else page_url
        parsed = urlsplit(absolute)
        site = urlsplit(site_url)
        if parsed.username is not None or parsed.password is not None:
            return None, "credentialed_target"
        if parsed.scheme not in {"http", "https"}:
            return None, "unsupported_scheme"
        if parsed.hostname != site.hostname or _nondefault_port(parsed) != _nondefault_port(site):
            return None, "external_target"
        decoded = unquote(parsed.path, errors="surrogateescape")
        if "\\" in target or "\\" in decoded or any(ord(char) < 32 for char in decoded):
            return None, "invalid_target_url"
        normalized = posixpath.normpath("/" + decoded.lstrip("/"))
        prefix = unquote(site.path, errors="strict").rstrip("/")
        if prefix and normalized != prefix and not normalized.startswith(prefix + "/"):
            return None, "outside_repository"
        local_path = normalized[len(prefix):].lstrip("/")
    except (ValueError, UnicodeError):
        return None, "invalid_target_url"
    for parent in [local_path, *[str(p) for p in PurePosixPath(local_path).parents if str(p) != "."]]:
        entry = entries.get(parent)
        if entry and entry.mode == "120000":
            return local_path, "symlink_target"
        if entry and entry.kind != "blob":
            return local_path, "non_blob_target"
    if local_path not in entries:
        directory_index = posixpath.join(local_path, "index.html")
        if directory_index in entries:
            local_path = directory_index
        else:
            return local_path, "missing_target"
    if _is_provenance(local_path):
        return local_path, "excluded_provenance_target"
    if not _is_html(local_path):
        return local_path, "non_html_target"
    if entries[local_path].mode not in REGULAR_MODES:
        return local_path, "symlink_target" if entries[local_path].mode == "120000" else "non_blob_target"
    return local_path, None


def _redirects(html, site_url, entries):
    result = {}
    for path, facts in html.items():
        if not facts.refreshes:
            continue
        targets = [_refresh_target(content) for content in facts.refreshes]
        target, reason = targets[0]
        if len(set(targets)) > 1:
            reason = "ambiguous_refresh"
        local, target_reason = (None, reason) if reason else _local_target(
            path, target, facts.base_href, site_url, entries,
        )
        result[path] = Redirect(_public_target(target), local, reason or target_reason)
    return result


def _resolve_redirects(redirects, payload_paths):
    resolved = {path: Resolution(path) for path in payload_paths}
    for start in sorted(redirects):
        trail = []
        positions = {}
        current = start
        while current not in resolved:
            if current in positions:
                cycle = tuple(sorted(trail[positions[current]:]))
                result = Resolution(None, "redirect_cycle", min(cycle), cycle)
                break
            positions[current] = len(trail)
            trail.append(current)
            edge = redirects[current]
            if edge.reason:
                result = Resolution(None, edge.reason, current)
                break
            current = edge.local_target
        else:
            result = resolved[current]
        for path in trail:
            resolved[path] = result
    return resolved


def _json_object(data, path):
    def unique_object(pairs):
        result = {}
        for key, value in pairs:
            if key in result:
                raise ValueError("Duplicate JSON key")
            result[key] = value
        return result

    def invalid_constant(value):
        raise ValueError("Non-JSON numeric constant")

    try:
        result = json.loads(
            data.decode("utf-8-sig"), object_pairs_hook=unique_object,
            parse_constant=invalid_constant,
        )
    except (UnicodeError, ValueError) as exc:
        raise CatalogError(f"{path}: malformed UTF-8 JSON in the committed catalog.") from exc
    if not isinstance(result, dict):
        raise CatalogError(f"{path}: catalog must be a JSON object.")
    return result


def _metadata_records(catalogs, entries, site_url):
    records = []
    sources = []

    def require(value, expected, catalog, location):
        if not isinstance(value, expected):
            raise CatalogError(f"{catalog}: {location} must be a {expected.__name__}.")
        return value

    def record(app, catalog, priority, category="", inherited=None):
        require(app, dict, catalog, "app entry")
        path = require(app.get("path"), str, catalog, "app.path")
        if not path.strip():
            raise CatalogError(f"{catalog}: app.path must not be empty.")
        if path not in entries:
            local, _ = _local_target("index.html", path, None, site_url, entries)
            if local is not None:
                path = local
        fields = {}
        for key, fallback in (
            ("title", ""), ("description", ""), ("category", category),
        ):
            value = app.get(key, (inherited or {}).get(key, fallback))
            fields[key] = require(value, str, catalog, f"app.{key}").strip()
        item = Metadata(path, catalog, priority, **fields)
        records.append(item)
        return item

    for catalog in METADATA_PATHS:
        if catalog not in catalogs:
            sources.append({"path": catalog, "status": "missing", "entries": 0})
            continue
        data = _json_object(catalogs[catalog], catalog)
        before = len(records)
        if catalog == "vibe_gallery_config.json":
            gallery = require(data.get("vibeGallery"), dict, catalog, "vibeGallery")
            categories = require(gallery.get("categories"), dict, catalog, "vibeGallery.categories")
            for category, group in sorted(categories.items()):
                require(group, dict, catalog, f"category {category}")
                for app in require(group.get("apps"), list, catalog, f"category {category}.apps"):
                    parent = record(app, catalog, 0, category)
                    for version in require(app.get("versions", []), list, catalog, "app.versions"):
                        record(
                            version, catalog, 1, parent.category,
                            {"title": parent.title, "description": parent.description, "category": parent.category},
                        )
        else:
            for app in require(data.get("apps"), list, catalog, "apps"):
                record(app, catalog, 2)
        sources.append({"path": catalog, "status": "present", "entries": len(records) - before})
    return records, sources


def _stable_id(prefix, *parts):
    return prefix + hashlib.sha256("\0".join(parts).encode("utf-8", "surrogateescape")).hexdigest()[:24]


def _tasks(tools, unresolved, records, resolutions, canonical_by_path, commit, max_tasks):
    candidates = {}
    unresolved_paths = {issue["path"] for issue in unresolved}

    def add(operation, title, why, paths, acceptance, score, evidence):
        paths = sorted(set(paths))
        task_id = _stable_id("task-", operation, title, *paths)
        candidates[task_id] = {
            "id": task_id, "operation": operation, "title": title, "why": why,
            "paths": paths, "acceptance": acceptance, "score": score,
            "base_commit": commit, "status": "proposed", "evidence": evidence,
        }

    failures = {}
    for issue in unresolved:
        key = (issue.get("failure_path", issue["path"]), issue["reason"])
        failures.setdefault(key, []).append(issue)
    for (failure_path, reason), issues in sorted(failures.items()):
        paths = {issue["path"] for issue in issues}
        paths.add(failure_path)
        add(
            "review_unresolved_alias", f"Review unresolved HTML lineage at {failure_path}",
            f"Committed-tree discovery reports {reason}; {len(issues)} HTML path(s) are affected.",
            paths,
            [
                "Read the affected committed sources and identify the intended local destination or intentional exception.",
                "Repair the chain or record an explicit, reviewable reason it must remain unresolved; do not delete originals.",
                "Rebuild at the new commit and verify every affected path resolves as intended or has documented exception evidence.",
            ],
            100 if reason == "redirect_cycle" else 95,
            {"kind": reason, "paths": sorted(paths)},
        )
    for record in sorted(set(records), key=lambda item: (item.catalog, item.path, item.priority)):
        resolution = resolutions.get(record.path)
        destination = resolution.destination if resolution else None
        if destination is None:
            if record.path in unresolved_paths:
                continue
            add(
                "repair_metadata_reference", f"Review catalog reference to {record.path}",
                f"{record.catalog} references a path with no discoverable committed HTML payload.",
                [record.catalog],
                [
                    f"Read the entry for {record.path} and identify the intended committed source.",
                    "Correct or explicitly retire the stale metadata entry without silently removing a source file.",
                    "Rebuild and verify the metadata reference points to an inventoried payload or has a documented exclusion.",
                ],
                85, {"kind": "unavailable_metadata_path", "catalog": record.catalog, "entry_path": record.path},
            )
        elif record.priority == 0 and destination != record.path:
            canonical = canonical_by_path[destination]
            add(
                "update_redirect_primary", f"Select the body behind gallery primary {record.path}",
                f"The main gallery selects a meta-refresh alias; its committed payload is cataloged at {canonical}.",
                [record.catalog, record.path, canonical],
                [
                    "Verify the pinned alias and destination belong to the same intended gallery entry.",
                    "Point the preferred gallery path at the real body while preserving the old URL as an alias.",
                    "Rebuild and verify the gallery primary is a non-redirect payload and the old path still resolves.",
                ],
                80, {"kind": "gallery_primary_is_redirect", "alias": record.path, "canonical": canonical},
            )
    for tool in tools:
        if tool["role"] != "app_candidate":
            continue
        missing = tool["metadata"]["missing_fields"]
        if not tool["metadata"]["sources"] or missing:
            add(
                "complete_metadata", f"Document discovery metadata for {tool['path']}",
                (
                    "No committed discovery catalog describes this payload."
                    if not tool["metadata"]["sources"]
                    else "Discovery fields have no source evidence: " + ", ".join(missing) + "."
                ),
                [tool["path"], *tool["metadata"]["sources"]],
                [
                    "Read the exact source before describing its purpose; do not infer capabilities from the filename.",
                    "Record an accurate title, description, and category in repository-owned discovery metadata.",
                    "Rebuild and verify metadata provenance and the unchanged source hash; validate separately before making runtime claims.",
                ],
                55, {"kind": "metadata_gap", "sha256": tool["sha256"], "missing_fields": missing},
            )
    ordered = sorted(
        candidates.values(),
        key=lambda task: (-task["score"], task["operation"], task["paths"], task["id"]),
    )
    return ordered[:max_tasks], len(ordered)


def build_catalog(repo_root, ref="HEAD", *, repository=DEFAULT_REPOSITORY, site_url=None, max_tasks=10) -> dict:
    """Return a catalog of one immutable commit; optional metadata may be absent.

    ``repository`` is a public GitHub ``owner/name``, never an inferred remote.
    ``site_url`` overrides the default GitHub Pages base for local URL resolution.
    Task scores express fixed maintenance priorities, not measured app quality.
    """
    if not isinstance(max_tasks, int) or isinstance(max_tasks, bool) or max_tasks < 0:
        raise CatalogError("max_tasks must be a nonnegative integer.")
    repo = _repository(repository, site_url)
    commit, tree, entries = _snapshot(repo_root, ref)
    repo.update({"commit": commit, "tree": tree})
    html_paths = sorted(path for path in entries if _is_html(path))
    excluded = [
        {"path": path, "reason": "generated_autocomplete_provenance"}
        for path in html_paths if _is_provenance(path)
    ]
    included = [path for path in html_paths if not _is_provenance(path)]
    regular = [path for path in included if entries[path].mode in REGULAR_MODES]
    for path in METADATA_PATHS:
        if path in entries and entries[path].mode not in REGULAR_MODES:
            raise CatalogError(f"{path}: committed metadata must be a regular blob; symlinks are not followed.")
    needed = regular + [path for path in METADATA_PATHS if path in entries]
    facts_by_oid = {}
    catalog_blobs_by_oid = {}
    html_oids = {entries[path].oid for path in regular}
    metadata_oids = {entries[path].oid for path in METADATA_PATHS if path in entries}
    for oid, data in _blobs(repo_root, (entries[path].oid for path in needed)):
        if oid in html_oids:
            facts_by_oid[oid] = _html_facts(data)
        if oid in metadata_oids:
            catalog_blobs_by_oid[oid] = data
    catalog_blobs = {
        path: catalog_blobs_by_oid[entries[path].oid]
        for path in METADATA_PATHS if path in entries
    }
    html = {path: facts_by_oid[entries[path].oid] for path in regular}
    records, metadata_sources = _metadata_records(catalog_blobs, entries, repo["site_url"])
    redirects = _redirects(html, repo["site_url"], entries)
    payload_paths = set(html) - set(redirects)
    resolutions = _resolve_redirects(redirects, payload_paths)

    def source_url(path):
        return f"https://raw.githubusercontent.com/{repository}/{commit}/{_quote_path(path)}"

    groups = {}
    for path in sorted(payload_paths):
        groups.setdefault(html[path].sha256, []).append(path)
    primaries = {item.path for item in records if item.priority == 0}
    versions = {item.path for item in records if item.priority == 1}
    canonical_by_path = {}
    for paths in groups.values():
        canonical = min(paths, key=lambda path: (
            path not in primaries, _path_rank(path)[0], path not in versions, *_path_rank(path)[1:],
        ))
        canonical_by_path.update({path: canonical for path in paths})
    aliases = {}
    redirect_records = []
    unresolved = []
    for path in included:
        if path not in html:
            unresolved.append({
                "path": path, "target": "", "reason": (
                    "symlink_not_followed" if entries[path].mode == "120000" else "non_blob_html_path"
                ),
                "source_url": source_url(path), "failure_path": path,
            })
    for path, redirect in sorted(redirects.items()):
        resolution = resolutions[path]
        canonical = canonical_by_path.get(resolution.destination)
        info = {
            "path": path, "target": redirect.target, "normalized_target": redirect.local_target,
            "resolved_path": resolution.destination, "canonical_path": canonical,
            "source_url": source_url(path), "sha256": html[path].sha256,
            "bytes": html[path].size, "git_blob": entries[path].oid,
        }
        if canonical:
            aliases.setdefault(canonical, []).append(path)
        else:
            info.update({"reason": resolution.reason, "failure_path": resolution.failure_path})
            if resolution.cycle:
                info["cycle"] = list(resolution.cycle)
            unresolved.append(dict(info))
        redirect_records.append(info)
    unresolved.sort(key=lambda item: item["path"])
    metadata_by_canonical = {}
    for record in records:
        resolution = resolutions.get(record.path)
        if resolution and resolution.destination:
            canonical = canonical_by_path[resolution.destination]
            metadata_by_canonical.setdefault(canonical, []).append(record)
    tools = []
    for paths in groups.values():
        canonical = canonical_by_path[paths[0]]
        facts = html[canonical]
        matched = sorted(
            metadata_by_canonical.get(canonical, []),
            key=lambda item: (item.priority, item.path != canonical, item.path, item.title, item.description, item.category),
        )
        values = {}
        evidence = {}
        for key, fallback in (("title", facts.title), ("description", facts.description), ("category", "")):
            candidate = next((item for item in matched if getattr(item, key)), None)
            values[key] = getattr(candidate, key) if candidate else fallback
            evidence[key] = (
                {"catalog": candidate.catalog, "entry_path": candidate.path} if candidate
                else {"html_path": canonical} if fallback else None
            )
        missing = sorted(key for key, value in values.items() if not value)
        values["title"] = values["title"] or PurePosixPath(canonical).stem
        values["category"] = values["category"] or "uncategorized"
        tools.append({
            "id": _stable_id("tool-", canonical),
            **values, "path": canonical,
            "url": repo["site_url"] + _quote_path(canonical),
            "source_url": source_url(canonical),
            "sha256": facts.sha256, "bytes": facts.size, "git_blob": entries[canonical].oid,
            "aliases": sorted(aliases.get(canonical, [])),
            "equivalent_paths": sorted(path for path in paths if path != canonical),
            "signals": facts.signals,
            "role": _role(canonical),
            "path_roles": {path: _role(path) for path in sorted(paths)},
            "metadata": {
                "sources": sorted({item.catalog for item in matched}),
                "fields": evidence, "missing_fields": missing,
            },
        })
    tools.sort(key=lambda tool: tool["path"])
    tasks, task_candidates = _tasks(
        tools, unresolved, records, resolutions, canonical_by_path, commit, max_tasks,
    )
    return {
        "schema": SCHEMA,
        "generated_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "repository": repo,
        "counts": {
            "tracked_paths": len(entries),
            "html_paths": len(html_paths),
            "redirect_paths": len(redirects),
            "canonical_tools": len(tools),
            "duplicate_paths": sum(len(tool["equivalent_paths"]) for tool in tools),
            "unresolved_paths": len(unresolved),
            "resolved_alias_paths": sum(len(tool["aliases"]) for tool in tools),
            "excluded_html_paths": len(excluded),
        },
        "count_definitions": {
            "tracked_paths": "All leaf entries in the full committed Git tree, including symlinks and gitlinks.",
            "html_paths": "All tracked paths ending in .html or .htm, case-insensitively, including excluded and nonregular paths.",
            "redirect_paths": "Scanned regular HTML paths declaring meta refresh, whether resolved or unresolved.",
            "canonical_tools": "Distinct exact-byte non-redirect HTML payloads after folding; not a count of complete or independent apps.",
            "duplicate_paths": "Extra non-redirect paths with exactly the same raw bytes as a canonical payload; excludes redirects.",
            "unresolved_paths": "HTML paths not assigned to a payload because of unresolved refresh or unsupported Git entry type.",
            "resolved_alias_paths": "Successful meta-refresh source paths, each assigned to exactly one canonical payload.",
            "excluded_html_paths": "Generated autocomplete evidence/receipt/artifact HTML excluded from content discovery.",
            "partition": "html_paths = canonical_tools + duplicate_paths + resolved_alias_paths + unresolved_paths + excluded_html_paths",
        },
        "tools": tools, "unresolved": unresolved, "tasks": tasks,
        "redirects": redirect_records, "excluded": excluded,
        "metadata_sources": [
            {**item, "source_url": source_url(item["path"]) if item["status"] == "present" else None}
            for item in metadata_sources
        ],
        "planning": {
            "task_limit": max_tasks, "candidate_tasks": task_candidates,
            "ranking": "Fixed maintenance priority descending, then operation, source paths, and stable task id.",
            "score_meaning": "Backlog priority only; never runtime quality, novelty, or implementation completion.",
            "extension": {
                "schema": "localfirst-autocomplete-proposal/v1",
                "instructions": [
                    "Search this catalog and inspect nearest committed source ancestors before proposing new work.",
                    "Cite ancestor paths, pinned source URLs, hashes, and observations actually read from their source.",
                    "Explain the unmet user need and overlap with existing payloads; filenames and titles are not novelty evidence.",
                    "Propose a bounded change with observable acceptance and executable validation; do not claim implementation yet.",
                    "Record actual changes and validation separately as RAPP/1 receipts; a proposal or discovery timestamp is not proof of first invention.",
                ],
                "proposal_template": {
                    "base_commit": commit, "operation": "propose_improvement",
                    "title": "", "why": "", "paths": [],
                    "nearest_ancestors": [
                        {"path": "", "source_url": "", "sha256": "", "source_observation": ""},
                    ],
                    "catalog_overlap": [], "acceptance": [], "validation_plan": [],
                    "status": "proposed",
                },
            },
        },
        "limitations": [
            "Discovery uses only the resolved committed tree; dirty, staged, untracked, and submodule contents are not included.",
            "Only .html/.htm payloads and the two named JSON metadata catalogs are inspected; generated JSON provenance is never app content.",
            "Missing optional metadata catalogs are supported initial-repository state; present malformed catalogs are errors.",
            "Meta-refresh discovery is static HTMLParser analysis, not browser execution; JavaScript, HTTP redirects, and noscript behavior are not verified.",
            "Local targets are case-sensitive, percent-decoded once, constrained to the configured site prefix, and never followed through symlinks.",
            "Directory URLs resolve only to committed index.html; hosting rewrites, extensionless routes, and custom server behavior are not inferred.",
            "HTML text is decoded as UTF-8 with replacement for parsing; source hashes and byte counts always use untouched committed bytes.",
            "Aliases are resolved refresh paths; equivalent_paths are additional exact-byte payload copies, not title-based or semantic matches.",
            "Roles are path-based labels, not proof of completeness; docs, operational pages, archives, templates, and vendor artifacts can be payloads.",
            "Signals are source heuristics: persistence identifier mentions, HTTP(S)/protocol-relative script src, and either import/export word; comments may match.",
            "Signals do not prove offline operation, accessibility, safety, portability, runtime quality, or successful tests; external loads can also occur dynamically.",
            "Live URLs are mutable; source URLs, Git object IDs, hashes, and repository.commit pin the evidence used for this catalog.",
            "Tool IDs derive from canonical paths, may change on canonical relocation, and are not RAPP identities.",
            "Tasks are bounded maintenance proposals, not implemented improvements, synthetic scores, novelty findings, or legal priority claims.",
            "generated_at is the UTC catalog build time, not a trusted timestamp, commit date, publication event, or proof of first invention.",
        ],
    }


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", required=True, type=Path, help="Local Git repository to inspect (never published).")
    parser.add_argument("--ref", default="HEAD", help="Commit-ish to resolve once, then inspect immutably.")
    parser.add_argument("--output", required=True, type=Path, help="Destination JSON file.")
    parser.add_argument("--repository", default=DEFAULT_REPOSITORY, help="Public GitHub owner/name; no remote is inferred.")
    parser.add_argument("--site-url", help="Public site base URL; defaults to the repository's GitHub Pages prefix.")
    parser.add_argument("--max-tasks", default=10, type=int, help="Maximum ranked tasks (default: 10; zero disables tasks).")
    args = parser.parse_args(argv)
    try:
        catalog = build_catalog(
            args.repo, args.ref, repository=args.repository,
            site_url=args.site_url, max_tasks=args.max_tasks,
        )
        output = json.dumps(catalog, indent=2, ensure_ascii=True, allow_nan=False) + "\n"
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(output, encoding="utf-8")
    except (CatalogError, OSError) as exc:
        message = str(exc) if isinstance(exc, CatalogError) else "Could not write the requested catalog output."
        parser.exit(2, f"autocomplete_catalog: {message}\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
