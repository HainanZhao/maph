"""Exact tools for many-boson interference in a Fourier multiport.

Modes are numbered 0, ..., m-1 and the single-particle unitary is

    F[j, k] = zeta_m ** (j*k) / sqrt(m).

Only exact zero/nonzero questions are considered here, so the common
normalization factors can be discarded.
"""

from __future__ import annotations

from functools import lru_cache
from typing import Iterator, Sequence


Occupation = tuple[int, ...]


def occupation_vectors(particles: int, modes: int) -> Iterator[Occupation]:
    """Yield all weak compositions of ``particles`` into ``modes`` parts."""
    if particles < 0 or modes < 1:
        raise ValueError("particles must be nonnegative and modes positive")
    if modes == 1:
        yield (particles,)
        return
    for first in range(particles + 1):
        for rest in occupation_vectors(particles - first, modes - 1):
            yield (first,) + rest


def _validate_pair(input_occupation: Sequence[int],
                   output_occupation: Sequence[int]) -> tuple[Occupation, Occupation]:
    input_tuple = tuple(input_occupation)
    output_tuple = tuple(output_occupation)
    if not input_tuple or len(input_tuple) != len(output_tuple):
        raise ValueError("occupations must have the same positive number of modes")
    if any(value < 0 for value in input_tuple + output_tuple):
        raise ValueError("occupation numbers must be nonnegative")
    if sum(input_tuple) != sum(output_tuple):
        raise ValueError("input and output must contain the same number of particles")
    return input_tuple, output_tuple


def phase_histogram(input_occupation: Sequence[int],
                    output_occupation: Sequence[int]) -> tuple[int, ...]:
    """Return the exact path-count histogram for a Fourier transition.

    Entry ``c[e]`` counts labelled terms in the permanent whose phase is
    ``zeta_m**e``.  Thus the unnormalised transition amplitude is

        sum(c[e] * zeta_m**e for e in range(m)).

    The dynamic program distinguishes identical columns by multiplying a
    mode choice by the number of labelled particles still in that mode.
    """
    input_tuple, output_tuple = _validate_pair(
        input_occupation, output_occupation
    )
    modes = len(input_tuple)
    output_modes = tuple(
        mode
        for mode, multiplicity in enumerate(output_tuple)
        for _ in range(multiplicity)
    )

    @lru_cache(maxsize=None)
    def recurse(position: int, remaining: Occupation) -> tuple[int, ...]:
        if position == len(output_modes):
            return (1,) + (0,) * (modes - 1)

        result = [0] * modes
        output_mode = output_modes[position]
        for input_mode, multiplicity in enumerate(remaining):
            if multiplicity == 0:
                continue
            next_remaining = list(remaining)
            next_remaining[input_mode] -= 1
            tail = recurse(position + 1, tuple(next_remaining))
            phase_increment = output_mode * input_mode
            for exponent, count in enumerate(tail):
                result[(exponent + phase_increment) % modes] += (
                    multiplicity * count
                )
        return tuple(result)

    return recurse(0, input_tuple)


def prime_power_base(number: int) -> int | None:
    """Return p if ``number`` is a positive power of the prime p."""
    if number < 2:
        return None
    candidate = 2
    while candidate * candidate <= number and number % candidate:
        candidate += 1
    prime = candidate if number % candidate == 0 else number
    remainder = number
    while remainder % prime == 0:
        remainder //= prime
    return prime if remainder == 1 else None


def is_dark_prime_power_histogram(histogram: Sequence[int]) -> bool:
    """Test exact vanishing when the number of modes is a prime power.

    For m=p^a, Phi_m(x)=1+x^(m/p)+...+x^((p-1)m/p).  A polynomial
    C(x)=sum(c[e]x^e) of degree below m vanishes at a primitive m-th root
    exactly when, for each residue r modulo m/p,

        c[r] = c[r+m/p] = ... = c[r+(p-1)m/p].
    """
    counts = tuple(histogram)
    modes = len(counts)
    prime = prime_power_base(modes)
    if prime is None:
        raise ValueError("the number of modes must be a prime power")
    step = modes // prime
    return all(
        len({counts[residue + multiple * step]
             for multiple in range(prime)}) == 1
        for residue in range(step)
    )


def is_dark_prime_power(input_occupation: Sequence[int],
                        output_occupation: Sequence[int]) -> bool:
    """Return whether a prime-power Fourier transition is exactly dark."""
    return is_dark_prime_power_histogram(
        phase_histogram(input_occupation, output_occupation)
    )


def cyclic_stabilizer_shifts(occupation: Sequence[int]) -> tuple[int, ...]:
    """Return nonzero cyclic shifts that leave an occupation fixed."""
    values = tuple(occupation)
    modes = len(values)
    return tuple(
        shift
        for shift in range(1, modes)
        if tuple(values[(index - shift) % modes] for index in range(modes))
        == values
    )


def _one_sided_cyclic_rule(input_occupation: Occupation,
                           output_occupation: Occupation) -> bool:
    modes = len(input_occupation)
    output_mode_sum = sum(
        mode * multiplicity
        for mode, multiplicity in enumerate(output_occupation)
    )
    return any(
        shift * output_mode_sum % modes != 0
        for shift in cyclic_stabilizer_shifts(input_occupation)
    )


def simple_cyclic_rule_predicts_dark(
    input_occupation: Sequence[int],
    output_occupation: Sequence[int],
) -> bool:
    """Apply the elementary cyclic selection rule in both directions.

    Fourier matrices are symmetric, so a cyclic stabilizer of either the
    input or the output can force the transition to vanish.  This is a
    deliberately narrow baseline, not a claim to implement every known
    group-theoretic suppression law.
    """
    input_tuple, output_tuple = _validate_pair(
        input_occupation, output_occupation
    )
    return (
        _one_sided_cyclic_rule(input_tuple, output_tuple)
        or _one_sided_cyclic_rule(output_tuple, input_tuple)
    )


def _rotate(values: Occupation, amount: int) -> Occupation:
    return values[amount:] + values[:amount]


def canonical_dark_pair(input_occupation: Sequence[int],
                        output_occupation: Sequence[int]) -> tuple[Occupation, Occupation]:
    """Canonicalize under independent rotations and input/output exchange."""
    input_tuple, output_tuple = _validate_pair(
        input_occupation, output_occupation
    )
    modes = len(input_tuple)
    representatives: list[tuple[Occupation, Occupation]] = []
    for input_shift in range(modes):
        for output_shift in range(modes):
            rotated_input = _rotate(input_tuple, input_shift)
            rotated_output = _rotate(output_tuple, output_shift)
            representatives.append((rotated_input, rotated_output))
            representatives.append((rotated_output, rotated_input))
    return min(representatives)
