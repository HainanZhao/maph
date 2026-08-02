from __future__ import annotations

from fractions import Fraction as Q
import importlib.util
from pathlib import Path
import unittest


PROJECT = Path(__file__).resolve().parents[1]
CONVENTIONS = PROJECT / "conventions/vector_harmonic_two_scale_v1.py"


def load_module():
    spec = importlib.util.spec_from_file_location("vector_harmonic_two_scale_v1", CONVENTIONS)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class Cycle38VectorHarmonicTwoScaleV1Tests(unittest.TestCase):
    def test_geometry(self):
        row = load_module().geometry(Q(3, 10))
        self.assertEqual(row["expanded_height"], Q(27, 10))
        self.assertEqual(row["collision_multiplicity"], Q(3, 10))
        self.assertGreater(row["collision_multiplicity"], Q(4, 25))

    def test_two_scale_r2(self):
        row = load_module().two_scale(Q(3, 5))
        self.assertEqual(row["per_row_two_scale_energy"], Q(14, 5))
        self.assertEqual(row["target_vector_bound"], Q(91, 25))

    def test_two_scale_r4(self):
        row = load_module().two_scale(Q(6, 5))
        self.assertEqual(row["per_row_two_scale_energy"], Q(11, 5))
        self.assertEqual(row["target_vector_bound"], Q(76, 25))

    def test_prime_monomial_labels(self):
        row = load_module().prime_monomial()
        self.assertEqual(row["cardinality"], "M^2")
        self.assertEqual(row["coefficient_square_norm"], "M^2")
        self.assertIn("m+1", row["injectivity"])

    def test_cross_checks(self):
        rows = load_module().verify_all()
        self.assertEqual(rows["registered_scales"]["geometry"]["fan_height"], Q(9, 10))

    def test_claim_boundary(self):
        document = (PROJECT / "docs/cycle-38-vector-harmonic-two-scale-v1.md").read_text(encoding="utf-8")
        self.assertIn("replacing that ambient", document)
        self.assertIn("No kernel-count, density, or interval improvement", document)
        self.assertIn("cancellation", document)


if __name__ == "__main__":
    unittest.main()
