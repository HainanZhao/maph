"""Cycle 140 multiplier-fiber saturation and jump ledger."""

from __future__ import annotations

from fractions import Fraction


def saturation_ledger(
    xi: Fraction,
    mu: Fraction,
    rho: Fraction,
    tau: Fraction,
    edge: Fraction,
    slack: Fraction,
) -> dict[str, Fraction]:
    if not Fraction(16, 25) <= xi < Fraction(58, 75):
        raise ValueError("xi outside lower band")
    if not 0 <= mu <= (1 - xi) / 4:
        raise ValueError("mu outside low-multiplicity range")
    if tau <= 3 * rho or min(edge, slack) < 0:
        raise ValueError("outside registered saturation range")
    height = 2 * rho - edge - slack
    if height < 0:
        raise ValueError("negative multiplier height")
    target = Fraction(2, 3) - 2 * mu
    discretization = 4 * rho - 2 * slack
    volume = Fraction(3, 5) + 6 * rho - 2 * tau - 2 * slack
    threshold_discretization = 2 * rho - Fraction(1, 3) + mu
    threshold_volume = 3 * rho - tau + mu - Fraction(1, 30)
    return {
        "height": height,
        "weighted_discretization": discretization,
        "weighted_volume": volume,
        "target": target,
        "discretization_margin": target - discretization,
        "volume_margin": target - volume,
        "slack_threshold_discretization": threshold_discretization,
        "slack_threshold_volume": threshold_volume,
        "slack_threshold": max(Fraction(0), threshold_discretization, threshold_volume),
        "legendre_margin": 2 * tau + 2 * edge + 2 * slack - 6 * rho,
        "next_denominator_floor": 2 * tau - 4 * rho + edge + slack,
        "next_partial_quotient_floor": 2 * tau - 6 * rho + 2 * edge + 2 * slack,
    }


def reduced_labels(
    a: int, b: int, p_reduced: int, q_reduced: int, u: int, v: int
) -> tuple[tuple[int, int], tuple[int, int]]:
    if min(a, b, p_reduced, q_reduced, u, v) <= 0 or a % u or b % v:
        raise ValueError("invalid divisor class")
    left = (v * p_reduced, u * q_reduced)
    right = ((a // u) * p_reduced, (b // v) * q_reduced)
    return left, right


def theorem_record() -> dict[str, object]:
    return {
        "slack_parameter": (
            "write the actual multiplier height as H=N^2/(JZ), Z=X^zeta>=1"
        ),
        "weighted_count": (
            "the exceptional weighted discretization and volume exponents are "
            "4rho-2zeta and 3/5+6rho-2tau-2zeta"
        ),
        "closure_threshold": (
            "the block closes if zeta exceeds both "
            "2rho-1/3+mu and 3rho-tau+mu-1/30"
        ),
        "amplified_jump": (
            "a survivor has Legendre margin 2tau+2j+2zeta-6rho, next "
            "denominator exponent 2tau-4rho+j+zeta, and next partial "
            "quotient exponent 2tau-6rho+2j+2zeta"
        ),
        "divisor_seed": (
            "one class u|A, v|B with uv~H carries J X^{-epsilon} edges; "
            "there p=v*p0, q=u*q0 and the paired reduced labels are "
            "v*p0/(u*q0) and (A/u)*p0/((B/v)*q0), with signed tails retained"
        ),
        "near_saturation": (
            "when zeta=o(1), that divisor class occupies an X^{-o(1)} "
            "fraction of its capacity JZ and is a genuine fiber-saturation seed"
        ),
        "boundary": (
            "no theorem forces zeta=o(1) in every survivor, and no recurrence, "
            "full paired norm, endpoint, moment, density, or prime intervals is proved"
        ),
    }
