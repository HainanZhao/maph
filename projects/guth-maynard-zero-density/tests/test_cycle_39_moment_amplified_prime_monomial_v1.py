from __future__ import annotations

from fractions import Fraction as Q
import importlib.util
from pathlib import Path
import unittest


PROJECT = Path(__file__).resolve().parents[1]
CONVENTIONS = PROJECT / "conventions/moment_amplified_prime_monomial_v1.py"


def load_module():
    spec = importlib.util.spec_from_file_location("moment_amplified_prime_monomial_v1", CONVENTIONS)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class Cycle39MomentAmplifiedPrimeMonomialV1Tests(unittest.TestCase):
    def test_coefficient_bounds(self):
        module = load_module()
        self.assertEqual(module.coefficient_ledger(3)["coefficient_bound"], 12)
        self.assertEqual(module.coefficient_ledger(4)["coefficient_bound"], 72)
        self.assertEqual(module.coefficient_ledger(4)["uniform_harmonic_range"], "every integer m>=2")

    def test_r2_closure(self):
        row = load_module().amplified_ledger(3, Q(3, 5))
        self.assertEqual(row["restriction_target"], Q(61, 10))
        self.assertEqual(row["conditional_count_bound"], Q(1, 2))
        self.assertEqual(row["closing_margin"], Q(17, 50))

    def test_r4_closure(self):
        row = load_module().amplified_ledger(4, Q(6, 5))
        self.assertEqual(row["restriction_target"], Q(71, 10))
        self.assertEqual(row["conditional_count_bound"], Q(7, 10))
        self.assertEqual(row["closing_margin"], Q(7, 50))

    def test_least_moments(self):
        module = load_module()
        self.assertEqual(module.least_closing_moment(Q(3, 5)), 3)
        self.assertEqual(module.least_closing_moment(Q(6, 5)), 4)

    def test_unamplified_does_not_close(self):
        module = load_module()
        self.assertEqual(module.amplified_ledger(1, Q(3, 5))["conditional_count_bound"], Q(13, 10))
        self.assertEqual(module.amplified_ledger(1, Q(6, 5))["conditional_count_bound"], Q(19, 10))

    def test_claim_boundary(self):
        document = (PROJECT / "docs/cycle-39-moment-amplified-prime-monomial-v1.md").read_text(encoding="utf-8")
        self.assertIn("not a proof", document)
        self.assertIn("no kernel-count, density, or interval improvement", document)
        self.assertIn("uniform over", document)


if __name__ == "__main__":
    unittest.main()
