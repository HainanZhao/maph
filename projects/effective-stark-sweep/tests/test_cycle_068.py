import hashlib
import json
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]


def load(path: str) -> dict:
    return json.loads((ROOT / path).read_text(encoding="utf-8"))


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


class Cycle068Test(unittest.TestCase):
    def test_paper_contains_the_single_conjugation_lemma(self):
        paper = (ROOT / "paper/effective-stark-sweep-draft.md").read_text(
            encoding="utf-8"
        )
        self.assertIn("Lemma (absolute-abelian one-place obstruction)", paper)
        self.assertIn("are the same single element", paper)
        self.assertIn("never governed by an absolutely abelian ray field", paper)
        self.assertIn("no fourth abelian", paper)

    def test_proxy_scope_names_every_load_bearing_stage(self):
        audit = load("artifacts/proxy-scope-and-tag-audit-v1.json")
        stages = {row["stage"]: row for row in audit["pipeline_scope"]}
        self.assertEqual(len(stages), 9)
        self.assertTrue(
            stages["W1_ENGINE_B_ROUTING_AND_INDEX_TAXONOMY"][
                "proxy_used"
            ]
        )
        self.assertTrue(
            stages["W1_ENGINE_C_STRUCTURAL_PREFILTER"]["proxy_used"]
        )
        self.assertTrue(stages["GENERIC_ENGINE_B_W2"]["proxy_used"])
        self.assertFalse(
            stages["COMPLETE_ENGINE_C_GEOMETRY_AND_W3"]["proxy_used"]
        )
        self.assertFalse(stages["W1_FOURIER_SUPPORT"]["proxy_used"])

    def test_code_paths_match_the_scope_attestation(self):
        b = (ROOT / "scripts/screen_engine_b_two_route.gp").read_text()
        c = (ROOT / "scripts/screen_engine_c_geometry.gp").read_text()
        c_analysis = (
            ROOT / "scripts/analyze_engine_c_geometry.py"
        ).read_text()
        self.assertIn("normal_relative = bnrclassfield(ray_both", b)
        self.assertNotIn("nfsplitting", b)
        self.assertIn("nfsplitting(absolute", c)
        self.assertIn('row["shintani_index"] == 2', c_analysis)

    def test_no_promoted_theorem_case_depends_on_proxy(self):
        audit = load("artifacts/proxy-scope-and-tag-audit-v1.json")
        tags = audit["verified_case_tag_audit"]
        self.assertEqual(tags["census_theorem_case_count"], 25)
        self.assertEqual(tags["false_case_level_theorem_tags"], 0)
        self.assertTrue(tags["engine_b_all_moduli_stable"])
        self.assertTrue(tags["engine_c_actual_splitting_closure_proof_chain"])
        self.assertEqual(
            tags["engine_c_unstable_but_proxy_independent_case_ids"],
            ["RQ-007577"],
        )

    def test_intermediate_w2_tag_family_is_honestly_superseded(self):
        audit = load("artifacts/proxy-scope-and-tag-audit-v1.json")
        correction = audit["intermediate_tag_correction"]
        self.assertFalse(
            correction["strong_zero_false_tags_sentence_permitted"]
        )
        self.assertEqual(correction["completed_w2_closures"], 51)
        self.assertEqual(correction["genuine_stable_w2_closures"], 50)
        self.assertEqual(
            correction["superseded_w2_closure_case_ids"],
            ["RQ-007500"],
        )
        self.assertEqual(correction["member_transport_state"], "PENDING")

    def test_recovery_queue_covers_all_proxy_exposure(self):
        recovery = load("artifacts/proxy-recovery-queue-v1.json")
        b = recovery["engine_b_actual_normal_closure"]
        self.assertEqual(b["case_count"], 241)
        self.assertEqual(b["former_proxy_pass_pending_count"], 64)
        self.assertEqual(b["former_proxy_negative_withdrawn_count"], 177)
        self.assertEqual(
            len(set(b["case_ids"])),
            241,
        )
        self.assertEqual(
            recovery["engine_c_catch_up_geometry"]["case_count"], 252
        )
        index = recovery["entire_index_distribution_rerun"]
        self.assertEqual(index["representative_count"], 8200)
        self.assertEqual(
            index["stable_modulus_direct_reconstruction_count"], 2461
        )
        self.assertEqual(
            index["unstable_modulus_actual_normal_closure_count"], 5739
        )
        self.assertFalse(recovery["w4_gate"]["open"])
        self.assertTrue(recovery["five_exception_files_retained"])

    def test_census_v4_is_exact_and_does_not_double_count(self):
        v4 = load("artifacts/full-census-yield-declaration-v4.json")
        self.assertEqual(v4["representative_count"], 8200)
        self.assertEqual(
            sum(
                row["row_occurrences"]
                for row in v4["histogram"].values()
            ),
            8200,
        )
        accounting = v4["accounting"]
        self.assertEqual(accounting["substantive_safe_eligible"], 2419)
        self.assertEqual(accounting["substantive_pending_b"], 64)
        self.assertEqual(
            accounting["frontier_proxy_negative_withdrawn_pending"], 177
        )
        overlap = v4["index_one_proxy_overlap_no_double_count"]
        self.assertEqual(
            overlap["inside_proved_trivial"]
            + overlap["inside_substantive_engine_a"]
            + overlap["proposed_engine_d_rejected_and_retained_in_frontier"],
            overlap["proxy_rows"],
        )
        self.assertEqual(
            v4["rejected_engine_d_split"]["status"],
            "PROPOSED_AND_REJECTED",
        )
        self.assertEqual(
            v4["tag_history"]["false_case_level_theorem_tags"], 0
        )
        self.assertEqual(
            v4["tag_history"]["stronger_zero_false_tags_claim"],
            "NOT_MADE",
        )

    def test_new_artifact_source_hashes_replay(self):
        for artifact_path in (
            "artifacts/proxy-scope-and-tag-audit-v1.json",
            "artifacts/proxy-recovery-queue-v1.json",
            "artifacts/full-census-yield-declaration-v4.json",
        ):
            artifact = load(artifact_path)
            for relative, expected in artifact["source_hashes"].items():
                self.assertEqual(
                    sha(ROOT / relative),
                    expected,
                    f"{artifact_path}: {relative}",
                )


if __name__ == "__main__":
    unittest.main()
