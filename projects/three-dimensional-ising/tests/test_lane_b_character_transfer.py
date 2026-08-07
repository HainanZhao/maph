"""Regression test for the independent character-transfer implementation."""

from __future__ import annotations

import unittest

from proof.verify_lane_b_character_transfer import verify


class LaneBCharacterTransferTest(unittest.TestCase):
    def test_transfer_matches_sector_walsh_route(self)->None:
        result=verify()
        self.assertEqual([row["length"] for row in result["cases"]],[4,5])
        self.assertTrue(all(
            evaluation["all_agree"]
            for row in result["cases"]
            for evaluation in row["evaluations"]
        ))


if __name__=="__main__":
    unittest.main()
