"""Refusal witnesses for the public evidence projection gate."""

import copy
import importlib.util
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "autocomplete_release_gate", ROOT / "scripts/check_autocomplete.py"
)
GATE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(GATE)


class EvidenceProjectionTests(unittest.TestCase):
    def setUp(self):
        self.expected = {
            "schema": "localfirst-autocomplete-evidence/v1",
            "generated_at": "2026-09-05T00:00:00.000Z",
            "counts": {"streams": 1, "frames": 1, "artifacts": 1},
            "reference": {"commit": "a" * 40},
            "events": [{
                "frame_hash": "b" * 64,
                "outcome": "checks_failed",
                "summary": "A controlled failed attempt.",
                "checks": [{"argv": ["example"], "exit_code": 1}],
                "artifacts": [{"path": "example.py", "sha256": "c" * 64, "bytes": 7}],
            }],
        }

    def test_projection_time_can_change_without_changing_recorded_events(self):
        published = copy.deepcopy(self.expected)
        published["generated_at"] = "2026-09-06T00:00:00.000Z"
        GATE.verify_index_projection(published, self.expected)

    def test_authentic_frame_hash_does_not_authorize_a_changed_outcome(self):
        published = copy.deepcopy(self.expected)
        published["events"][0]["outcome"] = "checks_passed"
        with self.assertRaisesRegex(ValueError, "verified frame payloads"):
            GATE.verify_index_projection(published, self.expected)

    def test_mutated_check_results_artifact_hashes_and_claims_are_refused(self):
        mutations = [
            lambda value: value["events"][0]["checks"][0].update(exit_code=0),
            lambda value: value["events"][0]["artifacts"][0].update(sha256="d" * 64),
            lambda value: value["events"][0]["artifacts"][0].update(path="different.py"),
            lambda value: value["events"][0].update(summary="Everything succeeded."),
            lambda value: value["events"][0].update(first_invention_proven=True),
            lambda value: value["reference"].update(commit="e" * 40),
        ]
        for mutate in mutations:
            with self.subTest(mutation=mutations.index(mutate)):
                published = copy.deepcopy(self.expected)
                mutate(published)
                with self.assertRaises(ValueError):
                    GATE.verify_index_projection(published, self.expected)

    def test_event_fields_are_compared_directly_with_the_verified_frame(self):
        payload = {
            "run_id": "run", "worker": "worker", "phase": "implementation",
            "outcome": "checks_failed", "summary": "Controlled projection fixture",
            "artifacts": [], "checks": [{"exit_code": 1}], "references": [],
            "repository": {"base_commit": "a" * 40},
            "changed_artifacts": [], "base_commit_unchanged": True,
        }
        envelope = {
            "utc": "2026-09-05T00:00:00.000Z", "stream_id": "fixture-stream",
            "seq": 0, "payload_hash": "b" * 64, "frame_hash": "c" * 64,
        }
        frame = {"payload": payload, **envelope}
        event = {**copy.deepcopy(payload), **envelope, "path": "runs/run/worker/frames/0.json"}
        GATE.verify_event_projection(event, frame, event["path"])
        event["outcome"] = "checks_passed"
        with self.assertRaisesRegex(ValueError, "payload field: outcome"):
            GATE.verify_event_projection(event, frame, event["path"])


if __name__ == "__main__":
    unittest.main()
