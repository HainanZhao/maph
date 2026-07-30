import hashlib
import json
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]


def load(path: str) -> dict:
    return json.loads((ROOT / path).read_text(encoding="utf-8"))


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


class Cycle066Test(unittest.TestCase):
    def test_normalization_formulas_and_plain_identity(self):
        theory = load("data/engine-c-general-e-theory-v2.json")
        self.assertEqual(
            theory["formulas"]["class_log_forward"],
            "zeta'_S(0,g)=-(2/e)*ell_g",
        )
        self.assertEqual(
            theory["formulas"]["direct_lprime_forward"],
            "L'_S(0,psi)=-(4/e)*(ell_1-i*ell_sigma)",
        )
        identity = theory["rq000458_plain_identity"]
        self.assertEqual(identity["field"], "Q(sqrt(14))")
        self.assertEqual(identity["finite_ideal_hnf"], [[12, 0], [0, 6]])
        self.assertEqual(identity["support_orders"], [4])

    def test_root_reality_is_precisely_scoped(self):
        roots = load("artifacts/engine-c-packet-root-reality-v1.json")
        self.assertEqual(roots["packet_signature"], [4, 2])
        self.assertIn("not the first", roots["pattern"])
        for route in roots["routes"]:
            self.assertEqual(
                route["conjugation_fixed_artin_class_count"], 4
            )
            self.assertEqual(route["compatible_normal_embedding_count"], 8)

    def test_hard_controls_replay_byte_identically(self):
        gate = load("artifacts/engine-c-reproduction-gate-v1.json")
        self.assertEqual(gate["generic_pipeline_execution_count"], 2)
        self.assertTrue(gate["byte_identical_record_replay"])
        self.assertTrue(gate["byte_identical_transcript_replay"])
        self.assertTrue(gate["rq000458_c_side_reproduced"])
        self.assertTrue(gate["q6_algebraic_half_reproduced"])
        q6_secondary = next(
            row
            for row in gate["records"]
            if row["case_id"] == "RQ-000129"
            and row["route_id"] == "Qsqrt(-3)"
        )
        self.assertTrue(q6_secondary["relative_abelian_certified"])
        self.assertFalse(q6_secondary["pari_rnfisabelian_diagnostic"])
        self.assertGreater(
            q6_secondary["classfield_roundtrip_isomorphism_count"], 0
        )
        for version in range(3):
            self.assertTrue(
                (
                    ROOT
                    / f"artifacts/engine-c-reproduction-gate-failed-v{version}.txt"
                ).exists()
            )

    def test_first_e6_tranche_is_fully_verified(self):
        seal = load("artifacts/engine-c-e6-tranche-01-verified-v1.json")
        self.assertEqual(seal["claim_tag"], "VERIFIED")
        self.assertEqual(seal["field_count"], 3)
        self.assertEqual(seal["occurrence_count"], 14)
        self.assertEqual(
            [row["canonical_case_id"] for row in seal["bundles"]],
            ["RQ-001569", "RQ-007519", "RQ-001894"],
        )
        self.assertTrue(all(seal["gates"].values()))

    def test_q6_auxiliary_prime_closure(self):
        q6 = load("data/q6-norm8-case-v2.json")
        cert = load("artifacts/q6-auxiliary-prime-independence-v1.json")
        self.assertEqual(q6["verdict"], "VERIFIED")
        self.assertEqual(cert["auxiliary_primes"], [3, 5])
        self.assertEqual(
            cert["exact_euler_multipliers_at_s0"],
            {"3": "1+i", "5": "2"},
        )
        self.assertTrue(cert["normalized_q_independence"])
        self.assertEqual(cert["verdict"], "VERIFIED")
        for route in cert["route_records"]:
            self.assertEqual(route["q5_group_ring_relation"], "2*natural")

    def test_odd_index_correlates(self):
        audit = load("artifacts/frontier-odd-index-correlates-v1.json")
        population = audit["odd_population"]
        self.assertEqual(population["row_count"], 88)
        self.assertEqual(
            population["commutator_equals_shintani_index_count"], 85
        )
        self.assertEqual(
            population["support_shares_odd_prime_with_index_count"], 86
        )
        self.assertEqual(
            audit["three_primary_support_contingency"]["odd_index"][
                "share"
            ]["reduced"],
            "10/11",
        )

    def test_engine_d_inventory(self):
        engine_d = load("artifacts/engine-d-index-one-candidates-v1.json")
        counts = engine_d["counts"]
        self.assertEqual(
            counts["all_index_one_abelian_over_q_occurrences"], 3521
        )
        self.assertEqual(
            counts["substantive_frontier_engine_d_candidates"], 276
        )
        self.assertEqual(
            counts["substantive_frontier_engine_d_fields"], 85
        )
        self.assertEqual(
            [row["case_id"] for row in engine_d["examples"]],
            ["RQ-000018", "RQ-000032", "RQ-000274"],
        )
        self.assertEqual(
            engine_d["engine_d_question"]["status"],
            "CONJECTURAL_ENGINE_DESIGN_NOT_YET_A_THEOREM",
        )

    def test_new_artifact_source_hashes_replay(self):
        paths = [
            "artifacts/engine-c-reproduction-gate-v1.json",
            "artifacts/engine-c-e6-tranche-01-verified-v1.json",
            "artifacts/q6-auxiliary-prime-independence-v1.json",
            "artifacts/frontier-odd-index-correlates-v1.json",
            "artifacts/engine-d-index-one-candidates-v1.json",
        ]
        for artifact_path in paths:
            artifact = load(artifact_path)
            for relative, expected in artifact["source_hashes"].items():
                self.assertEqual(
                    sha(ROOT / relative),
                    expected,
                    f"{artifact_path}: {relative}",
                )


if __name__ == "__main__":
    unittest.main()
