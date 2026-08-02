import unittest

from conventions.prime_edge_cumulant_v1 import kernel_ledger, signed_expansion, verify_all


class Cycle56PrimeEdgeCumulantTests(unittest.TestCase):
    def test_s3_expansion(self) -> None:
        data = kernel_ledger(3)
        self.assertEqual(data["term_count"], 8)
        self.assertEqual(data["coefficient_l1"], 16)
        self.assertEqual(data["coefficient_sum"], 0)

    def test_s4_expansion(self) -> None:
        data = kernel_ledger(4)
        self.assertEqual(data["term_count"], 10)
        self.assertEqual(data["coefficient_l1"], 32)
        self.assertEqual(data["coefficient_sum"], 0)

    def test_binomial_coefficients(self) -> None:
        first_half = signed_expansion(4)[:5]
        self.assertEqual([row["coefficient"] for row in first_half], [1, -4, 6, -4, 1])

    def test_kernel_properties(self) -> None:
        data = kernel_ledger(4)
        self.assertTrue(data["positive_semidefinite"])
        self.assertIn("E_(m,s)(0,g)", data["zero_edge"])

    def test_verification(self) -> None:
        self.assertIn("analytic_gate", verify_all())


if __name__ == "__main__":
    unittest.main()
