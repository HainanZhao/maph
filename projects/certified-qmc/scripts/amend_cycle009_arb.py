#!/usr/bin/env python3
"""Create the Arb-first Cycle-009 preregistration amendment."""

from __future__ import annotations

from hashlib import sha256
import argparse
import json
from pathlib import Path


PROJECT = Path(__file__).resolve().parents[1]
AMENDED_AT = "2026-07-29T04:36:30Z"


def digest(value) -> str:
    return sha256(
        json.dumps(
            value,
            sort_keys=True,
            separators=(",", ":"),
            ensure_ascii=True,
        ).encode("ascii")
    ).hexdigest()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    original = json.loads(
        (PROJECT / "certificates" / "cycle-009-preregistration.json")
        .read_text()
    )
    payload = {
        "schema": "certified-qmc-cycle009-preregistration-v2",
        "tag": "PREREGISTERED_AMENDMENT",
        "amended_at_utc": AMENDED_AT,
        "target_run_started_before_amendment": False,
        "supersedes_checkpoint_sha256": original["checkpoint_sha256"],
        "unchanged_target": original["target"],
        "unchanged_crt_budget": original["crt_budget"],
        "primary_decision_architecture": {
            "ground_truth": original["three_representations"]["ground_truth"],
            "shadow": "compiled Arb balls at 106-bit precision",
            "escalation": (
                "balanced exact CRT reconstruction of candidate difference"
            ),
            "arb_precision_may_increase": True,
            "double_double_enabled": False,
            "correctness_basis": (
                "outward-rounded Arb operations; no new DD radius proof"
            ),
        },
        "unchanged_acceptance_gate": {
            "comparison_count": 802767,
            "exact_crt_escalation_rate": (
                "exact_crt_escalated/802767"
            ),
            "predicate": "exact_crt_escalated<803",
            "maximum_passing_count": 802,
        },
        "mandatory_report": {
            "exact_escalation_count_against": 803,
            "depth_histogram": [
                "double_double_resolved",
                "arb_resolved",
                "exact_crt_resolved"
            ],
            "primary_run_double_double_resolved_value": 0,
            "arb_wall_seconds": True,
            "arb_fraction_of_total_wall_time": True,
        },
        "conditional_double_double_optimization": {
            "authorized_before_arb_profile": False,
            "required_source": (
                "published rigorous double-word building-block constants"
            ),
            "dual_shadow_same_tournament": True,
            "required_trace_fields": [
                "stage",
                "comparison_index",
                "incumbent_exponent",
                "challenger_exponent",
                "comparison_sign",
                "selected_exponent"
            ],
            "promotion_predicate": (
                "bit-identical complete branch trace to banked Arb run"
            ),
            "same_final_vector_alone_is_insufficient": True,
        },
        "data_run_started": False,
    }
    payload["checkpoint_sha256"] = digest(payload)
    rendered = json.dumps(payload, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered, encoding="utf-8")
    else:
        print(rendered, end="")


if __name__ == "__main__":
    main()
