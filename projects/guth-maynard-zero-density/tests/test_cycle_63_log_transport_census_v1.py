from fractions import Fraction as Q
import unittest

from conventions.log_transport_census_v1 import transport_ledger, verify_all


class Cycle63LogTransportCensusTests(unittest.TestCase):
    def test_total_targets(self) -> None:
        data = transport_ledger()
        self.assertEqual(data["summed_pointwise_census"], Q(19, 25))
        self.assertEqual(data["desired_total_census_open_endpoint"], Q(16, 25))
        self.assertEqual(data["saving_beyond_summed_hs_required"], Q(3, 25))

    def test_geometry(self) -> None:
        data = transport_ledger()
        self.assertEqual(data["hessian_determinant_exponent"], -Q(6, 5))
        self.assertIn("negative", "negative square")

    def test_pair_targets(self) -> None:
        data = transport_ledger()
        self.assertEqual(data["desired_pair_census_open_endpoint"], Q(17, 25))
        self.assertEqual(data["crude_hs_pair_census"], Q(6, 5))
        self.assertEqual(data["random_difference_pair_volume"], Q(12, 25))

    def test_random_volume(self) -> None:
        self.assertEqual(transport_ledger()["random_volume_census"], Q(1, 25))

    def test_verification(self) -> None:
        self.assertIn("pair_census", verify_all()["analytic_gate"])


if __name__ == "__main__":
    unittest.main()
