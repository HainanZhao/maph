from fractions import Fraction as Q
import unittest

from conventions.farey_packet_transport_v1 import packet_ledger, verify_all


class Cycle64FareyPacketTransportTests(unittest.TestCase):
    def test_uniqueness_margins(self) -> None:
        data = packet_ledger()
        self.assertEqual(data["window_smaller_than_farey_gap_margin"], Q(3, 25))
        self.assertEqual(data["window_smaller_than_curve_gap_margin"], Q(2, 5))
        self.assertTrue(data["unique_reduced_approximant_per_ell"])
        self.assertTrue(data["unique_ell_per_reduced_approximant"])

    def test_packet_target(self) -> None:
        data = packet_ledger()
        self.assertEqual(data["packet_weight_prefactor_exponent"], Q(22, 25))
        self.assertEqual(data["harmonic_packet_mass_target_open"], -Q(1, 5))

    def test_random_scale(self) -> None:
        data = packet_ledger()
        self.assertEqual(data["random_harmonic_packet_mass_exponent"], -Q(2, 5))
        self.assertEqual(data["random_margin_to_target"], Q(1, 5))

    def test_multiple_bound(self) -> None:
        self.assertIn("H^2/(2q)", packet_ledger()["weighted_multiples_upper"])

    def test_verification(self) -> None:
        self.assertIn("low_denominator_recurrence", verify_all()["analytic_gate"])


if __name__ == "__main__":
    unittest.main()
