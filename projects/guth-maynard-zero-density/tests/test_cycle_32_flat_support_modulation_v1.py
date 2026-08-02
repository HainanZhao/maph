from fractions import Fraction
import importlib.util
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
PATH = ROOT / "conventions/flat_support_modulation_v1.py"


def load_module():
    spec = importlib.util.spec_from_file_location("flat_support_modulation_v1", PATH)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class FlatSupportModulationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.rows = load_module().verify_all()

    def test_discarded_mass(self):
        self.assertLessEqual(self.rows["finite_dyadic"]["discarded_mass"], Fraction(1, 4))

    def test_selected_mass(self):
        self.assertEqual(self.rows["finite_dyadic"]["selected_mass"], Fraction(3, 4))

    def test_flat_bounds(self):
        row = self.rows["finite_dyadic"]
        self.assertTrue(all(row["flat_lower_squared"] <= value <= row["flat_upper_squared"] for value in row["normalized_squared_magnitudes"]))

    def test_square_endpoint(self):
        row = self.rows["support_ladder"][0]
        self.assertEqual(row["prime_coordinate_support"], row["rows"])

    def test_full_endpoint(self):
        self.assertEqual(self.rows["support_ladder"][-1]["prime_coordinate_support"], Fraction(1))


if __name__ == "__main__":
    unittest.main()
