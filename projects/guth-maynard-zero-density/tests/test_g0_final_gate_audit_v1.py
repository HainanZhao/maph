import json
from decimal import Decimal
from pathlib import Path
import subprocess
import sys
import unittest


PROJECT = Path(__file__).resolve().parents[1]
SCRIPT = PROJECT / "proof" / "audit_g0_final_gate_v1.py"
ARTIFACT = PROJECT / "artifacts" / "g0-final-gate-audit-v1.json"


class G0FinalGateAuditV1Tests(unittest.TestCase):
    def test_fixed_hostile_audit_replays(self) -> None:
        subprocess.run([sys.executable, str(SCRIPT), "--check"], check=True)

    def test_all_preregistered_coverage_counts_and_pass_recommendation(self) -> None:
        audit = json.loads(ARTIFACT.read_text())
        self.assertEqual(audit["cycle1_required_labels"]["count"], 24)
        self.assertEqual(audit["stream_b_required_nodes"]["count"], 7)
        self.assertEqual(audit["stream_c_required_labels"]["count"], 26)
        self.assertEqual(audit["recommendation"]["status"], "PASS")
        self.assertEqual(audit["recommendation"]["epistemic_status"], "OBSERVED")

    def test_plan_is_intentionally_not_frozen_and_resource_limits_are_strict(self) -> None:
        audit = json.loads(ARTIFACT.read_text())
        self.assertNotIn("plan", audit["frozen_dependencies"])
        self.assertIn("intentionally not hash-frozen", audit["governance_note"])
        for result in audit["resource_gate"]["route_results"]:
            self.assertLess(Decimal(result["wall_seconds"]), Decimal(60))
            self.assertLess(result["max_rss_kib"], 256 * 1024)
        self.assertEqual(audit["route_independence_and_circularity"]["status"], "NO_CIRCULARITY_OBSERVED")


if __name__ == "__main__":
    unittest.main()
