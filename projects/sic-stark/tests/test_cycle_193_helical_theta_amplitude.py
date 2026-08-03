from __future__ import annotations

import json
from pathlib import Path
import subprocess
import sys
import unittest


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "proof" / "verify_cycle_193_helical_theta_amplitude.py"


class Cycle193HelicalThetaAmplitudeTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        completed = subprocess.run(
            [sys.executable, str(SCRIPT)],
            check=True,
            capture_output=True,
            text=True,
        )
        cls.result = json.loads(completed.stdout)

    def test_continuous_theta_transport_retains_exact_closure(self) -> None:
        theta = self.result["continuous_theta_preservation"]
        self.assertEqual(theta["epistemic_status"], "PROVED")
        self.assertEqual(theta["finite_fibre_dimension"], 18)
        self.assertTrue(theta["F24_preserves_finite_fibre"])
        self.assertTrue(theta["p1_boundary_twisted_three_shift_retained"])
        self.assertIn("OPEN", theta["kernel_domain_status"])

    def test_projection_loses_only_the_declared_odd_pairs(self) -> None:
        projection = self.result["fibre_projection"]
        self.assertEqual(projection["odd_pair_count"], 6)
        self.assertEqual(
            projection["Pi_V_loses_odd_antisymmetric_subspace_dimension"],
            6,
        )
        self.assertEqual(
            projection["projection_records"][1]["Pi_V_of_e_N"],
            {"1": "1/2", "13": "1/2"},
        )
        self.assertEqual(
            projection["projection_records"][2]["Pi_V_of_e_N"],
            {"2": 1},
        )

    def test_divisor_witnesses_separate_every_pair(self) -> None:
        divisors = self.result["beta_divisor_separation"]
        self.assertTrue(
            divisors["all_twelve_N_vs_N_plus_12_pairs_distinct"]
        )
        records = divisors["pair_divisor_records"]
        self.assertEqual(len(records), 12)
        self.assertTrue(
            all(record["R_N"]["has_true_pole"] for record in records)
        )
        self.assertTrue(
            all(
                record["R_N_plus_12"]["is_finite_nonzero"]
                for record in records
            )
        )

    def test_obstruction_is_scoped_and_reaches_all_odd_rows(self) -> None:
        coverage = self.result["all36_coverage"]
        obstruction = self.result["scoped_amplitude_obstruction"]
        self.assertEqual(coverage["odd_characteristic_count"], 18)
        self.assertTrue(coverage["all_12_odd_labels_appear"])
        self.assertEqual(obstruction["affected_characteristics"], 18)
        self.assertIn("larger fibre", obstruction["does_not_exclude"][0])


if __name__ == "__main__":
    unittest.main()
