from __future__ import annotations

import hashlib
import importlib.util
import json
from pathlib import Path
import unittest


PROJECT = Path(__file__).resolve().parents[1]
SCRIPT = PROJECT / "proof" / "audit_g1_current_literature_v1.py"
ARTIFACT = PROJECT / "artifacts" / "g1-current-literature-audit-v1.json"

spec = importlib.util.spec_from_file_location("g1_current_literature_audit_v1", SCRIPT)
if spec is None or spec.loader is None:
    raise RuntimeError("cannot load g1 current-literature audit module")
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


class G1CurrentLiteratureAuditV1Test(unittest.TestCase):
    def setUp(self) -> None:
        self.data = json.loads(ARTIFACT.read_text(encoding="utf-8"))

    def test_builder_reconstructs_artifact_exactly(self) -> None:
        self.assertEqual(module.encoded(module.build()), ARTIFACT.read_bytes())

    def test_source_hashes_and_extractions_are_pinned(self) -> None:
        rows = self.data["source_verification"]["source_hashes"]
        self.assertEqual(set(rows), set(module.PINS))
        for key, row in rows.items():
            path = PROJECT / row["relative_path"]
            self.assertEqual(hashlib.sha256(path.read_bytes()).hexdigest(), module.PINS[key][1])
        module.verify_extraction("guth_tar", "guth_tex")
        module.verify_extraction("chen_tar", "chen_tex")

    def test_required_scope_and_route_boundary(self) -> None:
        self.assertEqual(self.data["epistemic_status"], "OBSERVED")
        self.assertEqual(self.data["route_decision"], "NOT_MADE: this audit is not an authorized substitute for the frozen G1 atlas or its route-selection gate.")
        boundary = self.data["claim_boundary"]
        self.assertIn("proves no theorem", boundary)
        self.assertIn("no global novelty claim", boundary)

    def test_guth_energy_sign_issue_is_contained(self) -> None:
        anchors = self.data["sources"]["guth_2503_07410v1"]["anchors"]
        row = next(row for row in anchors if row["id"] == "GUTH-ENERGY-CORRECTION")
        self.assertEqual(row["status"], "OBSERVED")
        self.assertIn("CONTAINED_SOURCE_SIGN_INCONSISTENCY", row["finding"])
        self.assertIn("not an authority", row["finding"])

    def test_chen_v2_status_authors_and_overlap_are_not_overclaimed(self) -> None:
        source = self.data["sources"]["chen_gupta_li_2507_08296v2"]
        self.assertIn("preprint", source["status"])
        self.assertIn("three-author v2", source["status"])
        self.assertIn("7/3", source["status"])
        overlap = self.data["overlap_disposition"]
        self.assertIn("direct prior work", overlap["P2B_energy"])
        self.assertIn("must concede", overlap["P6_dirichlet_L"])
        higher = next(row for row in source["anchors"] if row["id"] == "CGL-HIGHER-TRACE-SEARCH")
        self.assertIn("bounded textual-absence", higher["finding"])

    def test_page_anchor_coverage(self) -> None:
        anchors = self.data["source_verification"]["pdf_page_anchors"]
        self.assertEqual(set(anchors["guth"]), set(module.PAGE_ANCHORS["guth"]))
        self.assertEqual(set(anchors["chen_gupta_li"]), set(module.PAGE_ANCHORS["chen"]))
        module.verify_page_anchors("guth")
        module.verify_page_anchors("chen")


if __name__ == "__main__":
    unittest.main()
