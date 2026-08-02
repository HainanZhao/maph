from fractions import Fraction as Q
import unittest

from conventions.hs_joint_sieve_v1 import joint_ledger, verify_all, wrap_exponent


class Cycle48HSJointSieveTests(unittest.TestCase):
    def test_wrap_piecewise_transition(self) -> None:
        self.assertEqual(wrap_exponent(Q(1, 10)), Q(1, 10))
        self.assertEqual(wrap_exponent(Q(1, 5)), Q(1, 5))
        self.assertEqual(wrap_exponent(Q(11, 25)), Q(8, 25))

    def test_keep_both_large_sieve_terms(self) -> None:
        row = joint_ledger(Q(11, 25))
        self.assertEqual(row["energy_direct"], Q(58, 25))
        self.assertEqual(row["energy_spacing"], Q(37, 25))
        self.assertGreater(row["energy_direct"], row["energy_spacing"])

    def test_endpoint_saving(self) -> None:
        row = joint_ledger(Q(11, 25))
        self.assertEqual(row["joint"], Q(73, 50))
        self.assertEqual(row["saving"], Q(7, 50))

    def test_comparisons(self) -> None:
        comparisons = verify_all()["comparisons"]
        self.assertEqual(comparisons["gain_over_cycle45"], Q(3, 50))
        self.assertEqual(comparisons["gap_to_full_missing"], Q(1, 50))


if __name__ == "__main__":
    unittest.main()
