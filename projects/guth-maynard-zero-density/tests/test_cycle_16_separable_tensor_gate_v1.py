from fractions import Fraction
import importlib.util
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
PATH = ROOT / "conventions/separable_tensor_gate_v1.py"


def load_module():
    spec = importlib.util.spec_from_file_location("separable_tensor_gate_v1", PATH)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class SeparableTensorGateTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.rows = load_module().verify_all()

    def test_tensor_identities(self):
        for row in self.rows["tensor_examples"]:
            self.assertEqual(row["quadratic"], row["fourth"])
            self.assertEqual(row["S_z"], [value * value for value in row["P"]])

    def test_identical_rows_are_sharp(self):
        for row in self.rows["identical_row_countermodels"]:
            self.assertEqual(row["lambda_max"], row["separable_witness"])

    def test_overlap_certificate(self):
        for row in self.rows["spectral_overlap_examples"]:
            self.assertLessEqual(row["quadratic"], row["upper"])
            self.assertGreaterEqual(row["overlap"], row["certified_lower"])

    def test_exponent_gate(self):
        row = self.rows["exponents"]
        self.assertEqual(row["required_sep"], Fraction(56, 25))
        self.assertEqual(row["saving"], Fraction(4, 25))


if __name__ == "__main__":
    unittest.main()
