from fractions import Fraction
import importlib.util
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
PATH = ROOT / "conventions/stable_anchor_kernel_v1.py"


def load_module():
    spec = importlib.util.spec_from_file_location("stable_anchor_kernel_v1", PATH)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class StableAnchorKernelTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.rows = load_module().verify_all()

    def test_one_anchor_lower(self):
        row = self.rows["one_anchor"]
        self.assertGreaterEqual(row["kernel_lower"], row["coarse_lower"])

    def test_stable_multi_anchor(self):
        self.assertEqual(self.rows["multi_anchor"]["l1_norm"], 1)

    def test_kernel_threshold(self):
        self.assertEqual(self.rows["exponents"]["unnormalized_kernel"], Fraction(7, 10))

    def test_target_skeleton(self):
        self.assertEqual(self.rows["exponents"]["target_skeleton"], Fraction(21, 25))

    def test_missing_saving(self):
        self.assertEqual(self.rows["exponents"]["missing_saving"], Fraction(4, 25))


if __name__ == "__main__":
    unittest.main()
