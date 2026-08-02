from fractions import Fraction
import importlib.util
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
PATH = ROOT / "conventions/rank_j_spectral_shift_v1.py"


def load_module():
    spec = importlib.util.spec_from_file_location("rank_j_spectral_shift_v1", PATH)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class RankJSpectralShiftTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.rows = load_module().verify_all()

    def test_determinant_identity(self):
        row = self.rows["determinant_example"]
        self.assertEqual(row["H_det"] / row["B_det"], row["D_product"] * row["det_I_plus_L"])

    def test_reconstruction_direction(self):
        row = self.rows["reconstruction_example"]
        self.assertEqual(row["c_star_S"], tuple(row["top_eigenvalue"] * entry for entry in row["y"]))

    def test_reconstruction_error(self):
        row = self.rows["reconstruction_example"]
        self.assertEqual(row["error_squared"], Fraction(1, row["top_eigenvalue"]))

    def test_singular_split(self):
        row = self.rows["singular_examples"]
        self.assertTrue(any(row["reconstructing_c_star_S"]))
        self.assertFalse(any(row["annihilating_c_star_S"]))

    def test_critical_scale(self):
        row = self.rows["critical_ledger"]
        self.assertEqual(row["k_rho"], Fraction(6, 25))
        self.assertEqual(row["reconstruction_constant"], Fraction(1, 64))


if __name__ == "__main__":
    unittest.main()
