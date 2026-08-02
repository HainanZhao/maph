"""Exact Cycle 45 joint p-k large-sieve exponent ledger."""
from __future__ import annotations

from fractions import Fraction as Q


DELTA = Q(3, 5)
PRIME_LENGTH = Q(1)
PRIME_L2 = Q(1)
RESOLUTION = Q(11, 25)
MISSING_SAVING = Q(4, 25)


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def joint_sum(nu: Q, alias_exponent: Q = Q(1)) -> dict[str, Q]:
    require(0 <= nu <= DELTA, "Fourier exponent range")
    require(0 <= alias_exponent <= 1, "alias exponent range")
    trivial = PRIME_L2 + DELTA
    energy = alias_exponent * nu + PRIME_LENGTH + PRIME_L2
    joint_bound = DELTA / 2 + energy / 2
    saving = trivial - joint_bound
    return {
        "fourier_exponent": nu,
        "alias_exponent": alias_exponent,
        "trivial_joint_sum": trivial,
        "large_sieve_energy": energy,
        "joint_bound": joint_bound,
        "saving": saving,
    }


def required_alias_exponent(nu: Q, required_saving: Q) -> Q:
    require(nu > 0, "positive Fourier exponent")
    return (2 * (Q(3, 10) - required_saving)) / nu


def registered_scales() -> dict[str, object]:
    naive = joint_sum(RESOLUTION, Q(1))
    dealiased = joint_sum(RESOLUTION, Q(0))
    threshold = required_alias_exponent(RESOLUTION, MISSING_SAVING)
    narrow_margin_threshold = required_alias_exponent(RESOLUTION, Q(7, 50))
    require(naive["joint_bound"] == Q(38, 25), "naive joint bound")
    require(naive["saving"] == Q(2, 25), "naive saving")
    require(dealiased["joint_bound"] == Q(13, 10), "dealiased bound")
    require(dealiased["saving"] == Q(3, 10), "dealiased saving")
    require(threshold == Q(7, 11), "missing-saving alias threshold")
    require(narrow_margin_threshold == Q(8, 11), "narrow-margin alias threshold")
    return {
        "resolution": RESOLUTION,
        "naive_wrap_coloring": naive,
        "full_dealiasing": dealiased,
        "alias_threshold_for_4_25": threshold,
        "alias_threshold_for_7_50": narrow_margin_threshold,
    }


def verify_all() -> dict[str, object]:
    return registered_scales()


if __name__ == "__main__":
    print(verify_all())
