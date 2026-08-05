#!/usr/bin/env python3
"""Cycle 34 exact characteristic-zero affine-obstruction search."""
from __future__ import annotations

from fractions import Fraction
import hashlib
import json
import math
from pathlib import Path
import subprocess
import sys
import time

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "discovery"))
import lrc_gf2_tensor as source
import lrc_odd_tensor as odd

OUT = ROOT / "discovery/out/cycle34-rational-tensor"
FIELD = 5
VARIABLES = 1394
EXPECTED_HASH = "de06f7bea5bf1673f5a31d2febcac3e130fd67f5bf1ed6112e237b76a0cf5f84"
SOLVE_CAP = 16
AUGMENTATION_CAP = 8
HEIGHT_CAP = 262144
PARI_STACK = 4294967296


def gf5_skeleton(equations: list[int]) -> tuple[list[int], list[int], int]:
    """Return original pivot rows/columns and first inconsistent row."""
    coefficient_mask = (1 << VARIABLES) - 1
    vector_mask = (1 << (VARIABLES + 1)) - 1
    basis: dict[int, tuple[int, ...]] = {}
    basis_rows: list[int] = []
    pivot_columns: list[int] = []
    for index, coefficients in enumerate(equations):
        row = odd.binary_row(coefficients, VARIABLES, FIELD)
        while True:
            support = 0
            for plane in row:
                support |= plane & coefficient_mask
            if not support:
                if odd.value(row, VARIABLES):
                    return basis_rows, pivot_columns, index
                break
            pivot = (support & -support).bit_length() - 1
            pivot_value = odd.value(row, pivot)
            if pivot not in basis:
                inverse = pow(pivot_value, -1, FIELD)
                basis[pivot] = odd.scale(row, inverse, FIELD)
                basis_rows.append(index)
                pivot_columns.append(pivot)
                break
            row = odd.subtract(row, basis[pivot], pivot_value, FIELD, vector_mask)
    raise AssertionError("GF(5) system unexpectedly consistent")


def bit_at(row: int, column: int) -> int:
    return (row >> column) & 1


def exact_solve(equations: list[int], basis_rows: list[int], pivot_columns: list[int], target_index: int, solve_ordinal: int) -> list[Fraction]:
    """Solve B^T alpha=target exactly using pinned GP/PARI."""
    gp_path = OUT / f"solve-{solve_ordinal:02d}.gp"
    answer_path = OUT / f"solve-{solve_ordinal:02d}.txt"
    answer_path.unlink(missing_ok=True)
    matrix_columns = []
    for row_index in basis_rows:
        row = equations[row_index]
        matrix_columns.append("Col([" + ",".join(str(bit_at(row, col)) for col in pivot_columns) + "])")
    target = equations[target_index]
    target_vector = ",".join(str(bit_at(target, col)) for col in pivot_columns)
    program = (
        "Btrans=Mat([" + ",".join(matrix_columns) + "]);\n"
        "rhs=Col([" + target_vector + "]);\n"
        "alpha=matsolve(Btrans,rhs);\n"
        f'file="{answer_path}";\n'
        "for(i=1,#alpha,write(file,numerator(alpha[i]),\"/\",denominator(alpha[i])));\n"
        "quit;\n"
    )
    gp_path.write_text(program, encoding="utf-8")
    completed = subprocess.run(
        ["taskset", "-c", "0-2", "gp", "-q", "-f", "-s", str(PARI_STACK), str(gp_path)],
        cwd=ROOT,
        stdin=subprocess.DEVNULL,
        text=True,
        capture_output=True,
        timeout=1800,
        check=False,
    )
    if completed.returncode != 0 or not answer_path.exists():
        raise RuntimeError(f"GP solve failed: {completed.stderr[-2000:]}")
    values = [Fraction(line.strip()) for line in answer_path.read_text(encoding="utf-8").splitlines() if line.strip()]
    if len(values) != len(basis_rows):
        raise AssertionError("GP solution length")
    return values


