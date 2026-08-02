"""Exact effective-degree and wrap-fiber ledgers for Cycle 163."""
from __future__ import annotations

from fractions import Fraction
from typing import Sequence

def effective_support(weights: Sequence[Fraction]) -> Fraction:
    if any(x < 0 for x in weights):
        raise ValueError("nonnegative weights required")
    e = sum((x*x for x in weights), Fraction())
    return Fraction() if not e else sum(weights, Fraction())**2/e

def wrap_fiber_ledger(fibers: Sequence[Sequence[Fraction]]) -> dict[str, Fraction]:
    flat = tuple(x for fiber in fibers for x in fiber)
    d = sum(flat, Fraction())
    e = sum((x*x for x in flat), Fraction())
    d2 = sum((sum(fiber, Fraction())**2 for fiber in fibers), Fraction())
    rw = Fraction() if not d2 else d*d/d2
    rf = Fraction() if not e else d2/e
    return {"D": d, "E": e, "wrap_square_mass": d2, "R": effective_support(flat), "R_wrap": rw, "R_fiber": rf}

def theorem_record() -> dict[str, object]:
    return {"factorization": "R_s=R_s^wrap R_s^fiber exactly", "common_wrap": "in the complementary arm R_s^wrap<H, sum_mD_(s,m)^2=D_s^2/R_s^wrap>D_s^2/H and R_s^fiber>=H; after the D_s^2-weighted global split, common-wrap mass is aggregate rather than one-fiber mass; a common wrap gives |log(q_v/q_w)+2pi(d_v-d_w)/D|<<1/(KQ)", "boundary": "this conditional pullback does not prove a rational web closes transport, a moment bound, density, or intervals"}
