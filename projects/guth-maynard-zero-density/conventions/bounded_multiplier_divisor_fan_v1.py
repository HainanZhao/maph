"""Cycle 152 exact bounded-multiplier divisor-fan compiler."""

from __future__ import annotations

from fractions import Fraction
from math import gcd
from typing import Iterable


def ceil_fraction(value: Fraction) -> int:
    if value <= 0:
        raise ValueError("positive value required")
    return (value.numerator + value.denominator - 1) // value.denominator


def multiplier_cap(*, contribution_bound: Fraction, target_mass: Fraction) -> int:
    if contribution_bound <= 0 or target_mass <= 0:
        raise ValueError("positive bound and target required")
    return ceil_fraction(2 * contribution_bound / target_mass)


def divisor_fan_row(*, witness_denominator: int, multiplier: int, divisor: int) -> dict[str, int]:
    if min(witness_denominator, multiplier, divisor) <= 0:
        raise ValueError("positive integers required")
    if witness_denominator % divisor:
        raise ValueError("divisor must divide witness denominator")
    if gcd(multiplier, witness_denominator // divisor) != 1:
        raise ValueError("fan row does not have the requested gcd")
    mode_denominator = multiplier * divisor
    if gcd(witness_denominator, mode_denominator) != divisor:
        raise AssertionError("gcd identity failed")
    return {
        "witness_denominator": witness_denominator,
        "multiplier": multiplier,
        "gcd": divisor,
        "mode_denominator": mode_denominator,
    }


def bounded_multiplier_inverse(
    *, contribution_bound: Fraction, target_mass: Fraction, rows: Iterable[tuple[Fraction, int, Fraction]]
) -> dict[str, object]:
    """Compile normalized negative mass into one bounded multiplier.

    Each row is (positive_weight, multiplier, actual_negative_mass), with
    actual_negative_mass <= contribution_bound * positive_weight / multiplier.
    """
    cap = multiplier_cap(contribution_bound=contribution_bound, target_mass=target_mass)
    parsed = list(rows)
    if not parsed:
        raise ValueError("nonempty mode family required")
    total_weight = sum((weight for weight, _, _ in parsed), Fraction())
    total_mass = sum((mass for _, _, mass in parsed), Fraction())
    if total_weight > 1:
        raise ValueError("weights must be normalized by at most one")
    for weight, multiplier, mass in parsed:
        if weight < 0 or multiplier < 1 or mass < 0:
            raise ValueError("invalid mode row")
        if mass > contribution_bound * weight / multiplier:
            raise ValueError("row exceeds the frozen per-mode contribution bound")
    if total_mass < target_mass:
        raise ValueError("target negative mass not present")
    tail_mass = sum((mass for _, multiplier, mass in parsed if multiplier > cap), Fraction())
    if tail_mass > contribution_bound / cap:
        raise AssertionError("large-m tail bound failed")
    bounded_mass = total_mass - tail_mass
    if bounded_mass < target_mass / 2:
        raise AssertionError("bounded multipliers do not retain half the target mass")
    by_multiplier: dict[int, Fraction] = {}
    for _, multiplier, mass in parsed:
        if multiplier <= cap:
            by_multiplier[multiplier] = by_multiplier.get(multiplier, Fraction()) + mass
    chosen = min(
        (multiplier for multiplier, mass in by_multiplier.items() if mass >= target_mass / (2 * cap)),
        default=None,
    )
    if chosen is None:
        raise AssertionError("pigeonhole multiplier not found")
    return {
        "multiplier_cap": cap,
        "total_weight": total_weight,
        "total_negative_mass": total_mass,
        "large_multiplier_mass_upper_bound": contribution_bound / cap,
        "bounded_multiplier_mass": bounded_mass,
        "chosen_multiplier": chosen,
        "chosen_multiplier_mass": by_multiplier[chosen],
        "chosen_multiplier_lower_bound": target_mass / (2 * cap),
    }


def theorem_record() -> dict[str, object]:
    return {
        "tail_concentration": (
            "if sum_b w_b<=1, 0<=n_b<=C w_b/m_b, and sum_b n_b>=kappa, then "
            "m_b<=ceil(2C/kappa) retains at least kappa/2 negative mass"
        ),
        "bounded_multiplier": (
            "one m_0<=ceil(2C/kappa) carries at least "
            "kappa/(2 ceil(2C/kappa)) negative mass"
        ),
        "divisor_fan": (
            "for d_b=gcd(h,h_b) and m_b=h_b/d_b, every extracted mode has "
            "h_b=m_0 d_b, d_b|h, and gcd(m_0,h/d_b)=1"
        ),
        "label_retention": (
            "the inverse retains b,d_b,m_0,r_b,tau_b,w_b,n_b and does not "
            "replace the actual negative-lobe condition by an unlabelled count"
        ),
        "boundary": (
            "this is a conditional concentration inverse only; it does not bound "
            "the divisor fan, boundary denominators, phase-changing charts, nonsmooth payload, "
            "a full moment, density, or prime intervals"
        ),
    }
