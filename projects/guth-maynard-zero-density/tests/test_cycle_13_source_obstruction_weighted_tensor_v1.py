from fractions import Fraction
import importlib.util
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
PATH = ROOT / "conventions/weighted_fractional_tensor_v1.py"


def load_module():
    spec = importlib.util.spec_from_file_location("weighted_fractional_tensor_v1", PATH)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class WeightedFractionalTensorTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.module = load_module()
        cls.rows = cls.module.verify_all()

    def test_source_support(self):
        source = self.rows["source_support"]
        self.assertEqual(source["mobius_sum"], 1)
        self.assertEqual(source["fivefold_coefficient_at_prime"], 0)

    def test_registered_examples(self):
        self.assertEqual(self.rows["balanced"]["tau"], Fraction(2, 5))
        self.assertEqual(self.rows["registered_unbalanced"]["tau"], Fraction(1, 3))
        self.assertEqual(self.rows["registered_unbalanced"]["moments"]["local_rows"], Fraction(23, 3))
        self.assertFalse(self.rows["registered_rough_failure"]["admissible"])

    def test_grid_accounting(self):
        grid = self.rows["grid"]
        self.assertEqual(grid["checked"], 1442)
        self.assertEqual(grid["singleton_admissible"], 978)
        self.assertEqual(grid["strict_gain"], 927)
        self.assertEqual(grid["zero_gain"], 17)
        self.assertEqual(grid["negative_gain"], 34)
        self.assertEqual(grid["singleton_failed"], 464)

    def test_universal_budget(self):
        rows = self.module.moment_rows((Fraction(1),) * 5, Fraction(2, 5))
        self.assertEqual(rows["universal_tau_upper_bound"], Fraction(2, 5))
        self.assertEqual(rows["gain"], Fraction(4, 5))


if __name__ == "__main__":
    unittest.main()
