import json
from pathlib import Path
import subprocess
import sys
import unittest


PROJECT = Path(__file__).resolve().parents[1]
SCRIPT = PROJECT / "proof" / "audit_g0_dependency_evidence_v3.py"
ARTIFACT = PROJECT / "artifacts" / "g0-dependency-evidence-matrix-v3.json"


class G0DependencyEvidenceMatrixV3Tests(unittest.TestCase):
    def test_fixed_scope_correction_replays(self) -> None:
        subprocess.run([sys.executable, str(SCRIPT), "--check"], check=True)

    def test_v2_in_place_refresh_is_explicitly_contained(self) -> None:
        data = json.loads(ARTIFACT.read_text())
        correction = data["v2_in_place_refresh_correction"]
        self.assertEqual(correction["status"], "OBSERVED CORRECTION")
        self.assertIn("UNRECOVERABLE_FROM_LOCAL_WORKTREE", correction["pre_refresh_v2_identity"])
        self.assertEqual(correction["post_refresh_v2_sha256"], "504cc31047ba8191cd1996ee7238cf3f95ab8e007f75824b39307999abb131ae")

    def test_scope_is_static_and_g0_remains_open(self) -> None:
        data = json.loads(ARTIFACT.read_text())
        self.assertIn("Only the named FROZEN inputs", data["fixed_scope"]["rule"])
        self.assertNotIn("glob(", SCRIPT.read_text())
        nodes = {row["id"]: row for row in data["nodes"]}
        self.assertEqual(nodes["G0-FULL-RECONSTRUCTION"]["status"], "OPEN")
        self.assertEqual(nodes["STREAM-C-V5-RECONCILIATION"]["status"], "OPEN")
        self.assertEqual(nodes["G0-RESOURCE-PERFORMANCE"]["status"], "OPEN")
        self.assertIn("source_manifest_v3", data["fixed_scope"]["frozen_dependencies"])
        self.assertIn("stream_c_route_a_v5", data["fixed_scope"]["frozen_dependencies"])
        self.assertIn("stream_c_route_b_v5", data["fixed_scope"]["frozen_dependencies"])


if __name__ == "__main__":
    unittest.main()
