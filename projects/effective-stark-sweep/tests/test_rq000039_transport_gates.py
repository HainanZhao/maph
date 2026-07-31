#!/usr/bin/env python3
"""Regression checks for the first exact Engine-B transport gates."""

from __future__ import annotations

import json
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]


class RQ000039TransportGatesTest(unittest.TestCase):
    def test_exact_conductor_and_ray_map(self) -> None:
        data = json.loads((ROOT / "artifacts/rq000039-engine-b-transport-gates-1-2-v1.json").read_text())
        self.assertEqual(data["claim_tag"], "PROVED_EXACT_TRANSPORT_GATES_1_2")
        self.assertEqual((data["source_case_id"], data["target_case_id"], data["closure_id"]),
                         ("RQ-000021", "RQ-000039", "B5-015"))
        self.assertEqual(data["open_gates"], [
            "positive_orientation_at_the_split_real_place",
            "Artin-labelled_packet_distribution_or_direct_target_equality",
        ])
        self.assertIn("unique norm-two prime", data["proved_gates"]["finite_modulus_relation"])
        self.assertIn("matrix 1", data["proved_gates"]["ray_class_map"])


if __name__ == "__main__":
    unittest.main()
