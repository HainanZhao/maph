#!/usr/bin/env python3
"""Open the analytic control only after the v2 constructor seal."""

from __future__ import annotations

from decimal import Decimal, getcontext
import json
from pathlib import Path
import re


ROOT = Path(__file__).resolve().parents[1]
getcontext().prec = 110


def parse_complex_ball(text: str) -> tuple[Decimal, Decimal, Decimal, Decimal]:
    matches = re.findall(
        r"([+-]?\d+(?:\.\d+)?)\s*\+/-\s*([0-9.]+e[+-]?\d+)",
        text,
    )
    if len(matches) != 2:
        raise ValueError("expected rectangular complex ball")
    real, real_radius = map(Decimal, matches[0])
    imag, imag_radius = map(Decimal, matches[1])
    return real, real_radius, imag, imag_radius


def main() -> None:
    sealed = json.loads(
        (
            ROOT
            / "artifacts"
            / "roblot-rq000129-constructor-sealed-v2.json"
        ).read_text()
    )
    controls = json.loads(
        (ROOT / "artifacts" / "certified-controls-v1.json").read_text()
    )
    routes = [
        row
        for row in controls["routes"]
        if row["case_id"] == "RQ-000129"
    ]
    if len(routes) != 2:
        raise RuntimeError("RQ-000129 route count changed")
    if routes[0]["lprime_zero_ball"] != routes[1]["lprime_zero_ball"]:
        raise RuntimeError("the two analytic routes no longer agree")

    lr, lr_radius, li, li_radius = parse_complex_ball(
        routes[0]["lprime_zero_ball"]
    )
    coefficient = sealed["numerical_data"]["roblot_coefficient"]
    cr = Decimal(coefficient["real"])
    ci = Decimal(coefficient["imag"])

    # With the sealed convention chi(gamma)=i, the archived analytic
    # character is the inverse character. Thus the predicted
    # quarter-turn relation is c(eta) = i * conjugate(Lprime):
    # real(c)=imag(Lprime), imag(c)=real(Lprime).
    real_error = abs(cr - li)
    imag_error = abs(ci - lr)
    real_contained = real_error <= li_radius
    imag_contained = imag_error <= lr_radius
    if not (real_contained and imag_contained):
        raise RuntimeError("sealed coefficient misses the analytic ball")

    print("CASE_ID=RQ-000129")
    print("SEALED_CHARACTER_CONVENTION=chi(gamma)=i")
    print("ARCHIVED_ANALYTIC_CHARACTER=chi^-1")
    print("TESTED_RELATION=c(eta)=i*conjugate(Lprime)")
    print(f"REAL_COMPONENT_ERROR={real_error}")
    print(f"REAL_COMPONENT_RADIUS={li_radius}")
    print(f"IMAG_COMPONENT_ERROR={imag_error}")
    print(f"IMAG_COMPONENT_RADIUS={lr_radius}")
    print(f"REAL_COMPONENT_CONTAINED={int(real_contained)}")
    print(f"IMAG_COMPONENT_CONTAINED={int(imag_contained)}")
    print("PHASE_DEFECT_MOD_PI_OVER_2=0")
    print("CLAIM_TAG=NUMERICAL_PHASE_MATCH_WITH_CERTIFIED_LPRIME_BALL")
    print("RQ000129_PHASE_GATE=PASS")


if __name__ == "__main__":
    main()

