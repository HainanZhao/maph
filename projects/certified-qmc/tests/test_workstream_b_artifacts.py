from __future__ import annotations

from hashlib import sha256
import json
from pathlib import Path
import subprocess
import sys
import unittest

from src.certificate import canonical_sha256, verify_certificate


PROJECT = Path(__file__).resolve().parents[1]


def load(name: str):
    return json.loads((PROJECT / "certificates" / name).read_text())


def digest(path: Path) -> str:
    return sha256(path.read_bytes()).hexdigest()


class WorkstreamBArtifactTests(unittest.TestCase):
    def test_fftw_plan_metadata_is_complete_and_deterministic(self):
        artifact = load("workstream-b-fftw-plan-audit.json")
        self.assertEqual(artifact["claim_tag"], "VERIFIED_PLAN_METADATA")
        self.assertTrue(
            artifact["replay"]["identical_consecutive_transcripts"]
        )
        self.assertEqual(artifact["environment"]["rounding_mode"], "0")
        self.assertEqual(artifact["environment"]["planner_flag"], "FFTW_ESTIMATE")
        plans = artifact["plans"]
        self.assertEqual(len(plans), 38)
        for exponent in range(19):
            selected = [
                plan for plan in plans if plan["length"] == 2**exponent
            ]
            self.assertEqual(
                {plan["direction"] for plan in selected}, {"r2c", "c2r"}
            )
            for plan in selected:
                self.assertGreaterEqual(plan["adds"], 0)
                self.assertGreaterEqual(plan["muls"], 0)
                self.assertGreaterEqual(plan["fmas"], 0)
                self.assertTrue(plan["description"])
        source = (
            PROJECT
            / "tools"
            / "numerical-crosscheck"
            / "native"
            / "fftw_plan_audit.c"
        )
        self.assertEqual(
            digest(source), artifact["artifacts"]["source_sha256"]
        )
        self.assertIn(
            "not themselves a proof", artifact["boundary"]
        )

    def test_direct_error_certificate_contains_independent_oracles(self):
        artifact = load("workstream-b-direct-producer-bound.json")
        self.assertEqual(
            artifact["claim_tag"], "ENCLOSED_DIRECT_PRODUCER_ERROR"
        )
        self.assertTrue(
            artifact["gate"]["all_independent_arb_targets_contained"]
        )
        for case in artifact["adversarial_cases"]:
            result = case["result"]
            self.assertTrue(result["contains_independent_arb_target"])
            self.assertIn("forward_error_bound", result)
            self.assertGreater(result["operation_counts"]["mul"], 0)
        source = PROJECT / artifact["source_artifacts"]["implementation"]
        test = PROJECT / artifact["source_artifacts"]["test"]
        self.assertEqual(
            digest(source),
            artifact["source_artifacts"]["implementation_sha256"],
        )
        self.assertEqual(
            digest(test), artifact["source_artifacts"]["test_sha256"]
        )
        self.assertIn("does not bound FFTW", artifact["boundary"])

    def test_compiled_latnet_midpoints_are_bit_identical(self):
        artifact = load("workstream-b-latnet-direct-replay.json")
        self.assertEqual(
            artifact["claim_tag"], "VERIFIED_DIRECT_MIDPOINT_REPLAY"
        )
        self.assertTrue(artifact["gate"]["all_midpoints_bit_identical"])
        self.assertTrue(
            artifact["gate"]["all_independent_targets_contained"]
        )
        for case in artifact["cases"]:
            self.assertTrue(case["bit_identical_midpoint"])
            self.assertEqual(
                case["latnet_float_hex"], case["replay_float_hex"]
            )
        self.assertIn("does not validate fast-CBC", artifact["boundary"])

    def test_synthetic_fastcbc_branches_are_certified_but_gate_stays_closed(self):
        artifact = load("workstream-b-fastcbc-synthetic-transcript.json")
        self.assertEqual(
            artifact["claim_tags"]["fast_candidate_decisions"],
            "ENCLOSED_OR_EXACT_TIE_CERTIFIED_SYNTHETIC",
        )
        gate = artifact["gate"]
        self.assertTrue(gate["all_fast_branches_certified"])
        self.assertTrue(gate["all_direct_midpoints_replayed"])
        self.assertFalse(gate["fft_forward_error_bound_complete"])
        self.assertFalse(gate["external_comparison_authorized"])
        exact_tie_count = 0
        for case in artifact["cases"]:
            branch = case["branch_certificate"]
            self.assertTrue(branch["all_branches_certified"])
            for stage in branch["stages"]:
                self.assertTrue(
                    stage["all_competitors_nonnegative_or_exact_ties"]
                )
                exact_tie_count += len(stage["exact_tied_competitors"])
        self.assertEqual(exact_tie_count, 3)
        self.assertIn(
            "not a general FFT forward-error bound", artifact["boundary"]
        )

    def test_format_preflight_has_no_external_merit(self):
        artifact = load("workstream-b-format-bound-preflight.json")
        self.assertEqual(
            artifact["claim_tag"], "VERIFIED_EXACT_FORMAT_CELLS"
        )
        self.assertEqual(
            artifact["current_frozen_set"]["merit_column_count"], 0
        )
        self.assertEqual(
            artifact["current_frozen_set"]["format_bounds_required"], 0
        )
        self.assertIn("No external merit", artifact["boundary"])

    def test_radix2_model_transform_gate(self):
        artifact = load("workstream-b-radix2-model.json")
        self.assertEqual(
            artifact["claim_tag"], "VERIFIED_MODEL_TRANSFORM_BOUND"
        )
        self.assertTrue(artifact["gate"]["all_twiddles_contained"])
        self.assertTrue(artifact["gate"]["all_transforms_contained"])
        self.assertEqual(len(artifact["validation"]), 12)
        self.assertEqual(len(artifact["sensitivity"]), 2)
        self.assertIn(
            "must additionally compose", artifact["boundary"]
        )

    def test_vector_only_reference_table_replays_every_prefix(self):
        artifact = load("workstream-b-unsw-prefix-reference-table.json")
        supplied_hash = artifact.pop("table_sha256")
        self.assertEqual(canonical_sha256(artifact), supplied_hash)
        self.assertEqual(
            artifact["tag"], "VERIFIED_REFERENCE_TABLE_PREFIX"
        )
        self.assertFalse(artifact["published_merit_values_present"])
        self.assertFalse(
            artifact["external_merit_subtractions_performed"]
        )
        self.assertFalse(
            artifact["target"]["full_upstream_table_certified"]
        )
        self.assertEqual(artifact["dimensions"], list(range(1, 17)))
        self.assertEqual(len(artifact["rows"]), 16)
        for dimension, row in enumerate(artifact["rows"], start=1):
            self.assertEqual(row["dimension"], dimension)
            self.assertTrue(verify_certificate(row["core_certificate"]))

    def test_one_command_reference_entry_replay(self):
        completed = subprocess.run(
            [
                sys.executable,
                str(PROJECT / "scripts" / "verify_certificate.py"),
                str(
                    PROJECT
                    / "certificates"
                    / "workstream-b-unsw-prefix-reference-table.json"
                ),
                "--dimension",
                "7",
            ],
            check=True,
            capture_output=True,
            text=True,
        )
        result = json.loads(completed.stdout)
        self.assertEqual(result["dimension"], 7)
        self.assertEqual(
            result["status"], "VERIFIED_REFERENCE_ENTRY_REPLAY"
        )

    def test_full_grid_budget_is_exact_and_blocks_production(self):
        artifact = load("workstream-b-production-budget.json")
        supplied_hash = artifact.pop("certificate_sha256")
        self.assertEqual(canonical_sha256(artifact), supplied_hash)
        self.assertEqual(
            artifact["claim_tag"], "VERIFIED_PRECOMPUTE_BOUND_BUDGET"
        )
        worst = artifact["worst_cell"]
        self.assertEqual(worst["N"], 2**20)
        self.assertEqual(worst["dimension"], 3600)
        self.assertEqual(worst["weight_profile"], "gamma_j=1/j^2")
        self.assertEqual(worst["proved_reconstruction_bits"], 228015)
        self.assertEqual(
            worst["conservative_61_bit_work_primes"], 3738
        )
        self.assertEqual(
            artifact["totals"]["combined_direct_update_lower_bound"],
            54901459582976,
        )
        self.assertFalse(
            artifact["gate"]["full_production_authorized"]
        )

    def test_failed_streaming_pilot_is_preserved(self):
        artifact = load("workstream-b-streaming-pilot-failed-v1.json")
        supplied_hash = artifact.pop("certificate_sha256")
        self.assertEqual(canonical_sha256(artifact), supplied_hash)
        self.assertFalse(
            artifact["correctness"]["all_selected_residues_match"]
        )
        self.assertTrue(
            artifact["decision"]["throughput_pass"]
        )
        self.assertTrue(
            artifact["decision"]["replay_overhead_pass"]
        )
        self.assertEqual(
            artifact["decision"]["disposition"], "REDESIGN_REQUIRED"
        )

    def test_streaming_pilot_passes_prospective_gate(self):
        artifact = load("workstream-b-streaming-pilot.json")
        supplied_hash = artifact.pop("certificate_sha256")
        self.assertEqual(canonical_sha256(artifact), supplied_hash)
        self.assertEqual(
            digest(PROJECT / artifact["implementation"]["source"]),
            artifact["implementation"]["source_sha256"],
        )
        self.assertEqual(len(artifact["runs"]), 5)
        self.assertEqual(artifact["prime_schedule"]["work_count"], 151)
        self.assertEqual(artifact["prime_schedule"]["overflow_count"], 2)
        self.assertEqual(
            artifact["measurement"]["work_updates_per_run"], 39583744
        )
        self.assertEqual(
            artifact["measurement"]["full_grid_work_updates"],
            54901459582976,
        )
        self.assertEqual(
            artifact["measurement"]["state_bytes_per_prime"], 8192
        )
        self.assertTrue(
            artifact["correctness"]["all_selected_residues_match"]
        )
        self.assertEqual(
            len(
                artifact["correctness"]["selected_residue_checks"]
            ),
            25,
        )
        self.assertTrue(
            all(
                check["equal"]
                for check in artifact["correctness"][
                    "selected_residue_checks"
                ]
            )
        )
        self.assertTrue(
            artifact["correctness"]["all_checkpoint_replays_pass"]
        )
        self.assertTrue(
            artifact["correctness"][
                "overflow_primes_evaluated_for_every_prefix"
            ]
        )
        decision = artifact["decision"]
        expected = (
            decision["correctness_pass"]
            and artifact["measurement"]["projected_node_days"]
            <= decision["frozen_maximum_node_days"]
            and artifact["measurement"][
                "median_replay_overhead_fraction"
            ]
            <= decision["frozen_maximum_replay_overhead_fraction"]
        )
        self.assertEqual(
            decision["full_exact_fidelity_grid_authorized"], expected
        )
        self.assertTrue(expected)
        self.assertEqual(
            decision["disposition"],
            "FULL_EXACT_FIDELITY_GRID_AUTHORIZED",
        )
        self.assertFalse(artifact["fallback"]["applied"])
        self.assertTrue(
            artifact["budget_reconciliation"][
                "incremental_count_matches_preflight"
            ]
        )
        self.assertFalse(
            artifact["budget_reconciliation"][
                "per_cell_from_scratch_used"
            ]
        )


if __name__ == "__main__":
    unittest.main()
