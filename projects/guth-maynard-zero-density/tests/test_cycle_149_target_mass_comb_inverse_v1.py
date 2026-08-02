import unittest
from fractions import Fraction

from conventions.target_mass_comb_inverse_v1 import (
    exponent_ledger,
    modulus_correlation_average,
    occupancy_ratio,
    relative_antialignment,
    theorem_record,
)


class TargetMassCombInverseTests(unittest.TestCase):
    def test_critical_occupancy(self) -> None:
        ratio = occupancy_ratio(
            endpoint_modes=Fraction(1, 10),
            all_modes=Fraction(1),
            q_over_n=Fraction(10),
        )
        self.assertEqual(ratio, 1)

    def test_power_excess_forces_half_power_alignment(self) -> None:
        self.assertEqual(
            relative_antialignment(
                full_budget_constant=1.0,
                comb_to_budget_ratio=16.0,
            ),
            0.25,
        )

    def test_modulus_witness_average(self) -> None:
        self.assertEqual(
            modulus_correlation_average(
                comb_norm_squared=100.0,
                endpoint_weight=10.0,
                relative_error=0.2,
            ),
            8.0,
        )

    def test_exponent_ledger(self) -> None:
        row = exponent_ledger(
            rho=Fraction(1, 5),
            endpoint_mode_exponent=Fraction(1, 2),
        )
        self.assertEqual(row["threshold_exponent"], Fraction(7, 15))
        self.assertEqual(row["comb_to_global_diagonal"], Fraction(1, 30))
        self.assertEqual(row["relative_antialignment_exponent"], Fraction(-1, 60))

    def test_record_retains_denominator_and_boundary(self) -> None:
        row = theorem_record()
        self.assertIn("R_C/D=N/Q", row["occupancy_threshold"])
        self.assertIn("denominator h", row["modulus_witness"])
        self.assertIn("not excluded", row["boundary"])


if __name__ == "__main__":
    unittest.main()
