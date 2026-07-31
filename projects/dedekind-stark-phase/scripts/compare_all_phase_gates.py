#!/usr/bin/env python3
"""Open all five phase defects after the remaining-constructor seal."""

from __future__ import annotations

from decimal import Decimal, getcontext
import json
from pathlib import Path
import re


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
        cr = Decimal(coefficients[case_id]["real"])
        ci = Decimal(coefficients[case_id]["imag"])
        matches = []
        for orientation in ("direct", "inverse"):
            oriented_imag = li if orientation == "direct" else -li
            for rotation in range(4):
                xr, xi, xrr, xri = quarter_turn(
                    lr, oriented_imag, rr, ri, rotation
                )
                if abs(cr - xr) <= xrr and abs(ci - xi) <= xri:
                    matches.append(
                        {
                            "orientation": orientation,
                            "coefficient_rotation": rotation,
                            "defect_quarter_turn": (-rotation) % 4,
                            "real_error": str(abs(cr - xr)),
                            "real_radius": str(xrr),
                            "imag_error": str(abs(ci - xi)),
                            "imag_radius": str(xri),
                        }
                    )
        if len(matches) != 1:
            raise RuntimeError(
                f"{case_id}: expected one convention match, got {matches}"
            )
        result = {"case_id": case_id, **matches[0]}
        results.append(result)
        print(
            f"{case_id}|ORIENTATION={result['orientation']}"
            f"|COEFFICIENT_ROTATION={result['coefficient_rotation']}"
            f"|DEFECT_QUARTER_TURN={result['defect_quarter_turn']}"
            "|CONTAINED=1"
        )
    print(f"QUANTIZED_COUNT={len(results)}")
    print("ALL_FIVE_PHASE_GATES=PASS")


if __name__ == "__main__":
    main()
