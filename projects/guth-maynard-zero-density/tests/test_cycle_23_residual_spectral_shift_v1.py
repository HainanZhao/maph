from fractions import Fraction
import importlib.util
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
PATH = ROOT / "conventions/residual_spectral_shift_v1.py"


def load_module():
    spec = importlib.util.spec_from_file_location("residual_spectral_shift_v1", PATH)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class ResidualSpectralShiftTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.rows = load_module().verify_all()

    def test_shift_exponent(self):
        self.assertEqual(self.rows["critical_exponents"]["k_rho"], Fraction(6, 25))

    def test_normalized_residual(self):
        self.assertEqual(self.rows["finite_diagonal_residual"]["normalized_residual_B_diagonal"], 1)

    def test_inverse_leverage(self):
        self.assertEqual(self.rows["finite_diagonal_residual"]["inverse_leverage"], Fraction(4, 3))

    def test_determinant_identity(self):
        row = self.rows["finite_diagonal_residual"]
        self.assertEqual(row["determinant_ratio"], row["direct_determinant"])

    def test_top_eigenvalue(self):
        self.assertEqual(self.rows["finite_diagonal_residual"]["direct_top_eigenvalue"], Fraction(7, 4))


if __name__ == "__main__":
    unittest.main()
