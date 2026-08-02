from __future__ import annotations

from fractions import Fraction as Q
import importlib.util
from pathlib import Path
import unittest


PROJECT = Path(__file__).resolve().parents[1]
CONVENTIONS = PROJECT / "conventions/inverse_wrap_curvature_v1.py"


def load_module():
    spec = importlib.util.spec_from_file_location("inverse_wrap_curvature_v1", CONVENTIONS)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class Cycle46InverseWrapCurvatureV1Tests(unittest.TestCase):
    def test_critical_geometry(self):
        row = load_module().inverse_curve()
        self.assertEqual(row["slope"], Q(4, 25))
        self.assertEqual(row["curvature"], Q(-7, 25))
        self.assertEqual(row["tube_width"], Q(-21, 25))

    def test_reciprocal_transition(self):
        row = load_module().inverse_curve()
        self.assertEqual(row["target_count"], Q(7, 25))
        self.assertEqual(row["target_count"], row["reciprocal_curvature"])

    def test_alias_identity(self):
        self.assertEqual(Q(11, 25) * Q(7, 11), Q(7, 25))

    def test_claim_boundary(self):
        document = (PROJECT / "docs/cycle-46-inverse-wrap-curvature-v1.md").read_text(encoding="utf-8")
        self.assertIn("in both", document)
        self.assertIn("reciprocal-curvature", document)
        self.assertIn("No de-aliasing theorem", document)


if __name__ == "__main__":
    unittest.main()
