"""Regression test for Cycle 19's corrected cap boundary."""

from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "proof"))
from check_cycle_19_symbolic_antichain import audit


class Cycle19SymbolicAntichainTest(unittest.TestCase):
    def test_corrected_boundary(self) -> None:
        result = audit()
        self.assertEqual(result["aggregate_wall_caps"], 76)
        self.assertEqual(result["sentinel_label_corrections"], 3)
        self.assertEqual(result["certified"], 0)


if __name__ == "__main__":
    unittest.main()
