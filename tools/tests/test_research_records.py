from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from tools import research_records


REPOSITORY_ROOT = Path(__file__).resolve().parents[2]
GUTH_PROFILE = REPOSITORY_ROOT / "projects/guth-maynard-zero-density/research-records.json"


class ResearchRecordsTest(unittest.TestCase):
    def test_standard_profile_rebuilds_and_validates(self) -> None:
        research_records.configure(GUTH_PROFILE)
        with tempfile.TemporaryDirectory() as temporary:
            database = Path(temporary) / "index.duckdb"
            research_records.rebuild(database)
            con = research_records.duckdb.connect(str(database), read_only=True)
            expected_count = len(list(GUTH_PROFILE.parent.glob("artifacts/cycle-*.json")))
            self.assertEqual(con.execute("SELECT count(*) FROM artifacts").fetchone()[0], expected_count)
            self.assertEqual(
                con.execute("SELECT status FROM artifacts WHERE cycle_number = 151").fetchone()[0],
                "SEALED_GCD_WEIGHTED_NEGATIVE_TAIL_LOBE_OR_BOUNDARY_OPEN",
            )
            status = research_records.render_status(con)
            self.assertIn("## Cold-start handoff", status)
            self.assertIn("No improved zero-density coefficient", status)
            self.assertIn("## Latest sealed record", status)
            self.assertIn("research cycle 63", status)
            self.assertIn("diagonal-aware direct triple census", status)
            self.assertEqual(research_records.check(con), 0)
            con.close()

    def test_top_level_claim_prefers_claim_boundary(self) -> None:
        rows = list(
            research_records.tagged_claims(
                {"epistemic_status": "PROVED", "claim_boundary": "concise boundary"}
            )
        )
        self.assertEqual(rows, [("artifact", "PROVED", "concise boundary")])
