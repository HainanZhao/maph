"""Artifact-payload regression tests for Cycle 3."""

import unittest

from proof.build_cycle3_lane_b_rank_reduction import payload


class CycleThreeLaneBArtifactTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.payload = payload()

    def test_gate_and_claim_boundary(self) -> None:
        self.assertEqual(
            self.payload["gate_outcome"],
            "GATE_2_POSITIVE_FINITE_INSTANCE_COMPRESSION",
        )
        self.assertEqual(self.payload["success_level"], 2)

    def test_rank_witness_is_frozen(self) -> None:
        ranks = self.payload["exact_replay"]["physical_symplectic_ranks"]
        self.assertEqual(
            ranks["exact_rank_seven_survivor"]["generic_TT_rank_over_Q(t)"],
            [2, 4, 7, 4, 2],
        )


if __name__ == "__main__":
    unittest.main()
