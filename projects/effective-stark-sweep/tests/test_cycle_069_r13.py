import json
import hashlib
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]


def load(path: str) -> dict:
    return json.loads((ROOT / path).read_text(encoding="utf-8"))


class Cycle069R13Test(unittest.TestCase):
    def test_no_proxy_or_mixed_record_is_effectively_verified(self):
        ledger = load("artifacts/predicate-provenance-ledger-r13-v1.json")
        for row in ledger["records"]:
            if row["predicate_provenance"] != "GENUINE":
                self.assertFalse(row["effective_tag"].startswith("VERIFIED"))
        historical = []
        for path in (ROOT / "artifacts").glob("*.json"):
            data = json.loads(path.read_text(encoding="utf-8"))
            if str(data.get("claim_tag", "")).startswith("VERIFIED_W2"):
                historical.append(f"artifacts/{path.name}")
        relabelled = {row["artifact"] for row in ledger["records"]}
        self.assertEqual(set(historical) - relabelled, set())

    def test_every_completed_individual_w2_certificate_is_relabelled(self):
        ledger = load("artifacts/predicate-provenance-ledger-r13-v1.json")
        individual = [
            row
            for row in ledger["records"]
            if row["artifact"].startswith("artifacts/rq")
            and row["artifact"].endswith("-b-closure-w2-v1.json")
        ]
        self.assertEqual(len(individual), 51)
        proxy = [
            row for row in individual
            if row["predicate_provenance"] == "PROXY"
        ]
        self.assertEqual(
            [row["artifact"] for row in proxy],
            ["artifacts/rq007500-b-closure-w2-v1.json"],
        )
        self.assertEqual(proxy[0]["effective_tag"], "SUPERSEDED_PROXY_W2")
        self.assertEqual(
            sum(
                row["predicate_provenance"] == "GENUINE"
                for row in individual
            ),
            50,
        )

    def test_root_cause_names_joint_failure_and_five_paths(self):
        text = (ROOT / "docs/methods-proxy-root-cause-r13.md").read_text()
        normalized = " ".join(text.split())
        self.assertIn("joint architecture-and-verifier failure", normalized)
        self.assertIn("five load-bearing paths", normalized)
        self.assertIn("246-for-246 two-route agreement", normalized)
        self.assertIn("zero false case-level theorem tags", normalized)

    def test_rq007500_genuine_recovery_repasses(self):
        recovery = load("artifacts/rq007500-genuine-recovery-v1.json")
        self.assertEqual(recovery["verdict"]["outcome"], "RE_PASSES")
        self.assertEqual(
            recovery["verdict"]["effective_tag"],
            "VERIFIED_W2_GENUINE_RECOVERY",
        )
        self.assertEqual(
            recovery["genuine_reconstruction"][
                "normal_closure_group_id"
            ],
            [32, 38],
        )
        self.assertTrue(
            recovery["genuine_reconstruction"][
                "identical_to_historical_polynomial"
            ]
        )
        self.assertEqual(
            recovery["genuine_reconstruction"][
                "independent_ray_reconstruction_matches"
            ],
            [True, True],
        )
        ledger = load("artifacts/predicate-provenance-ledger-r13-v1.json")
        self.assertEqual(
            ledger["rq007500_effective_state"],
            "VERIFIED_W2_GENUINE_RECOVERY",
        )

    def test_genuine_anchor_gates_are_closed(self):
        b = load("artifacts/genuine-b-battery-anchor-v2.json")
        full = load("artifacts/r13-genuine-anchor-reproduction-v1.json")
        self.assertEqual(b["predicate_provenance"], "GENUINE")
        self.assertEqual(b["passed_anchor_count"], 3)
        self.assertEqual(
            b["verdict"], "GENUINE_B_ANCHORS_3_OF_3_PASSED"
        )
        self.assertEqual(full["completed_anchor_count"], 7)
        self.assertEqual(full["verdict"], "ANCHOR_GATE_PASSED")

    def test_results_paper_is_count_independent(self):
        paper = (ROOT / "paper/effective-stark-results-paper.md").read_text()
        self.assertIn("Results-paper scope:** FROZEN", paper)
        self.assertIn("first order-six", paper)
        self.assertIn("first unconditional order-ten", paper)
        self.assertIn("absolute-abelian one-place obstruction", paper)
        seal = load("artifacts/results-paper-scope-seal-v1.json")
        self.assertEqual(
            seal["paper_sha256"],
            hashlib.sha256(paper.encode()).hexdigest(),
        )
        self.assertIn(
            "FRONTIER share versus conductor norm",
            seal["excluded_claim_families"],
        )

    def test_recovery_claim_boundary_is_frozen(self):
        plan = load("artifacts/r13-recovery-plan-and-claim-boundary-v1.json")
        self.assertEqual(
            plan["status"],
            "FROZEN_BEFORE_POPULATION_RECLASSIFICATION",
        )
        self.assertEqual(
            [row["population"] for row in plan["strict_order"]],
            [241, 252, 8200],
        )
        self.assertFalse(plan["census_v5_gate"]["open"])
        self.assertIn(
            "all 25 promoted case-level theorem identities",
            plan["claims_that_cannot_change"],
        )
        self.assertTrue(
            plan["trend_status"].startswith("PROVISIONAL_WITHDRAWN")
        )


if __name__ == "__main__":
    unittest.main()
