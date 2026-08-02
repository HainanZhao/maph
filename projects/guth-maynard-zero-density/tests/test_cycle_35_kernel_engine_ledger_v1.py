from __future__ import annotations

from fractions import Fraction as Q
import importlib.util
from pathlib import Path
import unittest


PROJECT = Path(__file__).resolve().parents[1]
CONVENTIONS = PROJECT / "conventions/kernel_engine_ledger_v1.py"


def load_module():
    spec = importlib.util.spec_from_file_location("kernel_engine_ledger_v1", CONVENTIONS)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class Cycle35KernelEngineLedgerV1Tests(unittest.TestCase):
    def test_hollow_fractional_exponents(self):
        row = load_module().hollow_fractional()
        self.assertEqual(row["threshold_mass"], Q(84, 25))
        self.assertEqual(row["target_bound"], Q(21, 5))
        self.assertEqual(row["required_saving"], Q(3, 5))
        self.assertEqual(row["coherent_zero"] - row["target_bound"], Q(3, 5))

    def test_curvature_margin(self):
        row = load_module().curvature(Q(1, 100))
        self.assertEqual(row["kernel"], Q(7, 10) - Q(1, 200))
        self.assertLess(row["boundary_count"], Q(21, 25))

    def test_entropy_volume_match(self):
        row = load_module().phase_entropy()
        self.assertEqual(row["per_row_entropy"], Q(-3, 5))
        self.assertEqual(row["target_accumulation_budget"], Q(6, 25))
        self.assertEqual(row["target_accumulation_budget"], row["residual_shift_match"])

    def test_histogram_pinsker_constant(self):
        row = load_module().histogram_pinsker(Q(1, 10), Q(1, 20))
        self.assertEqual(row["l1_lower"], Q(1, 20))
        self.assertEqual(row["entropy_lower"], Q(1, 800))
        self.assertEqual(row["coarse_entropy_lower"], Q(1, 800))

    def test_cross_checks(self):
        rows = load_module().verify_all()
        self.assertEqual(rows["scale"]["height"], Q(12, 5))
        self.assertEqual(rows["hollow_fractional"]["required_saving"], rows["scale"]["spacing"])

    def test_claim_boundary(self):
        document = (PROJECT / "docs/cycle-35-kernel-engine-ledger-v1.md").read_text(encoding="utf-8")
        self.assertIn("does **not** prove `(SPC)`", document)
        self.assertIn("High times", document)
        self.assertIn("No kernel-count, zero-density, or", document)


if __name__ == "__main__":
    unittest.main()
