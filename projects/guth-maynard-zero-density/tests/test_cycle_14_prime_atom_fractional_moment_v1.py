from fractions import Fraction
import importlib.util
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
PATH = ROOT / "conventions/prime_atom_fractional_moment_v1.py"


def load_module():
    spec = importlib.util.spec_from_file_location("prime_atom_fractional_moment_v1", PATH)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class PrimeAtomTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.rows = load_module().verify_all()

    def test_integer_optimum(self):
        census = self.rows["integer_census"]
        self.assertEqual(census["optimum_k"], 2)
        self.assertEqual(census["optimum_local_rows"], 8)

    def test_continuous_optimum(self):
        row = self.rows["continuous_optimum"]
        self.assertEqual(row["k"], Fraction(12, 5))
        self.assertEqual(row["local_rows"], Fraction(36, 5))
        self.assertEqual(row["integer_penalty"], Fraction(4, 5))

    def test_interpolation_fails(self):
        self.assertEqual(self.rows["ordinary_interpolation"]["local_rows"], Fraction(42, 5))

    def test_fractional_target(self):
        target = self.rows["fractional_prime_target"]
        self.assertEqual(target["target_moment"], 24)
        self.assertEqual(target["gain"], Fraction(4, 5))


if __name__ == "__main__":
    unittest.main()
