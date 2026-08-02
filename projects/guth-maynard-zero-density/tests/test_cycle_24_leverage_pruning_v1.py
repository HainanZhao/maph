from fractions import Fraction
import importlib.util
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
PATH = ROOT / "conventions/leverage_pruning_v1.py"


def load_module():
    spec = importlib.util.spec_from_file_location("leverage_pruning_v1", PATH)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class LeveragePruningTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.rows = load_module().verify_all()

    def test_structure_scale(self):
        self.assertEqual(self.rows["critical_exponents"]["k_rho"], Fraction(6, 25))

    def test_constant_budget(self):
        row = self.rows["frozen_constants"]
        self.assertEqual(row["leverage_lower_exponent_fraction"] - row["delta_exponent_fraction"], row["small_eigenvalue_exponent_fraction"])

    def test_near_cauchy_pair(self):
        row = self.rows["finite_near_cauchy_check"]
        self.assertEqual(row["kernel_lower"], 1 - 2 * row["delta"])

    def test_regular_subsystem_size(self):
        row = self.rows["finite_regular_check"]
        self.assertGreaterEqual(row["n"], row["k"] // 2)

    def test_leverage_to_eigenvalue(self):
        row = self.rows["finite_regular_check"]
        self.assertEqual(row["lambda_min_upper"], row["s_norm_squared_upper"] / row["leverage_lower"])


if __name__ == "__main__":
    unittest.main()
