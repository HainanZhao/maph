from fractions import Fraction as Q
import unittest

from conventions.coordinatewise_bessel_ledger_v1 import amplifier_ledger, exposure_row, verify_all


class Cycle54CoordinatewiseBesselLedgerTests(unittest.TestCase):
    def test_penultimate_with_q_saving(self) -> None:
        for s in (3, 4):
            row = exposure_row(s, s - 1, True)
            self.assertEqual(row["signed_gap_trigger_minus_selected"], Q(3, 50))
            self.assertEqual(row["status"], "MISSES_STRICT_TRIGGER")

    def test_full_exposure_with_q_saving(self) -> None:
        for s in (3, 4):
            row = exposure_row(s, s, True)
            self.assertEqual(row["signed_gap_trigger_minus_selected"], -Q(47, 50))
            self.assertEqual(row["status"], "TRIGGERS")

    def test_without_q_saving(self) -> None:
        for s in (3, 4):
            self.assertEqual(exposure_row(s, s - 1, False)["signed_gap_trigger_minus_selected"], Q(1, 5))
            self.assertEqual(exposure_row(s, s, False)["signed_gap_trigger_minus_selected"], -Q(4, 5))

    def test_outcomes(self) -> None:
        for s in (3, 4):
            data = amplifier_ledger(s)
            self.assertEqual(data["first_trigger_with_q_saving"], s)
            self.assertEqual(data["outcome"], "FULL_ORDINARY_EXPOSURE_NECESSARY")
        self.assertIn("s4", verify_all())


if __name__ == "__main__":
    unittest.main()
