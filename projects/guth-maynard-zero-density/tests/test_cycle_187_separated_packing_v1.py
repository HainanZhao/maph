import unittest

from conventions.separated_packing_v1 import separated_critical_occupancy, verify_all


class Cycle187SeparatedPackingTest(unittest.TestCase):
    def test_exact_separated_critical_ledger(self) -> None:
        ledger = separated_critical_occupancy(1)
        self.assertGreater(ledger["support"]["minimum_pairwise_separation"], ledger["parameters"]["T"])
        self.assertGreaterEqual(8 * ledger["mass"]["ordered_cross_mass"], ledger["mass"]["critical_target"])
        self.assertLess(ledger["support"]["ambient_upper"], ledger["parameters"]["Delta"])

    def test_replay_boundary(self) -> None:
        self.assertIn("no actual exponential phase assignment", verify_all()["boundary"])


if __name__ == "__main__":
    unittest.main()
