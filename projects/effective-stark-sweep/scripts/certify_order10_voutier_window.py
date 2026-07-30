#!/usr/bin/env python3
"""Freeze the height-rigidity window for the first order-ten target."""

from __future__ import annotations

from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path

from flint import arb, ctx


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "artifacts" / "rq001107-voutier-window-v1.json"
SAFE_EXPONENT = 15840
NORMAL_CLOSURE_DEGREE = 40
MAX_COMPARISON_DEGREE = 2 * NORMAL_CLOSURE_DEGREE
MARGIN_FACTOR = 100


def bound(degree: int) -> arb:
    value = arb(degree)
    return (value.log().log() / value.log()) ** 3 / (4 * degree)


def main() -> None:
    ctx.dps = 100
    bounds = [(degree, bound(degree)) for degree in range(3, 81)]
    minimum_degree, minimum_ball = min(
        bounds, key=lambda item: item[1].lower()
    )
    certified_minimum = arb(minimum_ball.lower())
    degree_80 = bound(80)
    raw_log_error_ceiling = (
        certified_minimum / (MARGIN_FACTOR * SAFE_EXPONENT)
    )
    payload = {
        "schema": "effective-stark-rq001107-voutier-window-v1",
        "claim_tag": "ENCLOSED",
        "recorded_at_utc": datetime.now(timezone.utc).isoformat(),
        "case_id": "RQ-001107",
        "normal_closure_degree": NORMAL_CLOSURE_DEGREE,
        "maximum_packet_comparison_degree": MAX_COMPARISON_DEGREE,
        "degree_cap_derivation": (
            "The quotient/comparison element lies in a compositum of at "
            "most two degree-40 packet fields, hence degree <= 80. The "
            "actual degree must replace this cap in the final certificate."
        ),
        "voutier_formula": (
            "(log(log(d))/log(d))^3/(4*d), for integer d >= 3"
        ),
        "degree_window": [3, MAX_COMPARISON_DEGREE],
        "minimum_occurs_at_degree": minimum_degree,
        "minimum_voutier_lower_ball": str(certified_minimum),
        "degree_80_voutier_ball": str(degree_80),
        "safe_exponent": SAFE_EXPONENT,
        "required_margin_factor": MARGIN_FACTOR,
        "raw_log_error_ceiling_ball": str(raw_log_error_ceiling),
        "final_certificate_obligation": (
            "State the exact maximum comparison degree reached, the "
            "minimum certified Voutier bound over degrees 3 through that "
            "maximum, the powered height upper bound, and their ratio."
        ),
    }
    serialized = json.dumps(payload, indent=2, sort_keys=True) + "\n"
    OUTPUT.write_text(serialized, encoding="utf-8")
    print(f"MAXIMUM_PACKET_COMPARISON_DEGREE={MAX_COMPARISON_DEGREE}")
    print(f"VOUTIER_MINIMUM_DEGREE={minimum_degree}")
    print(f"VOUTIER_MINIMUM_LOWER={certified_minimum}")
    print(f"VOUTIER_DEGREE_80={degree_80}")
    print(f"RAW_LOG_ERROR_CEILING={raw_log_error_ceiling}")
    print(
        "OUTPUT_SHA256="
        + hashlib.sha256(serialized.encode()).hexdigest()
    )


if __name__ == "__main__":
    main()
