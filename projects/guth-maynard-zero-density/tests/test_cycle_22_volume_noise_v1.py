from fractions import Fraction
import importlib.util
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
PATH = ROOT / "conventions/volume_noise_v1.py"


def load_module():
    spec = importlib.util.spec_from_file_location("volume_noise_v1", PATH)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class VolumeNoiseTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.rows = load_module().verify_all()

    def test_operator_gap(self):
        self.assertEqual(self.rows["critical_exponents"]["operator_power_gap"], Fraction(13, 25))

    def test_volume_gap(self):
        row = self.rows["critical_exponents"]
        self.assertEqual(row["bulk_log_volume"], Fraction(17, 25))
        self.assertEqual(row["bulk_minus_signal"], Fraction(11, 25))

    def test_square_root_entries(self):
        row = self.rows["finite_block_unitary"]
        self.assertEqual(row["off_diagonal_squared"], Fraction(1, row["m"]))

    def test_operator_discrepancy(self):
        row = self.rows["finite_block_unitary"]
        self.assertEqual(row["delta_squared"], Fraction(row["k"], 2 * row["m"]))

    def test_determinant(self):
        self.assertEqual(self.rows["finite_block_unitary"]["determinant"], Fraction(3, 4) ** 4)


if __name__ == "__main__":
    unittest.main()
