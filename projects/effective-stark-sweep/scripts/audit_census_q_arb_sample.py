#!/usr/bin/env python3
"""Independent 50-row Arb regulator audit of the exact Q corpus."""

from __future__ import annotations

import argparse
from fractions import Fraction
import hashlib
import json
from pathlib import Path
import re
import subprocess
import sys


ROOT = Path(__file__).resolve().parents[1]
MONOREPO = ROOT.parents[1]
FLINT_SITE = (
    MONOREPO
    / "projects"
    / "dedekind-stark-phase"
    / ".venv"
    / "lib"
    / "python3.12"
    / "site-packages"
)
if str(FLINT_SITE) not in sys.path:
    sys.path.insert(0, str(FLINT_SITE))

from flint import acb, acb_poly, arb, ctx, fmpq, fmpq_poly  # noqa: E402


SAMPLE = ROOT / "data" / "census-paper-q-arb-sample-v1.json"
PREREGISTRATION = (
    ROOT / "data" / "census-paper-preregistration-amendment-v6.json"
)
CENSUS = ROOT / "artifacts" / "w1-full-census-v1.json"
CORPUS = ROOT / "artifacts" / "census-q-packets-v1" / "rows"
GP_SCRIPT = ROOT / "scripts" / "export_census_q_regulator_route.gp"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def scalar(output: str, key: str) -> str:
    prefix = f"{key}="
    values = [
        line[len(prefix) :]
        for line in output.splitlines()
        if line.startswith(prefix)
    ]
    if len(values) != 1:
        raise RuntimeError(f"expected one {key}, got {values}")
    return values[0]


def gp_vector(value: str) -> list[Fraction]:
    inner = value.strip()[1:-1].strip()
    if not inner:
        return []
    return [Fraction(item.strip()) for item in inner.split(",")]


def flint_rational(value: Fraction) -> fmpq:
    return fmpq(value.numerator, value.denominator)


def polynomial_from_gp_vector(value: str) -> fmpq_poly:
    descending = gp_vector(value)
    return fmpq_poly([flint_rational(item) for item in reversed(descending)])


def evaluate_polynomial(value: str, root: acb) -> acb:
    descending = gp_vector(value)
    answer = acb(0)
    for coefficient in descending:
        answer = (
            answer * root
            + acb(coefficient.numerator) / coefficient.denominator
        )
    return answer


def isolated_roots(polynomial: fmpq_poly) -> list[acb]:
    return acb_poly(polynomial).roots(tol="1e-90", maxprec=768)


def regulator_rank_one(polynomial: fmpq_poly, unit: str) -> arb:
    roots = isolated_roots(polynomial)
    real_roots = [root for root in roots if root.imag.contains(0)]
    if len(real_roots) != 2:
        raise RuntimeError("base real-root count changed")
    value = abs(evaluate_polynomial(unit, real_roots[0]))
    if value.contains(0):
        raise RuntimeError("base unit embedding contains zero")
    return abs(value.log())


def regulator_signature_21(
    polynomial: fmpq_poly, unit_1: str, unit_2: str
) -> arb:
    roots = isolated_roots(polynomial)
    real_roots = [root for root in roots if root.imag.contains(0)]
    if len(real_roots) != 2 or len(roots) != 4:
        raise RuntimeError("quartic signature root count changed")
    rows = []
    for root in real_roots:
        values = []
        for unit in (unit_1, unit_2):
            absolute = abs(evaluate_polynomial(unit, root))
            if absolute.contains(0):
                raise RuntimeError("quartic unit embedding contains zero")
            values.append(absolute.log())
        rows.append(values)
    determinant = rows[0][0] * rows[1][1] - rows[0][1] * rows[1][0]
    regulator = abs(determinant)
    if regulator.contains(0):
        raise RuntimeError("quartic regulator contains zero")
    return regulator


def parse_trace_expressions(value: str) -> list[str]:
    expressions = []
    index = 0
    while True:
        start = value.find("Mod(", index)
        if start < 0:
            break
        position = start + 4
        depth = 1
        expression_start = position
        while position < len(value):
            character = value[position]
            if character == "(":
                depth += 1
            elif character == ")":
                depth -= 1
            elif character == "," and depth == 1:
                expressions.append(value[expression_start:position].strip())
                break
            position += 1
        index = position + 1
    return expressions


def parse_linear_trace(expression: str) -> tuple[Fraction, Fraction]:
    compact = expression.replace(" ", "")
    terms = compact.replace("-", "+-").split("+")
    y_coefficient = Fraction(0)
    constant = Fraction(0)
    for term in terms:
        if not term:
            continue
        if "y" in term:
            coefficient = term.replace("*y", "").replace("y", "")
            if coefficient in ("", "+"):
                coefficient = "1"
            elif coefficient == "-":
                coefficient = "-1"
            y_coefficient += Fraction(coefficient)
        else:
            constant += Fraction(term)
    return y_coefficient, constant


def character_sign(
    character: list[int], element: list[int], cyc: list[int]
) -> int:
    pairing = sum(
        (
            Fraction(character[index] * element[index], cyc[index])
            for index in range(len(cyc))
        ),
        Fraction(0),
    )
    return 1 if pairing.denominator == 1 else -1


