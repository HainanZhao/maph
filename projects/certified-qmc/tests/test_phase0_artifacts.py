from __future__ import annotations

import json
from pathlib import Path
import unittest

from src.certificate import verify_audit_wrapper, verify_certificate
from src.ntt_prime import audit_ntt_prime


ROOT = Path(__file__).resolve().parents[1]


class Phase0ArtifactTests(unittest.TestCase):
    def test_core_example_replays(self):
        payload = json.loads(
            (ROOT / "certificates" / "example-n8-d2.json").read_text()
        )
        self.assertTrue(verify_certificate(payload))

    def test_all_frozen_unsw_prefixes_replay(self):
        target = json.loads(
            (ROOT / "data" / "phase0-targets.json").read_text()
        )["targets"][0]
        for dimension in target["initial_certified_dimensions"]:
            path = (
                ROOT
                / "certificates"
                / f"unsw-j2-n1024-d{dimension}.json"
            )
            wrapper = json.loads(path.read_text())
            self.assertTrue(verify_audit_wrapper(wrapper))
            self.assertEqual(
                wrapper["audit_target"]["upstream_sha256"],
                target["upstream_sha256"],
            )
            self.assertEqual(
                wrapper["core_certificate"]["input"]["dimension"],
                dimension,
            )

    def test_ntt_prime_artifact_matches_exact_recomputation(self):
        recorded = json.loads(
            (
                ROOT
                / "certificates"
                / "reference-ntt-prime.json"
            ).read_text()
        )
        expected = audit_ntt_prime(
            4611685941117976577,
            3,
            {2: 33, 311: 1, 1726273: 1},
        )
        self.assertEqual(recorded, expected)


if __name__ == "__main__":
    unittest.main()
