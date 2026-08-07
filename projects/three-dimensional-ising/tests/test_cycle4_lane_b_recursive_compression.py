"""Artifact-payload regression tests for Cycle 4."""

from __future__ import annotations

import unittest

from proof.build_cycle4_lane_b_recursive_compression import payload


class CycleFourLaneBArtifactTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls)->None:
        cls.payload=payload()

    def test_gate_and_success_level(self)->None:
        self.assertEqual(
            self.payload["gate_outcome"],
            "GATES_3_AND_4_POSITIVE_FIXED_TRANSVERSE_COMPRESSION",
        )
        self.assertEqual(self.payload["success_level"],2)

    def test_uniform_rank_bound(self)->None:
        family=self.payload["exact_replay"]["all_size_family"]
        transfer=family["collective_transfer"]
        self.assertEqual(transfer["uniform_handle_site_TT_rank_upper_bound"],1024)
        self.assertEqual(transfer["uniform_binary_site_TT_rank_upper_bound"],2048)

    def test_claim_boundary_excludes_full_solution(self)->None:
        self.assertIn("not solved",self.payload["claim_boundary"])


if __name__=="__main__":
    unittest.main()
