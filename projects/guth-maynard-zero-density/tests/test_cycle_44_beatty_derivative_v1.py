from __future__ import annotations

from fractions import Fraction as Q
import importlib.util
from pathlib import Path
import unittest


PROJECT = Path(__file__).resolve().parents[1]
CONVENTIONS = PROJECT / "conventions/beatty_derivative_v1.py"


def load_module():
    spec = importlib.util.spec_from_file_location("beatty_derivative_v1", CONVENTIONS)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class Cycle44BeattyDerivativeV1Tests(unittest.TestCase):
    def test_low_mode(self):
        self.assertEqual(load_module().derivative_test(3, Q(0))["guaranteed_saving"], Q(2, 15))

    def test_required_resolution(self):
        module = load_module()
        self.assertEqual(module.derivative_test(3, Q(11, 25))["guaranteed_saving"], Q(3, 50))
        self.assertEqual(module.derivative_test(4, Q(11, 25))["guaranteed_saving"], Q(12, 175))

    def test_margin_failure(self):
        rows = load_module().registered_scales()
        self.assertLess(rows["best_registered_saving"], rows["cycle39_margin_r4"])
        self.assertLess(rows["best_registered_saving"], rows["cycle39_margin_r2"])

    def test_claim_boundary(self):
        document = (PROJECT / "docs/cycle-44-beatty-derivative-v1.md").read_text(encoding="utf-8")
        self.assertIn("fixed real", document)
        self.assertIn("scoped", document)
        self.assertIn("No density or interval gain", document)


if __name__ == "__main__":
    unittest.main()
