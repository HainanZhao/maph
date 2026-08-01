from __future__ import annotations

import hashlib
import json
from pathlib import Path
import subprocess
import sys
import unittest


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "proof/p6_primitive_to_all_transfer_v1.py"
ARTIFACT = ROOT / "artifacts/p6-primitive-to-all-transfer-v1.json"
CGL_TAR = ROOT / "artifacts/sources/g1-literature-audit-v1/arxiv-2507.08296v2.tar"


class P6PrimitiveToAllTransferV1Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.data = json.loads(ARTIFACT.read_text(encoding="utf-8"))

    def test_replay_and_pinned_source(self) -> None:
        check = subprocess.run(
            [sys.executable, str(SCRIPT), "--check"], cwd=ROOT,
            text=True, capture_output=True, timeout=60,
        )
        self.assertEqual(check.returncode, 0, check.stderr)
        source = self.data["source_checks"]["cgl_v2_tar"]
        self.assertEqual(source["sha256"], hashlib.sha256(CGL_TAR.read_bytes()).hexdigest())
        self.assertEqual(source["locators"]["primitive_reduction_announcement"], "TeX 2109")

    def test_zero_multiset_and_exact_conductor_partition(self) -> None:
        lemma = self.data["lemma"]
        factors = lemma["euler_factor_zero_transfer"]
        self.assertEqual(
            factors["identity"],
            "L(s,chi)=L(s,chi*) product_{p|q, p not|d}(1-chi*(p)p^(-s)).",
        )
        self.assertIn("Re(s)=0", factors["derivation"][2])
        self.assertEqual(
            lemma["exact_partition"]["identity"],
            "sum_{chi mod q} N(sigma,T,chi)=sum_{d|q} N^*(sigma,T;d), for sigma>0.",
        )
        self.assertIn("one and only one primitive", lemma["primitive_inducer"]["statement"])

    def test_uniformity_small_conductors_and_scope(self) -> None:
        transfer = self.data["lemma"]["conditional_envelope_transfer"]
        self.assertIn("tau(q)<<_delta q^delta", transfer["divisor_loss"])
        self.assertIn("dT<K_delta", transfer["small_dT"])
        effect = self.data["p6_effect"]
        self.assertEqual(effect["Z05"], "PROVED_FOR_ZERO_COUNTS_IN_Re_s_GREATER_THAN_0")
        self.assertEqual(effect["Z06"], "PROVED_FOR_MONOTONE_PRIMITIVE_ENVELOPES_WITH_UNIFORMITY_AND_SMALL_dT_HANDLED")
        self.assertIn("q1-sensitive intermediate formulae", effect["not_promoted"])
        self.assertIn("Z03_TAIL_X_RANGE", effect["not_promoted"])

    def test_no_paper_stage_audit(self) -> None:
        boundary = self.data["claim_boundary"]
        self.assertIn("No hostile audit is initiated", boundary)
        self.assertNotIn("CGL-v2 zero-density theorem", self.data["p6_effect"]["Z05"])


if __name__ == "__main__":
    unittest.main()
