"""Artifact-payload regression tests for Gate B5."""

from __future__ import annotations

import unittest

from proof.build_cycle5_lane_b_width_rank_audit import payload


class CycleFiveLaneBArtifactTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.payload = payload()

    def test_claim_boundary(self) -> None:
        boundary = self.payload["claim_boundary"]
        self.assertIn("not an optimized-basis lower bound", boundary)
        self.assertIn("not solved", boundary)

    def test_all_six_width_four_minors(self) -> None:
        audits = self.payload["exact_replay"]["width_rank_audit"]["prime_audits"]
        determinants = []
        for audit in audits.values():
            for case in audit["w4"]["cases"].values():
                certificate = next(iter(case["central_full_minor_mod_prime"].values()))
                determinants.append(certificate["determinant"])
        self.assertEqual(len(determinants), 6)
        self.assertTrue(all(determinants))


if __name__ == "__main__":
    unittest.main()
