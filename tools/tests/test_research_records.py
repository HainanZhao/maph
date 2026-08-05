from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from tools import research_records


REPOSITORY_ROOT = Path(__file__).resolve().parents[2]
GUTH_PROFILE = REPOSITORY_ROOT / "projects/guth-maynard-zero-density/research-records.json"
SIC_STARK_PROFILE = REPOSITORY_ROOT / "projects/sic-stark/research-records.json"


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
            self.assertIn("## Start here", status)
            self.assertIn("Strategic state, claim boundary, active gate, and deferred work: `PROGRAM.md`", status)
            self.assertIn("## Current evidence", status)
            self.assertIn("research cycle 63", status)
            self.assertIn("Newest immutable record", status)
            self.assertNotIn("## Recent sealed records", status)
            self.assertNotIn("- Boundary:", status)
            self.assertEqual(research_records.check(con), 0)
            con.close()

    def test_top_level_claim_prefers_claim_boundary(self) -> None:
        rows = list(
            research_records.tagged_claims(
                {"epistemic_status": "PROVED", "claim_boundary": "concise boundary"}
            )
        )
        self.assertEqual(rows, [("artifact", "PROVED", "concise boundary")])

    def test_profile_can_omit_generated_status(self) -> None:
        research_records.configure(SIC_STARK_PROFILE)
        self.assertIsNone(research_records.STATUS)
        with tempfile.TemporaryDirectory() as temporary:
            database = Path(temporary) / "index.duckdb"
            research_records.rebuild(database)
            con = research_records.duckdb.connect(str(database), read_only=True)
            self.assertIn("Newest immutable record", research_records.render_status(con))
            self.assertEqual(research_records.check(con), 0)
            con.close()
