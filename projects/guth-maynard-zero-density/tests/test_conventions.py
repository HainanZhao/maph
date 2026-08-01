import importlib.util
from fractions import Fraction
from pathlib import Path
import unittest


MODULE_PATH = Path(__file__).resolve().parents[1] / "conventions" / "baseline.py"
SPEC = importlib.util.spec_from_file_location("gm_baseline_conventions", MODULE_PATH)
assert SPEC is not None and SPEC.loader is not None
BASELINE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(BASELINE)


class FrozenConventionTests(unittest.TestCase):
    def test_expected_values_are_exact_fractions(self) -> None:
        self.assertEqual(BASELINE.EXPECTED_CROSSOVER_SIGMA, Fraction(7, 10))
        self.assertEqual(BASELINE.EXPECTED_DENSITY_CONSTANT, Fraction(30, 13))
        self.assertEqual(BASELINE.EXPECTED_UNIFORM_THETA, Fraction(17, 30))
        self.assertEqual(BASELINE.EXPECTED_ALMOST_ALL_THETA, Fraction(2, 15))

    def test_parameter_interval_contains_crossover(self) -> None:
        self.assertLess(BASELINE.SIGMA_LOWER, BASELINE.EXPECTED_CROSSOVER_SIGMA)
        self.assertLess(BASELINE.EXPECTED_CROSSOVER_SIGMA, BASELINE.SIGMA_UPPER)
        self.assertEqual(
            BASELINE.INGHAM_SWITCH_UPPER,
            BASELINE.EXPECTED_CROSSOVER_SIGMA,
        )


if __name__ == "__main__":
    unittest.main()

