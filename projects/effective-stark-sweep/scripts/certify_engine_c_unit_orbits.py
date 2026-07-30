#!/usr/bin/env python3
"""Isolate Engine-C Stark-unit orbits in exact anti-unit lattices."""

from __future__ import annotations

from fractions import Fraction
import hashlib
import json
from pathlib import Path
import re
import subprocess

from flint import acb, arb, ctx, fmpq, fmpz_poly

import certify_engine_c_theta_targets as theta


ROOT = Path(__file__).resolve().parents[1]
SELF = Path(__file__).resolve()
CONFIG = ROOT / "data/engine-c-unit-orbit-cases-v1.json"
THETA_CONFIG = ROOT / "data/engine-c-theta-evaluator-cases-v1.json"
GP_SOURCE = ROOT / "scripts/export_engine_c_unit_lattice.gp"
OUTPUT = ROOT / "artifacts/engine-c-unit-orbits-v1.json"
TRANSCRIPT = ROOT / "artifacts/engine-c-unit-orbits-v1.transcript"


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def scalar(text: str, key: str) -> str:
    found = re.findall(rf"^{re.escape(key)}=(.*)$", text, re.MULTILINE)
    if len(found) != 1:
        raise RuntimeError(f"{key}: got {len(found)} values")
    return found[0]


def parse_polynomial(text: str, label: str) -> list[fmpq]:
    degree = int(scalar(text, f"{label}_DEGREE"))
    answer = []
    for index in range(degree + 1):
        numerator, denominator = scalar(
            text, f"{label}_COEFF_{index}"
        ).split("/")
        answer.append(fmpq(int(numerator), int(denominator)))
    return answer


def evaluate(coefficients: list[fmpq], argument: acb) -> acb:
    value = acb(0)
    for coefficient in reversed(coefficients):
        value = value * argument + coefficient
    return value


def solve(matrix: list[list[arb]], target: tuple[arb, arb]) -> tuple[arb, arb]:
    determinant = (
        matrix[0][0] * matrix[1][1]
        - matrix[0][1] * matrix[1][0]
    )
    if determinant.contains(0):
        raise RuntimeError("logarithmic matrix is singular")
    return (
        (
            target[0] * matrix[1][1]
            - target[1] * matrix[0][1]
        )
        / determinant,
        (
            matrix[0][0] * target[1]
            - matrix[1][0] * target[0]
        )
        / determinant,
    )


def near_integer(value: arb, integer: int, radius: Fraction) -> bool:
    width = arb(radius.numerator) / radius.denominator
    return value > arb(integer) - width and value < arb(integer) + width


def transformed_targets(target: acb) -> list[tuple[str, tuple[arb, arb]]]:
    real, imag = target.real, target.imag
    return [
        ("z", (real, imag)),
        ("-z", (-real, -imag)),
        ("i*z", (-imag, real)),
        ("-i*z", (imag, -real)),
        ("conj(z)", (real, -imag)),
        ("-conj(z)", (-real, imag)),
        ("i*conj(z)", (imag, real)),
        ("-i*conj(z)", (-imag, -real)),
    ]


def live_theta_target(record: dict, theta_config: dict, source: str) -> acb:
    conductor, coefficients, _ = theta.run_gp(
        record, theta_config["coefficient_limit"], source
    )
    Q = arb(conductor).sqrt() / (2 * arb.pi())
    c = 1 / Q
    q = (-c).exp()
    theta_one = acb(0)
    integral_zero = acb(0)
    integral_one = acb(0)
    for n, (real, imag) in enumerate(coefficients, start=1):
        coefficient = acb(real, imag)
        argument = arb(n) * c
        exponential = (-argument).exp()
        theta_one += coefficient * exponential
        integral_zero += coefficient * acb(argument).gamma_upper(0)
        integral_one += (
            coefficient.conjugate() * Q / arb(n) * exponential
        )
    limit = len(coefficients)
    theta_tail = q ** (limit + 1) * (
        arb(limit + 1) - arb(limit) * q
    ) / (1 - q) ** 2
    integral_tail = Q * q ** (limit + 1) / (1 - q)
    theta_one += theta.complex_error(theta_tail)
    integral_zero += theta.complex_error(integral_tail)
    integral_one += theta.complex_error(integral_tail)
    return (
        integral_zero
        + theta_one / theta_one.conjugate() * integral_one
    )


