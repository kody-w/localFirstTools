"""Committed-tree catalog tests; disposable Git repositories stay under this checkout."""

from contextlib import redirect_stderr
import hashlib
import io
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import unittest
from unittest.mock import patch
import uuid

import scripts.autocomplete_catalog as catalog_module
from scripts.autocomplete_catalog import CatalogError, build_catalog, main


def page(title="Example", body="An example body", description=""):
    return (
        f'<!doctype html><html><head><title>{title}</title>'
        f'<meta name="description" content="{description}"></head><body>{body}</body></html>'
    )


def refresh(target):
    return f'<meta http-equiv="refresh" content="0; url={target}">'


class CatalogTests(unittest.TestCase):
    def setUp(self):
        self.fixture_root = Path("tests/.autocomplete-catalog-fixtures")
        self.case = self.fixture_root / uuid.uuid4().hex
        self.repo = self.case / "repo"
        self.repo.mkdir(parents=True)
        self.addCleanup(self.clean_fixture)
        self.git("init", "--quiet")

    def clean_fixture(self):
        shutil.rmtree(self.case)
        try:
            self.fixture_root.rmdir()
        except OSError:
            pass

    def git(self, *args, input=None):
        environment = os.environ.copy()
        for key in (
            "GIT_DIR", "GIT_WORK_TREE", "GIT_INDEX_FILE", "GIT_COMMON_DIR",
            "GIT_OBJECT_DIRECTORY", "GIT_ALTERNATE_OBJECT_DIRECTORIES",
        ):
            environment.pop(key, None)
        environment.update({
            "GIT_CONFIG_NOSYSTEM": "1",
            "GIT_CONFIG_GLOBAL": os.devnull,
            "GIT_AUTHOR_DATE": "2026-09-01T12:00:00+00:00",
            "GIT_COMMITTER_DATE": "2026-09-01T12:00:00+00:00",
        })
        return subprocess.run(
            [
                "git", "-C", str(self.repo),
                "-c", "user.name=Catalog Tests", "-c", "user.email=catalog@example.invalid",
                "-c", "commit.gpgsign=false", "-c", "core.hooksPath=.git/no-hooks",
                "-c", "init.defaultBranch=main", *args,
            ],
            env=environment, input=input, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
        ).stdout.decode("utf-8").strip()

    def write(self, path, contents):
        destination = self.repo / path
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_bytes(contents if isinstance(contents, bytes) else contents.encode("utf-8"))

    def write_json(self, path, data):
        self.write(path, json.dumps(data, ensure_ascii=False))

    def gallery(self, apps, category="utilities"):
        self.write_json("vibe_gallery_config.json", {
            "vibeGallery": {"categories": {category: {"apps": apps}}},
        })

    def commit(self):
        self.git("add", "--all")
        return self.commit_index()

    def commit_index(self):
        return self.git("commit", "--quiet", "--allow-empty", "-m", "catalog fixture") or self.git("rev-parse", "HEAD")

    def stage_blob(self, path, contents, mode="100644"):
        data = contents if isinstance(contents, bytes) else contents.encode("utf-8")
        oid = self.git("hash-object", "-w", "--stdin", input=data)
        self.git("update-index", "--add", "--cacheinfo", mode, oid, path)

    def catalog(self, **kwargs):
        return build_catalog(self.repo, **kwargs)

    def assert_reference_outcome(self, reference_name, failure_contains=None):
        result = unittest.TestResult()
        CatalogTests(reference_name).run(result)
        self.assertEqual(result.testsRun, 1, "The named reference test must actually execute.")
        self.assertEqual(result.skipped, [], "Reference coverage must never silently skip.")
        self.assertEqual(result.errors, [], "An unrelated exception is not a mutation witness.")
        self.assertEqual(result.expectedFailures, [])
        self.assertEqual(result.unexpectedSuccesses, [])
        expected_failures = 0 if failure_contains is None else 1
        self.assertEqual(len(result.failures), expected_failures, result.failures)
        if failure_contains is not None:
            self.assertIn(failure_contains, result.failures[0][1])

    def assert_mutation_is_caught(self, reference_name, mutation, failure_contains):
        self.assert_reference_outcome(reference_name)
        with mutation:
            self.assert_reference_outcome(reference_name, failure_contains)
        self.assert_reference_outcome(reference_name)

    def assert_partition(self, catalog):
        counts = catalog["counts"]
        self.assertEqual(
            counts["html_paths"],
            sum(counts[key] for key in (
                "canonical_tools", "duplicate_paths", "resolved_alias_paths",
                "unresolved_paths", "excluded_html_paths",
            )),
        )

    def test_initial_repository_without_optional_catalogs(self):
        raw = page("A real title", "localStorage; Import backup", "Useful description").encode("utf-8")
        self.write("app.html", raw)
        self.write("README.md", "Not an HTML app")
        commit = self.commit()
        catalog = self.catalog()
        self.assertEqual(catalog["schema"], "localfirst-autocomplete-catalog/v1")
        self.assertRegex(catalog["generated_at"], r"^\d{4}-\d\d-\d\dT\d\d:\d\d:\d\dZ$")
        self.assertEqual(catalog["repository"]["commit"], commit)
        self.assertEqual(catalog["repository"]["tree"], self.git("rev-parse", "HEAD^{tree}"))
        self.assertEqual(catalog["counts"]["tracked_paths"], 2)
        self.assertEqual(catalog["counts"]["html_paths"], 1)
        self.assertEqual([source["status"] for source in catalog["metadata_sources"]], ["missing", "missing"])
        tool = catalog["tools"][0]
        self.assertEqual(tool["sha256"], hashlib.sha256(raw).hexdigest())
        self.assertEqual(tool["bytes"], len(raw))
        self.assertEqual(tool["title"], "A real title")
        self.assertEqual(tool["description"], "Useful description")
        self.assertIn(f"/{commit}/app.html", tool["source_url"])
        self.assertTrue(tool["signals"]["local_persistence"])
        self.assertTrue(tool["signals"]["import_export_mentions"])
        self.assertEqual(catalog["tasks"][0]["operation"], "complete_metadata")
        self.assert_partition(catalog)

    def test_empty_committed_tree(self):
        self.commit()
        catalog = self.catalog()
        self.assertEqual(catalog["tools"], [])
        self.assertEqual(catalog["tasks"], [])
        self.assertEqual(catalog["counts"]["tracked_paths"], 0)
        self.assert_partition(catalog)

    def test_redirect_chains_fold_aliases_into_exact_payload_group(self):
        raw = page()
        self.write("entry.html", refresh("nested/alias.html"))
        self.write("nested/alias.html", refresh("../apps/body.html?mode=1&amp;view=2#section"))
        self.write("apps/body.html", raw)
        self.write("copies/body.html", raw)
        self.commit()
        catalog = self.catalog()
        tool = catalog["tools"][0]
        self.assertEqual(tool["path"], "apps/body.html")
        self.assertEqual(tool["aliases"], ["entry.html", "nested/alias.html"])
        self.assertEqual(tool["equivalent_paths"], ["copies/body.html"])
        self.assertEqual(catalog["counts"]["redirect_paths"], 2)
        self.assertEqual(catalog["counts"]["duplicate_paths"], 1)
        self.assertEqual(catalog["unresolved"], [])
        lineage = {item["path"]: item for item in catalog["redirects"]}
        self.assertEqual(lineage["entry.html"]["normalized_target"], "nested/alias.html")
        self.assertEqual(lineage["entry.html"]["resolved_path"], "apps/body.html")
        self.assertEqual(lineage["nested/alias.html"]["target"], "../apps/body.html?mode=1&view=2#section")
        self.assert_partition(catalog)

    def test_url_normalization_spaces_unicode_entities_case_and_pages_prefix(self):
        destination = "apps/Café space & fun.HTML"
        self.write(destination, page("Café"))
        targets = {
            "relative.html": "apps/Caf%C3%A9%20space%20%26%20fun.HTML?x=1&amp;y=2#top",
            "nested/relative.html": "../apps/Caf%C3%A9%20space%20%26%20fun.HTML",
            "absolute.html": "/localFirstTools/apps/Caf%C3%A9%20space%20%26%20fun.HTML",
            "host.html": "https://KODY-W.github.io/localFirstTools/apps/Caf%C3%A9%20space%20%26%20fun.HTML",
            "default-port.html": "https://kody-w.github.io:443/localFirstTools/apps/Caf%C3%A9%20space%20%26%20fun.HTML",
            "protocol.html": "//kody-w.github.io/localFirstTools/apps/Caf%C3%A9%20space%20%26%20fun.HTML",
            "dots.html": "/localFirstTools/ignored/../apps/Caf%C3%A9%20space%20%26%20fun.HTML",
            "encoded-dots.html": "/localFirstTools/ignored/%2e%2e/apps/Caf%C3%A9%20space%20%26%20fun.HTML",
            "literal.html": "apps/Café space &amp; fun.HTML",
        }
        for path, target in targets.items():
            self.write(path, refresh(target))
        self.write("wrong-case.html", refresh("apps/café space &amp; fun.HTML"))
        self.commit()
        catalog = self.catalog()
        tool = catalog["tools"][0]
        self.assertEqual(tool["path"], destination)
        self.assertEqual(tool["aliases"], sorted(targets))
        self.assertEqual(catalog["unresolved"][0]["reason"], "missing_target")
        self.assertIn("Caf%C3%A9%20space%20%26%20fun.HTML", tool["url"])
        self.assert_partition(catalog)

    def test_literal_percent_and_entities_are_decoded_only_once(self):
        self.write("apps/a%20b.html", page("Percent"))
        self.write("apps/a&amp;b.html", page("Entity"))
        self.write("percent.html", refresh("apps/a%2520b.html"))
        self.write("entity.html", refresh("apps/a&amp;amp;b.html"))
        self.commit()
        catalog = self.catalog()
        tools = {item["path"]: item for item in catalog["tools"]}
        self.assertEqual(tools["apps/a%20b.html"]["aliases"], ["percent.html"])
        self.assertEqual(tools["apps/a&amp;b.html"]["aliases"], ["entity.html"])
        self.assertEqual(catalog["unresolved"], [])

    def test_refresh_parser_quotes_case_directory_and_base_href(self):
        self.write("apps/tool.html", page("Tool"))
        self.write("directory/index.html", page("Directory"))
        self.write(
            "alias.html",
            '<BASE href="/localFirstTools/apps/"><META CONTENT="5.5; URL = \'tool.html\'" HTTP-EQUIV=" Refresh ">',
        )
        self.write("dir.html", refresh("directory/"))
        self.write("dir-no-slash.html", refresh("directory"))
        self.write("base-external.html", '<base href="https://example.org/">' + refresh("tool.html"))
        self.commit()
        catalog = self.catalog()
        tools = {item["path"]: item for item in catalog["tools"]}
        self.assertEqual(tools["apps/tool.html"]["aliases"], ["alias.html"])
        self.assertEqual(tools["directory/index.html"]["aliases"], ["dir-no-slash.html", "dir.html"])
        self.assertEqual(catalog["unresolved"][0]["reason"], "external_target")

    def test_missing_non_html_external_cross_repository_and_cycles_are_explicit(self):
        targets = {
            "a.html": "b.html", "b.html": "a.html", "before-cycle.html": "a.html",
            "missing.html": "gone.html", "before-missing.html": "missing.html",
            "external.html": "https://example.org/tool.html",
            "cross-repo.html": "https://kody-w.github.io/other/tool.html",
            "outside-prefix.html": "/tool.html",
            "prefix-collision.html": "/localFirstTools-copy/tool.html",
            "escape.html": "/localFirstTools/%2e%2e/other/tool.html",
            "text.html": "README.md",
            "unsupported.html": "javascript:alert(1)",
            "self.html": "#here",
            "credentials.html": "https://user:secret@kody-w.github.io/localFirstTools/tool.html",
        }
        for path, target in targets.items():
            self.write(path, refresh(target))
        self.write("README.md", "Not HTML")
        self.commit()
        catalog = self.catalog()
        reasons = {item["path"]: item["reason"] for item in catalog["unresolved"]}
        for path in ("a.html", "b.html", "before-cycle.html", "self.html"):
            self.assertEqual(reasons[path], "redirect_cycle")
        for path in ("missing.html", "before-missing.html"):
            self.assertEqual(reasons[path], "missing_target")
        for path in ("cross-repo.html", "outside-prefix.html", "prefix-collision.html", "escape.html"):
            self.assertEqual(reasons[path], "outside_repository")
        self.assertEqual(reasons["external.html"], "external_target")
        self.assertEqual(reasons["text.html"], "non_html_target")
        self.assertEqual(reasons["unsupported.html"], "unsupported_scheme")
        self.assertEqual(reasons["credentials.html"], "credentialed_target")
        self.assertNotIn("user:secret", json.dumps(catalog))
        self.assertEqual(catalog["counts"]["unresolved_paths"], len(targets))
        self.assertEqual(catalog["tools"], [])
        self.assert_partition(catalog)

    def test_refusal_of_bad_aliases_even_when_a_local_basename_matches(self):
        self.write("apps/body.html", page("Real local body"))
        targets = {
            "external.html": "https://example.org/localFirstTools/apps/body.html",
            "cross-repo.html": "/another-repository/apps/body.html",
            "prefix-lookalike.html": "/localFirstTools-copy/apps/body.html",
            "missing.html": "missing/body.html",
            "wrong-case.html": "apps/Body.html",
        }
        for path, target in targets.items():
            self.write(path, refresh(target))
        self.commit()
        catalog = self.catalog()
        self.assertEqual(
            catalog["tools"][0]["aliases"], [],
            "Invalid aliases cannot be attached to a local payload.",
        )
        self.assertEqual(
            {item["path"]: item["reason"] for item in catalog["unresolved"]},
            {
                "external.html": "external_target",
                "cross-repo.html": "outside_repository",
                "prefix-lookalike.html": "outside_repository",
                "missing.html": "missing_target",
                "wrong-case.html": "missing_target",
            },
        )
        self.assert_partition(catalog)

    def test_mutation_witness_bad_alias_acceptance_turns_reference_red(self):
        real_local_target = catalog_module._local_target
        for invalid_alias in (
            "external.html", "cross-repo.html", "prefix-lookalike.html",
            "missing.html", "wrong-case.html",
        ):
            with self.subTest(mutated_alias=invalid_alias):
                def accept_bad_alias(source_path, *args):
                    if source_path == invalid_alias:
                        return "apps/body.html", None
                    return real_local_target(source_path, *args)

                self.assert_mutation_is_caught(
                    "test_refusal_of_bad_aliases_even_when_a_local_basename_matches",
                    patch.object(catalog_module, "_local_target", side_effect=accept_bad_alias),
                    "Invalid aliases cannot be attached to a local payload.",
                )

    def test_refresh_reload_malformed_and_ambiguous_tags_are_not_payloads(self):
        self.write("reload.html", '<meta http-equiv="refresh" content="10">')
        self.write("bad.html", '<meta http-equiv="refresh" content="url=target.html">')
        self.write("absent.html", '<meta http-equiv="refresh">')
        self.write("quotes.html", '<meta http-equiv="refresh" content="0; url=\'target.html">')
        self.write("ambiguous.html", refresh("one.html") + refresh("two.html"))
        self.write("template.html", '<template>' + refresh("missing.html") + '</template><title>Template</title>')
        self.commit()
        catalog = self.catalog()
        reasons = {item["path"]: item["reason"] for item in catalog["unresolved"]}
        self.assertEqual(reasons["reload.html"], "redirect_cycle")
        self.assertEqual(reasons["ambiguous.html"], "ambiguous_refresh")
        for path in ("absent.html", "bad.html", "quotes.html"):
            self.assertEqual(reasons[path], "malformed_refresh")
        self.assertEqual([tool["path"] for tool in catalog["tools"]], ["template.html"])
        self.assert_partition(catalog)

    def test_long_redirect_chains_do_not_use_python_recursion(self):
        self.write("body.html", page())
        for index in range(1050):
            target = f"r{index + 1:04}.html" if index < 1049 else "body.html"
            self.write(f"r{index:04}.html", refresh(target))
        self.commit()
        catalog = self.catalog(max_tasks=0)
        self.assertEqual(len(catalog["tools"][0]["aliases"]), 1050)
        self.assertEqual(catalog["unresolved"], [])
        self.assert_partition(catalog)

    def test_identical_titles_are_not_content_duplicates(self):
        first = page("Same title", "first body")
        self.write("first.html", first)
        self.write("first-copy.html", first)
        self.write("second.html", page("Same title", "second body"))
        self.commit()
        catalog = self.catalog()
        self.assertEqual(catalog["counts"]["canonical_tools"], 2)
        self.assertEqual(catalog["counts"]["duplicate_paths"], 1)
        self.assertEqual([tool["title"] for tool in catalog["tools"]], ["Same title", "Same title"])
        self.assertEqual(len({tool["sha256"] for tool in catalog["tools"]}), 2)

    def test_gallery_primary_preferred_and_categories_come_from_same_snapshot(self):
        raw = page("HTML title", description="HTML description")
        for path in ("chosen.html", "v2/apps/other.html", "vendor/copy.html"):
            self.write(path, raw)
        self.gallery([{"path": "chosen.html", "title": "Gallery title", "description": "Gallery description"}])
        self.write_json("landgrab/index.json", {
            "apps": [{"path": "v2/apps/other.html", "title": "Old title", "category": "wrong"}],
        })
        self.commit()
        tool = self.catalog()["tools"][0]
        self.assertEqual(tool["path"], "chosen.html")
        self.assertEqual(tool["title"], "Gallery title")
        self.assertEqual(tool["description"], "Gallery description")
        self.assertEqual(tool["category"], "utilities")
        self.assertEqual(tool["metadata"]["fields"]["title"]["catalog"], "vibe_gallery_config.json")
        self.assertEqual(tool["path_roles"]["vendor/copy.html"], "artifact")

    def test_redirect_primary_and_version_metadata_preserve_source_lineage(self):
        self.write("old.html", refresh("apps/body.html"))
        self.write("apps/body.html", page("Source title"))
        self.write("root-copy.html", page("Source title"))
        self.gallery([{
            "path": "old.html", "title": "Selected title", "description": "Metadata description",
            "versions": [{"path": "apps/body.html"}],
        }], category="education")
        self.commit()
        catalog = self.catalog()
        tool = catalog["tools"][0]
        self.assertEqual(tool["path"], "apps/body.html")
        self.assertEqual(tool["title"], "Selected title")
        self.assertEqual(tool["category"], "education")
        self.assertEqual(tool["aliases"], ["old.html"])
        task = next(task for task in catalog["tasks"] if task["operation"] == "update_redirect_primary")
        self.assertEqual(task["paths"], ["apps/body.html", "old.html", "vibe_gallery_config.json"])
        self.assertEqual(task["evidence"]["canonical"], "apps/body.html")

    def test_deterministic_path_ranking_avoids_artifacts_and_archives(self):
        raw = page()
        for path in ("archive/a.html", "vendor/a.html", "dist/a.html", "v2/apps/live.html", "a.html"):
            self.write(path, raw)
        self.commit()
        tool = self.catalog()["tools"][0]
        self.assertEqual(tool["path"], "v2/apps/live.html")
        self.assertEqual(tool["equivalent_paths"], ["a.html", "archive/a.html", "dist/a.html", "vendor/a.html"])
        self.assertEqual(tool["role"], "app_candidate")

    def test_immutable_commit_ignores_dirty_staged_deleted_and_untracked_files(self):
        original = page("Committed", description="Committed description")
        self.write("app.html", original)
        self.write("copy.html", original)
        self.gallery([{"path": "copy.html", "title": "Committed gallery title"}])
        commit = self.commit()
        self.write("app.html", page("Dirty bytes"))
        self.git("add", "app.html")
        self.write("vibe_gallery_config.json", "{not valid JSON")
        (self.repo / "copy.html").unlink()
        self.write("untracked.html", page("Do not attribute me"))
        catalog = self.catalog()
        self.assertEqual(catalog["repository"]["commit"], commit)
        self.assertEqual(catalog["counts"]["html_paths"], 2)
        self.assertEqual(
            catalog["tools"][0]["path"], "copy.html",
            "Canonical payload selection must come from the committed tree.",
        )
        self.assertEqual(catalog["tools"][0]["title"], "Committed gallery title")
        self.assertEqual(
            catalog["tools"][0]["sha256"], hashlib.sha256(original.encode()).hexdigest(),
            "Committed source bytes must not come from dirty or staged files.",
        )
        self.write_json("vibe_gallery_config.json", {"vibeGallery": {"categories": {}}})
        self.commit()
        old_catalog = self.catalog(ref=commit)
        catalog.pop("generated_at")
        old_catalog.pop("generated_at")
        self.assertEqual(old_catalog, catalog)
        self.assertNotEqual(self.catalog()["repository"]["commit"], commit)

    def test_mutation_witness_working_tree_blob_leak_turns_reference_red(self):
        real_blobs = catalog_module._blobs

        def read_dirty_body(repo_root, object_ids):
            body_oid = catalog_module._git(
                repo_root, "rev-parse", "--verify", "HEAD:app.html",
            ).decode("ascii").strip()
            for oid, data in real_blobs(repo_root, object_ids):
                if oid == body_oid:
                    data = (Path(repo_root) / "app.html").read_bytes()
                yield oid, data

        self.assert_mutation_is_caught(
            "test_immutable_commit_ignores_dirty_staged_deleted_and_untracked_files",
            patch.object(catalog_module, "_blobs", side_effect=read_dirty_body),
            "Committed source bytes must not come from dirty or staged files.",
        )

    def test_mutation_witness_staged_tree_leak_turns_reference_red(self):
        real_git = catalog_module._git

        def list_staged_tree(repo_root, *args):
            if args[0] == "ls-tree":
                staged_tree = real_git(repo_root, "write-tree").decode("ascii").strip()
                args = (*args[:-1], staged_tree)
            return real_git(repo_root, *args)

        self.assert_mutation_is_caught(
            "test_immutable_commit_ignores_dirty_staged_deleted_and_untracked_files",
            patch.object(catalog_module, "_git", side_effect=list_staged_tree),
            "Canonical payload selection must come from the committed tree.",
        )

    def test_valid_dirty_metadata_cannot_override_committed_metadata(self):
        self.write("app.html", page("HTML title"))
        self.gallery([{"path": "app.html", "title": "Committed title"}], category="utilities")
        commit = self.commit()
        self.gallery([{"path": "app.html", "title": "Dirty title"}], category="games")
        catalog = self.catalog()
        self.assertEqual(
            catalog["tools"][0]["title"], "Committed title",
            "Discovery metadata must come from the pinned Git tree.",
        )
        self.assertEqual(catalog["tools"][0]["category"], "utilities")
        self.assertEqual(catalog["repository"]["commit"], commit)

    def test_mutation_witness_dirty_metadata_leak_turns_reference_red(self):
        real_blobs = catalog_module._blobs

        def read_dirty_metadata(repo_root, object_ids):
            metadata_oid = catalog_module._git(
                repo_root, "rev-parse", "--verify", "HEAD:vibe_gallery_config.json",
            ).decode("ascii").strip()
            for oid, data in real_blobs(repo_root, object_ids):
                if oid == metadata_oid:
                    data = (Path(repo_root) / "vibe_gallery_config.json").read_bytes()
                yield oid, data

        self.assert_mutation_is_caught(
            "test_valid_dirty_metadata_cannot_override_committed_metadata",
            patch.object(catalog_module, "_blobs", side_effect=read_dirty_metadata),
            "Discovery metadata must come from the pinned Git tree.",
        )

    def test_refs_resolve_once_even_when_branch_changes_during_scan(self):
        self.write("app.html", page("Old"))
        original = self.commit()
        self.write("app.html", page("New"))
        newer = self.commit()
        self.git("branch", "snapshot", original)
        import scripts.autocomplete_catalog as module
        real_git = module._git

        def moving_ref(repo, *args):
            result = real_git(repo, *args)
            if args[0] == "rev-parse" and "snapshot^{commit}" in args:
                self.git("branch", "--force", "snapshot", newer)
            return result

        with patch.object(module, "_git", side_effect=moving_ref):
            catalog = self.catalog(ref="snapshot")
        self.assertEqual(catalog["repository"]["commit"], original)
        self.assertEqual(catalog["tools"][0]["title"], "Old")

    def test_git_replace_objects_cannot_change_pinned_content(self):
        self.write("app.html", page("Original"))
        commit = self.commit()
        original_blob = self.git("rev-parse", "HEAD:app.html")
        self.write("app.html", page("Replacement"))
        replacement_blob = self.git("hash-object", "-w", "app.html")
        self.git("replace", original_blob, replacement_blob)
        catalog = self.catalog()
        self.assertEqual(catalog["repository"]["commit"], commit)
        self.assertEqual(catalog["tools"][0]["title"], "Original")

    def test_inherited_git_repository_environment_does_not_override_repo_argument(self):
        self.write("app.html", page("Correct repository"))
        commit = self.commit()
        with patch.dict(os.environ, {
            "GIT_DIR": str(self.case.resolve() / "nonexistent.git"),
            "GIT_WORK_TREE": str(self.case.resolve() / "nonexistent"),
            "GIT_INDEX_FILE": str(self.case.resolve() / "nonexistent.index"),
            "GIT_NAMESPACE": "unrelated",
        }):
            catalog = self.catalog()
        self.assertEqual(catalog["repository"]["commit"], commit)
        self.assertEqual(catalog["tools"][0]["title"], "Correct repository")

    def test_symlinks_and_symlinked_directories_are_not_followed(self):
        outside = self.case / "outside"
        outside.mkdir()
        (outside / "body.html").write_text(page("Private outside body"), encoding="utf-8")
        self.write("redirect.html", refresh("link.html"))
        self.write("directory-redirect.html", refresh("linked/body.html"))
        self.git("add", "--all")
        # Git symlink modes exercise refusal even where creating OS symlinks is denied.
        self.stage_blob("link.html", "../outside/body.html", mode="120000")
        self.stage_blob("linked", "../outside", mode="120000")
        self.commit_index()
        catalog = self.catalog()
        reasons = {item["path"]: item["reason"] for item in catalog["unresolved"]}
        self.assertEqual(reasons["link.html"], "symlink_not_followed")
        self.assertEqual(reasons["redirect.html"], "symlink_target")
        self.assertEqual(reasons["directory-redirect.html"], "symlink_target")
        self.assertNotIn("Private outside body", json.dumps(catalog))
        self.assertEqual(catalog["counts"]["tracked_paths"], 4)
        self.assertEqual(catalog["tools"], [])
        self.assert_partition(catalog)

    def test_symlink_metadata_is_an_error_not_a_working_tree_read(self):
        (self.case / "outside.json").write_text('{"apps": []}', encoding="utf-8")
        self.stage_blob("landgrab/index.json", "../../outside.json", mode="120000")
        self.commit_index()
        with self.assertRaisesRegex(CatalogError, "regular blob"):
            self.catalog()

    def test_malformed_json_and_catalog_shapes_surface_errors(self):
        bad_catalogs = [
            ("landgrab/index.json", "{"),
            ("landgrab/index.json", "[]"),
            ("landgrab/index.json", '{"apps": {}}'),
            ("landgrab/index.json", '{"apps": [{"title": "No path"}]}'),
            ("landgrab/index.json", '{"apps": [{"path": "app.html", "title": 17}]}'),
            ("landgrab/index.json", '{"apps": [], "count": NaN}'),
            ("landgrab/index.json", '{"apps": [], "apps": []}'),
            ("vibe_gallery_config.json", "{}"),
            ("vibe_gallery_config.json", '{"vibeGallery": {"categories": []}}'),
            ("vibe_gallery_config.json", '{"vibeGallery": {"categories": {"x": {"apps": [{"path": "x.html", "versions": {}}]}}}}'),
        ]
        for name, contents in bad_catalogs:
            with self.subTest(catalog=name, contents=contents):
                for path in ("landgrab/index.json", "vibe_gallery_config.json"):
                    if (self.repo / path).exists():
                        (self.repo / path).unlink()
                self.write(name, contents)
                self.commit()
                with self.assertRaises(CatalogError) as error:
                    self.catalog()
                self.assertIn(name, str(error.exception))
                self.assertNotIn(str(self.repo.resolve()), str(error.exception))

    def test_present_malformed_metadata_cannot_be_treated_as_missing(self):
        self.write("app.html", page())
        self.write("landgrab/index.json", "{invalid JSON")
        self.commit()
        with self.assertRaisesRegex(
            CatalogError, "landgrab/index.json",
            msg="Present malformed metadata cannot become missing metadata.",
        ):
            self.catalog()

    def test_mutation_witness_suppressed_metadata_error_turns_reference_red(self):
        real_metadata_records = catalog_module._metadata_records

        def ignore_present_catalog(catalogs, entries, site_url):
            remaining = {path: data for path, data in catalogs.items() if path != "landgrab/index.json"}
            return real_metadata_records(remaining, entries, site_url)

        self.assert_mutation_is_caught(
            "test_present_malformed_metadata_cannot_be_treated_as_missing",
            patch.object(catalog_module, "_metadata_records", side_effect=ignore_present_catalog),
            "Present malformed metadata cannot become missing metadata.",
        )

    def test_identical_metadata_blobs_are_read_for_both_catalog_paths(self):
        data = {"apps": [], "vibeGallery": {"categories": {}}}
        self.write_json("landgrab/index.json", data)
        self.write_json("vibe_gallery_config.json", data)
        self.commit()
        catalog = self.catalog()
        self.assertEqual([item["status"] for item in catalog["metadata_sources"]], ["present", "present"])

    def test_output_order_and_task_ids_are_deterministic_and_bounded(self):
        for index in reversed(range(18)):
            self.write(f"apps/{index:02}.html", page(f"Title {index}"))
        self.write("broken.html", refresh("missing.html"))
        self.commit()
        first = self.catalog()
        second = self.catalog()
        first.pop("generated_at")
        second.pop("generated_at")
        self.assertEqual(first, second)
        self.assertEqual(len(first["tasks"]), 10)
        self.assertGreater(first["planning"]["candidate_tasks"], 10)
        self.assertEqual(first["tasks"][0]["operation"], "review_unresolved_alias")
        self.assertEqual([tool["path"] for tool in first["tools"]], sorted(tool["path"] for tool in first["tools"]))
        self.assertTrue(all(isinstance(task["score"], int) for task in first["tasks"]))
        self.assertTrue(all(task["paths"] and task["acceptance"] and task["evidence"] for task in first["tasks"]))
        self.assertEqual(len(self.catalog(max_tasks=2)["tasks"]), 2)
        self.assertEqual(self.catalog(max_tasks=0)["tasks"], [])
        with self.assertRaises(CatalogError):
            self.catalog(max_tasks=-1)

    def test_metadata_is_not_deduplicated_by_title_or_version_membership(self):
        self.write("one.html", page("Original"))
        self.write("two.html", page("Different implementation"))
        self.gallery([{"path": "one.html", "title": "Same title", "versions": [{"path": "two.html"}]}])
        self.commit()
        catalog = self.catalog()
        self.assertEqual(catalog["counts"]["canonical_tools"], 2)
        self.assertEqual([tool["title"] for tool in catalog["tools"]], ["Same title", "Same title"])

    def test_generated_provenance_excluded_and_other_roles_are_honest(self):
        paths = {
            "landgrab/autocomplete/index.html": "operational",
            "docs/guide.html": "documentation",
            "vendor/unique.html": "artifact",
            "archive/unique.html": "archive",
            "apps/unique.html": "app_candidate",
        }
        for path in paths:
            self.write(path, page(path))
        self.write("landgrab/autocomplete/receipts/report.html", page("Not a tool"))
        self.write("landgrab/autocomplete/catalog.json", "{deliberately not a metadata source}")
        self.write("report-alias.html", refresh("landgrab/autocomplete/receipts/report.html"))
        self.commit()
        catalog = self.catalog()
        self.assertEqual({tool["path"]: tool["role"] for tool in catalog["tools"]}, paths)
        self.assertEqual(catalog["counts"]["excluded_html_paths"], 1)
        self.assertEqual(catalog["unresolved"][0]["reason"], "excluded_provenance_target")
        metadata_tasks = [task for task in catalog["tasks"] if task["operation"] == "complete_metadata"]
        self.assertEqual([task["paths"] for task in metadata_tasks], [["apps/unique.html"]])
        self.assert_partition(catalog)

    def test_source_signals_are_boolean_static_evidence_not_quality_scores(self):
        self.write(
            "signals.html", page("Signals", '<script src="//cdn.example.org/lib.js"></script>'
                                 '<script src="./local.js"></script><!-- indexedDB; export -->'),
        )
        self.write("relative.html", page("Relative script", '<script src="local.js"></script>'))
        self.commit()
        catalog = self.catalog()
        tools = {tool["path"]: tool for tool in catalog["tools"]}
        self.assertEqual(tools["signals.html"]["signals"], {
            "local_persistence": True, "external_scripts": True, "import_export_mentions": True,
        })
        self.assertFalse(tools["relative.html"]["signals"]["external_scripts"])
        self.assertTrue(any("heuristics" in line for line in catalog["limitations"]))
        proposal = catalog["planning"]["extension"]["proposal_template"]
        self.assertEqual(proposal["base_commit"], catalog["repository"]["commit"])
        self.assertIn("nearest_ancestors", proposal)
        self.assertEqual(proposal["status"], "proposed")

    def test_missing_metadata_references_create_source_grounded_review_task(self):
        self.write_json("landgrab/index.json", {
            "apps": [{"path": path, "title": "Removed"} for path in ("removed.html", "also-removed.html")],
        })
        self.commit()
        catalog = self.catalog()
        self.assertEqual(len(catalog["tasks"]), 2)
        for task in catalog["tasks"]:
            self.assertEqual(task["operation"], "repair_metadata_reference")
            self.assertEqual(task["paths"], ["landgrab/index.json"])
        self.assertEqual(
            {task["evidence"]["entry_path"] for task in catalog["tasks"]},
            {"removed.html", "also-removed.html"},
        )
        self.assertEqual(len({task["id"] for task in catalog["tasks"]}), 2)

    def test_single_batch_process_handles_spaces_newlines_and_unicode_paths(self):
        paths = ("apps/with space.html", "apps/üñîçødé.html", "apps/line\nbreak.html")
        for index, path in enumerate(paths):
            self.write(path, page(f"Title {index}"))
        self.commit()
        real_popen = subprocess.Popen
        with patch("scripts.autocomplete_catalog.subprocess.Popen", wraps=real_popen) as popen:
            catalog = self.catalog()
        batch_calls = [call for call in popen.call_args_list if "--batch" in call.args[0]]
        tree_calls = [call for call in popen.call_args_list if "ls-tree" in call.args[0]]
        self.assertEqual(len(batch_calls), 1)
        self.assertEqual(len(tree_calls), 1)
        self.assertEqual({tool["path"] for tool in catalog["tools"]}, set(paths))
        self.assertTrue(all(" " not in tool["source_url"] and "\n" not in tool["source_url"] for tool in catalog["tools"]))

    def test_non_utf8_git_filename_bytes_are_preserved_without_reading_the_worktree(self):
        filename = b"raw-\xff.html".decode("utf-8", "surrogateescape")
        self.write("body-source.txt", page("Byte filename"))
        self.write("alias.html", refresh("raw-%ff.html"))
        body = self.git("hash-object", "-w", "body-source.txt")
        alias = self.git("hash-object", "-w", "alias.html")
        tree = self.git("mktree", "-z", input=(
            f"100644 blob {alias}\talias.html\0".encode()
            + f"100644 blob {body}\t".encode() + b"raw-\xff.html\0"
        ))
        commit = self.git("commit-tree", tree, "-m", "byte filename fixture")
        self.git("update-ref", "HEAD", commit)
        catalog = self.catalog()
        tool = catalog["tools"][0]
        self.assertEqual(tool["path"], filename)
        self.assertEqual(tool["aliases"], ["alias.html"])
        self.assertIn("raw-%FF.html", tool["source_url"])
        json.dumps(catalog, ensure_ascii=True).encode("utf-8")

    def test_cli_writes_valid_json_with_explicit_public_repository_metadata(self):
        self.write("app.html", page())
        self.write("alias.html", refresh("/tools/app.html"))
        self.git("remote", "add", "origin", "https://private-user:private-token@example.invalid/private/repo.git")
        commit = self.commit()
        output = self.case / "output/catalog.json"
        self.assertEqual(main([
            "--repo", str(self.repo), "--ref", commit, "--output", str(output),
            "--repository", "example/tools", "--site-url", "https://example.org/tools/",
            "--max-tasks", "1",
        ]), 0)
        serialized = output.read_text(encoding="utf-8")
        result = json.loads(serialized)
        self.assertEqual(result["repository"]["full_name"], "example/tools")
        self.assertEqual(result["repository"]["url"], "https://github.com/example/tools")
        self.assertEqual(result["tools"][0]["url"], "https://example.org/tools/app.html")
        self.assertEqual(result["tools"][0]["aliases"], ["alias.html"])
        self.assertNotIn("private-token", serialized)
        self.assertNotIn(str(self.repo.resolve()), serialized)
        self.assertNotIn(str(self.repo), serialized)
        self.assertEqual(len(result["tasks"]), 1)

    def test_cli_error_does_not_overwrite_existing_catalog_or_leak_local_paths(self):
        self.write("landgrab/index.json", "{invalid")
        self.commit()
        output = self.case / "catalog.json"
        output.write_text("previous catalog", encoding="utf-8")
        error = io.StringIO()
        with redirect_stderr(error), self.assertRaises(SystemExit) as status:
            main(["--repo", str(self.repo), "--output", str(output)])
        self.assertEqual(status.exception.code, 2)
        self.assertEqual(output.read_text(encoding="utf-8"), "previous catalog")
        self.assertIn("malformed", error.getvalue())
        self.assertNotIn(str(self.repo.resolve()), error.getvalue())

    def test_python_script_entrypoint_runs_with_only_stdlib(self):
        self.write("app.html", page())
        self.commit()
        output = self.case / "cli.json"
        result = subprocess.run(
            [
                sys.executable, "scripts/autocomplete_catalog.py",
                "--repo", str(self.repo), "--ref", "HEAD", "--output", str(output),
            ],
            stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False,
        )
        self.assertEqual(result.returncode, 0, result.stderr.decode("utf-8"))
        self.assertEqual(json.loads(output.read_text(encoding="utf-8"))["counts"]["canonical_tools"], 1)

    def test_invalid_ref_and_credentialed_repository_options_are_rejected(self):
        self.commit()
        with self.assertRaises(CatalogError):
            self.catalog(ref="not-a-commit")
        with self.assertRaises(CatalogError):
            self.catalog(ref="--all")
        for kwargs in (
            {"repository": "https://user:secret@github.com/example/tools"},
            {"site_url": "https://user:secret@example.org/tools/"},
            {"site_url": "https://example.org/tools/../other/"},
        ):
            with self.subTest(kwargs=kwargs), self.assertRaises(CatalogError):
                self.catalog(**kwargs)


if __name__ == "__main__":
    unittest.main()
