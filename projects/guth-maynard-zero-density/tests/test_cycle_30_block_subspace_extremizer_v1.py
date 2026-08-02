from fractions import Fraction
import importlib.util
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
PATH = ROOT / "conventions/block_subspace_extremizer_v1.py"


def load_module():
    spec = importlib.util.spec_from_file_location("block_subspace_extremizer_v1", PATH)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class BlockSubspaceExtremizerTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.rows = load_module().verify_all()

    def test_finite_parameters(self):
        row = self.rows["finite_extremizer"]
        self.assertEqual(row["L_target"], Fraction(175, 81))
        self.assertEqual(row["epsilon"], Fraction(108, 175))

    def test_shift_cancellation(self):
        self.assertEqual(self.rows["finite_extremizer"]["multiplicative_determinant_ratio"], 1)

    def test_positive_residual(self):
        row = self.rows["finite_extremizer"]
        self.assertGreater(row["epsilon"], 0)
        self.assertGreater(row["residual_other_eigenvalue"], 0)

    def test_perfect_block_synchronization(self):
        self.assertEqual(self.rows["block_synchronization"]["nontrivial_hadamard_values"], (0, 0, 0))

    def test_critical_scale(self):
        self.assertEqual(self.rows["critical_exponents"]["k_rho"], Fraction(6, 25))


if __name__ == "__main__":
    unittest.main()
