#!/usr/bin/env python3
"""Scope the conjugation proxy and audit every promoted theorem tag."""

from __future__ import annotations

from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path

from audit_engine_d_modulus_stability import run_stability_audit


ROOT = Path(__file__).resolve().parents[1]
ARTIFACTS = ROOT / "artifacts"
W1 = ARTIFACTS / "w1-full-census-v1.json"
QUEUES = ARTIFACTS / "identification-queues-v2.json"
C_GEOMETRY = ARTIFACTS / "engine-c-geometry-analysis-v1.json"
B_COVERAGE = ARTIFACTS / "engine-b-closure-w2-coverage-v1.json"
B_ANALYSIS = ARTIFACTS / "engine-b-two-route-analysis-v1.json"
CONTAINMENT = ARTIFACTS / "conjugation-dependent-census-audit-v1.json"
C_FIRST = ARTIFACTS / "engine-c-w3-tranche-01-verified-v1.json"
C_E6 = ARTIFACTS / "engine-c-e6-tranche-01-verified-v1.json"
OUTPUT = ARTIFACTS / "proxy-scope-and-tag-audit-v1.json"
RECOVERY = ARTIFACTS / "proxy-recovery-queue-v1.json"

B_VERIFIED_CASES = {
    "RQ-000021",
    "RQ-000108",
    "RQ-000190",
    "RQ-000419",
    "RQ-000458",
    "RQ-001107",
    "RQ-002057",
    "RQ-002955",
}
C_STANDALONE_VERIFIED_CASES = {
    "RQ-000129",
    "RQ-000458",
}


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    w1 = json.loads(W1.read_text(encoding="utf-8"))
    rows = w1["records"]
    by_id = {row["case_id"]: row for row in rows}
    stability = run_stability_audit(rows)
    queues = json.loads(QUEUES.read_text(encoding="utf-8"))
    c_geometry = json.loads(C_GEOMETRY.read_text(encoding="utf-8"))
    b_coverage = json.loads(B_COVERAGE.read_text(encoding="utf-8"))
    b_analysis = json.loads(B_ANALYSIS.read_text(encoding="utf-8"))
    containment = json.loads(CONTAINMENT.read_text(encoding="utf-8"))
    c_first = json.loads(C_FIRST.read_text(encoding="utf-8"))
    c_e6 = json.loads(C_E6.read_text(encoding="utf-8"))

    c_verified = {
        row["case_id"] for row in c_first["members"]
    } | {
        occurrence["case_id"]
        for bundle in c_e6["bundles"]
        for occurrence in bundle["occurrences"]
    } | C_STANDALONE_VERIFIED_CASES
    theorem_case_ids = B_VERIFIED_CASES | c_verified
    if not all(stability[case_id] for case_id in B_VERIFIED_CASES):
        raise RuntimeError("a promoted Engine-B theorem has unstable modulus")

    screened_c = {
        record["case_id"] for record in c_geometry["packet_records"]
    }
    unscreened_quartic = {
        row["case_id"]
        for row in rows
        if row["support_count"] > 0
        and row["max_support_order"] == 4
        and row["case_id"] not in screened_c
    }
    if len(unscreened_quartic) != 252:
        raise RuntimeError("quartic proxy-exclusion population changed")

    b_pending = set(
        containment["engine_b_containment"][
            "quarantined_unstable_case_ids"
        ]
    )
    if len(b_pending) != 64:
        raise RuntimeError("B quarantine population changed")
    if b_pending & unscreened_quartic:
        raise RuntimeError("B and quartic recovery queues unexpectedly overlap")

    b_screened = {
        record["case_id"] for record in b_analysis["records"]
    }
    b_unstable_screened = {
        case_id for case_id in b_screened if not stability[case_id]
    }
    b_unstable_negative = {
        record["case_id"]
        for record in b_analysis["records"]
        if not stability[record["case_id"]]
        and record["classification"] == "NO_ABELIAN_IMAGINARY_BASE"
    }
    if len(b_unstable_screened) != 241:
        raise RuntimeError("unstable B screen population changed")
    if len(b_unstable_negative) != 177:
        raise RuntimeError("unstable B negative population changed")
    if b_unstable_screened != b_pending | b_unstable_negative:
        raise RuntimeError("unstable B proxy outcomes do not partition")

    closure_representatives = {
        record["canonical_representative"]
        for record in b_coverage["closures"]
    }
    stable_closures = {
        case_id
        for case_id in closure_representatives
        if stability[case_id]
    }
    unstable_closures = closure_representatives - stable_closures
    if unstable_closures != {"RQ-007500"}:
        raise RuntimeError(
            f"unexpected unstable W2 closures: {unstable_closures}"
        )
    closure_members = {
        case_id
        for record in b_coverage["closures"]
        for case_id in record["member_case_ids"]
    }

    unstable_all = {
        case_id for case_id, is_stable in stability.items() if not is_stable
    }
    payload = {
        "schema": "effective-stark-proxy-scope-and-tag-audit-v1",
        "recorded_at_utc": datetime.now(timezone.utc).isoformat(),
        "claim_tag": "VERIFIED_DEPENDENCY_AUDIT",
        "proxy_definition": (
            "the map obtained by applying base conjugation to ideals "
            "and expressing the images in the same ray group without "
            "first requiring the finite modulus to be fixed"
        ),
        "pipeline_scope": [
            {
                "stage": "W1_FOURIER_SUPPORT",
                "proxy_used": False,
                "effect": (
                    "support characters and their orders are intrinsic "
                    "to the one-place ray group"
                ),
            },
            {
                "stage": "W1_ENGINE_A_ROUTING",
                "proxy_used": "diagnostic_only",
                "effect": (
                    "A_ABSOLUTE_CONJUGATION_INVARIANT was recorded, "
                    "but Engine-A routing depends only on support order "
                    "<=2; its 1,560 substantive rows are unaffected"
                ),
            },
            {
                "stage": "W1_ENGINE_B_ROUTING_AND_INDEX_TAXONOMY",
                "proxy_used": True,
                "effect": (
                    "load-bearing for B eligibility, INDEX_GT_2 labels, "
                    "index distributions, and the old norm trend"
                ),
            },
            {
                "stage": "W1_ENGINE_C_STRUCTURAL_PREFILTER",
                "proxy_used": True,
                "effect": (
                    "load-bearing for which quartic rows reached the "
                    "complete geometry screen; 252 supported order-4 "
                    "rows were never screened"
                ),
            },
            {
                "stage": "COMPLETE_ENGINE_C_GEOMETRY_AND_W3",
                "proxy_used": False,
                "effect": (
                    "constructs the actual packet splitting closure by "
                    "nfsplitting and checks its Galois group and CM "
                    "bases; all 728 positive cases and all promoted "
                    "C packets remain valid, but census completeness "
                    "awaits the 252-row catch-up screen"
                ),
            },
            {
                "stage": "C_FAILURE_TO_B_REROUTING",
                "proxy_used": True,
                "effect": (
                    "the reroute test reused W1 shintani_index==2 and "
                    "must be recomputed for unstable moduli"
                ),
            },
            {
                "stage": "GENERIC_ENGINE_B_W2",
                "proxy_used": True,
                "effect": (
                    "screen_engine_b_two_route.gp used the proxy "
                    "commutator-fixed field and called the ray field at "
                    "one finite modulus the normal closure; valid for "
                    "stable moduli only"
                ),
            },
            {
                "stage": "ENGINE_B_W3_PROMOTIONS",
                "proxy_used": "upstream_but_stability_closed",
                "effect": (
                    "every promoted B theorem case has a stable finite "
                    "modulus, so its W2 reconstruction is genuine"
                ),
            },
            {
                "stage": "FRONTIER_INDEX_AND_W4",
                "proxy_used": True,
                "effect": (
                    "all structural index distributions and correlates "
                    "must be rerun on actual normal closures before W4"
                ),
            },
        ],
        "verified_case_tag_audit": {
            "phase0_anchor_packets": {
                "count": 7,
                "proxy_in_proof_chain": False,
                "reason": (
                    "paper-anchor scripts construct their ray fields "
                    "and theorem routes directly"
                ),
            },
            "census_theorem_case_count": len(theorem_case_ids),
            "census_theorem_case_ids": sorted(theorem_case_ids),
            "engine_b_theorem_case_ids": sorted(B_VERIFIED_CASES),
            "engine_b_all_moduli_stable": True,
            "engine_c_theorem_case_ids": sorted(c_verified),
            "engine_c_actual_splitting_closure_proof_chain": True,
            "engine_c_unstable_but_proxy_independent_case_ids": sorted(
                case_id for case_id in c_verified if not stability[case_id]
            ),
            "false_case_level_theorem_tags": 0,
        },
        "intermediate_tag_correction": {
            "strong_zero_false_tags_sentence_permitted": False,
            "reason": (
                "VERIFIED_W2_SCREEN and VERIFIED_W2_TRANCHE were issued "
                "for proxy-dependent classification artifacts; one of "
                "51 completed canonical closure certificates, "
                "RQ-007500, is unstable and is superseded"
            ),
            "defensible_sentence": (
                "Across four accounting revisions, zero false "
                "case-level theorem tags were issued: every predicate "
                "correction preceded W3 promotion. Intermediate "
                "proxy-dependent W2 classification tags are explicitly "
                "superseded in revision v4."
            ),
            "completed_w2_closures": len(closure_representatives),
            "genuine_stable_w2_closures": len(stable_closures),
            "superseded_w2_closure_case_ids": sorted(unstable_closures),
            "closure_member_cases": len(closure_members),
            "closure_member_cases_with_unstable_modulus": sum(
                not stability[case_id] for case_id in closure_members
            ),
            "member_transport_state": "PENDING",
        },
        "source_hashes": {
            str(path.relative_to(ROOT)): sha(path)
            for path in (
                W1,
                QUEUES,
                C_GEOMETRY,
                B_COVERAGE,
                B_ANALYSIS,
                CONTAINMENT,
                C_FIRST,
                C_E6,
                Path(__file__).resolve(),
            )
        },
    }
    OUTPUT.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )

    recovery = {
        "schema": "effective-stark-proxy-recovery-queue-v1",
        "recorded_at_utc": datetime.now(timezone.utc).isoformat(),
        "claim_tag": "FROZEN_RECOVERY_GATE",
        "engine_b_actual_normal_closure": {
            "case_count": len(b_unstable_screened),
            "case_ids": sorted(b_unstable_screened),
            "former_proxy_pass_pending_count": len(b_pending),
            "former_proxy_pass_pending_case_ids": sorted(b_pending),
            "former_proxy_negative_withdrawn_count":
                len(b_unstable_negative),
            "former_proxy_negative_withdrawn_case_ids":
                sorted(b_unstable_negative),
            "construction": (
                "construct H(f,infinity_2), construct its conjugate "
                "H(fbar,infinity_1), form their compositum (or compute "
                "the splitting field), then compute the actual maximal "
                "absolutely abelian subfield and Shintani index"
            ),
            "required_outputs": [
                "actual normal-closure polynomial",
                "Galois group and commutator subgroup",
                "maximal absolute-abelian fixed field",
                "genuine index",
                "Engine-B hypotheses and two-route imaginary-base reconstruction",
            ],
        },
        "engine_c_catch_up_geometry": {
            "case_count": len(unscreened_quartic),
            "case_ids": sorted(unscreened_quartic),
            "purpose": (
                "remove W1 proxy preselection from the completeness "
                "claim by running the already-banked actual splitting-"
                "closure geometry screen"
            ),
        },
        "entire_index_distribution_rerun": {
            "representative_count": len(rows),
            "stable_modulus_direct_reconstruction_count":
                len(rows) - len(unstable_all),
            "unstable_modulus_actual_normal_closure_count":
                len(unstable_all),
            "unstable_case_ids": sorted(unstable_all),
            "rule": (
                "publish no index distribution, odd-index law, or "
                "frontier-vs-index analysis until every row carries a "
                "genuine reconstruction record"
            ),
        },
        "w4_gate": {
            "open": False,
            "requirements": [
                "241-row B reconstruction and reclassification complete (64 former passes plus 177 withdrawn negatives)",
                "252-row C catch-up geometry complete",
                "8200-row genuine index ledger complete",
                "occurrence transport closed",
            ],
        },
        "unaffected_tracks": {
            "engine_a_bulk": "OPEN",
            "engine_c_existing_728_positive_bulk": "OPEN",
            "engine_b_stable_131_population": "OPEN",
        },
        "five_exception_files_retained": True,
        "source_hashes": {
            str(path.relative_to(ROOT)): sha(path)
            for path in (W1, CONTAINMENT, C_GEOMETRY, OUTPUT)
        },
    }
    RECOVERY.write_text(
        json.dumps(recovery, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(f"THEOREM_CASES_AUDITED={len(theorem_case_ids)}")
    print("FALSE_CASE_LEVEL_THEOREM_TAGS=0")
    print(f"B_RECOVERY_CASES={len(b_unstable_screened)}")
    print(f"C_CATCH_UP_CASES={len(unscreened_quartic)}")
    print(f"INDEX_RECONSTRUCTIONS={len(rows)}")
    print(f"OUTPUT_SHA256={sha(OUTPUT)}")
    print(f"RECOVERY_SHA256={sha(RECOVERY)}")


if __name__ == "__main__":
    main()
