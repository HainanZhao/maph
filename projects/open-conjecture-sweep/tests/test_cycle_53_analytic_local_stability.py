from __future__ import annotations
import unittest
from proof.check_cycle_53_analytic_local_stability import audit


class Cycle53AnalyticLocalStabilityTest(unittest.TestCase):
    def test_exact_inputs(self):
        result = audit()
        self.assertEqual(result["status"], "PASS")
        self.assertEqual(result["four_cycles"], 5)
        self.assertEqual(result["kernel_cubic_survivors"], 0)


if __name__ == "__main__":
    unittest.main()
