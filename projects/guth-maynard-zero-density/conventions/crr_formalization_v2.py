"""Corrected symbolic conventions for the Cycle 4 CRR-U formalization.

Every exponent is stored as ``(constant, delta_coefficient)`` and denotes
``constant + delta_coefficient*delta(v)``.  This module defines and checks
bookkeeping only; it makes no existence or incompatibility claim.
"""
from __future__ import annotations

from fractions import Fraction


AffineExponent = tuple[Fraction, Fraction]

SCALE_EXPONENTS = {
    "global_height_T0": 13,
    "local_height_H": 12,
    "polynomial_length_L": 10,
    "cardinality_center_R": 8,
    "affine_scale_M": 2,
    "rational_height_Q": 4,
    "large_value_center_V": 7,
}

SIGMA_V: AffineExponent = (Fraction(7, 10), Fraction(-1, 10))
CARDINALITY_UPPER: AffineExponent = (Fraction(8), Fraction(1))
SEPARATION_EXPONENT_IN_H = Fraction(1, 100)
SLACK = "delta(v)=1/sqrt(log(v)) for integer v>=3"
FOURIER_CONVENTION = "hat(f)(xi)=integral_R f(u) exp(-2*pi*i*xi*u) du"
EXPONENTIAL_CONVENTION = "e(x)=exp(2*pi*i*x)"
S3_REALITY_INVOLUTION = "conjugate(I_(m1,m2,m3))=I_(-m3,-m2,-m1), after reversing t2 and t3"

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


def add(*values: AffineExponent) -> AffineExponent:
    return (sum((value[0] for value in values), Fraction()), sum((value[1] for value in values), Fraction()))


def scale(value: Fraction | int, exponent: AffineExponent) -> AffineExponent:
    factor = Fraction(value)
    return (factor * exponent[0], factor * exponent[1])


def exact_slack_checks() -> dict[str, list[AffineExponent]]:
    """Return all exact affine-in-delta rows for the admitted witness."""
    h: AffineExponent = (Fraction(12), Fraction())
    n: AffineExponent = (Fraction(10), Fraction())
    m: AffineExponent = (Fraction(2), Fraction())
    value: AffineExponent = (Fraction(7), Fraction(-1))
    r = CARDINALITY_UPPER
    sigma = SIGMA_V

    large_values = [
        add(scale(2, n), scale(-2, value)),
        add(scale(Fraction(18, 5), n), scale(-4, value)),
        add(h, scale(Fraction(12, 5), n), scale(-4, value)),
    ]
    energy = [
        add(r, scale(4, n), scale(-4, scale(10, sigma))),
        add(scale(Fraction(21, 8), r), scale(Fraction(1, 4), h), n, scale(-2, scale(10, sigma))),
        add(scale(3, r), n, scale(-2, scale(10, sigma))),
    ]
    s3 = [
        add(scale(2, h), scale(Fraction(3, 2), r)),
        add(h, r, scale(3, n), scale(-2, scale(10, sigma))),
        add(h, scale(2, r), scale(Fraction(3, 2), n), scale(-1, scale(10, sigma))),
        add(scale(Fraction(9, 8), h), scale(Fraction(29, 16), r), scale(Fraction(3, 2), n), scale(-1, scale(10, sigma))),
    ]
    rational_lower_moments = [(Fraction(8), Fraction(-3)), (Fraction(20), Fraction(-5))]
    rational_induced_affine_lower = [add(scale(6, m), scale(2, rational_lower_moments[0])), add(scale(4, m), rational_lower_moments[1])]
    source_affine_upper_from_base = [(Fraction(28), Fraction(2)), (Fraction(28), Fraction(1))]

    expected = {
        "large_values_upper": [(6, 2), (8, 4), (8, 4)],
        "energy_upper_at_cardinality_upper": [(20, 5), (20, Fraction(37, 8)), (20, 5)],
        "s3_upper_at_cardinality_upper": [(36, Fraction(3, 2)), (36, 3), (36, 3), (36, Fraction(45, 16))],
        "rational_lower_moments": [(8, -3), (20, -5)],
        "rational_induced_affine_lower": [(28, -6), (28, -5)],
        "source_affine_upper_from_base": [(28, 2), (28, 1)],
    }
    actual = {
        "large_values_upper": large_values,
        "energy_upper_at_cardinality_upper": energy,
        "s3_upper_at_cardinality_upper": s3,
        "rational_lower_moments": rational_lower_moments,
        "rational_induced_affine_lower": rational_induced_affine_lower,
        "source_affine_upper_from_base": source_affine_upper_from_base,
    }
    normalized_expected = {key: [(Fraction(a), Fraction(b)) for a, b in rows] for key, rows in expected.items()}
    if actual != normalized_expected:
        raise RuntimeError("corrected CRR slack bookkeeping mismatch")
    if n[0] < Fraction(3, 4) * h[0]:
        raise RuntimeError("four-term S3 range mismatch")
    return actual

