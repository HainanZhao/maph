from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "proof"))
from check_cycle_43_moment_h2 import audit


class Cycle43MomentH2Test(unittest.TestCase):
    def test_selected_canonical_coupling(self):
        result = audit()
        self.assertEqual(result["status"], "PASS")
        self.assertEqual(result["canonical_fills"], 3954)
        self.assertEqual(result["canonical_failures"], 0)


if __name__ == "__main__":
    unittest.main()
