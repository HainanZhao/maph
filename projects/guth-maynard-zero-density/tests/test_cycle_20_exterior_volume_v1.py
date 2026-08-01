from fractions import Fraction
import importlib.util
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
PATH = ROOT / "conventions/exterior_volume_v1.py"


def load_module():
    spec = importlib.util.spec_from_file_location("exterior_volume_v1", PATH)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class ExteriorVolumeTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.rows = load_module().verify_all()

    def test_collapse_exponent(self):
        self.assertEqual(cls_row := self.rows["critical_exponents"]["k_rho"], Fraction(6, 25))
        self.assertEqual(cls_row, self.rows["critical_exponents"]["sufficient_lower_bound_exponent_strictly_below"])

    def test_sharp_model_diagonal(self):
        row = self.rows["sharp_finite_model"]
        self.assertEqual(row["diagonal"], row["M"])

    def test_sharp_model_positive(self):
        row = self.rows["sharp_finite_model"]
        self.assertGreater(row["residual_eigenvalue"], 0)
        self.assertGreaterEqual(row["top_eigenvalue"], row["M"])

    def test_determinant_formula_is_attained(self):
        row = self.rows["sharp_finite_model"]
        self.assertEqual(row["normalized_determinant"], row["collapse_formula"])

    def test_witness_norm_is_exact(self):
        row = self.rows["sharp_finite_model"]
        self.assertEqual(row["minimum_witness_norm_squared"], row["A"])


if __name__ == "__main__":
    unittest.main()
