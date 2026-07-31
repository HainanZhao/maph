#!/usr/bin/env python3
"""Replay only the exact B2 orientation; never search its inverse."""

from __future__ import annotations

from decimal import Decimal, getcontext
import json
from pathlib import Path
import re
import sys


ROOT = Path(__file__).resolve().parents[1]
getcontext().prec = 110


def parse_ball(text: str) -> tuple[Decimal, Decimal, Decimal, Decimal]:
    matches = re.findall(
        r"([+-]?\d+(?:\.\d+)?)\s*\+/-\s*([0-9.]+e[+-]?\d+)",
        text,
    )
    if len(matches) != 2:
        raise ValueError("expected rectangular complex ball")
    real, real_radius = map(Decimal, matches[0])
    imag, imag_radius = map(Decimal, matches[1])
    return real, real_radius, imag, imag_radius


def quarter_turn(
    real: Decimal,
    imag: Decimal,
    real_radius: Decimal,
    imag_radius: Decimal,
    exponent: int,
) -> tuple[Decimal, Decimal, Decimal, Decimal]:
    exponent %= 4
    if exponent == 0:
        return real, imag, real_radius, imag_radius
    if exponent == 1:
        return -imag, real, imag_radius, real_radius
    if exponent == 2:
        return -real, -imag, real_radius, imag_radius
    return imag, -real, imag_radius, real_radius


def main() -> None:
    transport = json.loads(
        (ROOT / "artifacts" / "b2-artin-transport-v1.json").read_text()
    )
    orientations = {
        row["case_id"]: row["dedekind_to_analytic_orientation"]
        for row in transport["cases"]
    }
    controls = json.loads(
        (ROOT / "artifacts" / "certified-controls-v1.json").read_text()
    )
    first = json.loads(
        (
            ROOT
            / "artifacts"
            / "roblot-rq000129-constructor-sealed-v2.json"
        ).read_text()
    )
    remaining = json.loads(
        (
            ROOT
            / "artifacts"
            / "remaining-roblot-constructors-sealed-v1.json"
        ).read_text()
    )
    coefficients = {
        "RQ-000129": first["numerical_data"]["roblot_coefficient"],
        **{
            row["case_id"]: row["coefficient"]
            for row in remaining["cases"]
        },
    }

    results = []
    for case_id in sorted(coefficients):
        routes = [
            row
            for row in controls["routes"]
            if row["case_id"] == case_id
        ]
        if len(routes) != 2:
            raise RuntimeError(f"{case_id}: route count changed")
        if routes[0]["lprime_zero_ball"] != routes[1]["lprime_zero_ball"]:
            raise RuntimeError(f"{case_id}: route values disagree")
        lr, rr, li, ri = parse_ball(routes[0]["lprime_zero_ball"])
        orientation = orientations[case_id]
        oriented_imag = li if orientation == "direct" else -li
        cr = Decimal(coefficients[case_id]["real"])
        ci = Decimal(coefficients[case_id]["imag"])
        matches = []
        minimum_linf_gap = None
        for rotation in range(4):
            xr, xi, xrr, xri = quarter_turn(
                lr, oriented_imag, rr, ri, rotation
            )
            gap = max(abs(cr - xr) - xrr, abs(ci - xi) - xri)
            if minimum_linf_gap is None or gap < minimum_linf_gap:
                minimum_linf_gap = gap
            if abs(cr - xr) <= xrr and abs(ci - xi) <= xri:
                matches.append(rotation)
        results.append(
            {
                "case_id": case_id,
                "exact_orientation": orientation,
                "quarter_turn_match_count": len(matches),
                "matching_rotations": matches,
                "minimum_linf_gap": str(minimum_linf_gap),
            }
        )

    failed = [
        row["case_id"]
        for row in results
        if row["quarter_turn_match_count"] != 1
    ]
    if failed:
        raise RuntimeError(f"containment failure set changed: {failed}")
    output = {
        "schema": "dedekind-stark-b2-oriented-phase-replay-v1",
        "status": "PASS_FIVE_EXACT_ORIENTATIONS",
        "claim_tag": "OBSERVED_FIVE_CASE_ORIENTED_MATCH",
        "cases": results,
        "failed_cases": failed,
        "alternative_orientation_searched": False,
        "promotion_authorized": True,
    }
    print(json.dumps(output, indent=2, sort_keys=True))
    print("B2_ORIENTED_PHASE_REPLAY=PASS", file=sys.stderr)


if __name__ == "__main__":
    main()
