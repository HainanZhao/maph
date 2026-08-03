#!/usr/bin/env python3
"""Exact factorwise recurrence audit of C198 target binomials for C207/B044.

For each elementary target binomial, this records the class multiset of the
four capital-Gamma factors in each product.  The class is invariant under the
admitted T1/T2 shifts and changes sign under normalized reflection.  A class
mismatch therefore rules out *only* a factorwise shift/reflection derivation
of the target identity; it says nothing about the special endpoint value.
"""
from __future__ import annotations

import argparse
from fractions import Fraction
import json
from pathlib import Path

try:  # Supports package tests and direct proof-script replay.
    from proof.verify_cycle_198_analytic_frequency_endpoint import characteristic_ledger
except ModuleNotFoundError:
    from verify_cycle_198_analytic_frequency_endpoint import characteristic_ledger


DIMENSION = 6
CLASS_MODULUS = 72


def gamma_class(u: Fraction, v: Fraction, discrete: int) -> int:
    """Return 3*(m-5u+v) mod 72 for one capital-Gamma factor."""

    value = 3 * (Fraction(discrete) - 5 * u + v)
    assert value.denominator == 1
    return value.numerator % CLASS_MODULUS


def unoriented_class(value: int) -> int:
    """Reflection identifies class c with -c."""

    residue = value % CLASS_MODULUS
    return min(residue, (-residue) % CLASS_MODULUS)


def relation_basis_audit() -> dict[str, object]:
    """Check the class law for the exact frozen relation generators."""

    probes = [
        (Fraction(-1, 9), Fraction(1, 9), -7),
        (Fraction(0), Fraction(0), 2),
        (Fraction(5, 18), Fraction(-5, 18), 20),
    ]
    records = []
    for u, v, discrete in probes:
        initial = gamma_class(u, v, discrete)
        t1 = gamma_class(u + 1, v, discrete + 5)
        t2 = gamma_class(u, v + 1, discrete - 1)
        reflection = gamma_class(1 - u, 1 - v, 4 - discrete)
        assert t1 == initial
        assert t2 == initial
        assert reflection == (-initial) % CLASS_MODULUS
        records.append({
            "factor": {"u": str(u), "v": str(v), "m": discrete},
            "class": initial,
            "T1_class": t1,
            "T2_class": t2,
            "reflection_class": reflection,
            "unoriented_class": unoriented_class(initial),
        })
    return {
        "epistemic_status": "PROVED",
        "class": "c=3*(m-5*u+v) mod 72 for mu=u*omega+v",
        "generators": {
            "T1": "(u,v,m)->(u+1,v,m+5)",
            "T2": "(u,v,m)->(u,v+1,m-1)",
            "normalized_reflection": "(u,v,m)->(1-u,1-v,4-m), c->-c",
        },
        "records": records,
        "T1_T2_preserve_class": True,
        "reflection_negates_class": True,
    }


def endpoint_factor_records(row: dict[str, object]) -> list[dict[str, object]]:
    """Express C198's two oriented factors in the frozen relation lattice."""

    sigma = int(row["centered_frequency_sigma"])
    discrete = int(row["N"])
    alpha_u = Fraction(sigma, 18)
    alpha_v = -alpha_u
    first_class = gamma_class(alpha_u, alpha_v, discrete)
    second_class = gamma_class(-alpha_u, -alpha_v, 4 - discrete)
    assert first_class == (3 * discrete - sigma) % CLASS_MODULUS
    assert second_class == (12 - 3 * discrete + sigma) % CLASS_MODULUS
    return [
        {
            "role": "Gamma_M(alpha,N)",
            "u": str(alpha_u),
            "v": str(alpha_v),
            "m": discrete,
            "class_mod_72": first_class,
            "unoriented_class": unoriented_class(first_class),
        },
        {
            "role": "Gamma_M(-alpha,4-N)",
            "u": str(-alpha_u),
            "v": str(-alpha_v),
            "m": 4 - discrete,
            "class_mod_72": second_class,
            "unoriented_class": unoriented_class(second_class),
        },
    ]