def clear_and_compare(equations: list[int], basis_rows: list[int], target_index: int, alpha: list[Fraction]) -> dict[str, object]:
    denominator = 1
    for value in alpha:
        denominator = math.lcm(denominator, value.denominator)
        if denominator.bit_length() > HEIGHT_CAP:
            return {"status": "CAP", "reason": "denominator height cap", "height_bits": denominator.bit_length()}
    scaled = [value.numerator * (denominator // value.denominator) for value in alpha]
    max_height = max([denominator.bit_length()] + [abs(value).bit_length() for value in scaled])
    if max_height > HEIGHT_CAP:
        return {"status": "CAP", "reason": "coefficient height cap", "height_bits": max_height}

    column_sums = [0] * VARIABLES
    for coefficient, row_index in zip(scaled, basis_rows):
        bits = equations[row_index]
        while bits:
            bit = bits & -bits
            column_sums[bit.bit_length() - 1] += coefficient
            bits ^= bit
    target = equations[target_index]
    mismatches = []
    for column, total in enumerate(column_sums):
        expected = denominator if target & (1 << column) else 0
        if total != expected:
            mismatches.append((column, total - expected))
    affine_residual = denominator - sum(scaled)
    return {
        "status": "MATCH" if not mismatches else "RANK_INCREASE",
        "denominator": denominator,
        "scaled": scaled,
        "height_bits": max_height,
        "affine_residual": affine_residual,
        "mismatch_count": len(mismatches),
        "first_mismatch": list(mismatches[0]) if mismatches else None,
    }


def primitive_certificate(basis_rows: list[int], target_index: int, denominator: int, scaled: list[int]) -> tuple[list[dict[str, object]], int]:
    coefficients = [-value for value in scaled] + [denominator]
    rows = basis_rows + [target_index]
    divisor = 0
    for value in coefficients:
        divisor = math.gcd(divisor, abs(value))
    coefficients = [value // divisor for value in coefficients]
    first = next(value for value in coefficients if value)
    if first < 0:
        coefficients = [-value for value in coefficients]
    terms = [{"row_index": row, "coefficient": str(value)} for row, value in zip(rows, coefficients) if value]
    return terms, sum(coefficients)


def verify_certificate(equations: list[int], terms: list[dict[str, object]]) -> int:
    sums = [0] * VARIABLES
    rhs = 0
    for term in terms:
        coefficient = int(term["coefficient"])
        rhs += coefficient
        bits = equations[int(term["row_index"])]
        while bits:
            bit = bits & -bits
            sums[bit.bit_length() - 1] += coefficient
            bits ^= bit
    if any(sums) or rhs == 0:
        raise AssertionError("invalid integer left-null certificate")
    return rhs


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    started = time.monotonic()
    prepared = source.p199_prepare()
    assignments = source.initial_assignments(prepared["allowed"])
    assignment_hash = hashlib.sha256(b"".join(bytes(row) for row in assignments)).hexdigest()
    if assignment_hash != EXPECTED_HASH or len(prepared["reps"]) != VARIABLES or len(assignments) != 4243:
        raise AssertionError("frozen evaluation interface")
    full = (1 << VARIABLES) - 1
    equations = [source.equation(row, prepared["option_masks"], VARIABLES) & full for row in assignments]

    modular = odd.eliminate(equations, VARIABLES, FIELD)
    if modular["status"] != "INCONSISTENT" or modular["rank"] != 1228 or len(modular["contradiction_terms"]) != 985:
        raise AssertionError("Cycle 33 GF(5) replay")
    basis_rows, pivot_columns, contradiction_row = gf5_skeleton(equations)
    if not (len(basis_rows) == len(pivot_columns) == 1228):
        raise AssertionError("skeleton size")

    basis_set = set(basis_rows)
    candidate_rows = [contradiction_row] + [index for index in range(len(equations)) if index not in basis_set and index != contradiction_row]
    augmentations = []
    solve_count = 0
    result: dict[str, object] | None = None
    for target_index in candidate_rows:
        if solve_count >= SOLVE_CAP:
            result = {"status": "CAP", "reason": "exact solve cap"}
            break
        solve_count += 1
        alpha = exact_solve(equations, basis_rows, pivot_columns, target_index, solve_count)
        comparison = clear_and_compare(equations, basis_rows, target_index, alpha)
        if comparison["status"] == "CAP":
            result = comparison
            break
        if comparison["status"] == "RANK_INCREASE":
            if len(augmentations) >= AUGMENTATION_CAP:
                result = {"status": "CAP", "reason": "exact basis augmentation cap", "last_comparison": comparison}
                break
            mismatch_column, residual = comparison["first_mismatch"]
            augmentations.append({"row_index": target_index, "column_index": mismatch_column, "schur_residual_numerator": str(residual), "denominator": str(comparison["denominator"])})
            basis_rows.append(target_index)
            pivot_columns.append(mismatch_column)
            basis_set.add(target_index)
            continue
        if comparison["affine_residual"] == 0:
            continue
        terms, rhs = primitive_certificate(basis_rows, target_index, comparison["denominator"], comparison["scaled"])
        verified_rhs = verify_certificate(equations, terms)
        if rhs != verified_rhs:
            raise AssertionError("certificate RHS replay")
        result = {
            "status": "PROVED_RATIONAL_INCONSISTENCY",
            "target_row": target_index,
            "basis_rank": len(basis_rows),
            "height_bits": comparison["height_bits"],
            "certificate_terms": terms,
            "certificate_rhs": str(rhs),
        }
        break
    if result is None:
        result = {"status": "CAP", "reason": "candidate scan exhausted"}

    payload = {
        "status": "PASS",
        "epistemic_status": "PROVED" if result["status"] == "PROVED_RATIONAL_INCONSISTENCY" else "OBSERVED",
        "assignment_hash": assignment_hash,
        "assignments": len(assignments),
        "predicate_columns": VARIABLES,
        "gf5_skeleton": {"rank": 1228, "contradiction_size": 985, "contradiction_row": contradiction_row, "basis_rows": basis_rows, "pivot_columns": pivot_columns},
        "exact_solves": solve_count,
        "augmentations": augmentations,
        "outcome": result,
        "wall_seconds": time.monotonic() - started,
    }
    temporary = OUT / "result.json.tmp"
    temporary.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    temporary.replace(OUT / "result.json")
    print(json.dumps({"status": payload["status"], "outcome": result["status"], "basis_rank": result.get("basis_rank"), "certificate_terms": len(result.get("certificate_terms", [])), "height_bits": result.get("height_bits"), "wall_seconds": payload["wall_seconds"]}, sort_keys=True))


if __name__ == "__main__":
    main()
