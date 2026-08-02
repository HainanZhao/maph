import unittest

from conventions.k_stationary_correction_v1 import symbolic_correction, theorem_record


class KStationaryCorrectionTests(unittest.TestCase):
    def test_exact_phase_derivatives(self) -> None:
        row = symbolic_correction()
        self.assertEqual(row["stationary_point"], "k*=c*Delta/m")
        self.assertIn("c*c0*Delta/m", row["stationary_value"])
        self.assertIn("constant", row["anchor_location"])

    def test_containment(self) -> None:
        row = theorem_record()
        self.assertIn("Cycle 108", row["corrected_record"])
        self.assertIn("ell^(-3/2)", row["unaffected"])
        self.assertIn("cutoff", row["reaudit_required"])


if __name__ == "__main__":
    unittest.main()
