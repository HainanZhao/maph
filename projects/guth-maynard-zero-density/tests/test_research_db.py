"""Tests for the reusable research database interface."""

from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

import research_db
import research_index


class ResearchDBTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.tempdir = tempfile.TemporaryDirectory()
        cls.database = Path(cls.tempdir.name) / "index.duckdb"
        research_index.rebuild(cls.database)

    @classmethod
    def tearDownClass(cls) -> None:
        cls.tempdir.cleanup()

    def test_common_queries(self) -> None:
        with research_db.ResearchDB(self.database, rebuild_if_missing=False) as db:
            self.assertEqual(db.summary()["artifact_files"], len(research_index.artifact_paths()))
            self.assertEqual(db.artifact(151)[0]["artifact_id"], "cycle-151-sampled-comb-double-poisson-v1")
            self.assertTrue(db.recent(3))
            self.assertTrue(db.gates("NEGATIVE_TAIL"))
            self.assertTrue(db.claims("negative lobe", tag="PROVED", limit=5))
            self.assertTrue(db.dependencies("cycle-151-sampled-comb-double-poisson-v1"))
            self.assertTrue(db.evidence("cycle-151-sampled-comb-double-poisson-v1"))

    def test_read_only_sql(self) -> None:
        with research_db.ResearchDB(self.database, rebuild_if_missing=False) as db:
            rows = db.query("SELECT max(cycle_number) AS latest FROM artifacts")
            self.assertEqual(rows, [{"latest": 151}])


if __name__ == "__main__":
    unittest.main()
