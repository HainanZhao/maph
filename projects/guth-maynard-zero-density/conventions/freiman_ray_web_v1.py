"""Cycle 125 high-multiplicity rational-ray Freiman ledger."""

from __future__ import annotations

from fractions import Fraction


def threshold_ledger(xi: Fraction, mu: Fraction) -> dict[str, Fraction | bool]:
    if not Fraction(16, 25) <= xi < Fraction(58, 75):
        raise ValueError("xi outside lower band")
    if mu < 0 or mu > Fraction(1, 3):
        raise ValueError("multiplicity exponent outside [0,1/3]")
    threshold = (1 - xi) / 4
    return {
        "high_multiplicity_threshold": threshold,
        "high_multiplicity": mu > threshold,
        "primitive_denominator_ceiling": Fraction(1, 3) - mu,
        "occupied_mode_floor_from_excess": Fraction(1, 3) - mu,
        "energy_floor_from_excess": Fraction(11, 15) - 4 * mu,
    }


def theorem_record() -> dict[str, object]:
    return {
        "collision_web": (
            "for each occupied a, Cycle 92 supplies one injective reduced label "
            "r_a=p_a/q_a with |r_a-g^a|<<1/(KQ) and q_a<<Q/M"
        ),
        "quadruple_comparison": (
            "if a1+a2=a3+a4 then |r_a1 r_a2-r_a3 r_a4|<<1/(KQ)"
        ),
        "integer_forcing": (
            "a nonzero rational product difference is >>M^4/Q^4; therefore "
            "M^4K>>Q^3 forces r_a1 r_a2=r_a3 r_a4"
        ),
        "threshold": (
            "with M=X^mu and K=X^xi, the high-multiplicity condition is "
            "mu>(1-xi)/4; otherwise mu<=(1-xi)/4 up to the frozen constant buffer"
        ),
        "energy": (
            "for R occupied modes in an interval of D consecutive integers, "
            "E_plus(A)>=R^4/(2D-1); every one of these quadruples is an exact "
            "multiplicative-label quadruple in the high-multiplicity range"
        ),
        "valuation_web": (
            "for every prime p and additive quadruple, "
            "nu_p(r_a1)+nu_p(r_a2)=nu_p(r_a3)+nu_p(r_a4); the full valuation "
            "vector is a Freiman 2-homomorphism on the occupied mode set"
        ),
        "seed_gate": (
            "energy alone does not give an anchored transport seed; E16 still "
            "requires a popular-difference/codegree extraction and a phase-error "
            "budget tied to the original packet anchor"
        ),
        "boundary": (
            "no low-multiplicity collision bound, seed realization, simple-root "
            "closure, complete moment, density, or prime intervals is proved"
        ),
    }
