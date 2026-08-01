from __future__ import annotations

import hashlib
import json
from pathlib import Path
import subprocess
import sys
import unittest


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "proof/p6_tsmooth_corrected_hypothesis_repair_v1.py"
ARTIFACT = ROOT / "artifacts/p6-tsmooth-corrected-hypothesis-repair-v1.json"


class P6TSmoothCorrectedHypothesisRepairV1Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.data = json.loads(ARTIFACT.read_text(encoding="utf-8"))

    def test_replay_hash_and_resource_caps(self) -> None:
        replay = subprocess.run(
            [sys.executable, str(SCRIPT), "--check"], cwd=ROOT,
            text=True, capture_output=True, timeout=60,
        )
        self.assertEqual(replay.returncode, 0, replay.stderr)
        self.assertEqual(
            self.data["replay"]["script_sha256"],
            hashlib.sha256(SCRIPT.read_bytes()).hexdigest(),
        )
        self.assertEqual(self.data["replay"]["wall_cap_ns"], 60_000_000_000)
        self.assertEqual(self.data["replay"]["rss_cap_kib"], 1_048_576)

    def test_corrected_definition_is_not_attributed_to_cgl(self) -> None:
        corrected = self.data["corrected_theorem"]["corrected_hypothesis"]
        self.assertEqual(corrected["status"], "CORRECTED_HYPOTHESIS_NOT_SOURCE_ATTRIBUTION")
        self.assertIn("every prime p dividing q satisfies p<=T", corrected["definition"])
        self.assertIn("not asserted", corrected["not_claimed"])
        self.assertEqual(self.data["p6_effect"]["source_F08"], "REMAINS_OPEN_AS_UNDEFINED_IN_PINNED_CGL_V2")
        self.assertFalse(self.data["p6_effect"]["upstream_reconciliation_edited"])

    def test_divisor_chain_covers_edges_and_keeps_exact_endpoints(self) -> None:
        lemma = self.data["corrected_theorem"]["divisor_chain_lemma"]
        self.assertEqual(lemma["epistemic_status"], "PROVED")
        proof = " ".join(lemma["proof"])
        for phrase in ("largest divisor", "prime power", "d_{j+1}<=Td_j", "equality exactly", "1<=T<2", "Q=1"):
            self.assertIn(phrase, proof)
        finite = self.data["finite_sanity"]
        self.assertEqual(finite["status"], "OBSERVED_FINITE_SANITY_ONLY")
        self.assertGreater(finite["exact_rational_rows"], 1_000)
        self.assertGreater(finite["successor_equality_rows"], 0)
        self.assertGreater(finite["prime_power_rows"], 0)

    def test_fixed_v_repair_is_not_a_false_case_two_claim(self) -> None:
        repair = self.data["corrected_theorem"]["fixed_v_subdivision_repair"]
        self.assertEqual(repair["epistemic_status"], "PROVED_CONDITIONAL")
        self.assertIn("Later chain divisors can have", repair["why_this_is_not_the_source_case_2_verbatim"])
        self.assertIn("1+v(12-20*sigma)/5", repair["exact_bound"])
        algebra = self.data["exact_algebra"]
        self.assertIn("30/13", algebra["smooth_envelope"]["middle"])
        self.assertIn("15/7<30/13", algebra["smooth_envelope"]["right"])

    def test_conditional_branch_does_not_close_unrelated_p6_gaps(self) -> None:
        conclusion = self.data["corrected_theorem"]["conditional_zero_density_consequence"]
        self.assertEqual(conclusion["epistemic_status"], "PROVED_CONDITIONAL")
        self.assertIn("primitive-to-all", conclusion["statement"])
        self.assertIn("S03_MULTIPLICITY_NOT_STATED", conclusion["not_closed"])
        self.assertIn("S06_EXTERNAL_INPUTS", conclusion["not_closed"])
        self.assertIn("unrelated q1-sensitive intermediate formulae", self.data["p6_effect"]["not_repaired"])
        self.assertIn("hostile audit", self.data["claim_boundary"])


if __name__ == "__main__":
    unittest.main()
