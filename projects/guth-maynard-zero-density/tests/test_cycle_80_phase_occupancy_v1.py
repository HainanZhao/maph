from fractions import Fraction as Q
import unittest

from conventions.phase_occupancy_v1 import K_MAX, K_MIN, NEW_CUTOFF, occupancy_terms, verify_all


class Cycle80PhaseOccupancyTests(unittest.TestCase):
    def test_uniform_occupancy_endpoints(self) -> None:
        self.assertEqual(occupancy_terms(K_MIN)["occupancy_exponent"], Q(22, 45))
        self.assertEqual(occupancy_terms(K_MAX)["occupancy_exponent"], Q(22, 45))

    def test_new_band(self) -> None:
        self.assertTrue(occupancy_terms(K_MIN)["strictly_closed"])
        self.assertEqual(NEW_CUTOFF, Q(163, 450))

    def test_boundary_ties(self) -> None:
        row = occupancy_terms(NEW_CUTOFF)
        self.assertFalse(row["strictly_closed"])
        self.assertEqual(row["block_l1_exponent"], Q(31, 25))

    def test_verification(self) -> None:
        rows = verify_all()
        self.assertEqual(rows["band_width"], "43/450")
        self.assertIn("double B-process", rows["gate"])


if __name__ == "__main__":
    unittest.main()
