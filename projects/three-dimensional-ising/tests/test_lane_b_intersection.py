"""Regression tests for the two labeled intersection-form routes."""

import unittest

from proof.verify_lane_b_intersection import verify


class LaneBIntersectionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.result = verify()

    def test_genus_one_calibration(self) -> None:
        slab = self.result["genus_one_calibration"]
        self.assertEqual(slab["intersection_matrix_rows"], [2, 1])
        self.assertTrue(slab["independent_routes_agree_with_labels"])

    def test_genus_three_labeled_pairing(self) -> None:
        box = self.result["genus_three_box"]
        self.assertEqual(box["intersection_matrix_rows"], [38, 25, 1, 2, 34, 17])
        self.assertEqual(box["rank"], 6)
        self.assertTrue(box["alternating"])
        self.assertTrue(box["independent_routes_agree_with_labels"])
        self.assertEqual(box["symplectic_transport_rows"], [9, 6, 36, 24, 16, 32])


if __name__ == "__main__":
    unittest.main()
