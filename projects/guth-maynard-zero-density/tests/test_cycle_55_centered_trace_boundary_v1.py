from fractions import Fraction as Q
import unittest

from conventions.centered_trace_boundary_v1 import exponent_ledger, simplex_certificate, verify_all


class Cycle55CenteredTraceBoundaryTests(unittest.TestCase):
    def test_strictly_below_trigger(self) -> None:
        data = simplex_certificate(5, Q(1, 10))
        self.assertEqual(data["R_rho"], Q(1, 2))
        self.assertEqual(data["residual_gram_eigenvalue_constant_direction"], Q(1, 2))
        self.assertEqual(data["all_even_centered_traces"], 0)

    def test_endpoint(self) -> None:
        data = simplex_certificate(5, Q(1, 5))
        self.assertEqual(data["R_rho"], 1)
        self.assertEqual(data["residual_gram_eigenvalue_constant_direction"], 0)
        self.assertEqual(data["centered_gram"], "0_R")

    def test_penultimate_exponent(self) -> None:
        data = exponent_ledger()
        self.assertEqual(data["trigger_minus_selected_exponent"], Q(3, 50))
        self.assertEqual(data["R_rho_exponent"], -Q(3, 50))
        self.assertEqual(data["status"], "ABSTRACTLY_SHARP")

    def test_invalid_above_trigger(self) -> None:
        with self.assertRaises(RuntimeError):
            simplex_certificate(5, Q(1, 4))

    def test_verification(self) -> None:
        self.assertIn("endpoint_example", verify_all())


if __name__ == "__main__":
    unittest.main()