def orbit(seed: tuple[int, int], action: list[list[int]]) -> set[tuple[int, int]]:
    answer = set()
    current = seed
    for _ in range(4):
        answer.add(current)
        current = (
            action[0][0] * current[0] + action[0][1] * current[1],
            action[1][0] * current[0] + action[1][1] * current[1],
        )
    return answer


def main() -> None:
    config = json.loads(CONFIG.read_text(encoding="utf-8"))
    theta_config = json.loads(THETA_CONFIG.read_text(encoding="utf-8"))
    theta_records = {
        (row["case_id"], row["route_id"]): row
        for row in theta_config["records"]
    }
    theta_source = theta.GP_SOURCE.read_text(encoding="utf-8")
    lattice_source = GP_SOURCE.read_text(encoding="utf-8")
    ctx.dps = config["working_digits"]
    radius_num, radius_den = config["isolation_radius"].split("/")
    radius = Fraction(int(radius_num), int(radius_den))
    bound = config["coordinate_search_bound"]
    records = []
    transcripts = []

    for record in config["records"]:
        key = (record["case_id"], record["route_id"])
        prelude = (
            "CHARACTER_FIELD_POLYNOMIAL="
            f"{record['character_field_polynomial']};\n"
        )
        completed = subprocess.run(
            ["gp", "-q"],
            input=prelude + lattice_source,
            text=True,
            capture_output=True,
            cwd=ROOT,
            timeout=600,
            check=False,
        )
        if (
            completed.returncode != 0
            or "EXACT_ANTI_UNIT_LATTICE_EXPORT_COMPLETE=1"
            not in completed.stdout
        ):
            raise RuntimeError(completed.stdout + completed.stderr)
        if int(scalar(completed.stdout, "CHARACTER_FIELD_BNFCERTIFY")) != 1:
            raise RuntimeError(f"bnfcertify failed for {key}")
        roots_of_unity = int(
            scalar(completed.stdout, "CHARACTER_FIELD_ROOTS_OF_UNITY")
        )
        if roots_of_unity != record["expected_roots_of_unity"]:
            raise RuntimeError(f"root-of-unity count changed for {key}")

        polynomial_q = parse_polynomial(
            completed.stdout, "CHARACTER_FIELD"
        )
        if any(value.denominator != 1 for value in polynomial_q):
            raise RuntimeError("nonintegral defining polynomial")
        polynomial = fmpz_poly([int(value) for value in polynomial_q])
        sigma = parse_polynomial(completed.stdout, "C4_SIGMA")
        units = [
            parse_polynomial(completed.stdout, "ANTI_UNIT_1"),
            parse_polynomial(completed.stdout, "ANTI_UNIT_2"),
        ]
        action = [
            [
                int(scalar(completed.stdout, "ANTI_ACTION_11")),
                int(scalar(completed.stdout, "ANTI_ACTION_12")),
            ],
            [
                int(scalar(completed.stdout, "ANTI_ACTION_21")),
                int(scalar(completed.stdout, "ANTI_ACTION_22")),
            ],
        ]
        primitive_lprime = live_theta_target(
            theta_records[key], theta_config, theta_source
        )
        # The banked e/2 factor converts class-log coordinates.  Here
        # the input is already the quartic Fourier sum L'(0,psi).
        # Anti-unit symmetry l_{j+2}=-l_j duplicates the two independent
        # logarithms in that sum, so Fourier inversion contributes 1/2:
        # the two-coordinate target is (e/4) L'(0,psi).
        target = primitive_lprime * arb(roots_of_unity) / 4
        roots = [
            root
            for root, multiplicity in polynomial.complex_roots()
            if multiplicity == 1 and root.imag > 0
        ]
        if len(roots) != 4:
            raise RuntimeError(f"{key}: expected four upper roots")
        isolated: set[tuple[int, int]] = set()
        per_root = []
        for root_index, root in enumerate(roots):
            sigma_root = evaluate(sigma, root)
            matrix = [
                [abs(evaluate(unit, root)).log() for unit in units],
                [
                    abs(evaluate(unit, sigma_root)).log()
                    for unit in units
                ],
            ]
            root_matches = []
            for transform, transformed in transformed_targets(target):
                coordinates = solve(matrix, transformed)
                nearby = [
                    (first, second)
                    for first in range(-bound, bound + 1)
                    for second in range(-bound, bound + 1)
                    if near_integer(coordinates[0], first, radius)
                    and near_integer(coordinates[1], second, radius)
                ]
                for candidate in nearby:
                    root_matches.append(
                        {
                            "transform": transform,
                            "coordinates": list(candidate),
                            "coordinate_balls": [
                                str(coordinates[0]),
                                str(coordinates[1]),
                            ],
                        }
                    )
                    isolated.add(candidate)
            if not root_matches:
                raise RuntimeError(f"{key}: root {root_index} has no match")
            per_root.append(
                {"root_index": root_index, "matches": root_matches}
            )

        seed = min(isolated)
        exact_orbit = orbit(seed, action)
        if isolated != exact_orbit or len(exact_orbit) != 4:
            raise RuntimeError(
                f"{key}: isolated set {isolated} is not one C4 orbit "
                f"under {action}; expected {exact_orbit}"
            )
        expected_orbit = record.get("expected_isolated_orbit")
        if expected_orbit is not None and isolated != {
            tuple(item) for item in expected_orbit
        }:
            raise RuntimeError(f"{key}: regression-anchor orbit changed")
        records.append(
            {
                **record,
                "character_field_class_number": int(
                    scalar(
                        completed.stdout,
                        "CHARACTER_FIELD_CLASS_NUMBER",
                    )
                ),
                "roots_of_unity_e": roots_of_unity,
                "anti_unit_lattice": scalar(
                    completed.stdout, "ANTI_UNIT_LATTICE"
                ),
                "anti_action": action,
                "isolated_integral_orbit": [
                    list(item) for item in sorted(isolated)
                ],
                "per_root_isolation": per_root,
                "analytic_target_ball": str(target),
                "primitive_lprime_ball": str(primitive_lprime),
                "direct_lprime_to_log_factor": (
                    f"{roots_of_unity}/4"
                ),
            }
        )
        transcripts.append(
            f"===== {record['case_id']} {record['route_id']} =====\n"
            f"{completed.stdout}"
        )

    # The two independent bases must isolate the same abstract orbit
    # shape, even though their anti-unit bases are unrelated.
    new_records = [
        row for row in records if row["case_id"] == "RQ-001280"
    ]
    if len(new_records) != 2:
        raise RuntimeError("new-case route count changed")

    TRANSCRIPT.write_text("\n".join(transcripts), encoding="utf-8")
    payload = {
        "schema": "effective-stark-engine-c-unit-orbits-v1",
        "claim_tag": "ENCLOSED_UNIQUE_INTEGRAL_ANTI_UNIT_ORBIT",
        "records": records,
        "label_ambiguity": (
            "The exhaustive dihedral transforms are the C4 Artin-"
            "generator/inverse and complex-embedding choices. They isolate "
            "one exact C4 coordinate orbit; the packet bridge fixes labels."
        ),
        "source_hashes": {
            str(path.relative_to(ROOT)): sha(path)
            for path in (
                CONFIG, THETA_CONFIG, GP_SOURCE, theta.GP_SOURCE, SELF
            )
        },
        "transcript": {
            "path": str(TRANSCRIPT.relative_to(ROOT)),
            "sha256": sha(TRANSCRIPT),
        },
    }
    OUTPUT.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(f"ROUTE_COUNT={len(records)}")
    print("UNIQUE_INTEGRAL_ORBITS=3")
    print(f"OUTPUT_SHA256={sha(OUTPUT)}")


if __name__ == "__main__":
    main()
