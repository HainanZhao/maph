from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "proof"))
from check_cycle_42_h2_horn import audit


class Cycle42H2HornTest(unittest.TestCase):
    def test_exact_ambient_boundary(self):
        result = audit()
        self.assertEqual(result["status"], "PASS")
        self.assertEqual(result["nonzero_h2_q"], 3893)
        self.assertEqual(result["first_moment_filling_status"], "CONSISTENT")


if __name__ == "__main__":
    unittest.main()
