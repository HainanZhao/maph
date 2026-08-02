import unittest

from conventions.coefficient_projection_inverse_v1 import projection_ledger, verify_all


class Cycle61CoefficientProjectionInverseTests(unittest.TestCase):
    def test_s3(self) -> None:
        data = projection_ledger(3)
        self.assertEqual(data["fiber_bound"], 12)
        self.assertEqual(data["proper_anova_component_count"], 15)

    def test_s4(self) -> None:
        data = projection_ledger(4)
        self.assertEqual(data["fiber_bound"], 72)
        self.assertEqual(data["proper_anova_component_count"], 31)

    def test_factorization(self) -> None:
        data = projection_ledger(4)
        self.assertEqual(data["hilbert_synthesis"], "A=C B")
        self.assertIn("D_s", data["bessel_statement"])

    def test_marginals(self) -> None:
        data = projection_ledger(4)
        self.assertIn("k(mh_e)", data["powered_coordinate_marginal"])
        self.assertIn("k(h_e)", data["ordinary_coordinate_marginal"])

    def test_verification(self) -> None:
        self.assertIn("inverse_gate", verify_all())


if __name__ == "__main__":
    unittest.main()
