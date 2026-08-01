#!/usr/bin/env python3
"""Exact local order-ray obstruction screen for remaining noncanonical strata.

Discovery-only: an order>2 local quotient witness plus a nontrivial sign
class forces a nonquadratic character of 1-R.  This filters a stratum; it
does not enumerate AFK form classes, monoid strata, packets, or TCC.
"""

from __future__ import annotations

from math import gcd, isqrt
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKELETON = ROOT / "discovery" / "tcc-sweep-afk-tuple-skeleton-d1024-v1.json"
OUTPUT = ROOT / "discovery" / "tcc-sweep-nonmaximal-local-kernel-d1024-v1.json"


def multiply(left: tuple[int, int], right: tuple[int, int], d: int, delta: int, f: int) -> tuple[int, int]:
    a, b = left
    c, e = right
    constant = f * f * delta * (delta - 1) // 4
    trace = f * delta
    return ((a * c - constant * b * e) % d, (a * e + b * c + trace * b * e) % d)


def power(value: tuple[int, int], exponent: int, d: int, delta: int, f: int) -> tuple[int, int]:
    answer = (1, 0)
    while exponent:
        if exponent & 1:
            answer = multiply(answer, value, d, delta, f)
        value = multiply(value, value, d, delta, f)
        exponent //= 2
    return answer


def order_unit_generator(delta: int, f: int, trace: int) -> tuple[tuple[int, int], int]:
    # f_k=(epsilon^k-epsilon^-k)/sqrt(delta); find j_min(f).
    f1_square = (trace * trace - 4) // delta
    f1 = isqrt(f1_square)
    if f1 * f1 != f1_square:
        raise AssertionError((delta, trace, f1_square))
    previous, current = 0, f1
    trace_previous, trace_current = 2, trace
    k = 1
    while current % f:
        previous, current = current, trace * current - previous
        trace_previous, trace_current = trace_current, trace * trace_current - trace_previous
        k += 1
    if (trace_current - current * delta) % 2:
        raise AssertionError((delta, f, k, current, trace_current))
    return ((trace_current - current * delta) // 2, current // f), k


def local_witness(d: int, delta: int, f: int, fundamental_trace: int) -> dict[str, object]:
    epsilon, j_min = order_unit_generator(delta, f, fundamental_trace)
    epsilon = (epsilon[0] % d, epsilon[1] % d)
    powers: list[tuple[int, int]] = []
    value = (1, 0)
    while value not in powers:
        powers.append(value)
        value = multiply(value, epsilon, d, delta, f)
    if value != (1, 0):
        raise AssertionError(("unit residue did not cycle to identity", d, delta, f, fundamental_trace, epsilon, value, len(powers)))
    positive_unit_image = set(powers)
    sign_class = ((d - 1) % d, 0)
    if sign_class in positive_unit_image:
        return {
            "order_unit_generator_theta_coordinates": list(epsilon),
            "order_unit_generator_exponent_j_min": j_min,
            "positive_global_unit_image_order_mod_d": len(positive_unit_image),
            "sign_class_representative": [d - 1, 0],
            "sign_class_nontrivial": False,
            "local_verdict": "TRIVIAL_SIGN_CLASS",
        }
    # A scalar is enough for every remaining stratum in this finite range.
    witness = None
    for scalar in range(2, d):
        if gcd(scalar, d) != 1:
            continue
        value = (1, 0)
        for exponent in range(1, d * d + 1):
            value = ((value[0] * scalar) % d, 0)
            if value in positive_unit_image:
                if exponent > 2:
                    witness = (scalar, exponent)
                break
        if witness:
            break
    if witness is None:
        constant = f * f * delta * (delta - 1) // 4
        trace = f * delta
        for a in range(d):
            for b in range(d):
                if gcd(a * a + trace * a * b + constant * b * b, d) != 1:
                    continue
                value = (1, 0)
                for exponent in range(1, d * d + 1):
                    value = multiply(value, (a, b), d, delta, f)
                    if value in positive_unit_image:
                        if exponent > 2:
                            witness = ((a, b), exponent)
                        break
                if witness:
                    break
            if witness:
                break
    if witness is None:
        return {
            "order_unit_generator_theta_coordinates": list(epsilon),
            "order_unit_generator_exponent_j_min": j_min,
            "positive_global_unit_image_order_mod_d": len(positive_unit_image),
            "sign_class_representative": [d - 1, 0],
            "sign_class_nontrivial": True,
            "local_verdict": "NO_LOCAL_NONQUADRATIC_WITNESS",
        }
    return {
        "order_unit_generator_theta_coordinates": list(epsilon),
        "order_unit_generator_exponent_j_min": j_min,
        "positive_global_unit_image_order_mod_d": len(positive_unit_image),
        "sign_class_representative": [d - 1, 0],
        "sign_class_nontrivial": True,
        "local_verdict": "NONQUADRATIC_WITNESS",
        "local_nonquadratic_witness": {"residue": list(witness[0]) if isinstance(witness[0], tuple) else [witness[0], 0], "quotient_order": witness[1]},
    }


def main() -> None:
    skeleton = json.loads(SKELETON.read_text())
    records = skeleton["records"]
    root_trace = {}
    for row in records:
        if row["r"] == 1:
            delta = int(row["fundamental_discriminant"])
            root_trace[delta] = min(root_trace.get(delta, 10**100), int(row["n"]) - 2)
    rows = []
    for row in records:
        for f in row["allowed_form_conductors"]:
            delta = int(row["fundamental_discriminant"])
            rows.append({**row, "form_conductor": f, **local_witness(int(row["d"]), delta, f, root_trace[delta])})
    result = {
        "schema": "tcc-sweep-nonmaximal-local-kernel-v1",
        "claim_tag": "OBSERVED",
        "scope": "all AFK tuple/conductor strata through d=1024 before form-class expansion; local order-ray kernel only",
        "criterion": "A nontrivial R and an order>2 local quotient element imply a nonquadratic character chi with chi(R)!=1 by character separation and multiplication in the finite dual group.",
        "input_tuple_conductor_stratum_count": len(rows),
        "nonquadratic_witness_count": sum(row["local_verdict"] == "NONQUADRATIC_WITNESS" for row in rows),
        "trivial_sign_class_count": sum(row["local_verdict"] == "TRIVIAL_SIGN_CLASS" for row in rows),
        "no_local_nonquadratic_witness_count": sum(row["local_verdict"] == "NO_LOCAL_NONQUADRATIC_WITNESS" for row in rows),
        "records": rows,
    }
    OUTPUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print("TCC_SWEEP_NONMAXIMAL_LOCAL_KERNEL=PASS")


if __name__ == "__main__":
    main()
