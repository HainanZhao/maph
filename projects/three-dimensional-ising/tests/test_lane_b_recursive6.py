"""Regression tests for the second recursive Lane B handle step."""

from __future__ import annotations

import unittest

from proof.verify_lane_b_recursive6 import verify


class LaneBRecursiveSixTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.result=verify()

    def test_minimum_genus(self) -> None:
        self.assertEqual(self.result["minimum_genus_certificate"]["minimum_orientable_genus"],5)

    def test_relative_pattern_repeats(self) -> None:
        control=self.result["recurrence_control"]
        self.assertEqual(control["boundary_defect_dimensions"],[1,1])
        self.assertEqual(control["active_topological_window_widths"],[3,3])
        self.assertTrue(control["added_edge_semantic_pattern_repeats"])

    def test_relative_polynomials_reunite(self) -> None:
        identity=self.result["relative_sector_identity"]
        self.assertEqual(identity["refined_sectors"],512)
        self.assertTrue(identity["coefficientwise_reunion_verified"])


if __name__=="__main__":
    unittest.main()
