from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "proof"))
from check_cycle_44_nonanchor import audit


class Cycle44NonanchorTest(unittest.TestCase):
    def test_cone_or_acyclic_holdout(self):
        result = audit()
        self.assertEqual(result["status"], "PASS")
        self.assertEqual(result["selected_interfaces"], 2_000)
        self.assertEqual(result["canonical_failures"], 0)


if __name__ == "__main__":
    unittest.main()
