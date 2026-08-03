from __future__ import annotations

import json
from pathlib import Path
import subprocess
import sys
import unittest


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "proof" / "verify_cycle_195_finite_anti_residue_sum.py"


class Cycle195FiniteAntiResidueSumTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        completed = subprocess.run(
            [sys.executable, str(SCRIPT)], check=True, capture_output=True, text=True
        )
        cls.result = json.loads(completed.stdout)

    def test_corrected_true_pole_census_is_used(self) -> None:
        census = self.result["corrected_input"]
        self.assertEqual(census["orbit_cardinalities"], [2, 4, 6, 8, 10, 12])
        self.assertEqual(census["total_true_pole_summands"], 42)

    def test_all_six_finite_sums_have_unit_constant_term(self) -> None:
        combined = self.result["finite_combined_residues"]
        self.assertTrue(combined["all_six_finite_combined_residues_meromorphically_nonzero"])
        self.assertEqual(combined["constant_coefficient_vector"], [1] * 6)
        self.assertEqual(combined["maximum_q_adic_order"], 66)
        for record in combined["records"]:
            self.assertTrue(record["finite_combined_residue_meromorphically_nonzero"])
            self.assertFalse(record["all_point_nonvanishing_claimed"])
            self.assertFalse(record["endpoint_continuation_claimed"])

    def test_q_orders_are_strictly_positive_after_the_base_term(self) -> None:
        for record in self.result["finite_combined_residues"]["records"]:
            orders = record["cumulative_q_adic_orders"]
            self.assertEqual(orders, sorted(set(orders)))
            self.assertTrue(all(order > 0 for order in orders))
            increments = [
                row["q_adic_increment"] for row in record["source_multiplier_records"]
            ]
            self.assertEqual(increments, list(range(1, record["canonical_odd_N"] + 1)))


if __name__ == "__main__":
    unittest.main()
