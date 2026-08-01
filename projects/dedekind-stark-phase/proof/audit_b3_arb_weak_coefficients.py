#!/usr/bin/env python3
"""Certify the five control weak-unit coefficients with Arb balls."""

from __future__ import annotations

import ast
import hashlib
import json
from pathlib import Path
import platform
import re
import subprocess
import sys

import flint
from flint import acb, acb_poly, arb, arb_poly, ctx, fmpq


ROOT = Path(__file__).resolve().parents[1]
EXPORTER = ROOT / "proof" / "export_b3_control_orbits.gp"
RQ129 = ROOT / "artifacts" / "roblot-rq000129-constructor-sealed-v2.json"
REMAINING = (
    ROOT / "artifacts" / "remaining-roblot-constructors-sealed-v1.json"
)
PRECISIONS = (256, 512)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def parse_pairs(value: str) -> list[fmpq]:
    pairs = ast.literal_eval(value)
    return [fmpq(numerator, denominator) for numerator, denominator in pairs]


def exact_inputs() -> dict[str, dict[str, list[fmpq]]]:
    source = EXPORTER.read_text(encoding="utf-8")
    forbidden = (
        "all-five-phase-gates-v1.json",
        "certified-controls-v1.json",
        "control-phase-audit-v1.json",
    )
    if any(name in source for name in forbidden):
        raise RuntimeError("target-bearing artifact referenced by exact exporter")
    completed = subprocess.run(
        ["gp", "-q", str(EXPORTER)],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
        timeout=300,
    )
    if (
        completed.returncode
        or completed.stderr.strip()
        or "B3_CONTROL_ORBITS=PASS" not in completed.stdout
    ):
        raise RuntimeError(completed.stdout + completed.stderr)

    cases: dict[str, dict[str, list[fmpq]]] = {}
    current: dict[str, list[fmpq]] | None = None
    for line in completed.stdout.splitlines():
        if line.startswith("CASE_ID="):
            case_id = line.split("=", 1)[1]
            current = {}
            cases[case_id] = current
        elif current is not None and "_ASCENDING_PAIRS=" in line:
            key, value = line.split("=", 1)
            current[key] = parse_pairs(value)
    if set(cases) != {
        "RQ-000129",
        "RQ-001280",
        "RQ-001569",
        "RQ-001894",
        "RQ-007519",
    }:
        raise RuntimeError(f"control set changed: {sorted(cases)}")
    if any(
        set(case)
        != {
            "POLYNOMIAL_ASCENDING_PAIRS",
            "GAMMA_ASCENDING_PAIRS",
            "ORBIT_1_ASCENDING_PAIRS",
            "ORBIT_2_ASCENDING_PAIRS",
            "ORBIT_3_ASCENDING_PAIRS",
            "ORBIT_4_ASCENDING_PAIRS",
        }
        for case in cases.values()
    ):
        raise RuntimeError("an exact orbit export is incomplete")
    return cases


def archived_points() -> dict[str, tuple[str, str]]:
    rq129 = json.loads(RQ129.read_text(encoding="utf-8"))
    first = rq129["numerical_data"]["roblot_coefficient"]
    points = {"RQ-000129": (first["real"], first["imag"])}
    remaining = json.loads(REMAINING.read_text(encoding="utf-8"))
    for row in remaining["cases"]:
        points[row["case_id"]] = (
            row["coefficient"]["real"],
            row["coefficient"]["imag"],
        )
    return points


def ball_record(value: arb) -> dict[str, str]:
    return {
        "ball": str(value),
        "lower": str(value.lower()),
        "upper": str(value.upper()),
        "radius": str(value.rad()),
    }


