"""Exact primitive eligible-fibre no-go ledger for Cycle 172."""
from __future__ import annotations

from fractions import Fraction as Q
from math import gcd

from conventions.eligibility_weighted_projective_content_v1 import (
    divisor_content,
    factor_content,
    required_content,
)


def family(m: int) -> dict[str, object]:
    """Return the complete labelled primitive avoidance family at scale m."""
    if m <= 0:
        raise ValueError("positive scale required")
    H, source_depth, edge_depth, target_depth = 10 * m, 2 * m, 5 * m, 2 * m
    alpha, edge, alpha_plus = Q(-4, 5), Q(3, 2), Q(-7, 10)
    d, b, q, a, beta = 5, -4, 2, 3, Q(0)
    rows = []
    for t in range(m // 3 + 1):
        h = 15 * (m + t)
        j = -12 * (m + t)
        hp = 10 * (m + t)
        jp = -7 * (m + t)
        rows.append({"t": t, "h": h, "j": j, "h_plus": hp, "j_plus": jp, "beta": beta})
    return {
        "m": m,
        "H": H,
        "source_depth": source_depth,
        "edge_depth": edge_depth,
        "target_depth": target_depth,
        "alpha": alpha,
        "edge": edge,
        "alpha_plus": alpha_plus,
        "d": d,
        "b": b,
        "q": q,
        "a": a,
        "beta": beta,
        "rows": rows,
    }


def verify_family(m: int) -> dict[str, object]:
    data = family(m)
    H = data["H"]
    source_depth = data["source_depth"]
    edge_depth = data["edge_depth"]
    target_depth = data["target_depth"]
    alpha = data["alpha"]
    edge = data["edge"]
    alpha_plus = data["alpha_plus"]
    d, b, q, a = data["d"], data["b"], data["q"], data["a"]
    if gcd(d, b) != 1 or d * source_depth != H or q * edge_depth != H:
        raise RuntimeError("primitive source or depth ledger")
    if 1 + alpha_plus != edge * (1 + alpha) or q * edge != a:
        raise RuntimeError("exact exponential edge")
    if Q(2 * H, 5 * a * edge_depth) > 1:
        raise RuntimeError("Cycle-167 balance")
    content = factor_content(d=d, b=b, q=q, a=a)
    if content != {"D": 10, "N": -7, "g": 1, "c": 1, "u": 1, "v": 1}:
        raise RuntimeError("primitive two-factor avoidance")
    required = required_content(load=Q(0), D=content["D"], critical_depth=target_depth, height_cap=H)
    if required != 2 or H // 10 != m or m >= target_depth:
        raise RuntimeError("target denominator capacity")
    for row in data["rows"]:
        h, j, hp, jp = row["h"], row["j"], row["h_plus"], row["j_plus"]
        if not (H <= h <= 2 * H and H <= hp <= 2 * H):
            raise RuntimeError("frozen row range")
        if h % a or hp != q * h // a or jp != j + h - hp:
            raise RuntimeError("integral affine map")
        if j + row["beta"] - h * alpha != 0 or jp + row["beta"] - hp * alpha_plus != 0:
            raise RuntimeError("retained beta seed")
    return {
        "m": m,
        "row_count": len(data["rows"]),
        "source_relation": "5 alpha-(-4)=0",
        "edge_relation": "2 E-3=0 and 1+alpha_plus=E(1+alpha)",
        "eligibility": "all rows satisfy divisibility, both frozen ranges, q K_E=H, and balance 2HY/(aK_E)=4/15",
        "projective": "D=10, N=-7, g=c=u=v=1, Q=10, Lambda=0",
        "obstruction": "target capacity depth H/Q=m is below L=2m, while G_req=2 and g=1",
        "moment": "for any nonnegative labelled row weights, M=W/2",
    }


def verify_all() -> dict[str, object]:
    records = [verify_family(m) for m in (1, 2, 3, 12)]
    if [record["row_count"] for record in records] != [1, 1, 2, 5]:
        raise RuntimeError("massed affine fibre count")
    if divisor_content(1) != 1:
        raise RuntimeError("two-factor divisor expansion")
    return {
        "primitive_pullback": "for gcd(d,b)=1, Cycle-171 gives g=gcd(|d|,a) gcd(q,|d+b|), and the two factors are coprime",
        "no_go_family": "the exact m-family retains all complete affine-row and beta labels while u=v=1 and M=W/2",
        "scope": "this rules out forcing M>W from the listed signed abstract local primitive/reducedness/divisibility/range/balance/seed interface alone; alpha=-4/5 and alpha_plus=-7/10 lie outside the actual positive exponential curve, so it does not rule out a global exponential/fibre correlation theorem",
        "boundary": "This is a finite signed abstract local-interface countermodel and typed denominator-capacity obstruction family. It proves no statement about the actual positive-exponential global census, recurrence, skeleton, density, or intervals.",
        "checked_scales": [record["m"] for record in records],
    }


def theorem_record() -> dict[str, object]:
    return {"epistemic_status": "PROVED", **verify_all()}
