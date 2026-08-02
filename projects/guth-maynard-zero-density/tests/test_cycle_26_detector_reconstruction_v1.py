from fractions import Fraction
import importlib.util
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
PATH = ROOT / "conventions/detector_reconstruction_v1.py"


def load_module():
    spec = importlib.util.spec_from_file_location("detector_reconstruction_v1", PATH)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class DetectorReconstructionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.rows = load_module().verify_all()

    def test_critical_scale(self):
        self.assertEqual(self.rows["critical_exponents"]["k_rho"], Fraction(6, 25))

    def test_error_constant(self):
        self.assertEqual(self.rows["critical_exponents"]["reconstruction_error_exponent_fraction"], Fraction(1, 8))

    def test_positive_definite_common_coefficient(self):
        row = self.rows["positive_definite_check"]
        self.assertEqual(row["c_star_s"], row["L"])

    def test_positive_definite_error(self):
        row = self.rows["positive_definite_check"]
        self.assertEqual(row["normalized_error_squared"], Fraction(1, row["L"]))

    def test_singular_split(self):
        row = self.rows["singular_split_check"]
        self.assertNotEqual(row["reconstruction_coefficient"], 0)
        self.assertEqual(row["annihilation_coefficient"], 0)


if __name__ == "__main__":
    unittest.main()
