"""Cycle 148 endpoint rational-comb conventions and exponent ledger."""

from __future__ import annotations

from fractions import Fraction
from math import gcd


def anchored_reduced_denominator(
    *, numerator: int, denominator: int, anchor_numerator: int, anchor_denominator: int
) -> int:
    if min(numerator, denominator, anchor_numerator, anchor_denominator) <= 0:
        raise ValueError("positive rational data required")
    if gcd(numerator, denominator) != 1 or gcd(anchor_numerator, anchor_denominator) != 1:
        raise ValueError("input rationals must be reduced")
    raw_numerator = anchor_numerator * numerator
    raw_denominator = anchor_denominator * denominator
    return raw_denominator // gcd(raw_numerator, raw_denominator)


def major_arc_multiples(*, frequency_floor: int, frequency_ceiling: int, modulus: int) -> int:
    if frequency_floor < 1 or frequency_ceiling < frequency_floor or modulus < 1:
        raise ValueError("invalid comb range")
    return frequency_ceiling // modulus - (frequency_floor - 1) // modulus


def exponent_ledger(
    *, xi: Fraction, rho: Fraction, mode_mass: Fraction
) -> dict[str, Fraction]:
    if xi <= rho or rho < 0 or mode_mass < 0:
        raise ValueError("invalid endpoint exponents")
    diagonal = xi + Fraction(1, 3) + mode_mass
    comb_lower = xi + Fraction(2, 3) - rho + mode_mass
    return {
        "diagonal": diagonal,
        "comb_lower": comb_lower,
        "excess": comb_lower - diagonal,
        "comb_count": xi - rho,
    }


def theorem_record() -> dict[str, object]:
    return {
        "anchor_denominator": (
            "for c0=A/B and reduced p/q, the reduced denominator h of c0p/q "
            "satisfies q/A<=h<=Bq; bounded rational anchors preserve the "
            "denominator exponent"
        ),
        "poisson_nonmultiples": (
            "if h does not divide k, then ||k r/h||>=1/h; under "
            "h<<N<=QX^(-delta) and |c0g^a-r/h|<<1/(KQ), exact Poisson "
            "summation makes the length-Q smooth coefficient sum "
            "O_A(Q(Q/N)^(-A)) for every fixed A"
        ),
        "resonant_multiples": (
            "if h divides k and K<=k<=2K, the rational phase is integral; "
            "with a sufficiently small fixed endpoint buffer, the residual "
            "phase lies in a common pi/6 wedge and the real coefficient sum is >>Q"
        ),
        "comb_lower_bound": (
            "for positive fixed-chart mode weights u_a, summing the squared "
            "resonant incidence function gives M2(C)>>KQ^2/N sum_a u_a^2"
        ),
        "diagonal_comparison": (
            "the cell diagonal is comparable to KQ sum_a u_a^2, so the isolated "
            "endpoint operator has a Q/N=X^(1/3-rho) major-arc excess"
        ),
        "cycle132_input": (
            "Cycle 132 gives |g^a-p/q|<1/(qS); a strict shell with "
            "S>>KQ/q supplies the required O(1/(KQ)) endpoint buffer"
        ),
        "structural_implication": (
            "a proof that decomposes into endpoint operators and sums their "
            "second-moment norms cannot reach diagonal strength in any fixed "
            "rho<1/3 band; cancellation must occur between endpoint cells or "
            "through the full common coefficient vector"
        ),
        "mass_boundary": (
            "the theorem does not show that one endpoint class carries a "
            "target-sized share of the full fixed polynomial, and it does not "
            "exclude cross-cell cancellation"
        ),
        "boundary": (
            "no full second moment, endpoint, complete moment, density, or intervals is proved"
        ),
    }