def product_signature(left: dict[str, object], right: dict[str, object]) -> dict[str, object]:
    """Record one target-product's full factorwise invariant signature."""

    factors = endpoint_factor_records(left) + endpoint_factor_records(right)
    signature = sorted(factor["unoriented_class"] for factor in factors)
    assert len(factors) == 4 and len(signature) == 4
    return {
        "characteristics": [left["characteristic"], right["characteristic"]],
        "common_scalar": "(24*Gamma_M(Q,0))^2",
        "factors": factors,
        "unoriented_factor_signature": signature,
    }


def target_binomial_ledger() -> dict[str, object]:
    """Audit every 5-by-5 elementary C198 binomial before classifying it."""

    endpoint = characteristic_ledger()
    rows = endpoint["records"]
    assert len(rows) == DIMENSION * DIMENSION
    assert all(row["endpoint_value_finite_nonzero"] for row in rows)
    by_label = {tuple(row["characteristic"]): row for row in rows}
    records = []
    for first in range(DIMENSION - 1):
        for second in range(DIMENSION - 1):
            northwest = by_label[(first, second)]
            southeast = by_label[(first + 1, second + 1)]
            northeast = by_label[(first, second + 1)]
            southwest = by_label[(first + 1, second)]
            positive = product_signature(northwest, southeast)
            negative = product_signature(northeast, southwest)
            matches = positive["unoriented_factor_signature"] == negative["unoriented_factor_signature"]
            records.append({
                "square": [[first, second], [first + 1, second + 1]],
                "target_binomial": (
                    f"L_({first},{second})*L_({first + 1},{second + 1})"
                    f"-L_({first},{second + 1})*L_({first + 1},{second})"
                ),
                "positive_product": positive,
                "negative_product": negative,
                "factorwise_signature_match": matches,
                "factorwise_recurrence_status": (
                    "OPEN_RESIDUAL_PREFACTOR_AUDIT_REQUIRED"
                    if matches
                    else "FALSIFIED_FOR_DECLARED_FACTORWISE_SHIFT_REFLECTION_ROUTE"
                ),
                "endpoint_value_status": "NOT_EVALUATED_NO_NONVANISHING_CLAIM",
            })
    assert len(records) == (DIMENSION - 1) ** 2
    match_count = sum(record["factorwise_signature_match"] for record in records)
    return {
        "epistemic_status": "PROVED",
        "target_binomial_count": len(records),
        "common_scalar_cancels_only_between_formed_products": True,
        "factorwise_signature_match_count": match_count,
        "factorwise_signature_mismatch_count": len(records) - match_count,
        "records": records,
        "scope": (
            "A mismatch prevents a derivation from the admitted factorwise "
            "shift/reflection basis. It does not evaluate the endpoint binomial "
            "or rule out a multifactor identity."
        ),
    }


def run() -> dict[str, object]:
    basis = relation_basis_audit()
    binomials = target_binomial_ledger()
    assert basis["T1_T2_preserve_class"]
    assert basis["reflection_negates_class"]
    assert binomials["target_binomial_count"] == 25
    return {
        "schema": "sic-stark-cycle-207-target-binomial-recurrence-prototype-v1",
        "epistemic_status": "PROVED",
        "claim_boundary": (
            "For all 25 elementary C198 target binomials, this exact ledger "
            "tests only the stated factorwise Gamma_M shift/reflection relation "
            "basis. A signature mismatch rules out that derivation route; a "
            "signature match is not an identity. No endpoint-binomial value, "
            "multifactor equation-(66) theorem, projective equality, AFK, "
            "fusion, Stark, or TCC statement is proved."
        ),
        "relation_basis_audit": basis,
        "target_binomial_ledger": binomials,
        "gate_outcome": {
            "declared_factorwise_gamma_recurrence_route": (
                "FALSIFIED_FOR_EACH_SIGNATURE_MISMATCH_ONLY"
            ),
            "remaining_design_problem": (
                "For every unresolved target binomial, derive a genuinely "
                "multifactor equation-(66) relation, global pairing, or certified "
                "endpoint evaluation before asserting a projective intertwiner."
            ),
        },
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    rendered = json.dumps(run(), indent=2, sort_keys=True) + "\n"
    if args.output is None:
        print(rendered, end="")
    else:
        args.output.write_text(rendered, encoding="utf-8")


if __name__ == "__main__":
    main()
