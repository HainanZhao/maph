from __future__ import annotations

import hashlib
import json
from pathlib import Path
import subprocess
import sys
import unittest


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "proof/build_p7_hecke_qi_preregistration_v2.py"
ARTIFACT = ROOT / "artifacts/p7-hecke-qi-preregistration-v2.json"


class P7HeckeQiPreregistrationV2Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.data = json.loads(ARTIFACT.read_text(encoding="utf-8"))

    def test_replay_and_all_versioned_identities(self) -> None:
        result = subprocess.run([sys.executable, str(SCRIPT), "--check"], cwd=ROOT, text=True, capture_output=True, timeout=60)
        self.assertEqual(result.returncode, 0, result.stderr)
        for identity in self.data["artifact_identity"].values():
            path = ROOT / identity["path"]
            self.assertEqual(hashlib.sha256(path.read_bytes()).hexdigest(), identity["sha256"])

    def test_v1_is_preserved_and_replays(self) -> None:
        correction = self.data["correction"]
        predecessor = ROOT / correction["predecessor"]["path"]
        self.assertEqual(hashlib.sha256(predecessor.read_bytes()).hexdigest(), correction["predecessor"]["sha256"])
        self.assertIn("without an explicit epistemic tag", correction["defect"])
        self.assertIn("no-search/no-hostile-audit", correction["unchanged"])

    def test_witness_is_conjectured_and_gate_remains_unexecuted(self) -> None:
        gate = next(g for g in self.data["gates"] if g["id"] == "P7-1-NORM-AGGREGATION")
        self.assertEqual(gate["state"], "UNEXECUTED")
        self.assertEqual(gate["preselected_witness"]["epistemic_status"], "CONJECTURED")
        self.assertIn("becomes PROVED only if P7-1", gate["preselected_witness"]["status_boundary"])
        self.assertEqual(self.data["status"], "PREREGISTERED_UNEXECUTED_STATUS_CORRECTION")


if __name__ == "__main__":
    unittest.main()
