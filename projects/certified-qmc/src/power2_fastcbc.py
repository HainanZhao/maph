"""Exact modular fast-CBC score mapping for N=2^m.

For m>=3, U(2^m)=<-1> x <5>.  The B2 kernel and every running product
are invariant under k -> -k, so candidate signs can be quotiented.  A
nonzero k is additionally stratified by v2(k).  On the stratum
k=2^v*q, q belongs to U(2^(m-v)), and multiplication by candidate 5^a
becomes a cyclic shift of the 5-exponent modulo 2^(m-v-2).
"""

from __future__ import annotations

from fractions import Fraction
from math import prod
from typing import Sequence

from .exact_error import RuleSpec
from .ntt import ntt_plus_correlation
from .scaled_integer import factor_numerator


def _power_two_exponent(modulus: int) -> int:
    if modulus < 8 or modulus & (modulus - 1):
        raise ValueError("modulus must be 2^m with m>=3")
    return modulus.bit_length() - 1


def power2_candidate_classes(modulus: int) -> list[int]:
    """Represent U(2^m)/{+1,-1} by powers of 5."""

    exponent = _power_two_exponent(modulus)
    return [
        pow(5, index, modulus)
        for index in range(2 ** (exponent - 2))
    ]


def power2_strata(modulus: int) -> list[dict[str, int | str]]:
    """Describe the disjoint valuation strata of nonzero residues."""

    exponent = _power_two_exponent(modulus)
    strata: list[dict[str, int | str]] = []
    for valuation in range(exponent):
        unit_modulus = 2 ** (exponent - valuation)
        if unit_modulus >= 8:
            strata.append(
                {
                    "valuation": valuation,
                    "unit_modulus": unit_modulus,
                    "cyclic_length": unit_modulus // 4,
                    "multiplicity": 2,
                    "method": "C2-sign-quotient-plus-C_2^(ell-2)-NTT",
                }
            )
        else:
            strata.append(
                {
                    "valuation": valuation,
                    "unit_modulus": unit_modulus,
                    "cyclic_length": 1,
                    "multiplicity": unit_modulus // 2,
                    "method": "candidate-independent-small-stratum",
                }
            )
    return strata


def running_product_residues(
    modulus: int,
    prefix: Sequence[int],
    previous_weights: Sequence[Fraction],
    prime: int,
) -> list[int]:
    if len(prefix) != len(previous_weights):
        raise ValueError("prefix and previous weights must have equal length")
    return [
        prod(
            factor_numerator(k * z, modulus, weight) % prime
            for z, weight in zip(prefix, previous_weights)
        ) % prime
        for k in range(modulus)
    ]


def _validated_stage(
    modulus: int,
    prefix: Sequence[int],
    weights: Sequence[Fraction | int | str],
) -> tuple[tuple[int, ...], tuple[Fraction, ...]]:
    if len(weights) != len(prefix) + 1:
        raise ValueError("weights must contain prefix weights plus one")
    spec = RuleSpec.create(modulus, [*prefix, 1], weights)
    _power_two_exponent(modulus)
    return spec.generator[:-1], spec.weights


def direct_power2_candidate_scores(
    modulus: int,
    prefix: Sequence[int],
    weights: Sequence[Fraction | int | str],
    prime: int,
) -> tuple[list[int], list[int]]:
    """Enumerate every sign-quotiented candidate score modulo prime."""

    normalized_prefix, normalized_weights = _validated_stage(
        modulus, prefix, weights
    )
    running = running_product_residues(
        modulus,
        normalized_prefix,
        normalized_weights[:-1],
        prime,
    )
    new_weight = normalized_weights[-1]
    candidates = power2_candidate_classes(modulus)
    scores = [
        sum(
            running[k]
            * (
                factor_numerator(k * candidate, modulus, new_weight)
                % prime
            )
            for k in range(modulus)
        ) % prime
        for candidate in candidates
    ]
    return candidates, scores


def stratified_ntt_candidate_scores(
    modulus: int,
    prefix: Sequence[int],
    weights: Sequence[Fraction | int | str],
    prime: int,
    primitive_root: int,
) -> tuple[list[int], list[int]]:
    """Compute all candidate scores through valuation-stratified NTTs."""

    normalized_prefix, normalized_weights = _validated_stage(
        modulus, prefix, weights
    )
    exponent = _power_two_exponent(modulus)
    running = running_product_residues(
        modulus,
        normalized_prefix,
        normalized_weights[:-1],
        prime,
    )
    if any(
        running[k] != running[-k % modulus]
        for k in range(modulus)
    ):
        raise ArithmeticError("running product lacks required sign symmetry")

    new_weight = normalized_weights[-1]
    candidates = power2_candidate_classes(modulus)
    full_length = len(candidates)
    zero_contribution = (
        running[0] * factor_numerator(0, modulus, new_weight)
    ) % prime
    scores = [zero_contribution] * full_length

    for valuation in range(exponent):
        unit_exponent = exponent - valuation
        unit_modulus = 2**unit_exponent
        scale = 2**valuation
        if unit_exponent <= 2:
            contribution = 0
            for odd_part in range(1, unit_modulus, 2):
                k = scale * odd_part
                contribution += (
                    running[k]
                    * factor_numerator(k, modulus, new_weight)
                )
            contribution %= prime
            scores = [
                (score + contribution) % prime for score in scores
            ]
            continue

        cyclic_length = 2 ** (unit_exponent - 2)
        left: list[int] = []
        right: list[int] = []
        for index in range(cyclic_length):
            odd_part = pow(5, index, unit_modulus)
            k = scale * odd_part
            left.append(2 * running[k] % prime)
            right.append(
                factor_numerator(k, modulus, new_weight) % prime
            )
        correlation = ntt_plus_correlation(
            left, right, prime, primitive_root
        )
        scores = [
            (score + correlation[index % cyclic_length]) % prime
            for index, score in enumerate(scores)
        ]
    return candidates, scores
