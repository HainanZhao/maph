from __future__ import annotations

import unittest

from proof.verify_lane_b_character_duality import verify


class CharacterDualityTests(unittest.TestCase):
    def test_crossed_duality_and_triangular_transport(self) -> None:
        payload = verify()
        self.assertEqual(payload["claim_status"], "PROVED exact GF(2) coordinate identity")
        self.assertTrue(all(row["beta_unchanged"] for row in payload["cases"]))
        self.assertTrue(payload["manuscript_firewall"]["forbidden_anchors_absent"])


if __name__ == "__main__":
    unittest.main()
