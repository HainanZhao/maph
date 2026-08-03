from __future__ import annotations

import json
from pathlib import Path
import subprocess
import sys
import unittest


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "proof" / "verify_cycle_198_analytic_frequency_endpoint.py"


class Cycle198AnalyticFrequencyEndpointTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        completed = subprocess.run(
            [sys.executable, str(SCRIPT)],
            check=True,
            capture_output=True,
            text=True,
        )
        cls.result = json.loads(completed.stdout)

    def test_source_specialization_is_exact(self) -> None:
        checked = self.result["source_continuation"]["checked_parameters"]
        self.assertEqual(checked["p_times_r_plus_k_times_s"], 1)
        self.assertEqual(checked["phase_coefficient"], 437)
        self.assertFalse(
            self.result["source_continuation"][
                "added_entire_or_distributional_term_allowed"
            ]
        )

    def test_all_36_characters_are_distinct(self) -> None:
        ledger = self.result["characteristic_ledger"]
        self.assertEqual(ledger["row_count"], 36)
        self.assertEqual(ledger["test_space_dimension"], 36)
        self.assertEqual(
            ledger["distinct_continuous_discrete_character_count"], 36
        )

    def test_helical_dual_descent_recovers_every_characteristic(self) -> None:
        for row in self.result["characteristic_ledger"]["records"]:
            self.assertEqual(
                row["finite_frequency_recovered"], row["characteristic"]
            )
            self.assertEqual(
                4 * row["helical_integer_ell"]
                - row["raw_beta_discrete_mode"],
                row["centered_frequency_sigma"],
            )

    def test_all_frequency_factors_avoid_true_divisors(self) -> None:
        for row in self.result["characteristic_ledger"]["records"]:
            self.assertTrue(row["first_frequency_factor"]["finite_nonzero"])
            self.assertTrue(row["second_frequency_factor"]["finite_nonzero"])
            self.assertTrue(row["endpoint_value_finite_nonzero"])
        self.assertTrue(
            self.result["fixed_Gamma_M_Q_0"]["finite_nonzero"]
        )

    def test_zero_frequency_helical_labels_avoid_zero_discrete_label(self) -> None:
        ledger = self.result["characteristic_ledger"]
        self.assertEqual(ledger["zero_frequency_count"], 6)
        self.assertEqual(
            ledger["zero_frequency_N_mod_24"], [2, 6, 10, 14, 18, 22]
        )
        self.assertNotIn(0, ledger["zero_frequency_N_mod_24"])

    def test_claim_boundary_keeps_downstream_interfaces_open(self) -> None:
        self.assertFalse(
            self.result["endpoint_functional"]["ordinary_raw_contour_value"]
        )
        self.assertIn("helical/Zak periodization", self.result["gate_outcome"]["remaining_bottleneck"])
        self.assertIn("not the divergent raw endpoint integral", self.result["claim_boundary"])


if __name__ == "__main__":
    unittest.main()
