#!/usr/bin/env python3
"""Exact common-period audit for the C240 Faddeev two-kernel proposal."""
from __future__ import annotations

import json
from fractions import Fraction

try:
    from .verify_cycle_228_f3_square_residual_block import blocks
except ImportError:  # pragma: no cover - direct replay
    from verify_cycle_228_f3_square_residual_block import blocks


F = Fraction
Linear = tuple[Fraction, Fraction]  # a*t+b in Q(t), t^2=110*t-1


def add(left: Linear, right: Linear) -> Linear:
    return (left[0] + right[0], left[1] + right[1])


def neg(value: Linear) -> Linear:
    return (-value[0], -value[1])


def sub(left: Linear, right: Linear) -> Linear:
    return add(left, neg(right))


def mul(left: Linear, right: Linear) -> Linear:
    a, b = left
    c, d = right
    # ac*t^2+(ad+bc)*t+bd, reduced by t^2=110*t-1.
    return (F(110) * a * c + a * d + b * c, b * d - a * c)


def scale(value: Fraction, pair: Linear) -> Linear:
    return (value * pair[0], value * pair[1])


def render(value: Linear) -> str:
    a, b = value
    if a == 0:
        return str(b)
    if b == 0:
        return f"{a}*t"
    return f"{a}*t+{b}"


def from_c228_pair(item: dict[str, object]) -> Linear:
    alpha = item["alpha"]
    assert isinstance(alpha, list) and len(alpha) == 2
    return (F(str(alpha[0])), F(str(alpha[1])))


def period_pair(start: str) -> tuple[Linear, Linear, Linear, Linear]:
    first, second = blocks()[start][:2]
    p = (from_c228_pair(first), from_c228_pair({"alpha": first["beta"]}))
    q = (from_c228_pair(second), from_c228_pair({"alpha": second["beta"]}))
    return p[0], p[1], q[0], q[1]


def _audit_start(start: str) -> dict[str, object]:
    p0, p1, q0, q1 = period_pair(start)
    # Proportionality of P and Q, or P and swapped Q, is necessary and
    # sufficient for one common ordinary-gamma period system up to the only
    # source-permitted scale/swap changes.
    ordered = sub(mul(p0, q1), mul(p1, q0))
    swapped = sub(mul(p0, q0), mul(p1, q1))
    assert ordered != (F(0), F(0))
    assert swapped != (F(0), F(0))
    return {
        "start": start,
        "first_pair_periods": {
            "P": [render(p0), render(p1)],
            "Q": [render(q0), render(q1)],
        },
        "ordered_proportionality_determinant": render(ordered),
        "swapped_proportionality_determinant": render(swapped),
        "common_period_system_up_to_scale_or_swap": False,
        "individual_normalization_to_Faddeev_product": True,
        "faddeev_MIR_two_kernel_closure_available": False,
        "reason": "FTD can be normalized for one factor at a time, but MIR requires one shared period system and neither permitted period identification exists.",
    }


def audit() -> dict[str, object]:
    # The endpoint polynomial is irreducible: discriminant 110^2-4=576*21.
    # Thus a nonzero reduced a*t+b cannot vanish at the pinned t.
    endpoint = {"polynomial": "t^2-110*t+1", "discriminant": "576*21", "irreducible_over_Q": True}
    rows = [_audit_start(start) for start in ("A", "C")]
    assert all(not row["common_period_system_up_to_scale_or_swap"] for row in rows)
    return {
        "epistemic_status": "PROVED",
        "endpoint_field": endpoint,
        "source_composition": {
            "citation": "Faddeev, arXiv:1201.6464, equations (FTD) and (MIR)",
            "FTD": "one normalized period system per Fourier kernel",
            "MIR": "two-kernel closure requires one shared normalized period system",
            "allowed_period_identifications": ["nonzero common scaling", "swap"],
        },
        "starts": rows,
        "status": "FALSIFIED_FADDEEV_TWO_KERNEL_COMMON_PERIOD_CLOSURE",
        "conclusion": "Neither first C228 pair has one Faddeev period system even up to scaling and swap. Therefore the proposed FTD/MIR two-kernel closure cannot be instantiated, before transform order, auxiliary contour, or Fubini conditions arise. This does not rule out a new mixed-base composition theorem or another integral identity.",
    }


if __name__ == "__main__":
    print(json.dumps(audit(), indent=2, sort_keys=True))
