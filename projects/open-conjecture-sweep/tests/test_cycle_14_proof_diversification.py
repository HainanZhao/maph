"""Regression test for Cycle 14's structural audit."""

from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "proof"))
from check_cycle_14_proof_diversification import audit


class Cycle14ProofDiversificationTest(unittest.TestCase):
    def test_frozen_outcome(self) -> None:
        self.assertEqual(audit(False), {"census": 80, "certified": 16, "caps": 11, "role_groups_retained": 4, "final_clauses": 2329, "final_discriminating": 1180})


if __name__ == "__main__":
    unittest.main()
