from __future__ import annotations

from fractions import Fraction as Q
import importlib.util
from pathlib import Path
import unittest


PROJECT = Path(__file__).resolve().parents[1]
CONVENTIONS = PROJECT / "conventions/excess_harmonic_routing_v1.py"


def load_module():
    spec = importlib.util.spec_from_file_location("excess_harmonic_routing_v1", CONVENTIONS)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class Cycle37ExcessHarmonicRoutingV1Tests(unittest.TestCase):
    def test_registered_thresholds(self):
        rows = load_module().registered_scales()
        self.assertEqual(rows["r4_excess"]["kernel_harmonic"], Q(1, 4))
        self.assertEqual(rows["r2_excess"]["kernel_harmonic"], Q(11, 20))

    def test_harmonic_color_loss(self):
        row = load_module().routing(Q(3, 5))
        self.assertEqual(row["arc_count"], Q(3, 10))
        self.assertEqual(row["harmonic_color_loss"], Q(3, 10))
        self.assertGreater(row["harmonic_color_loss"], Q(4, 25))

    def test_exact_finite_model_is_explicit(self):
        row = load_module().finite_fourier_perturbation()
        self.assertIn("preserved exactly", row["first_harmonic"])
        self.assertIn("=a", row["new_harmonics"])

    def test_cross_checks(self):
        rows = load_module().verify_all()
        self.assertLess(rows["registered_scales"]["r2_excess"]["kernel_harmonic"], Q(7, 10))

    def test_claim_boundary(self):
        document = (PROJECT / "docs/cycle-37-excess-harmonic-routing-v1.md").read_text(encoding="utf-8")
        self.assertIn("not an actual-prime", document)
        self.assertIn("whole harmonic vector", document)
        self.assertIn("No kernel-count, density, or interval gain", document)


if __name__ == "__main__":
    unittest.main()
