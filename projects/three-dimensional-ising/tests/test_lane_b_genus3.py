"""Regression tests for the exact growing-genus Lane B verifier."""

import unittest

from proof.verify_lane_b_genus3 import verify


class LaneBGenusThreeTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.result = verify()

    def test_exact_controls(self) -> None:
        genus = self.result["minimum_genus_certificate"]
        self.assertEqual(genus["minimum_orientable_genus"], 3)
        self.assertEqual(genus["genus_two_face_covers"], 0)
        slab = self.result["genus_one_calibration"]
        self.assertTrue(slab["sealed_direct_enumeration_reproduced"])
        box = self.result["genus_three_box"]
        self.assertEqual(box["sector_count"], 64)
        self.assertEqual(box["maximum_frontier_states"], 16384)
        for evaluation in box["evaluations"].values():
            self.assertTrue(evaluation["independent_character_reconstruction"])
            self.assertEqual(
                evaluation["reference_handle_ordering_rank_profiles"],
                {"2,4,8,4,2": 48},
            )


if __name__ == "__main__":
    unittest.main()
