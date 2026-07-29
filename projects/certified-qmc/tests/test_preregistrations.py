from __future__ import annotations

from fractions import Fraction
from hashlib import sha256
import json
from pathlib import Path
import unittest

from src.ntt_prime import generate_ntt_prime_schedule
from src.scaled_integer import (
    balanced_crt_bits,
    candidate_difference_bound,
    error_numerator_bound,
)


PROJECT = Path(__file__).resolve().parents[1]
FROZEN_AT = "2026-07-29T04:24:47Z"


def canonical_digest(value) -> str:
    return sha256(
        json.dumps(
            value,
            sort_keys=True,
            separators=(",", ":"),
            ensure_ascii=True,
        ).encode("ascii")
    ).hexdigest()


class PreregistrationTests(unittest.TestCase):
    def load(self, folder: str, name: str):
        return json.loads((PROJECT / folder / name).read_text())

    def test_workstream_b_gate_precedes_external_merit_data(self):
        gate = self.load(
            "data", "workstream-b-discrepancy-preregistration.json"
        )
        self.assertEqual(gate["frozen_at_utc"], FROZEN_AT)
        status = gate["status_at_freeze"]
        self.assertFalse(status["published_merit_values_acquired"])
        self.assertFalse(
            status["exact_vs_published_merit_comparisons_performed"]
        )
        self.assertEqual(
            gate["classification"]["discrepancy_predicate"],
            "abs(y-q)>B_alg",
        )
        self.assertEqual(
            gate["classification"]["missing_bound_classification"],
            "UNCLASSIFIED_EXTERNAL",
        )
        self.assertTrue(
            gate["workstream_b_merit_computation_blocked_until_gate_replays"]
        )

    def test_workstream_b_inventory_has_no_merit_bearing_frozen_table(self):
        inventory = self.load(
            "data", "workstream-b-table-inventory.json"
        )
        self.assertEqual(inventory["counts"]["frozen_tables"], 1)
        self.assertEqual(
            inventory["counts"]["frozen_tables_with_merit_columns"], 0
        )
        self.assertEqual(
            inventory["counts"]["frozen_tables_without_merit_columns"], 1
        )
        for target in inventory["frozen_audit_set"]:
            self.assertFalse(target["merit_column_present"])
            self.assertIsNone(target["published_merit_precision"])
            self.assertEqual(
                target["classification_track"],
                "CERTIFIED_REFERENCE_MERIT_ONLY",
            )

    def test_workstream_b_v2_excludes_selection_and_stays_closed(self):
        gate = self.load(
            "data", "workstream-b-classification-v2.json"
        )
        self.assertTrue(gate["does_not_apply_retroactively"])
        self.assertFalse(gate["selection"]["included_in_B_alg"])
        self.assertEqual(
            gate["bound"]["formula"],
            "B_alg(M)=T_eval(M)+T_format",
        )
        self.assertEqual(
            gate["bound"]["missing_model_or_format_classification"],
            "UNCLASSIFIED_EXTERNAL",
        )
        self.assertFalse(gate["external_subtraction_authorized"])
        self.assertEqual(
            gate["current_frozen_set_disposition"],
            "NO_MERIT_COLUMNS; CERTIFIED_REFERENCE_MERITS ONLY",
        )

    def test_literature_perimeter_precedes_and_bounds_the_sweep(self):
        perimeter = self.load(
            "data", "workstream-b-literature-perimeter.json"
        )
        status = perimeter["status_at_freeze"]
        self.assertFalse(status["paper_bodies_inspected_for_merit_values"])
        self.assertFalse(status["numerical_merit_values_acquired"])
        self.assertFalse(
            status["exact_minus_published_merit_subtractions_performed"]
        )
        self.assertEqual(len(perimeter["papers"]), 6)
        self.assertFalse(perimeter["external_subtraction_authorized"])

        sweep = self.load(
            "data", "workstream-b-literature-sweep.json"
        )
        self.assertEqual(sweep["papers_inspected"], 6)
        self.assertEqual(
            sweep["papers_with_values_attached_to_frozen_vectors"], 0
        )
        self.assertEqual(sweep["qualifying_classification_targets"], 0)
        self.assertFalse(sweep["external_merit_subtractions_performed"])
        self.assertEqual(
            sweep["classification_branch"],
            "CLOSED_FOR_FROZEN_PERIMETER",
        )

    def test_production_grid_and_compute_gate_are_frozen(self):
        freeze = self.load(
            "data", "workstream-b-production-freeze.json"
        )
        self.assertEqual(
            freeze["fidelity_grid"]["modulus_exponents"],
            list(range(10, 21)),
        )
        self.assertEqual(
            freeze["fidelity_grid"]["dimensions"],
            "every prefix 1 through 3600",
        )
        self.assertEqual(
            [item["formula"] for item in freeze["weight_profiles"]],
            ["gamma_j=1/j^2", "gamma_j=1/j", "gamma_j=1/j^3"],
        )
        self.assertFalse(
            freeze["compute_gate"]["production_compute_authorized"]
        )

    def test_streaming_threshold_precedes_both_measurements(self):
        original = self.load(
            "data", "workstream-b-streaming-pilot-preregistration.json"
        )
        amended = self.load(
            "data",
            "workstream-b-streaming-pilot-preregistration-v2.json",
        )
        self.assertFalse(original["measurement_started"])
        self.assertFalse(amended["measurement_started"])
        for gate in (original, amended):
            self.assertEqual(
                gate["incremental_accounting"][
                    "full_grid_work_updates"
                ],
                54901459582976,
            )
            self.assertTrue(
                gate["incremental_accounting"][
                    "per_cell_from_scratch_forbidden"
                ]
            )
            self.assertEqual(
                gate["production_decision"][
                    "reference_budget_node_days"
                ],
                7,
            )
            self.assertEqual(
                Fraction(
                    gate["production_decision"][
                        "maximum_replay_overhead_fraction"
                    ]
                ),
                Fraction(15, 100),
            )
            self.assertEqual(
                gate["pilot"]["universal_overflow_check_primes"], 2
            )
            self.assertTrue(
                gate["artifact_geometry"][
                    "two_overflow_primes_universal"
                ]
            )
            self.assertEqual(
                gate["artifact_geometry"][
                    "worst_entry_work_residue_bytes"
                ],
                29904,
            )
        self.assertEqual(
            original["production_decision"],
            amended["production_decision"],
        )
        self.assertEqual(
            original["no_go_fallback"], amended["no_go_fallback"]
        )
        self.assertEqual(
            amended["predecessor"]["sha256"],
            sha256(
                (
                    PROJECT
                    / "data"
                    / "workstream-b-streaming-pilot-preregistration.json"
                ).read_bytes()
            ).hexdigest(),
        )
        self.assertEqual(
            amended["predecessor"]["failed_transcript_sha256"],
            sha256(
                (
                    PROJECT
                    / "certificates"
                    / "workstream-b-streaming-pilot-failed-v1.json"
                ).read_bytes()
            ).hexdigest(),
        )

    def test_extended_schedule_replays(self):
        artifact = self.load(
            "certificates", "cycle-009-prime-schedule-40.json"
        )
        supplied_hash = artifact.pop("schedule_sha256")
        self.assertEqual(canonical_digest(artifact), supplied_hash)
        self.assertEqual(
            artifact["primes"], generate_ntt_prime_schedule(40)
        )

    def test_cycle009_bounds_rate_and_hash_replay(self):
        checkpoint = self.load(
            "certificates", "cycle-009-preregistration.json"
        )
        supplied_hash = checkpoint.pop("checkpoint_sha256")
        self.assertEqual(canonical_digest(checkpoint), supplied_hash)
        self.assertEqual(checkpoint["frozen_at_utc"], FROZEN_AT)
        self.assertFalse(checkpoint["data_run_started"])

        weights = [Fraction(1, j * j) for j in range(1, 51)]
        difference = candidate_difference_bound(
            2**16, weights[:-1], weights[-1]
        )
        final = error_numerator_bound(2**16, weights)
        budget = checkpoint["crt_budget"]
        self.assertEqual(int(budget["candidate_difference_bound"]), difference)
        self.assertEqual(
            budget["candidate_crt_required_bits"],
            balanced_crt_bits(difference),
        )
        self.assertEqual(int(budget["final_error_bound"]), final)
        self.assertEqual(
            budget["final_error_crt_required_bits"],
            balanced_crt_bits(final),
        )
        decision = checkpoint["decision_protocol"]
        self.assertEqual(decision["comparison_count"], 802767)
        self.assertEqual(decision["maximum_exact_crt_escalations"], 802)
        self.assertEqual(
            decision["acceptance_predicate"],
            "exact_crt_escalation_rate<0.001",
        )
        self.assertTrue(budget["schedule_covers_final_plus_overflow"])

    def test_cycle009_arb_first_amendment_replays(self):
        checkpoint = self.load(
            "certificates", "cycle-009-preregistration-v2-arb106.json"
        )
        supplied_hash = checkpoint.pop("checkpoint_sha256")
        self.assertEqual(canonical_digest(checkpoint), supplied_hash)
        self.assertFalse(checkpoint["data_run_started"])
        architecture = checkpoint["primary_decision_architecture"]
        self.assertEqual(
            architecture["shadow"], "compiled Arb balls at 106-bit precision"
        )
        self.assertFalse(architecture["double_double_enabled"])
        gate = checkpoint["unchanged_acceptance_gate"]
        self.assertEqual(gate["comparison_count"], 802767)
        self.assertEqual(gate["maximum_passing_count"], 802)
        self.assertEqual(gate["predicate"], "exact_crt_escalated<803")
        conditional = checkpoint["conditional_double_double_optimization"]
        self.assertFalse(conditional["authorized_before_arb_profile"])
        self.assertTrue(conditional["same_final_vector_alone_is_insufficient"])

    def test_cycle009_is_explicitly_deferred_without_changing_gate(self):
        rescope = self.load("data", "cycle-009-rescope.json")
        self.assertEqual(
            rescope["execution_state"], "PREREGISTERED_NOT_RUN"
        )
        self.assertFalse(rescope["cancelled"])
        self.assertEqual(
            rescope["new_role"],
            "Workstream C entry gate for certified-CBC construction claims",
        )
        gate = rescope["unchanged_gate"]
        self.assertEqual(gate["comparison_count"], 802767)
        self.assertEqual(
            gate["maximum_passing_exact_crt_escalations"], 802
        )
        self.assertEqual(gate["predicate"], "exact_crt_escalated<803")
