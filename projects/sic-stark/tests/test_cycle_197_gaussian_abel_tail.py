from __future__ import annotations

import json
from pathlib import Path
import subprocess
import sys
import unittest


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "proof" / "verify_cycle_197_gaussian_abel_tail.py"


class Cycle197GaussianAbelTailTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        completed = subprocess.run([sys.executable, str(SCRIPT)], check=True, capture_output=True, text=True)
        cls.result = json.loads(completed.stdout)

    def test_full_frequency_ledger_is_exact(self) -> None:
        ledger = self.result["component_ledger"]
        self.assertEqual(ledger["component_count"], 36)
        self.assertEqual(ledger["nonzero_frequency_count"], 30)
        self.assertEqual(ledger["zero_frequency_count"], 6)
        self.assertTrue(ledger["all_30_nonzero_components_have_positive_gaussian_laplace_exponent"])

    def test_nonzero_components_have_positive_laplace_scale(self) -> None:
        for record in self.result["component_ledger"]["records"]:
            if record["centered_frequency_s"] == 0:
                self.assertEqual(record["classification"], "ZERO_FREQUENCY_SEPARATE")
            else:
                self.assertEqual(record["classification"], "POSITIVE_1_OVER_EPSILON_DIVERGENCE")
                self.assertGreater(record["gaussian_failure_exponent_numerator_s_squared"], 0)

    def test_scope_does_not_claim_a_distributional_no_go(self) -> None:
        self.assertEqual(self.result["gate_outcome"]["fixed_even_gaussian_abel"], "FALSIFIED_FOR_UNIFORM_RAW_36_COMPONENT_ENDPOINT_LIMIT")
        self.assertIn("may still", self.result["next_unresolved_boundary"]["statement"])


if __name__ == "__main__":
    unittest.main()
