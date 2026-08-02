from fractions import Fraction as Q
import unittest

from conventions.cumulant_support_collapse_v1 import collapse_ledger, verify_all


class Cycle57CumulantSupportCollapseTests(unittest.TestCase):
    def test_s3(self) -> None:
        data = collapse_ledger(3, 5)
        self.assertEqual(data["fiber_bound_uniform_m_ge_2"], 12)
        self.assertEqual(data["raw_precollapse_energy"], 256)
        self.assertEqual(data["support_collapse_power_loss"], 0)

    def test_s4(self) -> None:
        data = collapse_ledger(4, 5)
        self.assertEqual(data["fiber_bound_uniform_m_ge_2"], 72)
        self.assertEqual(data["raw_precollapse_energy"], 1024)
        self.assertEqual(data["raw_collapsed_energy_upper"], 72 * 1024)

    def test_normalized_energy(self) -> None:
        data = collapse_ledger(3, 5)
        self.assertEqual(data["normalized_precollapse_energy"], Q(4, 5) ** 4)
        self.assertEqual(data["normalized_collapsed_energy_upper"], 12 * Q(4, 5) ** 4)

    def test_uniform_status(self) -> None:
        data = verify_all()
        self.assertEqual(data["s4"]["status"], "CONSTANT_COST")
        self.assertIn("every m>=2", data["uniform_statement"])


if __name__ == "__main__":
    unittest.main()
