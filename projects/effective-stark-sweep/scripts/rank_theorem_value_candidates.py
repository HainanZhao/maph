#!/usr/bin/env python3
"""Freeze the post-measurement five-closure theorem portfolio."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RESULTS = ROOT / "artifacts" / "theorem-value-exponent-pilot-v1.json"
OUTPUT = ROOT / "artifacts" / "theorem-value-selection-v1.json"


SELECTED = [
    {
        "case_id": "RQ-000108",
        "rank": 1,
        "rationale": (
            "Only new degree-16 B closure; safe exponent 2880 on the "
            "Q(sqrt(-15)) route; order-four support rerouted from C, "
            "so it tests that engine choice is geometric rather than "
            "determined by character order."
        ),
    },
    {
        "case_id": "RQ-000021",
        "rank": 2,
        "rationale": (
            "Lowest measured safe exponent, 2016; degree 24 over the "
            "smallest real base Q(sqrt(2)); extends the Paper-II "
            "Q(sqrt(2)) tower at a much cheaper exponent."
        ),
    },
    {
        "case_id": "RQ-002057",
        "rank": 3,
        "rationale": (
            "Safe exponent 2592, degree 24, three closure occurrences, "
            "and a three-row prime-power conductor route; supplies a "
            "new local shape rather than another prime-conductor case."
        ),
    },
    {
        "case_id": "RQ-002955",
        "rank": 4,
        "rationale": (
            "Safe exponent 4032, degree 24, and four closure "
            "occurrences; a low-risk order-six transfer control after "
            "Q(sqrt(14))."
        ),
    },
    {
        "case_id": "RQ-001107",
        "rank": 5,
        "rationale": (
            "First order-ten target, with eight closure occurrences. "
            "Degree 40 and safe exponent 15840 make it the portfolio's "
            "deliberate high-value/high-cost theorem bet."
        ),
    },
]

RESERVES = [
    {
        "case_id": "RQ-006512",
        "reserve_rank": 1,
        "rationale": (
            "Ten occurrences, the largest multiplicity in the pilot, "
            "but order-six prime-conductor structure and safe exponent "
            "12096 make it best after the cheaper transfer control."
        ),
    },
    {
        "case_id": "RQ-007487",
        "reserve_rank": 2,
        "rationale": (
            "Safe exponent 3840 and mixed order-2/order-4 support on a "
            "C-to-B reroute, but degree 32 and one occurrence duplicate "
            "novelty already tested by RQ-000108."
        ),
    },
    {
        "case_id": "RQ-000686",
        "reserve_rank": 3,
        "rationale": (
            "Three occurrences and a four-row composite-conductor "
            "route, but safe exponent 12096 is dominated by RQ-002057."
        ),
    },
]


def main() -> None:
    results = json.loads(RESULTS.read_text())
    by_case: dict[str, list[dict]] = {}
    for record in results["records"]:
        by_case.setdefault(record["case_id"], []).append(record)

    def case_record(specification: dict) -> dict:
        routes = by_case[specification["case_id"]]
        best = min(routes, key=lambda row: row["safe_exponent"])
        return {
            **specification,
            "field_d": best["field_d"],
            "finite_norm": best["finite_norm"],
            "support_orders": best["support_orders"],
            "normal_closure_degree": best["normal_closure_degree"],
            "closure_multiplicity": best["closure_multiplicity"],
            "selected_route": best["route_label"],
            "selected_base_polynomial": best["base_polynomial"],
            "divisor_count": best["divisor_count"],
            "safe_exponent": best["safe_exponent"],
        }

    selected = [case_record(specification) for specification in SELECTED]
    reserves = [case_record(specification) for specification in RESERVES]
    if len({row["case_id"] for row in selected}) != 5:
        raise RuntimeError("selected portfolio must contain five closures")
    if {row["case_id"] for row in selected} & {
        row["case_id"] for row in reserves
    }:
        raise RuntimeError("selected and reserve closures overlap")

    payload = {
        "schema": "effective-stark-theorem-value-selection-v1",
        "claim_tag": "VERIFIED_SELECTION_INPUTS",
        "results_sha256": hashlib.sha256(RESULTS.read_bytes()).hexdigest(),
        "ranking_method": (
            "Pareto portfolio, not an arbitrary scalar score: prioritize "
            "safe exponent and closure degree, then multiplicity, while "
            "reserving one slot for a genuinely new character order."
        ),
        "active_before_additional_selection": [
            {
                "case_id": "RQ-000129",
                "engine": "C",
                "state": "Arb orientation pending",
            },
            {
                "case_id": "RQ-000419",
                "engine": "B",
                "safe_exponent": 4032,
                "state": "W3 pending",
            },
        ],
        "additional_selected_count": len(selected),
        "additional_selected": selected,
        "reserves": reserves,
        "explicitly_deprioritized": [
            {
                "case_id": "RQ-004467",
                "safe_exponent": 13810176,
                "reason": (
                    "Exponent is three orders of magnitude above every "
                    "selected closure; retain W2, defer W3."
                ),
            }
        ],
        "execution_order": [
            "RQ-000129",
            "RQ-000419",
            *[row["case_id"] for row in selected],
        ],
        "stop_rule": (
            "If either of the first two additional closures requires "
            "new industrial infrastructure or exceeds one node-hour for "
            "a single certificate step, pause the portfolio and rescope "
            "the W3 template before proceeding."
        ),
    }
    OUTPUT.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    for row in selected:
        print(
            f'{row["rank"]}. {row["case_id"]} '
            f'degree={row["normal_closure_degree"]} '
            f'exponent={row["safe_exponent"]} '
            f'multiplicity={row["closure_multiplicity"]} '
            f'support={row["support_orders"]}'
        )


if __name__ == "__main__":
    main()
