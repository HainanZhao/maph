"""Frozen symbolic conventions for the Cycle 4 CRR-U formalization.

This module contains definitions only.  It neither evaluates a witness nor
asserts that a witness exists or is impossible.
"""
from __future__ import annotations

from fractions import Fraction


SCALE_EXPONENTS = {
    "global_height_T0": 13,
    "local_height_H": 12,
    "polynomial_length_L": 10,
    "cardinality_R": 8,
    "affine_scale_M": 2,
    "rational_height_Q": 4,
    "large_value_V": 7,
}

SIGMA = Fraction(7, 10)
SEPARATION_EXPONENT_IN_H = Fraction(1, 100)

# delta(v)=1/sqrt(log v) is fixed for integers v>=3.  Thus delta(v)->0,
# while v**delta(v)=exp(sqrt(log v)) supplies explicit subpower slack.
SLACK = "delta(v)=1/sqrt(log(v)) for integer v>=3"

FOURIER_CONVENTION = "hat(f)(xi)=integral_R f(u) exp(-2*pi*i*xi*u) du"
EXPONENTIAL_CONVENTION = "e(x)=exp(2*pi*i*x)"

# eta and step are exact definitions of standard C-infinity functions.
SMOOTH_FUNCTIONS = {
    "eta": "eta(x)=0 for x<=0; eta(x)=exp(-1/x) for x>0",
    "step": "step(x)=eta(x)/(eta(x)+eta(1-x))",
    "w": "w(u)=step(5*(u-1))*step(5*(2-u))",
    "psi1": "psi1(x)=eta(1-x^2)/eta(1)",
    "psi2": "psi2(u)=eta(1-4*(u-1)^2)/eta(1)",
}

SUPPORT_AND_PLATEAU = {
    "w": "0<=w<=1; supp(w) subset [1,2]; w=1 on [6/5,9/5]",
    "psi1": "psi1>=0; supp(psi1) subset [-1,1]; psi1(0)=1",
    "psi2": "psi2>=0; supp(psi2) subset [1/2,3/2]; psi2(1)=1",
}


def exact_scale_checks() -> dict[str, list[Fraction]]:
    """Return the exact exponents used only for source-bound bookkeeping."""
    e = SCALE_EXPONENTS
    h = Fraction(e["local_height_H"])
    n = Fraction(e["polynomial_length_L"])
    r = Fraction(e["cardinality_R"])
    value = Fraction(e["large_value_V"])
    large_values = [2 * n - 2 * value, Fraction(18, 5) * n - 4 * value, h + Fraction(12, 5) * n - 4 * value]
    energy = [r + n * (4 - 4 * SIGMA), Fraction(21, 8) * r + h / 4 + n * (1 - 2 * SIGMA), 3 * r + n * (1 - 2 * SIGMA)]
    s3 = [2 * h + Fraction(3, 2) * r, h + r + n * (3 - 2 * SIGMA), h + 2 * r + n * (Fraction(3, 2) - SIGMA), Fraction(9, 8) * h + Fraction(29, 16) * r + n * (Fraction(3, 2) - SIGMA)]
    rational_moments = [Fraction(-4) + 2 * 6, Fraction(-4) + 4 * 6]
    affine = [6 * e["affine_scale_M"] + 2 * rational_moments[0], 4 * e["affine_scale_M"] + rational_moments[1]]
    if large_values != [6, 8, 8]:
        raise RuntimeError("large-values exponent mismatch")
    if energy != [20, 20, 20]:
        raise RuntimeError("energy exponent mismatch")
    if s3 != [36, 36, 36, 36]:
        raise RuntimeError("S3 exponent mismatch")
    if rational_moments != [8, 20]:
        raise RuntimeError("rational-mass moment exponent mismatch")
    if affine != [28, 28]:
        raise RuntimeError("affine exponent mismatch")
    if n < Fraction(3, 4) * h:
        raise RuntimeError("four-term S3 range mismatch")
    return {"large_values": large_values, "energy": energy, "s3": s3, "rational_moments": rational_moments, "affine": affine}
