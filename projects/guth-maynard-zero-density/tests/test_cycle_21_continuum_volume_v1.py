from fractions import Fraction
import importlib.util
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
PATH = ROOT / "conventions/continuum_volume_v1.py"


def load_module():
    spec = importlib.util.spec_from_file_location("continuum_volume_v1", PATH)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class ContinuumVolumeTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.rows = load_module().verify_all()

    def test_harmonic_row_sum(self):
        row = self.rows["finite_frame_check"]
        self.assertEqual(row["harmonic_number"], Fraction(25, 12))
        self.assertEqual(row["continuum_row_sum"], Fraction(1, 12))

    def test_perturbation_regime(self):
        row = self.rows["finite_frame_check"]
        self.assertEqual(row["total_error"], Fraction(1, 6))
        self.assertLess(row["total_error"], Fraction(1, 2))

    def test_determinant_lower_positive(self):
        self.assertGreater(self.rows["finite_frame_check"]["determinant_lower_factor"], 0)

    def test_volume_scale(self):
        self.assertEqual(self.rows["critical_exponents"]["volume_collapse_scale"], Fraction(6, 25))

    def test_continuum_error_has_log_gain(self):
        row = self.rows["critical_exponents"]
        self.assertEqual(row["continuum_error_power"], Fraction(-3, 5))
        self.assertEqual(row["continuum_log_improvement"], "1/log X")


if __name__ == "__main__":
    unittest.main()
