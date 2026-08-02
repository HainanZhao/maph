"""Regression tests for the rebuildable cycle-record index."""

from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

import research_index


class ResearchIndexTest(unittest.TestCase):
    def test_rebuild_imports_every_cycle_artifact_and_validates_evidence(self) -> None:
        with tempfile.TemporaryDirectory() as tempdir:
            database = Path(tempdir) / "index.duckdb"
            research_index.rebuild(database)
            con = research_index.duckdb.connect(str(database), read_only=True)
            self.assertEqual(
                con.execute("SELECT count(*) FROM artifacts").fetchone()[0],
                len(research_index.artifact_paths()),
            )
            self.assertEqual(
                con.execute("SELECT count(*) FROM evidence JOIN artifacts USING (artifact_id) WHERE cycle_number >= 90 AND (NOT exists_now OR sha256_matches IS NOT TRUE)").fetchone()[0],
                0,
            )
            latest = con.execute("SELECT status FROM artifacts WHERE cycle_number = 151").fetchone()[0]
            self.assertEqual(latest, "SEALED_GCD_WEIGHTED_NEGATIVE_TAIL_LOBE_OR_BOUNDARY_OPEN")
            rendered = research_index.render_status(con)
            self.assertIn("Artifacts by top-level epistemic status", rendered)
            self.assertIn("not independent claims", rendered)
            self.assertEqual(research_index.check(con), 0)
            con.close()


if __name__ == "__main__":
    unittest.main()
