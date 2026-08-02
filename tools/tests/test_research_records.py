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
            self.assertEqual(con.execute("SELECT count(*) FROM artifacts").fetchone()[0], 250)
            self.assertEqual(
                con.execute("SELECT status FROM artifacts WHERE cycle_number = 151").fetchone()[0],
                "SEALED_GCD_WEIGHTED_NEGATIVE_TAIL_LOBE_OR_BOUNDARY_OPEN",
            )
            self.assertEqual(research_records.check(con), 0)
            con.close()
