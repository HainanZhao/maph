from fractions import Fraction
import importlib.util
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
PATH = ROOT / "conventions/near_cauchy_exclusion_v1.py"


def load_module():
    spec = importlib.util.spec_from_file_location("near_cauchy_exclusion_v1", PATH)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class NearCauchyExclusionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.rows = load_module().verify_all()

    def test_critical_scale(self):
        self.assertEqual(self.rows["critical_exponents"]["k_rho"], Fraction(6, 25))

    def test_square_root_delta_cost(self):
        self.assertEqual(self.rows["critical_exponents"]["phase_error_exponent_fraction"], Fraction(1, 16))

    def test_concentration_constant_flow(self):
        row = self.rows["concentration_constants"]
        self.assertEqual(row["squared_distance_multiplier"], 4)
        self.assertEqual(row["ratio_distance_multiplier"], 4)

    def test_prime_intervals_are_disjoint(self):
        row = self.rows["prime_intervals"]
        self.assertLess(row["q_over_X"][1], row["p_over_X"][0])
        self.assertLess(row["p_over_X"][1], row["r_over_X"][0])
        self.assertLess(row["r_over_X"][1], 2)

    def test_asymptotic_contradiction_registered(self):
        self.assertTrue(self.rows["asymptotic_separation"]["contradiction_for_large_X"])


if __name__ == "__main__":
    unittest.main()
