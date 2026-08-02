from fractions import Fraction
import importlib.util
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
PATH = ROOT / "conventions/polynomial_block_subspace_v1.py"


def load_module():
    spec = importlib.util.spec_from_file_location("polynomial_block_subspace_v1", PATH)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class PolynomialBlockSubspaceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.rows = load_module().verify_all()

    def test_block_scale_inside_pnt_range(self):
        row = self.rows["exponents"]
        self.assertEqual(row["block_length"], Fraction(24, 25))
        self.assertGreater(row["block_length"], row["checked_pnt_endpoint"])

    def test_reconstruction_exponent(self):
        self.assertEqual(self.rows["exponents"]["reconstruction_exponent"], Fraction(1, 5))

    def test_no_projection_loss(self):
        self.assertEqual(self.rows["no_loss_projection"]["original_detector_energy_in_subspace"], 1)

    def test_markov_bad_fraction(self):
        row = self.rows["markov"]
        self.assertEqual(row["bad_fraction_upper"], Fraction(1, 12))
        self.assertGreater(row["good_per_subinterval_lower"], 0)

    def test_near_subspace_excluded(self):
        self.assertEqual(self.rows["asymptotic_alternatives"]["near_subspace_status"], "EXCLUDED_FOR_SUFFICIENTLY_LARGE_X")


if __name__ == "__main__":
    unittest.main()
