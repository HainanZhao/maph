from __future__ import annotations

import hashlib
import json
from pathlib import Path
import subprocess
import sys
import unittest


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "proof/build_p7_hecke_qi_preregistration_v1.py"
ARTIFACT = ROOT / "artifacts/p7-hecke-qi-preregistration-v1.json"


class P7HeckeQiPreregistrationV1Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.data = json.loads(ARTIFACT.read_text(encoding="utf-8"))

    def test_replay_and_source_pins(self) -> None:
        result = subprocess.run([sys.executable, str(SCRIPT), "--check"], cwd=ROOT, text=True, capture_output=True, timeout=60)
        self.assertEqual(result.returncode, 0, result.stderr)
        for key in ("zaman_1502_05679v4", "thorner_zaman_1510_08086v1"):
            source = self.data["source_checks"][key]
            for item in ("pdf", "source_tar"):
                path = ROOT / source[item]["path"]
                self.assertEqual(hashlib.sha256(path.read_bytes()).hexdigest(), source[item]["sha256"])
        mrl = self.data["source_checks"]["thorner_mrl_2019"]["publisher_pdf"]
        self.assertEqual(hashlib.sha256((ROOT / mrl["path"]).read_bytes()).hexdigest(), mrl["sha256"])

    def test_exact_family_and_counting_conventions(self) -> None:
        family = self.data["selection"]["family"]
        self.assertEqual(family["archimedean_type"], "trivial; no angular parameter m is allowed")
        self.assertIn("Q<Nf<=2Q", family["moduli"])
        self.assertIn("exact conductor", family["modulus_multiplicity"])
        zero = self.data["selection"]["zero_count"]
        self.assertEqual(zero["multiplicity"], "included")
        self.assertIn("N_F(sigma,T;Q)", self.data["collective_count"])

    def test_first_gate_contains_both_loss_and_type_mismatch(self) -> None:
        gate = next(g for g in self.data["gates"] if g["id"] == "P7-1-NORM-AGGREGATION")
        self.assertTrue(gate["first_falsifiable_gate"])
        self.assertEqual(gate["state"], "UNEXECUTED")
        self.assertIn("tau(n)", gate["frozen_identities"][0])
        witness = gate["preselected_witness"]
        self.assertEqual(witness["aggregated_coefficients"]["A_chi_3(17)"], -2)
        self.assertEqual(witness["aggregated_coefficients"]["A_chi_4(17)"], 2)
        self.assertIn("cannot be applied verbatim", gate["direct_import_boundary"])

    def test_all_required_gates_and_prior_work_are_retained(self) -> None:
        identifiers = [g["id"] for g in self.data["gates"]]
        self.assertEqual(identifiers, [
            "P7-0-SOURCE-FAMILY", "P7-1-NORM-AGGREGATION", "P7-2-RAY-CLASS-ORTHOGONALITY",
            "P7-3-IDEAL-CUBIC-ENERGY", "P7-4-DETECTOR-TAIL", "P7-5-PRIME-IDEAL-SHORT-INTERVALS",
        ])
        conceded = " ".join(self.data["prior_work_conceded"])
        self.assertIn("Bombieri--Vinogradov", conceded)
        self.assertIn("bounded-gap", conceded)
        self.assertEqual(self.data["source_checks"]["bgl_rejected_comparison"]["status"], "NOT_USED_AS_AUTHORITY")

    def test_no_search_or_hostile_audit_is_authorized(self) -> None:
        boundary = self.data["claim_boundary"]
        self.assertIn("no hostile audit", boundary)
        self.assertIn("no theorem search", boundary)
        self.assertEqual(self.data["status"], "PREREGISTERED_UNEXECUTED")


if __name__ == "__main__":
    unittest.main()
