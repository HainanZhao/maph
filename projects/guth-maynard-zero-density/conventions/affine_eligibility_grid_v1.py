"""Exact full-affine-fibre eligibility and capacity ledger for Cycle 175."""
from __future__ import annotations
from fractions import Fraction as Q
from math import gcd


def residue_class(h0: int, slope: int, a: int) -> tuple[int, int] | None:
    if a <= 0:
        raise ValueError("positive numerator required")
    divisor = gcd(a, slope)
    if h0 % divisor:
        return None
    modulus = a // divisor
    if modulus == 1:
        return 0, 1
    return (-h0 // divisor * pow((slope // divisor) % modulus, -1, modulus)) % modulus, modulus


def full_ledger(*, parameters: tuple[int, ...], h0: int, slope: int, a: int, q: int, H: int, K: int) -> dict[str, object]:
    if min(a, q, H, K) <= 0 or q * K > H:
        raise ValueError("admissible complete state required")
    ordered = tuple(sorted(set(parameters)))
    ranged = tuple(n for n in ordered if H <= h0 + slope*n <= 2*H and H <= Q(q*(h0+slope*n),a) <= 2*H)
    residue = residue_class(h0, slope, a)
    if residue is None:
        return {"parameters": ordered, "range_parameters": ranged, "residue": None, "eligible": (), "reason": "insoluble_residue", "capacity_ratio": Q(q*K,H)}
    value, modulus = residue
    eligible = tuple(n for n in ranged if n % modulus == value)
    ratio = Q(q*K,H)
    index = 0
    if ratio < Q(1,2):
        index = 1
        while ratio <= Q(1,2**index): index += 1
        index -= 1
    return {"parameters": ordered, "range_parameters": ranged, "residue": residue, "eligible": eligible, "breadth": len(eligible), "discrepancy": Q(len(eligible))-Q(len(ranged),modulus), "capacity_ratio": ratio, "capacity_class": "saturated" if index==0 else f"deficit_{index}"}


def verify_all() -> dict[str, object]:
    # Complete range but deliberately avoid the unique n=0 mod 5 class.
    avoid = full_ledger(parameters=(1,2,3,4,6,7,8,9), h0=25, slope=1, a=5, q=4, H=20, K=5)
    if avoid["eligible"] != () or avoid["capacity_class"] != "saturated":
        raise RuntimeError("residue avoidance")
    hit = full_ledger(parameters=(0,1,2,3,4), h0=25, slope=1, a=5, q=4, H=20, K=5)
    if hit["eligible"] != (0,) or hit["breadth"] != 1:
        raise RuntimeError("eligible grid")
    return {"ledger":"full affine parameter fibre is partitioned by range, exact residue class, eligible breadth, and one common capacity class","countermodel":"a high-parent parameter set can avoid its unique eligible residue class, so parent multiplicity alone gives no breadth","boundary":"This is a finite affine eligibility-grid/discrepancy classifier. It proves no actual breadth lower bound, target packet, recurrence, density, or interval gain."}


def theorem_record() -> dict[str, object]: return {"epistemic_status":"PROVED", **verify_all()}
