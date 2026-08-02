from fractions import Fraction
import importlib.util
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
PATH = ROOT / "conventions/weighted_continuum_volume_v2.py"


def load_module():
    spec = importlib.util.spec_from_file_location("weighted_continuum_volume_v2", PATH)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class WeightedContinuumVolumeCorrectionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.rows = load_module().verify_all()

    def test_reference_measure(self):
        self.assertEqual(self.rows["finite_weighted_check"]["reference_measure"], "e^y dy on [0,log 2]")

    def test_weighted_row_sum(self):
        self.assertEqual(self.rows["finite_weighted_check"]["weighted_row_sum"], Fraction(1, 8))

    def test_total_error(self):
        self.assertEqual(self.rows["finite_weighted_check"]["total_error"], Fraction(1, 4))

    def test_volume_exponent_preserved(self):
        self.assertEqual(self.rows["critical_exponents"]["volume_collapse_scale"], Fraction(6, 25))

    def test_discrepancy_scale_preserved(self):
        self.assertEqual(self.rows["critical_exponents"]["required_prime_operator_discrepancy"], "o(X^(-3/5))")


if __name__ == "__main__":
    unittest.main()
