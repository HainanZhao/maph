from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "proof"))
from check_cycle_45_morse import audit


class Cycle45MorseTest(unittest.TestCase):
    def test_critical_projection_boundary(self):
        result = audit()
        self.assertEqual(result["status"], "PASS")
        self.assertEqual(result["actual_interfaces"], 5_954)
        self.assertEqual(result["initial_nonzero_projections"], 470)
        self.assertEqual(result["signature_nonboundary_models"], 649)


if __name__ == "__main__":
    unittest.main()
