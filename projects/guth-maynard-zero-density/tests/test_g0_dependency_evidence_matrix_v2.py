import json
from pathlib import Path
import subprocess
import sys
import unittest


PROJECT = Path(__file__).resolve().parents[1]
SCRIPT = PROJECT / "proof" / "audit_g0_dependency_evidence_v2.py"
ARTIFACT = PROJECT / "artifacts" / "g0-dependency-evidence-matrix-v2.json"


class G0DependencyEvidenceMatrixV2Tests(unittest.TestCase):
    def test_dynamic_v2_builder_fails_closed_on_current_artifact_delta(self) -> None:
        result = subprocess.run([sys.executable, str(SCRIPT), "--check"], check=False, capture_output=True, text=True)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("unclassified artifact", result.stderr)
        matrix = json.loads(ARTIFACT.read_text())
        recorded = {row["file"] for row in matrix["artifact_inventory"]}
        current = {path.name for path in (PROJECT / "artifacts").glob("*.json")}
        delta = sorted(current - recorded)
        self.assertTrue(delta)
        self.assertIn(delta[0], result.stderr)

    def test_inherited_nodes_source_manifest_and_open_g0_are_present(self) -> None:
        matrix = json.loads(ARTIFACT.read_text())
        ids = {node["id"] for node in matrix["nodes"]}
        inherited = json.loads((PROJECT / "artifacts" / "g0-theorem-dependency-graph-v1.json").read_text())["nodes"]
        self.assertTrue({node["id"] for node in inherited}.issubset(ids))
        self.assertIn("SOURCE-MANIFEST", ids)
        state = matrix["inventory_scope"]["source_manifest_v2_state"]
        self.assertIn(state["status"], {"CURRENT", "STALE_OR_INCOMPLETE"})
        g0 = next(node for node in matrix["nodes"] if node["id"] == "G0-FULL-RECONSTRUCTION")
        self.assertIn("OBSERVED OPEN", g0["reported_tag_validity"])
        self.assertTrue(g0["open_gaps"])

    def test_post_refresh_v2_is_preserved_and_current_delta_is_contained_by_v3(self) -> None:
        matrix = json.loads(ARTIFACT.read_text())
        recorded = {row["file"] for row in matrix["artifact_inventory"]}
        current = {path.name for path in (PROJECT / "artifacts").glob("*.json")}
        self.assertIn("cycle-2-g0-per-route-resource-gate-config-v1.json", current - recorded)
        self.assertIn("cycle-2-g0-per-route-resource-gate-performance-v1.json", current - recorded)
        successor = PROJECT / "proof/audit_g0_dependency_evidence_v3.py"
        subprocess.run([sys.executable, str(successor), "--check"], check=True, capture_output=True, text=True)
        v3 = json.loads((PROJECT / "artifacts/g0-dependency-evidence-matrix-v3.json").read_text())
        correction = v3["v2_in_place_refresh_correction"]
        self.assertEqual(correction["post_refresh_v2_sha256"], "504cc31047ba8191cd1996ee7238cf3f95ab8e007f75824b39307999abb131ae")
        self.assertIn("UNRECOVERABLE_FROM_LOCAL_WORKTREE", correction["pre_refresh_v2_identity"])
        timing = {row["file"] for row in matrix["historical_nondeterministic_timing_artifacts"]}
        self.assertIn("cycle-2-stream-b-route-a-v2.json", timing)
        self.assertIn("cycle-2-stream-c-route-a-v2.json", timing)
        self.assertIn("cycle-2-stream-c-route-a-v1.json", timing)
        legacy = next(row for row in matrix["historical_nondeterministic_timing_artifacts"] if row["file"] == "cycle-2-stream-c-route-a-v1.json")
        self.assertIn("UNCONTAINED", legacy["containment_or_gap"])


if __name__ == "__main__":
    unittest.main()
