import unittest

from proof.verify_polynomial_tt_grid_cores import verify


class PolynomialTTGridCoreTests(unittest.TestCase):
    def test_direct_core_smoke_against_spin_reference(self):
        result = verify(smoke=True)
        self.assertTrue(result["no_final_tensor_factorization"])
        self.assertTrue(
            all(row["direct_core_matches_independent_reference"] for row in result["rows"])
        )


if __name__ == "__main__":
    unittest.main()

