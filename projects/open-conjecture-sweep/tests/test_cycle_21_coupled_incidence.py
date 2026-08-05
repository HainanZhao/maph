"""Regression test for Cycle 21 direct-CNF certificate replay."""

from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "proof"))
from check_cycle_21_coupled_incidence import audit


class Cycle21CoupledIncidenceTest(unittest.TestCase):
    def test_direct_cnf_replay(self) -> None:
        result = audit()
        self.assertEqual(result["status"], "PASS")
        self.assertEqual(result["certified_leaves"], 15)
        self.assertGreaterEqual(result["minimum_exact_margin"], 1)


if __name__ == "__main__":
    unittest.main()
