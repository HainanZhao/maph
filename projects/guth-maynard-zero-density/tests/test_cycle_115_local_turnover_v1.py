import unittest

from conventions.local_turnover_v1 import classify, theorem_record, transition_floor


class LocalTurnoverTests(unittest.TestCase):
    def test_three_cases(self) -> None:
        self.assertEqual(classify(delta=1e-8, eta=1.0, S2=10, M=2, x=0.1), "LOCAL_SIMPLE_ROOT")
        self.assertEqual(classify(delta=1e-8, eta=0.0, S2=10, M=2, x=0.1), "LOCAL_CRITICAL_POINT")
        floor = transition_floor(S2=10, M=2, x=0.1)
        self.assertEqual(classify(delta=2 * floor, eta=0.45, S2=10, M=2, x=0.1), "RESIDUAL_FLOOR")

    def test_record(self) -> None:
        row = theorem_record()
        self.assertIn("ell_x^2", row["transition_floor"])
        self.assertIn("S2/D^2", row["entropy_specialization"])


if __name__ == "__main__":
    unittest.main()
