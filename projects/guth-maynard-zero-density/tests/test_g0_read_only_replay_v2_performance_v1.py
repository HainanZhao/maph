"""Integrity checks for the observed complete-G0 replay measurement."""
from decimal import Decimal
import hashlib
import json
from pathlib import Path
import unittest


PROJECT = Path(__file__).resolve().parents[1]


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


class G0ReplayV2PerformanceV1Tests(unittest.TestCase):
    def test_observation_and_pinned_inputs(self) -> None:
        data = json.loads((PROJECT / "artifacts/g0-read-only-replay-v2-performance-v1.json").read_text())
        self.assertEqual(data["epistemic_status"], "OBSERVED")
        self.assertEqual((data["replay_result"], data["exit_status"]), ("PASS", 0))
        self.assertEqual(data["harness_sha256"], sha256(PROJECT / "proof/run_g0_replay_v2.py"))
        self.assertEqual(data["reconciliation_artifact_sha256"], sha256(PROJECT / "artifacts/g0-full-reconstruction-v1.json"))
        self.assertEqual(data["reconciliation_script_sha256"], sha256(PROJECT / "proof/reconcile_g0_full_v1.py"))
        self.assertLess(Decimal(data["wall_seconds"]), Decimal(60))
        self.assertLess(data["max_rss_kib"], 262144)


if __name__ == "__main__":
    unittest.main()
