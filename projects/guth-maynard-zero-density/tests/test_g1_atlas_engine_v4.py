"""Promotion-firewall regressions for G1 v4 and its adjudicator."""
from __future__ import annotations

from pathlib import Path
import sys
import tempfile
import unittest


PROJECT = Path(__file__).resolve().parents[1]
if str(PROJECT) not in sys.path:
    sys.path.insert(0, str(PROJECT))

from discovery import adjudicate_g1_atlas_v4 as adjudicator  # noqa: E402
from discovery import run_g1_atlas_v4 as engine  # noqa: E402


class G1AtlasEngineV4Tests(unittest.TestCase):
    def test_integrity_and_unverified_output_boundary(self) -> None:
        report = engine.integrity_report()
        self.assertEqual(report["production_mode"], "fresh checkpoint only; no resume")
        self.assertEqual(report["per_run_status"], "UNVERIFIED_PENDING_SECOND_FRESH_RUN")
        base = {"artifact_id": "v3", "correction": {}}
        output = engine.decorate_observations(base)
        self.assertFalse(output["promotion_boundary"]["promotion_allowed"])
        self.assertEqual(output["promotion_boundary"]["status"], "UNVERIFIED_PENDING_SECOND_FRESH_RUN")

    def test_fresh_production_rejects_existing_checkpoint(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            checkpoint = Path(directory) / "existing.json"
            checkpoint.write_text("existing", encoding="utf-8")
            with self.assertRaisesRegex(RuntimeError, "must be a new path"):
                engine.prepare_fresh_checkpoint(checkpoint, "A")

    def test_cached_assembly_alone_cannot_promote(self) -> None:
        cached_only = [{
            "label": "A", "fresh": False, "checkpoint": "/a",
            "observations": "/oa", "observations_sha256": "1" * 64,
        }]
        with self.assertRaisesRegex(RuntimeError, "exactly two fresh runs"):
            adjudicator.require_two_fresh_runs(cached_only)

    def test_structurally_plausible_tampered_second_run_cannot_promote(self) -> None:
        runs = [
            {"label": "A", "fresh": True, "checkpoint": "/a", "observations": "/oa", "observations_sha256": "1" * 64},
            {"label": "B", "fresh": True, "checkpoint": "/b", "observations": "/ob", "observations_sha256": "2" * 64},
        ]
        with self.assertRaisesRegex(RuntimeError, "not byte-identical"):
            adjudicator.require_two_fresh_runs(runs)

    def test_two_distinct_fresh_matching_records_pass_boundary(self) -> None:
        digest = "3" * 64
        runs = [
            {"label": "A", "fresh": True, "checkpoint": "/a", "observations": "/oa", "observations_sha256": digest},
            {"label": "B", "fresh": True, "checkpoint": "/b", "observations": "/ob", "observations_sha256": digest},
        ]
        adjudicator.require_two_fresh_runs(runs)

    def test_adjudicator_is_separate_standard_library_program(self) -> None:
        source = (PROJECT / "discovery/adjudicate_g1_atlas_v4.py").read_text(encoding="utf-8")
        self.assertNotIn("from discovery import", source)
        self.assertNotIn("import mpmath", source)


if __name__ == "__main__":
    unittest.main()
