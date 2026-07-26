from pathlib import Path
import unittest

from src.adaptive_thermal import adaptive_thermal_recovery
from src.matpower import load_matpower_case


DATA = Path(__file__).resolve().parents[1] / "data" / "pglib-opf-v23.07"


class AdaptiveThermalTests(unittest.TestCase):
    def test_ieee14_typical_retains_original_bound_and_finds_upper(self):
        case = load_matpower_case(DATA / "pglib_opf_case14_ieee.m")
        result = adaptive_thermal_recovery(case)
        self.assertTrue(result.converged)
        self.assertEqual(len(result.history), 1)
        self.assertGreaterEqual(
            result.feasible_upper_bound, result.original_lower_bound
        )
        self.assertLess(result.certified_gap_percent, 0.2)


if __name__ == "__main__":
    unittest.main()
