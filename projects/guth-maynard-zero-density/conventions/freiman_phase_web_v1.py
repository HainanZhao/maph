"""Exact Cycle 78 additive-to-multiplicative phase-web ledger."""
from __future__ import annotations

from fractions import Fraction as Q


Q_EXP = Q(1, 3)
ETA_EXP = -Q(83, 75)
TARGET = Q(2, 15)


def relation_ledger() -> dict[str, Q]:
    ratio_error = ETA_EXP - Q_EXP
    cross_multiplier = 4 * Q_EXP
    cross_error = ratio_error + cross_multiplier
    return {
        "ratio_error_exponent": ratio_error,
        "cross_multiplier_exponent": cross_multiplier,
        "cross_error_exponent": cross_error,
        "exactness_margin": -cross_error,
    }


def valuation_relation(v1: int, v2: int, v3: int) -> int:
    """Return the forced fourth valuation in v1+v2=v3+v4."""
    return v1 + v2 - v3


def geometric_height_lower_exponent(index: int) -> tuple[int, int]:
    """Encode height(r0*g^j)>=2^j/(C^2 Q^2) as powers of 2 and Q."""
    if index < 0:
        raise ValueError("nonnegative progression index required")
    return (index, -2)


def verify_all() -> dict[str, object]:
    row = relation_ledger()
    if row["ratio_error_exponent"] != -Q(36, 25):
        raise RuntimeError("ratio error")
    if row["cross_error_exponent"] != -Q(8, 75):
        raise RuntimeError("cross error")
    if row["exactness_margin"] != Q(8, 75):
        raise RuntimeError("exactness margin")
    if valuation_relation(3, -2, 4) != -3:
        raise RuntimeError("valuation relation")
    if geometric_height_lower_exponent(7) != (7, -2):
        raise RuntimeError("height encoding")
    return {
        "exact_relation": "ell1+ell2=ell3+ell4 implies r1*r2=r3*r4",
        "cross_error": "Q^4*(eta/Q)=Q^3*eta=X^(-8/75+o(1))",
        "valuation_web": "v_p(r1)+v_p(r2)=v_p(r3)+v_p(r4) for every prime p",
        "progression_image": "r_j=r_0*g^j on every complete arithmetic progression of hit indices",
        "progression_length": "O(log Q), since reduced height(r_0*g^j)>=2^j/(C^2 Q^2) unless g=1",
        "scope_boundary": "no additive relation is forced at packet cardinality X^(2/15); sparse Sidon-type sets remain possible",
        "gate": "use exact valuation webs as the structured output of an ACSI failure, while attacking sparse relation-poor sets analytically",
    }


if __name__ == "__main__":
    print(verify_all())
