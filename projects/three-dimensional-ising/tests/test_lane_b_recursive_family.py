"""Regression tests for the all-length Lane B recursive family."""

from __future__ import annotations

import unittest

from proof.verify_lane_b_recursive_family import verify


class LaneBRecursiveFamilyTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls)->None:
        cls.result=verify()

    def test_minimum_genus_family(self)->None:
        self.assertEqual(self.result["minimum_genus_theorem"]["minimum_genus_formula"],"L-1")

    def test_two_local_transition_types(self)->None:
        transitions=self.result["period_two_rotation"]["transition_checks"]
        self.assertEqual({row["parity"] for row in transitions},{"odd-target","even-target"})
        self.assertEqual({row["relative_defect_dimension"] for row in transitions},{1})
        self.assertEqual({row["active_topological_window_width"] for row in transitions},{3})

    def test_uniform_collective_rank_bound(self)->None:
        transfer=self.result["collective_transfer"]
        self.assertEqual(transfer["local_matrix_dimension"],256)
        self.assertEqual(transfer["uniform_handle_site_TT_rank_upper_bound"],1024)
        self.assertEqual(transfer["uniform_binary_site_TT_rank_upper_bound"],2048)


if __name__=="__main__":
    unittest.main()
