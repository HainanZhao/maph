"""Cycle 150 strict-comb sign and escape-norm ledger."""

from __future__ import annotations

from fractions import Fraction
from math import sqrt


def divisor_comb_norm(*, q_length: float, frequency_length: float, modulus: float) -> float:
    if q_length <= 0 or frequency_length <= 0 or modulus <= 0:
        raise ValueError("positive comb scales required")
    return q_length * sqrt(frequency_length / modulus)


def escape_norm_floor(
    *, negative_witness: float, strict_error: float, test_vector_norm: float
) -> float:
    if negative_witness < 0 or strict_error < 0 or test_vector_norm <= 0:
        raise ValueError("invalid escape data")
    return max(0.0, negative_witness - strict_error) / test_vector_norm


def one_ray_escape_ledger(*, xi: Fraction, rho: Fraction) -> dict[str, Fraction]:
    if xi <= rho or rho < 0:
        raise ValueError("invalid comb exponents")
    squared_norm = xi + Fraction(2, 3) - rho
    return {
        "escape_norm_squared": squared_norm,
        "one_mode_diagonal": xi + Fraction(1, 3),
        "excess": Fraction(1, 3) - rho,
    }


def theorem_record() -> dict[str, object]:
    return {
        "strict_sign_test": (
            "on sampled frequencies k=h ell, every other strict positive endpoint "
            "mode is either resonant, in which case its real coefficient sum is "
            ">>Q, or nonresonant, in which case exact Poisson summation makes it "
            "power-negligible; hence its divisor-comb correlation is nonnegative "
            "up to a power-negligible error"
        ),
        "no_strict_antialignment": (
            "strict positive endpoint combs with denominators <=QX^(-delta) "
            "reinforce rather than cancel one another on every retained modulus"
        ),
        "escape_split": (
            "any negative anti-aligner must leave the strict class through at "
            "least one of: endpoint error beyond c/(KQ), denominator within a "
            "fixed power of Q, coefficient phase outside the positive wedge, or "
            "nonsmooth/untransported payload"
        ),
        "escape_correlation": (
            "if Cycle 149 forces Re<R,w_h><=-M and the strict part P has "
            "Re<P,w_h>>=-eta, then H=R-P satisfies Re<H,w_h><=-(M-eta)"
        ),
        "escape_norm": (
            "Cauchy gives ||H||_2>=(M-eta)/||w_h||_2, where "
            "||w_h||_2 is comparable to Qsqrt(K/h)"
        ),
        "one_ray_scale": (
            "when endpoint weights are bounded and the Cycle-149 witness is "
            "inserted, the forced escape norm squared has the one-ray comb scale "
            "KQ^2/N, exceeding one-mode diagonal KQ by Q/N"
        ),
        "structural_implication": (
            "a diagonal full moment with supercritical strict endpoint mass forces "
            "a quantitatively large halo, boundary-denominator, sign-changing, or "
            "nonsmooth component; another strict endpoint population cannot be the canceler"
        ),
        "boundary": (
            "the escape class is not bounded or excluded here; no full second "
            "moment, endpoint, complete moment, density, or intervals is proved"
        ),
    }
