"""Regression tests for the first recursive Lane B handle step."""

from __future__ import annotations

import unittest

from proof.verify_lane_b_recursive import verify


class LaneBRecursiveTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.result = verify()

    def test_relative_boundary_defect(self) -> None:
        self.assertEqual(self.result["relative_boundary"]["defect_dimension"], 1)
        self.assertEqual(self.result["relative_boundary"]["nonzero_old_face_image"], 96)

    def test_old_intersection_form_is_preserved(self) -> None:
        self.assertTrue(self.result["old_homology"]["preserved_label_by_label"])

    def test_topological_support_is_three_bits(self) -> None:
        self.assertEqual(self.result["local_support"]["active_adapted_coordinates"], [5, 6, 7])

    def test_relative_sector_polynomials_reunite(self) -> None:
        identity = self.result["relative_sector_identity"]
        self.assertEqual(identity["refined_sectors"], 128)
        self.assertTrue(identity["coefficientwise_reunion_verified"])


if __name__ == "__main__":
    unittest.main()
