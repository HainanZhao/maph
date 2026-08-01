from __future__ import annotations

import json
from pathlib import Path
import subprocess
import sys
import unittest


PROJECT = Path(__file__).resolve().parents[1]
AUDIT = PROJECT / "proof/audit_g1_route_decision_v1_hostile.py"
ARTIFACT = PROJECT / "artifacts/g1-route-decision-v1-hostile-audit-v1.json"


class G1RouteDecisionV1HostileAuditTests(unittest.TestCase):
    def test_sealed_failure_and_required_containment(self) -> None:
        data = json.loads(ARTIFACT.read_text(encoding="utf-8"))
        self.assertEqual(data["epistemic_status"], "OBSERVED")
        self.assertEqual(data["status"], "FAIL_ROUTE_PREDICATE_COMPLETENESS")
        self.assertEqual(data["findings"]["route_predicates"]["status"], "FAIL")
        self.assertEqual(data["findings"]["adjudicator_identity"]["status"], "FAIL")

    def test_replay(self) -> None:
        subprocess.run([sys.executable, str(AUDIT), "--check", str(ARTIFACT)], cwd=PROJECT, check=True)


if __name__ == "__main__":
    unittest.main()