def certify_case(
    case: dict[str, list[fmpq]], precision: int
) -> tuple[dict, arb, arb]:
    ctx.prec = precision
    polynomial = case["POLYNOMIAL_ASCENDING_PAIRS"]
    # The archived constructor points have 100 decimal places.  Keep
    # the 512-bit arithmetic while requesting a 320-bit root radius so
    # that a correctly rounded archived decimal remains a meaningful
    # containment anchor rather than pretending it is an exact real.
    tolerance_bits = min(precision - 32, 320)
    tolerance = arb(2) ** (-tolerance_bits)
    roots = acb_poly([acb(value) for value in polynomial]).roots(
        tol=tolerance, maxprec=2 * precision
    )
    if len(roots) != 8:
        raise RuntimeError("defining polynomial did not yield eight roots")
    for left in range(len(roots)):
        for right in range(left + 1, len(roots)):
            if roots[left].overlaps(roots[right]):
                raise RuntimeError("root isolation balls overlap")

    real_root_balls = [root for root in roots if root.imag.contains(0)]
    if len(real_root_balls) != 4:
        raise RuntimeError("signature root count changed")
    distinguished_acb = min(
        real_root_balls, key=lambda root: float(root.real.mid())
    )
    distinguished = distinguished_acb.real
    for root in real_root_balls:
        if root is distinguished_acb:
            continue
        if not distinguished.upper() < root.real.lower():
            raise RuntimeError("least-real-root ordering is not certified")

    logs = []
    values = []
    for index in range(1, 5):
        orbit = case[f"ORBIT_{index}_ASCENDING_PAIRS"]
        value = arb_poly([arb(coefficient) for coefficient in orbit])(
            distinguished
        )
        if value.contains(0):
            raise RuntimeError("algebraic unit value ball contains zero")
        logarithm = abs(value).log()
        values.append(value)
        logs.append(logarithm)
    real = (logs[0] - logs[2]) / 2
    imag = (logs[1] - logs[3]) / 2
    # The legacy comparison values are printed decimals, not exact
    # reals.  Widen by 1e-97 (larger than half an ulp for every
    # archived component) so literal-decimal containment is a valid
    # regression check.  This only enlarges an already rigorous ball.
    anchor_padding = arb(0, "1e-97")
    real += anchor_padding
    imag += anchor_padding

    return (
        {
            "precision_bits": precision,
            "requested_root_tolerance_bits": tolerance_bits,
            "archived_decimal_anchor_padding": "1e-97",
            "root_isolation": {
                "degree": len(roots),
                "pairwise_disjoint": True,
                "real_root_count": len(real_root_balls),
                "distinguished_rule": "least real root",
                "distinguished_root": ball_record(distinguished),
            },
            "orbit_values_exclude_zero": True,
            "orbit_values": [ball_record(value) for value in values],
            "log_orbit": [ball_record(value) for value in logs],
            "coefficient": {
                "real": ball_record(real),
                "imag": ball_record(imag),
            },
        },
        real,
        imag,
    )


def main() -> None:
    inputs = exact_inputs()
    points = archived_points()
    records = []
    for case_id in sorted(inputs):
        runs = {}
        balls = {}
        for precision in PRECISIONS:
            run, real, imag = certify_case(inputs[case_id], precision)
            runs[str(precision)] = run
            balls[precision] = (real, imag)
        coarse_real, coarse_imag = balls[256]
        fine_real, fine_imag = balls[512]
        nested = coarse_real.contains(fine_real) and coarse_imag.contains(
            fine_imag
        )
        point_real, point_imag = points[case_id]
        point_contained = fine_real.contains(
            arb(point_real)
        ) and fine_imag.contains(arb(point_imag))
        if not nested or not point_contained:
            raise RuntimeError(
                f"{case_id}: nesting={nested}, point={point_contained}"
            )
        records.append(
            {
                "case_id": case_id,
                "runs": runs,
                "fine_ball_nested_in_coarse": nested,
                "archived_point_contained_in_512_bit_ball": point_contained,
            }
        )

    result = {
        "schema": "dedekind-stark-b3-arb-weak-coefficient-anchor-v1",
        "claim_tag": "CERTIFIED_NUMERICAL",
        "status": "PASS_FIVE_CONTROL_ARB_WEAK_COEFFICIENT_ANCHOR",
        "claim_boundary": {
            "certified": (
                "real-root isolation, nonzero algebraic-unit values, "
                "logarithms, and weak Fourier coefficients"
            ),
            "not_evaluated": "no L-function value or census phase target",
            "archived_points_role": "containment validation only",
        },
        "runtime": {
            "python": platform.python_version(),
            "python_implementation": platform.python_implementation(),
            "python_flint": flint.__version__,
            "flint": flint.__FLINT_VERSION__,
            "precisions_bits": list(PRECISIONS),
        },
        "independence_wall": {
            "exact_exporter_reads_target_artifacts": False,
            "evaluator_reads_lprime_or_phase_artifact": False,
            "root_orientation_chosen_from_archived_point": False,
            "precision_chosen_from_result": False,
        },
        "source_hashes": {
            "exact_exporter_sha256": sha256(EXPORTER),
            "rq000129_constructor_artifact_sha256": sha256(RQ129),
            "remaining_constructor_artifact_sha256": sha256(REMAINING),
            "evaluator_sha256": sha256(Path(__file__)),
        },
        "cases": records,
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
