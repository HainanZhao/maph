from fractions import Fraction as Q
import unittest

from conventions.strict_hybrid_margin_correction_v1 import adjusted_gap, verify_all


class Cycle58StrictHybridMarginCorrectionTests(unittest.TestCase):
    def test_hybrid_tie(self) -> None:
        data = adjusted_gap(Q(3, 50), True)
        self.assertEqual(data["adjusted_trigger_minus_selected"], 0)
        self.assertEqual(data["status"], "TIES_NO_TRIGGER")

    def test_hybrid_strict_surplus(self) -> None:
        data = adjusted_gap(Q(61, 1000), True)
        self.assertEqual(data["adjusted_trigger_minus_selected"], -Q(1, 1000))
        self.assertEqual(data["status"], "STRICTLY_TRIGGERS")

    def test_powered_tie(self) -> None:
        data = adjusted_gap(Q(1, 5), False)
        self.assertEqual(data["status"], "TIES_NO_TRIGGER")

    def test_verification(self) -> None:
        data = verify_all()
        self.assertIn("gamma>3/50", data["corrected_hybrid_target"])
        self.assertIn("gamma_q>1/5", data["corrected_powered_target"])


if __name__ == "__main__":
    unittest.main()
