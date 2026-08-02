from fractions import Fraction
import importlib.util
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
PATH = ROOT / "conventions/hadamard_detector_surgery_correction_v2.py"


def load_module():
    spec = importlib.util.spec_from_file_location("hadamard_detector_surgery_correction_v2", PATH)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class HadamardCorrectionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.rows = load_module().verify_all()

    def test_remainder_cap(self):
        row = self.rows["finite_remainder"]
        self.assertLess(row["discarded"], row["blocks"])

    def test_retained_divisible(self):
        row = self.rows["finite_remainder"]
        self.assertEqual(row["retained"] % row["blocks"], 0)

    def test_detector_loss(self):
        self.assertEqual(self.rows["exponents"]["detector_relative_loss_exponent"], Fraction(-7, 10))

    def test_mass_loss(self):
        self.assertEqual(self.rows["exponents"]["mass_relative_loss_exponent"], Fraction(-1))


if __name__ == "__main__":
    unittest.main()
