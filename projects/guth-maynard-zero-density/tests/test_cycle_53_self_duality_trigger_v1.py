from fractions import Fraction as Q
import unittest

from conventions.self_duality_trigger_v1 import trigger_ledger, verify_all


class Cycle53SelfDualityTriggerTests(unittest.TestCase):
    def test_s3(self) -> None:
        row = trigger_ledger(3)
        self.assertEqual(row["selected_r_plus_2v"], Q(29, 5))
        self.assertEqual(row["trigger_gap"], Q(11, 5))

    def test_s4(self) -> None:
        row = trigger_ledger(4)
        self.assertEqual(row["selected_r_plus_2v"], Q(34, 5))
        self.assertEqual(row["trigger_gap"], Q(16, 5))

    def test_status(self) -> None:
        data = verify_all()
        self.assertEqual(data["s3"]["status"], "NEEDS_MULTILINEARIZATION")
        self.assertEqual(data["s4"]["status"], "NEEDS_MULTILINEARIZATION")


if __name__ == "__main__":
    unittest.main()
