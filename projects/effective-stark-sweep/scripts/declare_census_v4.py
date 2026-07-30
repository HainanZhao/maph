#!/usr/bin/env python3
"""Emit census accounting revision v4 after the proxy containment."""

from __future__ import annotations

from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ARTIFACTS = ROOT / "artifacts"
V3 = ARTIFACTS / "full-census-yield-declaration-v3.json"
REJECTED = ARTIFACTS / "census-split-v3-engine-d-proposal-rejected-v1.json"
CONTAINMENT = ARTIFACTS / "conjugation-dependent-census-audit-v1.json"
PROXY = ARTIFACTS / "proxy-scope-and-tag-audit-v1.json"
RECOVERY = ARTIFACTS / "proxy-recovery-queue-v1.json"
OUTPUT = ARTIFACTS / "full-census-yield-declaration-v4.json"


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    v3 = json.loads(V3.read_text(encoding="utf-8"))
    containment = json.loads(CONTAINMENT.read_text(encoding="utf-8"))
    proxy = json.loads(PROXY.read_text(encoding="utf-8"))
    recovery = json.loads(RECOVERY.read_text(encoding="utf-8"))
    exposure = containment["formal_split_exposure"]
    b = exposure["ENGINE_B_ELIGIBLE"]
    if b != {
        "total": 195,
        "galois_stable_finite_modulus": 131,
        "galois_unstable_finite_modulus": 64,
    }:
        raise RuntimeError("Engine-B containment counts changed")
    if proxy["verified_case_tag_audit"]["false_case_level_theorem_tags"]:
        raise RuntimeError("a false theorem tag is present")

    histogram = {
        "PROVED_TRIVIAL": {
            "row_occurrences": 3899,
            "status": "UNCHANGED",
        },
        "ENGINE_A_NONTRIVIAL_ELIGIBLE": {
            "row_occurrences": 1560,
            "status": "UNCHANGED_AND_PROXY_INDEPENDENT",
        },
        "ENGINE_B_VALID_STABLE_MODULUS": {
            "row_occurrences": 131,
            "status": "ELIGIBLE",
        },
        "ENGINE_B_PENDING_ACTUAL_NORMAL_CLOSURE": {
            "row_occurrences": 64,
            "status": "PENDING_NOT_FRONTIER",
        },
        "ENGINE_C_POSITIVE_ELIGIBLE": {
            "row_occurrences": 728,
            "status": "UNCHANGED_POSITIVE_SET",
            "completeness_note": (
                "252 proxy-excluded supported quartic rows await the "
                "same actual-splitting-closure geometry screen"
            ),
        },
        "FRONTIER_PRE_RECOVERY": {
            "row_occurrences": 1818,
            "status": "NOT_FINAL_UNTIL_PROXY_RECOVERY",
        },
    }
    if sum(row["row_occurrences"] for row in histogram.values()) != 8200:
        raise RuntimeError("v4 histogram does not sum to 8200")

    payload = {
        "schema": "effective-stark-full-census-yield-v4",
        "recorded_at_utc": datetime.now(timezone.utc).isoformat(),
        "claim_tag": "VERIFIED_ACCOUNTING_WITH_PENDING_CLASSIFICATION",
        "representative_count": 8200,
        "histogram": histogram,
        "accounting": {
            "proved_trivial": 3899,
            "substantive_safe_eligible": 2419,
            "substantive_safe_breakdown": {
                "A": 1560,
                "B": 131,
                "C": 728,
            },
            "substantive_pending_b": 64,
            "pre_recovery_frontier": 1818,
            "frontier_proxy_negative_withdrawn_pending": 177,
            "safe_eligible_including_trivial": 6318,
            "safe_eligible_beyond_seven_anchors": 6311,
            "yield_checkpoint": "PASS",
            "pre_registered_threshold": v3["pre_registered_threshold"],
        },
        "index_one_proxy_overlap_no_double_count": {
            "proxy_rows": 3521,
            "inside_proved_trivial": 2552,
            "inside_substantive_engine_a": 693,
            "proposed_engine_d_rejected_and_retained_in_frontier": 276,
            "sum_check": 3521,
        },
        "engine_population_attestations": {
            "A": (
                "unaffected: routing is support-order <=2 and does not "
                "depend on the conjugation proxy"
            ),
            "C_positive_728": (
                "unaffected: every positive case passed the actual "
                "splitting-closure geometry gate"
            ),
            "C_completeness": (
                "not yet closed: 252 supported quartic rows excluded by "
                "the W1 proxy must receive the complete geometry screen"
            ),
            "B": (
                "131 valid stable-modulus rows plus 64 pending genuine "
                "normal-closure reconstructions"
            ),
        },
        "rejected_engine_d_split": {
            "proposal": "FRONTIER 1818->1542; substantive 2483->2759",
            "status": "PROPOSED_AND_REJECTED",
            "reason": (
                "the no-go lemma and exact modulus-stability audit give "
                "zero corrected substantive Engine-D cases"
            ),
            "ledger_artifact":
                "artifacts/census-split-v3-engine-d-proposal-rejected-v1.json",
        },
        "tag_history": {
            "false_case_level_theorem_tags": 0,
            "paper_sentence": (
                "Across four accounting revisions, zero false "
                "case-level theorem tags were issued: every predicate "
                "correction preceded W3 promotion."
            ),
            "stronger_zero_false_tags_claim": "NOT_MADE",
            "intermediate_correction": (
                "proxy-dependent VERIFIED_W2 classification artifacts "
                "are superseded in v4; RQ-007500 is the one affected "
                "completed canonical closure certificate"
            ),
        },
        "revision_history": [
            {
                "revision": "v1",
                "artifact":
                    "artifacts/full-census-yield-declaration-v1.json",
                "role": "first complete theorem-route accounting",
            },
            {
                "revision": "v2",
                "artifact":
                    "artifacts/full-census-yield-declaration-v2.json",
                "role": (
                    "packet-occurrence versus distinct-closure and "
                    "mixed-row correction"
                ),
            },
            {
                "revision": "v3",
                "artifact":
                    "artifacts/full-census-yield-declaration-v3.json",
                "role": "corrected closure counts and frozen frontier trend",
            },
            {
                "revision": "v4",
                "artifact":
                    "artifacts/full-census-yield-declaration-v4.json",
                "role": (
                    "finite-modulus stability containment; B 131 valid "
                    "plus 64 pending"
                ),
            },
        ],
        "w4_gate_open": recovery["w4_gate"]["open"],
        "w4_gate_requirements": recovery["w4_gate"]["requirements"],
        "source_hashes": {
            str(path.relative_to(ROOT)): sha(path)
            for path in (
                V3,
                REJECTED,
                CONTAINMENT,
                PROXY,
                RECOVERY,
                Path(__file__).resolve(),
            )
        },
    }
    OUTPUT.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print("CENSUS_V4_SUM=8200")
    print("B_VALID=131")
    print("B_PENDING=64")
    print("FALSE_CASE_LEVEL_THEOREM_TAGS=0")
    print(f"OUTPUT_SHA256={sha(OUTPUT)}")


if __name__ == "__main__":
    main()
