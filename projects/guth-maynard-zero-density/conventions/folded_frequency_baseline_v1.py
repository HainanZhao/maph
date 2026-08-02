"""Exact Cycle 68 folded-frequency exponent baseline."""
from __future__ import annotations

from fractions import Fraction as Q


DELTA = Q(3, 5)
MAX_THETA_PLUS_KAPPA = Q(11, 25)
RAW_TARGET = Q(31, 25)


def baseline(total_scale: Q) -> dict[str, object]:
    if total_scale < 0 or total_scale > MAX_THETA_PLUS_KAPPA:
        raise ValueError("total scale outside admissible range")
    frequency_length = 1 + total_scale
    generic_large_sieve = DELTA / 2 + frequency_length
    return {
        "theta_plus_kappa": total_scale,
        "frequency_length_exponent": frequency_length,
        "folded_coefficient_bound": "|A_m|<=C_f*tau(|m|)",
        "coefficient_square_norm_exponent": frequency_length,
        "generic_large_sieve_exponent": generic_large_sieve,
        "raw_target_exponent_open": RAW_TARGET,
        "saving_required": generic_large_sieve - RAW_TARGET,
    }


def verify_all() -> dict[str, object]:
    smallest = baseline(Q(0))
    largest = baseline(MAX_THETA_PLUS_KAPPA)
    if smallest["generic_large_sieve_exponent"] != Q(13, 10):
        raise RuntimeError("small-scale baseline")
    if smallest["saving_required"] != Q(3, 50):
        raise RuntimeError("small-scale gap")
    if largest["generic_large_sieve_exponent"] != Q(87, 50):
        raise RuntimeError("large-scale baseline")
    if largest["saving_required"] != Q(1, 2):
        raise RuntimeError("large-scale gap")
    return {
        "folding": "A_m=sum_(q'|m) sum_(b: bq'~Q) mu(b)/b fhat_C(m/(q'bKX))",
        "support": "|m|<<KXQ",
        "coefficient_bound": "each q'|m contributes a dyadic harmonic b-sum O(1), hence |A_m|<<tau(|m|)",
        "square_norm": "sum_|m|<=M |A_m|^2<=M*X^o(1)",
        "generic_baseline": "Cauchy plus the Delta^-1 separated large sieve gives X^(13/10+theta+kappa+o(1))",
        "required_saving": "3/50+theta+kappa",
        "gate": "retain Mobius cancellation or exploit the exponential transport phase; coefficient folding plus a generic large sieve is insufficient",
    }


if __name__ == "__main__":
    print(verify_all())
