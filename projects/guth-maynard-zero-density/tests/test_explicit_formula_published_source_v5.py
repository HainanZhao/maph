import json
from pathlib import Path
import subprocess
import sys
import unittest


PROJECT = Path(__file__).resolve().parents[1]


class ExplicitFormulaPublishedSourceV5Tests(unittest.TestCase):
    def test_published_item_and_theorem_scope(self) -> None:
        data = json.loads((PROJECT / "artifacts/cycle-2-stream-c-explicit-formula-published-source-v5.json").read_text())
        self.assertEqual(data["epistemic_status"], "PROVED")
        self.assertEqual(data["published_item"]["dspace_entity_type"], "Publication")
        self.assertEqual(data["published_item"]["dc_type"], "Learning Object")
        self.assertFalse(data["published_item"]["withdrawn"])
        self.assertIn("no assertion of journal", data["published_item"]["scope"])
        self.assertIn("x>=2 and T>0", data["published_theorem"]["hypotheses_checked"])

    def test_replay(self) -> None:
        subprocess.run([sys.executable, str(PROJECT / "proof/check_explicit_formula_published_source_v5.py"), "--check"], cwd=PROJECT, check=True)


if __name__ == "__main__":
    unittest.main()
