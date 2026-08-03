#!/usr/bin/env python3
"""Exact coordinate-ring pullback test for Cycle 208/B045."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

DIMENSION = 6
A6 = ((115, -24), (24, -5))


def coefficient_minor(a: int, aa: int, b: int, bb: int) -> str:
    return f"c_({a},{b})*c_({aa},{bb})-c_({a},{bb})*c_({aa},{b})"


def _add(*polynomials: dict[tuple[str, ...], int]) -> dict[tuple[str, ...], int]:
    result: dict[tuple[str, ...], int] = {}
    for polynomial in polynomials:
        for monomial, coefficient in polynomial.items():
            result[monomial] = result.get(monomial, 0) + coefficient
    return {monomial: coefficient for monomial, coefficient in result.items() if coefficient}


def _scale(coefficient: int, polynomial: dict[tuple[str, ...], int]) -> dict[tuple[str, ...], int]:
    return {monomial: coefficient * value for monomial, value in polynomial.items()}


def _term(coefficient: int, *variables: str) -> dict[tuple[str, ...], int]:
    return {tuple(sorted(variables)): coefficient}


def exact_reduction_audit() -> dict[str, object]:
    """Check F = (c-minor)x_(a,b)x_(aa,bb) + c_(a,bb)c_(aa,b) g.

    Here g is the matching generator of I_X.  This is a literal polynomial
    identity over Z[c_(i,j),x_(i,j)], so it proves the forward implication
    without a chosen coefficient specialization or a division.
    """
    records = []
    for a in range(6):
        for aa in range(a + 1, 6):
            for b in range(6):
                for bb in range(b + 1, 6):
                    x_ab, x_abb = f"x_({a},{b})", f"x_({a},{bb})"
                    x_aab, x_aabb = f"x_({aa},{b})", f"x_({aa},{bb})"
                    c_ab, c_abb = f"c_({a},{b})", f"c_({a},{bb})"
                    c_aab, c_aabb = f"c_({aa},{b})", f"c_({aa},{bb})"
                    pullback = _add(
                        _term(1, c_ab, c_aabb, x_ab, x_aabb),
                        _term(-1, c_abb, c_aab, x_abb, x_aab),
                    )
                    reduced = _add(
                        _term(1, c_ab, c_aabb, x_ab, x_aabb),
                        _term(-1, c_abb, c_aab, x_ab, x_aabb),
                    )
                    source_multiple = _add(
                        _term(1, c_abb, c_aab, x_ab, x_aabb),
                        _term(-1, c_abb, c_aab, x_abb, x_aab),
                    )
                    assert pullback == _add(reduced, source_multiple)
                    records.append({
                        "minor_indices": [[a, b], [aa, bb]],
                        "identity_checked": "F=(c-minor)*x_(a,b)*x_(aa,bb)+c_(a,bb)*c_(aa,b)*g_(a,aa;b,bb)",
                    })
    assert len(records) == 225
    return {
        "epistemic_status": "PROVED",
        "identity_count": 225,
        "coefficient_ring": "Z[c_(i,j),x_(i,j)]",
        "all_identities_checked": True,
        "records": records,
    }


def source_rank_one_ideal() -> dict[str, object]:
    records = []
    for a in range(6):
        for aa in range(a + 1, 6):
            for b in range(6):
                for bb in range(b + 1, 6):
                    records.append({
                "minor_indices": [[a, b], [aa, bb]],
                "generator": f"x_({a},{b})*x_({aa},{bb})-x_({a},{bb})*x_({aa},{b})",
                    })
    assert len(records) == 225
    return {"epistemic_status": "PROVED", "coordinate_count": 36,
            "variety": "X=Spec(C[x_(a,b)]/I_X), rank-one packet variety",
            "generator_count": 225, "generators": records}


def diagonal_pullbacks() -> dict[str, object]:
    records = []
    for a in range(6):
        for aa in range(a + 1, 6):
            for b in range(6):
                for bb in range(b + 1, 6):
                    c_minor = coefficient_minor(a, aa, b, bb)
                    records.append({
                "minor_indices": [[a, b], [aa, bb]],
                "target_minor": f"y_({a},{b})*y_({aa},{bb})-y_({a},{bb})*y_({aa},{b})",
                "J_pullback_mod_I_X": f"({c_minor})*x_({a},{b})*x_({aa},{bb})",
                "containment_iff": f"{c_minor}=0",
                    })
    assert len(records) == 225
    return {"epistemic_status": "PROVED", "map_family": "J_c(e_(a,b))=c_(a,b)*chi_(a,b)",
            "coefficient_count": 36, "pullback_count": 225, "records": records,
            "all_target_minors_pull_back_to_I_X_iff": "all 225 rank-one minors of c vanish"}


def nonmembership_witness() -> dict[str, object]:
    """Exact witness for the converse, over every coefficient specialization.

    At the rank-one source point x_(i,j)=1, every generator of I_X evaluates
    to zero.  Thus if a specialized pullback belonged to I_X, its evaluation
    would vanish.  Its reduced expression evaluates to the corresponding
    coefficient minor, proving non-membership whenever that scalar is nonzero.
    """
    witnesses = []
    for a in range(6):
        for aa in range(a + 1, 6):
            for b in range(6):
                for bb in range(b + 1, 6):
                    c_minor = coefficient_minor(a, aa, b, bb)
                    witnesses.append({
                        "minor_indices": [[a, b], [aa, bb]],
                        "rank_one_specialization": "x_(i,j)=1 for all 0<=i,j<6",
                        "source_generator_value": "1*1-1*1=0",
                        "reduced_pullback_value": c_minor,
                        "consequence": f"If {c_minor} is nonzero after any coefficient specialization, its target-minor pullback is not in I_X.",
                    })
    assert len(witnesses) == 225
    return {
        "epistemic_status": "PROVED",
        "witness_count": 225,
        "argument": "The specialization x_(i,j)=1 annihilates I_X. Therefore ideal membership forces zero specialization; each displayed pullback specializes to its coefficient minor.",
        "witnesses": witnesses,
    }


def a6_audit() -> dict[str, object]:
    for a in range(6):
        for b in range(6):
            assert ((115*a-24*b) % 6, (24*a-5*b) % 6) == (a,b)
    return {"epistemic_status": "PROVED", "A6_mod_6": [[1,0],[0,1]],
            "family_covariant": True, "coefficient_constraints_from_A6": 0,
            "all_square_reduction_from_A6": False}


def run() -> dict[str, object]:
    exact_reduction = exact_reduction_audit()
    source, pullback = source_rank_one_ideal(), diagonal_pullbacks()
    witness, a6 = nonmembership_witness(), a6_audit()
    return {"schema": "sic-stark-cycle-208-coordinate-ring-pullback-prototype-v1",
            "epistemic_status": "PROVED",
            "claim_boundary": "For the full label-preserving diagonal family J_c, all 225 target two-by-two minor pullbacks lie in the rank-one source ideal exactly when the corresponding 225 c-minors vanish. This supplies neither c nor a source interface, target-minor identity, AFK, fusion, Stark, or TCC.",
            "exact_reduction_audit": exact_reduction,
            "source_rank_one_ideal": source, "diagonal_pullbacks": pullback,
            "nonmembership_witness": witness, "a6_audit": a6,
            "gate_outcome": {"coordinate_ring_criterion": "PROVED_FOR_FULL_DIAGONAL_FAMILY",
                             "source_interface_coefficients": "OPEN_NOT_SUPPLIED",
                             "remaining_design_problem": "Derive c from a source-authorized equation-(66) construction, or falsify every constrained source-defined map family."}}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(); parser.add_argument("--output", type=Path); args = parser.parse_args()
    text = json.dumps(run(), indent=2, sort_keys=True) + "\n"
    print(text, end="") if args.output is None else args.output.write_text(text, encoding="utf-8")
