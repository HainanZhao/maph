from fractions import Fraction
import importlib.util
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
PATH = ROOT / "conventions/hadamard_detector_surgery_v1.py"


def load_module():
    spec = importlib.util.spec_from_file_location("hadamard_detector_surgery_v1", PATH)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class HadamardDetectorSurgeryTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.rows = load_module().verify_all()

    def test_hadamard_orthogonality(self):
        row = self.rows["hadamard"]
        self.assertEqual(row["row_gram"], tuple(tuple(4 if i == j else 0 for j in range(4)) for i in range(4)))

    def test_signed_norm(self):
        self.assertEqual(self.rows["hadamard"]["signed_detector_norm_squared"], 3)

    def test_parseval(self):
        row = self.rows["parseval"]
        self.assertEqual(row["total_energy"], row["block_energy"])
        self.assertEqual(row["complement_energy"], row["variance_energy"])

    def test_high_variance_branch(self):
        row = self.rows["branches"]["high_variance"]
        self.assertGreaterEqual(row["complement_energy"], row["threshold"])
        self.assertGreaterEqual(row["max_nontrivial_squared"], row["forced_max_squared"])

    def test_low_variance_branch(self):
        row = self.rows["branches"]["low_variance"]
        self.assertEqual(row["complement_energy"], Fraction(0))
        self.assertEqual(row["aligned_real_lower"], Fraction(3, 4))


if __name__ == "__main__":
    unittest.main()
