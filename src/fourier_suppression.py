"""Exact tools for many-boson interference in a Fourier multiport.

Modes are numbered 0, ..., m-1 and the single-particle unitary is

    F[j, k] = zeta_m ** (j*k) / sqrt(m).

Only exact zero/nonzero questions are considered here, so the common
normalization factors can be discarded.
"""

from __future__ import annotations

from functools import lru_cache
from math import comb
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


def four_mode_self_family_coefficient(a: int) -> int:
    """Return the polynomial coefficient for (0,a,2a,a) -> itself.

    With the irrelevant Fourier normalization and input factorials
    removed, the amplitude is

        [x^a y^(2a) z^a]
        (y^2 + (x-z)^2)^a (y-x-z)^(2a).

    This evaluates the coefficient by an exact finite binomial sum.  The
    pairing k <-> a-k proves directly that the result is zero for odd a.
    """
    if a < 0:
        raise ValueError("a must be nonnegative")

    result = 0
    for k in range(a + 1):
        # Coefficient of x^a z^a in
        # (x-z)^(2k) (x+z)^(2a-2k).
        central = 0
        lower = max(0, 2 * k - a)
        upper = min(2 * k, a)
        for z_from_first in range(lower, upper + 1):
            central += (
                (-1) ** z_from_first
                * comb(2 * k, z_from_first)
                * comb(2 * a - 2 * k, a - z_from_first)
            )
        result += comb(a, k) * comb(2 * a, 2 * k) * central
    return result


def four_mode_self_family_closed_form(a: int) -> int:
    """Return the proved closed form for the self-family coefficient."""
    if a < 0:
        raise ValueError("a must be nonnegative")
    if a % 2:
        return 0
    return (-1) ** (a // 2) * comb(2 * a, a) * comb(a, a // 2)


def four_mode_reflection_self_coefficient(a: int, b: int) -> int:
    """Return the coefficient for (0,a,b,a) -> itself in F_4."""
    if a < 0 or b < 0:
        raise ValueError("a and b must be nonnegative")

    result = 0
    for k in range(a + 1):
        degree_from_second = 2 * a - 2 * k
        if degree_from_second > b:
            continue
        central = 0
        lower = max(0, 2 * k - a)
        upper = min(2 * k, a)
        for z_from_first in range(lower, upper + 1):
            central += (
                (-1) ** z_from_first
                * comb(2 * k, z_from_first)
                * comb(2 * a - 2 * k, a - z_from_first)
            )
        result += (
            comb(a, k)
            * comb(b, degree_from_second)
            * central
        )
    return result


def four_mode_reflection_closed_sum(a: int, b: int) -> int:
    """Return the reflection-family coefficient by its binomial convolution.

    Krawtchouk duality reduces the nested coefficient in
    :func:`four_mode_reflection_self_coefficient` to

        (-1)^a sum_j (-1)^j
            binom(2(a-j), a-j) binom(b, 2j) binom(2j, j).

    The sum stops at ``min(a, b // 2)``.  This form exposes the
    exponential generating function and is much faster for large
    parameter scans.
    """
    if a < 0 or b < 0:
        raise ValueError("a and b must be nonnegative")

    return (-1) ** a * sum(
        (-1) ** j
        * comb(2 * (a - j), a - j)
        * comb(b, 2 * j)
        * comb(2 * j, j)
        for j in range(min(a, b // 2) + 1)
    )


def reflection_positive_tail_start(a: int) -> int:
    """Return a rigorous threshold beyond which ``C[a,b]`` is positive.

    Strict growth of the alternating binomial-convolution terms proves
    positivity for ``b >= 4*a - 3`` when ``a >= 3``.  The two exceptional
    thresholds are 3 for ``a == 1`` and 6 for ``a == 2``.  These are
    sufficient proof bounds, not claims that the bounds are sharp.
    """
    if a < 1:
        raise ValueError("a must be positive")
    if a == 1:
        return 3
    if a == 2:
        return 6
    return 4 * a - 3


def fourier_support_type_counts(
    input_occupation: Sequence[int],
    output_occupation: Sequence[int],
) -> tuple[int, int]:
    """Count occupied row and column types up to proportional phases.

    In a Fourier matrix, two rows restricted to the occupied input modes
    are proportional exactly when their phase-exponent vectors agree
    after subtracting a common exponent.  The column count is defined
    dually.  The result depends only on the supports, not multiplicities.
    """
    input_tuple, output_tuple = _validate_pair(
        input_occupation, output_occupation
    )
    modes = len(input_tuple)
    input_support = tuple(
        index for index, value in enumerate(input_tuple) if value
    )
    output_support = tuple(
        index for index, value in enumerate(output_tuple) if value
    )
    if not input_support:
        return (0, 0)

    def signatures(indices: tuple[int, ...],
                   restricted_to: tuple[int, ...]) -> set[tuple[int, ...]]:
        signatures_seen = set()
        reference = restricted_to[0]
        for index in indices:
            base = index * reference
            signatures_seen.add(
                tuple(
                    (index * other - base) % modes
                    for other in restricted_to
                )
            )
        return signatures_seen

    row_types = signatures(output_support, input_support)
    column_types = signatures(input_support, output_support)
    return len(row_types), len(column_types)


def has_at_most_two_fourier_support_types(
    input_occupation: Sequence[int],
    output_occupation: Sequence[int],
) -> bool:
    """Return whether the occupied scattering matrix has <=2 types per side.

    This is a structural filter for a possible single two-mode reduction,
    not by itself a proof that a zero is a standard SU(2) suppression.
    """
    row_types, column_types = fourier_support_type_counts(
        input_occupation, output_occupation
    )
    return row_types <= 2 and column_types <= 2


def lift_fourier_occupations(
    input_occupation: Sequence[int],
    output_occupation: Sequence[int],
    target_modes: int,
) -> tuple[Occupation, Occupation]:
    """Embed an F_d transition into F_m when d divides m.

    Input mode k is kept at k, while output mode j is sent to
    j*(m/d).  The selected F_m submatrix is a nonzero scalar multiple of
    F_d, so zero transition amplitudes are preserved.
    """
    input_tuple, output_tuple = _validate_pair(
        input_occupation, output_occupation
    )
    source_modes = len(input_tuple)
    if target_modes < source_modes or target_modes % source_modes:
        raise ValueError("target_modes must be a multiple of source modes")
    stride = target_modes // source_modes

    lifted_input = [0] * target_modes
    lifted_output = [0] * target_modes
    for mode, multiplicity in enumerate(input_tuple):
        lifted_input[mode] = multiplicity
    for mode, multiplicity in enumerate(output_tuple):
        lifted_output[mode * stride] = multiplicity
    return tuple(lifted_input), tuple(lifted_output)