def decode_element(code: int, cyc: list[int]) -> list[int]:
    answer = []
    for modulus in cyc:
        answer.append(code % modulus)
        code //= modulus
    return answer


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    # The preregistered 192-bit initial run failed only the radius gate
    # at RQ-006617 (radius 5.44e-27); the identical route is replayed
    # here at doubled precision.
    initial_precision_bits = 192
    ctx.prec = 384
    preregistration = json.loads(PREREGISTRATION.read_text())
    if sha256(SAMPLE) != preregistration["sample"]["sha256"]:
        raise RuntimeError("frozen Arb sample hash changed")
    sample = json.loads(SAMPLE.read_text())
    census = json.loads(CENSUS.read_text())
    by_id = {row["case_id"]: row for row in census["records"]}
    gp_source = GP_SCRIPT.read_text()
    inflation = arb(preregistration["acceptance"][
        "independent_ball_inflation_radius"
    ])
    radius_cap = arb(
        preregistration["acceptance"]["artin_difference_radius_max"]
    )

    # Stage 1 freezes the independent regulator-route balls without
    # opening corpus traces or packet factors.
    independent = {}
    export_hash = hashlib.sha256()
    for selected in sample["selected"]:
        case_id = selected["case_id"]
        row = by_id[case_id]
        hnf = row["finite_ideal_hnf"]
        prelude = (
            f'CASE_ID="{case_id}";\n'
            f'D_VALUE={row["d"]};\n'
            f"H11={hnf[0][0]};H12={hnf[0][1]};"
            f"H21={hnf[1][0]};H22={hnf[1][1]};\n"
        )
        completed = subprocess.run(
            ["gp", "-q"],
            input=prelude + gp_source,
            text=True,
            capture_output=True,
            cwd=ROOT,
            check=False,
            timeout=300,
        )
        if (
            completed.returncode
            or "REGULATOR_ROUTE_EXPORT=PASS" not in completed.stdout
            or "RELATIVE_UNIT_NORM_KERNEL_OPENED=0"
            not in completed.stdout
            or "PACKET_POLYNOMIAL_OPENED=0" not in completed.stdout
        ):
            raise RuntimeError(
                f"{case_id} export failed\n"
                f"{completed.stdout}{completed.stderr}"
            )
        export_hash.update(completed.stdout.encode())
        base_polynomial = polynomial_from_gp_vector(
            scalar(completed.stdout, "BASE_POLYNOMIAL_COEFFICIENTS")
        )
        base_regulator = regulator_rank_one(
            base_polynomial,
            scalar(completed.stdout, "BASE_UNIT_COEFFICIENTS"),
        )
        base_class_number = int(
            scalar(completed.stdout, "BASE_CLASS_NUMBER")
        )
        base_torsion = int(
            scalar(completed.stdout, "BASE_TORSION_ORDER")
        )
        supported = json.loads(
            scalar(completed.stdout, "SUPPORTED_CHARACTERS")
        )
        character_balls = []
        effective_characters = []
        for index, character in enumerate(supported, start=1):
            euler = int(
                scalar(completed.stdout, f"CHARACTER_{index}_EULER")
            )
            if euler == 0:
                continue
            if scalar(
                completed.stdout, f"CHARACTER_{index}_BNFCERTIFY"
            ) != "1":
                raise RuntimeError(f"{case_id}: quartic certification failed")
            quartic_polynomial = polynomial_from_gp_vector(
                scalar(
                    completed.stdout,
                    f"CHARACTER_{index}_ABSOLUTE_POLYNOMIAL_COEFFICIENTS",
                )
            )
            quartic_regulator = regulator_signature_21(
                quartic_polynomial,
                scalar(
                    completed.stdout,
                    f"CHARACTER_{index}_UNIT_1_COEFFICIENTS",
                ),
                scalar(
                    completed.stdout,
                    f"CHARACTER_{index}_UNIT_2_COEFFICIENTS",
                ),
            )
            quartic_class_number = int(
                scalar(
                    completed.stdout,
                    f"CHARACTER_{index}_CLASS_NUMBER",
                )
            )
            quartic_torsion = int(
                scalar(
                    completed.stdout,
                    f"CHARACTER_{index}_TORSION_ORDER",
                )
            )
            multiplier = Fraction(
                euler * quartic_class_number * base_torsion,
                base_class_number * quartic_torsion,
            )
            analytic = (
                arb(multiplier.numerator)
                / multiplier.denominator
                * quartic_regulator
                / base_regulator
            )
            analytic += arb(0, inflation.upper())
            effective_characters.append(character)
            character_balls.append(analytic)
        if len(character_balls) != int(
            scalar(completed.stdout, "EFFECTIVE_CHARACTER_COUNT")
        ):
            raise RuntimeError(f"{case_id}: effective count changed")
        independent[case_id] = {
            "group_order": int(scalar(completed.stdout, "GROUP_ORDER")),
            "ray_cyc": json.loads(scalar(completed.stdout, "RAY_CYC")),
            "effective_characters": effective_characters,
            "character_balls": character_balls,
        }

    # Stage 2 opens only the exact corpus traces required by the frozen
    # comparison rule. Packet factors and roots are not read.
    records = []
    total_artin_rows = 0
    for selected in sample["selected"]:
        case_id = selected["case_id"]
        route = independent[case_id]
        corpus_row = json.loads(
            (CORPUS / f"{case_id.lower()}.json").read_text()
        )
        if corpus_row["effective_characters"] != json.dumps(
            route["effective_characters"], separators=(", ", ": ")
        ):
            # GP and json.dumps differ only in whitespace; compare values.
            if json.loads(corpus_row["effective_characters"]) != route[
                "effective_characters"
            ]:
                raise RuntimeError(f"{case_id}: character order changed")
        traces = parse_trace_expressions(corpus_row["powered_traces"])
        q = corpus_row["common_denominator"]
        if len(traces) != len(route["character_balls"]):
            raise RuntimeError(f"{case_id}: powered trace count changed")
        d = by_id[case_id]["d"]
        base_polynomial = (
            fmpq_poly([-(d), 0, 1])
            if d % 4 != 1
            else fmpq_poly([(1 - d) // 4, -1, 1])
        )
        base_roots = isolated_roots(base_polynomial)
        split_root = max(
            (root for root in base_roots if root.imag.contains(0)),
            key=lambda root: float(root.real.mid()),
        )
        exact_character_balls = []
        group_order = route["group_order"]
        for expression in traces:
            y_coefficient, constant = parse_linear_trace(expression)
            trace = (
                split_root.real
                * arb(y_coefficient.numerator)
                / y_coefficient.denominator
                + arb(constant.numerator) / constant.denominator
            )
            exact_value = (trace / 2).acosh()
            exact_value *= arb(group_order) / (2 * q)
            exact_character_balls.append(exact_value)
        for analytic, exact_value in zip(
            route["character_balls"], exact_character_balls
        ):
            if not analytic.contains(exact_value):
                raise RuntimeError(
                    f"{case_id}: independent character ball misses exact trace"
                )

        signs = set()
        cyc = route["ray_cyc"]
        for code in range(group_order):
            element = decode_element(code, cyc)
            signs.add(
                tuple(
                    character_sign(character, element, cyc)
                    for character in route["effective_characters"]
                )
            )
        if not signs:
            signs = {()}
        maximum_radius = arb(0)
        for sign_row in sorted(signs):
            analytic_packet = sum(
                (
                    sign * value
                    for sign, value in zip(
                        sign_row, route["character_balls"]
                    )
                ),
                arb(0),
            ) * 2 / group_order
            exact_packet = sum(
                (
                    sign * value
                    for sign, value in zip(
                        sign_row, exact_character_balls
                    )
                ),
                arb(0),
            ) * 2 / group_order
            difference = analytic_packet - exact_packet
            if not difference.contains(0) or not (
                difference.rad() < radius_cap
            ):
                raise RuntimeError(
                    f"{case_id}: Artin-row Arb difference failed: "
                    f"difference={difference}, radius={difference.rad()}"
                )
            maximum_radius = max(maximum_radius, difference.rad())
        total_artin_rows += len(signs)
        records.append(
            {
                "case_id": case_id,
                "effective_character_count": len(
                    route["character_balls"]
                ),
                "artin_sign_image_size": len(signs),
                "independent_character_balls": [
                    str(value) for value in route["character_balls"]
                ],
                "exact_trace_character_balls": [
                    str(value) for value in exact_character_balls
                ],
                "maximum_artin_difference_radius": str(maximum_radius),
                "status": "PASS",
            }
        )

    result = {
        "schema": "effective-stark-census-q-arb-audit-v1",
        "status": "PASS_50_ROW_INDEPENDENT_ARB_AUDIT",
        "claim_tag": "CERTIFIED_NUMERICAL",
        "population": {
            "sample_rows": len(records),
            "effective_character_occurrences": sum(
                row["effective_character_count"] for row in records
            ),
            "checked_artin_sign_rows": total_artin_rows,
            "all_zero_rows": sum(
                row["effective_character_count"] == 0 for row in records
            ),
        },
        "independence_wall": {
            "independent_formula": preregistration["independent_formula"],
            "relative_unit_norm_kernel_opened": False,
            "packet_factor_or_roots_opened": False,
            "independent_balls_completed_before_corpus_traces_opened": True,
        },
        "precision": {
            "initial_bits": initial_precision_bits,
            "bits": ctx.prec,
            "independent_inflation_radius": str(inflation),
            "artin_difference_radius_cap": str(radius_cap),
        },
        "records": records,
        "source_hashes": {
            "sample_sha256": sha256(SAMPLE),
            "preregistration_sha256": sha256(PREREGISTRATION),
            "gp_script_sha256": sha256(GP_SCRIPT),
            "aggregate_gp_export_stdout_sha256": export_hash.hexdigest(),
        },
    }
    rendered = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.write_text(rendered, encoding="utf-8")
    else:
        print(rendered, end="")


if __name__ == "__main__":
    main()
