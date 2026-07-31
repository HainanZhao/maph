from __future__ import annotations

from pathlib import Path
import subprocess
import unittest


ROOT = Path(__file__).resolve().parents[1]


class CensusPaperManuscriptTest(unittest.TestCase):
    def test_compiled_manuscript_matches_frozen_artifacts(self):
        completed = subprocess.run(
            ["python3", "scripts/audit_census_paper.py"],
            cwd=ROOT,
            text=True,
            capture_output=True,
            check=False,
            timeout=60,
        )
        self.assertEqual(completed.returncode, 0, completed.stderr)
        self.assertIn("CENSUS_PAPER_AUDIT=PASS", completed.stdout)


if __name__ == "__main__":
    unittest.main()
