from fractions import Fraction as Q
import unittest

from conventions.primitive_poisson_contract_v1 import scale_contract, verify_all


class Cycle66PrimitivePoissonContractTests(unittest.TestCase):
    def test_scale_invariant_raw_target(self) -> None:
        for theta, kappa in ((Q(11, 25), Q(0)), (Q(1, 5), Q(6, 25)), (Q(0), Q(0))):
            self.assertEqual(
                scale_contract(theta, kappa)["raw_off_diagonal_target_exponent_open"],
                Q(31, 25),
            )

    def test_diagonal_margin(self) -> None:
        row = scale_contract(Q(11, 25), Q(0))
        self.assertEqual(row["diagonal_exponent"], Q(1, 25))
        self.assertEqual(row["diagonal_margin_to_target"], Q(1, 5))

    def test_deep_scale(self) -> None:
        row = scale_contract(Q(1, 5), Q(6, 25))
        self.assertTrue(row["admissible"])
        self.assertEqual(row["packet_count_target_exponent_open"], Q(0))
        self.assertEqual(row["diagonal_exponent"], -Q(11, 25))

    def test_frequency_ceiling(self) -> None:
        self.assertEqual(
            scale_contract(Q(11, 25), Q(0))["frequency_ceiling_exponent"],
            Q(36, 25),
        )

    def test_verification(self) -> None:
        rows = verify_all()
        self.assertIn("Mobius-Poisson", rows["analytic_gate"])
        self.assertIn("mu(b)", rows["identity"]["primitive_form"])


if __name__ == "__main__":
    unittest.main()
