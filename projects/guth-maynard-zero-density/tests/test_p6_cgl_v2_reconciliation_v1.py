from __future__ import annotations

import hashlib
import json
from pathlib import Path
import subprocess
import sys
import unittest


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "proof/reconcile_p6_cgl_v2_routes_v1.py"
ARTIFACT = ROOT / "artifacts/p6-cgl-v2-reconciliation-v1.json"
B_V2 = ROOT / "artifacts/p6-cgl-v2-route-b-v2-correction.json"


class P6CGLV2ReconciliationV1Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.data = json.loads(ARTIFACT.read_text())

    def test_replay_and_authority_chain(self) -> None:
        check = subprocess.run([sys.executable, str(SCRIPT), "--check"], cwd=ROOT, text=True, capture_output=True, timeout=60)
        self.assertEqual(check.returncode, 0, check.stderr)
        route_b = self.data["reconciled_authorities"]["route_b"]
        self.assertEqual(route_b["exact_margin_correction"]["sha256"], hashlib.sha256(B_V2.read_bytes()).hexdigest())
        self.assertEqual(route_b["authority_statement"], "B-v1 row reconstruction with B-v2 required for the q1=q exact-margin check.")

    def test_all_46_rows_and_raw_formula_comparisons_are_retained(self) -> None:
        expected = [*(f"S{i:02d}" for i in range(1, 7)), *(f"L{i:02d}" for i in range(1, 13)), *(f"M{i:02d}" for i in range(1, 9)), *(f"Z{i:02d}" for i in range(1, 11)), *(f"F{i:02d}" for i in range(1, 11))]
        rows = self.data["row_comparisons"]
        self.assertEqual([row["id"] for row in rows], expected)
        self.assertTrue(all(row["canonical_id_agreement"] for row in rows))
        for row in rows:
            self.assertTrue(row["formula_comparison"]["route_a_formula_or_chain_step"])
            self.assertTrue(row["formula_comparison"]["route_b_formula_or_check"])
            self.assertIn("comparison", row["source_locator_comparison"])
            self.assertIn("comparison", row["status_comparison"])
        self.assertEqual(next(row for row in rows if row["id"] == "F09")["formula_comparison"]["comparison"], "EXACT_CROSSINGS_COMPARED_IN_EXACT_ALGEBRA_BLOCK")
        self.assertEqual(next(row for row in rows if row["id"] == "F10")["formula_comparison"]["comparison"], "EXACT_Q1_EQUALS_Q_COMPARISON_CHECKED_IN_CORRECTED_BLOCK")

    def test_l12_disagreement_and_all_open_obligations_remain(self) -> None:
        l12 = self.data["l12_subcheck_reconciliation"]["subchecks"]
        self.assertEqual([item["id"] for item in l12], ["L12.odd_prime", "L12.two_power"])
        self.assertEqual(l12[1]["comparison"], "DISAGREEMENT_RETAINED_ROUTE_A_OPEN_ROUTE_B_RECORDED_SOURCE_DEPENDENT")
        open_inputs = self.data["open_analytic_obligations"]
        self.assertEqual(open_inputs["result"], "OPEN_ANALYTIC_INPUT")
        self.assertEqual(set(open_inputs["required_preregistered_obligations"]), set(open_inputs["shared_open_after_label_normalization"]))
        self.assertIn("S03_MULTIPLICITY_NOT_STATED", open_inputs["route_b_v2_inherited_raw_labels"])

    def test_v1_margin_defect_is_contained_and_v2_checks_margin(self) -> None:
        defect = self.data["route_b_v1_defect_contained"]
        self.assertEqual(defect["tag"], "ROUTE_B_V1_MARGIN_CHECK_IRRELEVANT")
        exact = self.data["exact_algebra_reconciliation"]
        self.assertEqual(exact["route_a_v1_identities"]["7/3-30/13"], "1/39")
        self.assertEqual(exact["route_b_v2_corrected_checks"]["7/3-30/13"]["cleared_integer_check"], "7*13-30*3=1")
        self.assertEqual(self.data["overall_disposition"], "OPEN_ANALYTIC_INPUT")


if __name__ == "__main__":
    unittest.main()
