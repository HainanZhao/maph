#!/usr/bin/env python3
"""Search four-photon dark events for local off-diagonal SU(4) tomography.

For a dark transition e=(r,s), let v_e be its twelve complex amplitude
derivatives under the six X_pq and six Y_pq output generators.  With an
unknown small real error theta and a known signed probe epsilon h,

    P_e(+epsilon h)-P_e(-epsilon h)
      = 4 epsilon Re[(v_e.h)^* (v_e.theta)] + higher orders.

Thus one dark event supplies at most two real linear measurements, even
if arbitrarily many probes are used.  This script certifies the exact
rank-nine Fock-input ceiling and an exact rank-twelve coherent-cat design
for the off-diagonal coordinates.
"""

from __future__ import annotations

import sys
from fractions import Fraction
from itertools import combinations
from math import factorial, gcd
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.analyze_unitary_leakage import (  # noqa: E402
    PAIRS,
    GaussianInteger,
    generator_moments,
    physical_denominator_squared,
    root_permanent,
)
from src.fourier_suppression import occupation_vectors  # noqa: E402


Occupation = tuple[int, int, int, int]
Event = tuple[Occupation, Occupation]
GaussianVector = tuple[GaussianInteger, ...]
COORDINATES = tuple(
    (generator, pair)
    for pair in PAIRS
    for generator in ("X", "Y")
)


def derivative_numerators(event: Event) -> GaussianVector:
    """Return Gaussian-integer numerators for <s|G F_4|r>."""
    r, s = event
    return tuple(
        generator_moments(r, s, pair, generator, 1)[1]
        for generator, pair in COORDINATES
    )


def rational_rank(rows: list[list[int | Fraction]]) -> int:
    """Exact row rank over the rationals."""
    matrix = [[Fraction(value) for value in row] for row in rows]
    rank = 0
    columns = len(matrix[0]) if matrix else 0
    for column in range(columns):
        pivot = next(
            (index for index in range(rank, len(matrix))
             if matrix[index][column]),
            None,
        )
        if pivot is None:
            continue
        matrix[rank], matrix[pivot] = matrix[pivot], matrix[rank]
        scale = matrix[rank][column]
        matrix[rank] = [value / scale for value in matrix[rank]]
        for index in range(len(matrix)):
            if index == rank or not matrix[index][column]:
                continue
            scale = matrix[index][column]
            matrix[index] = [
                value - scale * pivot_value
                for value, pivot_value in zip(matrix[index], matrix[rank])
            ]
        rank += 1
        if rank == len(matrix):
            break
    return rank


def rational_determinant(
    rows: list[list[int | Fraction]],
) -> Fraction:
    """Exact determinant over the rationals."""
    matrix = [[Fraction(value) for value in row] for row in rows]
    size = len(matrix)
    if any(len(row) != size for row in matrix):
        raise ValueError("determinant requires a square matrix")
    determinant = Fraction(1)
    for column in range(size):
        pivot = next(
            (index for index in range(column, size)
             if matrix[index][column]),
            None,
        )
        if pivot is None:
            return Fraction(0)
        if pivot != column:
            matrix[column], matrix[pivot] = matrix[pivot], matrix[column]
            determinant *= -1
        pivot_value = matrix[column][column]
        determinant *= pivot_value
        for entry in range(column, size):
            matrix[column][entry] /= pivot_value
        for index in range(column + 1, size):
            scale = matrix[index][column]
            if not scale:
                continue
            for entry in range(column, size):
                matrix[index][entry] -= scale * matrix[column][entry]
    return determinant


def event_rows(event: Event) -> tuple[list[int], list[int]]:
    vector = derivative_numerators(event)
    return (
        [value[0] for value in vector],
        [value[1] for value in vector],
    )


def primitive(row: list[int]) -> list[int]:
    divisor = 0
    for value in row:
        divisor = gcd(divisor, abs(value))
    if divisor:
        row = [value // divisor for value in row]
    first = next((value for value in row if value), 1)
    return [-value for value in row] if first < 0 else row


def greedy_events(events: list[Event]) -> list[Event]:
    """Greedily add the event giving the largest rank increment."""
    selected: list[Event] = []
    rows: list[list[int]] = []
    rank = 0
    remaining = events.copy()
    while rank < 12:
        best: Event | None = None
        best_rank = rank
        for event in remaining:
            candidate_rank = rational_rank(rows + list(event_rows(event)))
            if candidate_rank > best_rank:
                best = event
                best_rank = candidate_rank
                if best_rank == min(12, rank + 2):
                    break
        if best is None:
            break
        selected.append(best)
        rows.extend(event_rows(best))
        remaining.remove(best)
        rank = best_rank
    return selected


def best_probe_pair(event: Event) -> tuple[int, int, int]:
    """Return coordinate indices with largest exact quadrature determinant."""
    vector = derivative_numerators(event)
    best = (0, 0, 0)
    for left in range(12):
        for right in range(left + 1, 12):
            determinant = (
                vector[left][0] * vector[right][1]
                - vector[left][1] * vector[right][0]
            )
            if abs(determinant) > abs(best[2]):
                best = left, right, determinant
    return best


def differential_row(event: Event, probe_index: int) -> list[int]:
    """Unscaled row in the signed probe probability differential."""
    vector = derivative_numerators(event)
    reference = vector[probe_index]
    return [
        reference[0] * value[0] + reference[1] * value[1]
        for value in vector
    ]


def vector_rows(vector: GaussianVector) -> tuple[list[int], list[int]]:
    return (
        [value[0] for value in vector],
        [value[1] for value in vector],
    )


def noon_dark_vector(other_mode: int) -> GaussianVector:
    """Derivative vector for (|4_0>-|4_j>)/sqrt(2) -> |4_0>.

    The omitted common factor 1/sqrt(2) does not affect rank.
    """
    first = derivative_numerators(((4, 0, 0, 0), (4, 0, 0, 0)))
    other_input = tuple(4 if mode == other_mode else 0 for mode in range(4))
    second = derivative_numerators((other_input, (4, 0, 0, 0)))
    return tuple(
        (left[0] - right[0], left[1] - right[1])
        for left, right in zip(first, second)
    )


def four_mode_cat_dark_vector(output: Occupation) -> GaussianVector:
    """Derivative vector for sum_j |4_j>/2 at a dark output class."""
    vectors = []
    for occupied_mode in range(4):
        input_occupation = tuple(
            4 if mode == occupied_mode else 0 for mode in range(4)
        )
        vectors.append(
            derivative_numerators((input_occupation, output))
        )
    return tuple(
        (
            sum(vector[index][0] for vector in vectors),
            sum(vector[index][1] for vector in vectors),
        )
        for index in range(12)
    )


def vector_differential_row(
    vector: GaussianVector,
    probe_index: int,
) -> list[int]:
    reference = vector[probe_index]
    return [
        reference[0] * value[0] + reference[1] * value[1]
        for value in vector
    ]


def general_vector_differential_row(
    vector: GaussianVector,
    probe: tuple[int, ...],
) -> list[int]:
    """Unscaled differential row for an arbitrary real probe vector."""
    if len(probe) != len(vector):
        raise ValueError("probe and derivative vector sizes differ")
    reference = (
        sum(weight * value[0] for weight, value in zip(probe, vector)),
        sum(weight * value[1] for weight, value in zip(probe, vector)),
    )
    return [
        reference[0] * value[0] + reference[1] * value[1]
        for value in vector
    ]


def cat_physical_differential_row(
    output: Occupation,
    probe: tuple[int, ...],
) -> list[Fraction]:
    """Return the exact row in Delta P / epsilon for the normalized cat.

    The cat vector stored by ``four_mode_cat_dark_vector`` is the sum of
    four component numerators.  Division by two normalizes the cat.
    The factor four in the signed probability differential cancels the
    resulting factor 1/4.
    """
    vector = four_mode_cat_dark_vector(output)
    raw = general_vector_differential_row(vector, probe)
    denominator_squared = physical_denominator_squared(
        (4, 0, 0, 0), output
    )
    return [
        Fraction(value, denominator_squared)
        for value in raw
    ]


def fock_physical_differential_row(
    event: Event,
    probe_index: int,
) -> list[Fraction]:
    """Leading Jacobian row in lim_(eps->0) Delta P / eps.

    For a normalized Fock input, v=M/D.  Hence the factor four in the
    signed contrast remains:

        lim Delta P / eps = 4 Re[(v.h)^*(v.theta)].
    """
    raw = differential_row(event, probe_index)
    denominator_squared = physical_denominator_squared(*event)
    return [
        Fraction(4 * value, denominator_squared)
        for value in raw
    ]


def general_fourier_cat_probability(
    modes: int,
    particles: int,
    charge: int,
    output: tuple[int, ...],
) -> Fraction:
    """Exact F_m probability for the phase-twisted all-bunched cat.

    The amplitude is

        sqrt(n! / prod s_k!) m^((1-n)/2)

    in the modular sector sum(k*s_k) == charge, and zero otherwise.
    Returning its square avoids introducing algebraic square roots.
    """
    if modes < 2 or particles < 1:
        raise ValueError("modes must be at least two and particles positive")
    if len(output) != modes or sum(output) != particles:
        raise ValueError("output has the wrong size")
    modular_sum = sum(
        mode * multiplicity
        for mode, multiplicity in enumerate(output)
    ) % modes
    if modular_sum != charge % modes:
        return Fraction(0)
    denominator = modes ** (particles - 1)
    for multiplicity in output:
        denominator *= factorial(multiplicity)
    return Fraction(factorial(particles), denominator)


def certify_exact_cat_design() -> None:
    """Assert the two exact rank-six blocks and the general cat rule."""
    probe_x = (1, 0, -1, 0, 0, 0, 0, 0, 0, 0, 0, 0)
    probe_y = (0, 1, 0, -1, 0, 0, 0, 0, 0, 0, 0, 0)
    outputs_x = (
        (0, 0, 2, 2),
        (0, 1, 1, 2),
        (0, 3, 1, 0),
        (1, 0, 2, 1),
        (1, 0, 3, 0),
        (1, 1, 0, 2),
    )
    outputs_y = (
        (0, 0, 2, 2),
        (0, 1, 1, 2),
        (0, 2, 2, 0),
        (0, 3, 1, 0),
        (1, 0, 2, 1),
        (1, 1, 0, 2),
    )
    x_columns = (0, 2, 4, 6, 8, 10)
    y_columns = (1, 3, 5, 7, 9, 11)
    expected_x = [
        [0, Fraction(-3, 2), 0, 0, Fraction(-3, 2), 0],
        [Fraction(3, 4), 0, 0, Fraction(3, 4), 0, Fraction(3, 2)],
        [Fraction(9, 4), 0, 0, Fraction(3, 4), 0, 0],
        [Fraction(3, 4), 0, Fraction(3, 4), 0, 0, Fraction(3, 2)],
        [0, -4, 0, 0, 0, 0],
        [Fraction(3, 4), 0, Fraction(3, 2), Fraction(3, 4), 0, 0],
    ]
    expected_y = [
        [0, Fraction(-3, 2), 0, 0, Fraction(-3, 2), 0],
        [Fraction(3, 4), 0, 0, Fraction(3, 4), 0, Fraction(3, 2)],
        [0, Fraction(-3, 2), 0, 0, Fraction(3, 2), 0],
        [Fraction(9, 4), 0, 0, Fraction(3, 4), 0, 0],
        [Fraction(3, 4), 0, Fraction(-3, 4), 0, 0, Fraction(3, 2)],
        [Fraction(3, 4), 0, Fraction(-3, 2), Fraction(3, 4), 0, 0],
    ]
    full_matrix_x = [
        cat_physical_differential_row(output, probe_x)
        for output in outputs_x
    ]
    full_matrix_y = [
        cat_physical_differential_row(output, probe_y)
        for output in outputs_y
    ]
    matrix_x = [
        [row[column] for column in x_columns]
        for row in full_matrix_x
    ]
    matrix_y = [
        [row[column] for column in y_columns]
        for row in full_matrix_y
    ]
    assert matrix_x == expected_x
    assert matrix_y == expected_y
    # The advertised 12-by-12 Jacobian is exactly block diagonal, not
    # merely so after dropping numerically small cross terms.
    assert all(
        row[column] == 0
        for row in full_matrix_x
        for column in y_columns
    )
    assert all(
        row[column] == 0
        for row in full_matrix_y
        for column in x_columns
    )
    assert rational_determinant(matrix_x) == Fraction(-243, 8)
    assert rational_determinant(matrix_y) == Fraction(729, 32)
    assert (
        rational_determinant(matrix_x)
        * rational_determinant(matrix_y)
        == Fraction(-177147, 256)
    )

    # Every selected outcome is an exactly dark nonzero-charge output.
    for output in set(outputs_x + outputs_y):
        assert general_fourier_cat_probability(4, 4, 0, output) == 0

    # Exact normalization and selection-rule checks over several F_m,n.
    for modes in range(2, 9):
        for particles in range(1, 7):
            outputs = list(occupation_vectors(particles, modes))
            for charge in range(modes):
                probabilities = [
                    general_fourier_cat_probability(
                        modes, particles, charge, output
                    )
                    for output in outputs
                ]
                assert sum(probabilities) == 1
                for output, probability in zip(outputs, probabilities):
                    modular_sum = sum(
                        mode * multiplicity
                        for mode, multiplicity in enumerate(output)
                    ) % modes
                    assert (probability == 0) == (modular_sum != charge)

    print("exact normalized cat Jacobians certified")
    print("J_X =", matrix_x)
    print("det(J_X) =", rational_determinant(matrix_x))
    print("J_Y =", matrix_y)
    print("det(J_Y) =", rational_determinant(matrix_y))
    print(
        "det(diag(J_X,J_Y)) =",
        rational_determinant(matrix_x) * rational_determinant(matrix_y),
    )
    print("general F_m cat selection rule certified for 2<=m<=8, 1<=n<=6")


def certify_exact_fock_design() -> None:
    """Assert a normalized rank-nine Fock dark-event certificate."""
    input_occupation = (1, 1, 1, 1)
    specifications = (
        ((0, 0, 1, 3), 4),   # X03
        ((0, 0, 1, 3), 5),   # Y03
        ((0, 0, 2, 2), 2),   # X02
        ((0, 0, 2, 2), 3),   # Y02
        ((0, 0, 3, 1), 6),   # X12
        ((0, 0, 3, 1), 7),   # Y12
        ((0, 1, 1, 2), 10),  # X23
        ((0, 1, 1, 2), 11),  # Y23
        ((0, 2, 2, 0), 3),   # Y02
    )
    expected = [
        [0, 0, 0, 0, Fraction(3, 2), 0,
         0, 0, 0, 0, Fraction(-3, 2), 0],
        [0, 0, 0, 0, 0, Fraction(3, 2),
         0, 0, 0, 0, 0, Fraction(3, 2)],
        [0, 0, 1, 0, 0, 0, 0, 0, -1, 0, 0, 0],
        [0, 0, 0, 1, 0, 0, 0, 0, 0, -1, 0, 0],
        [0, 0, 0, 0, 0, 0, Fraction(3, 2), 0,
         0, 0, Fraction(-3, 2), 0],
        [0, 0, 0, 0, 0, 0, 0, Fraction(3, 2),
         0, 0, 0, Fraction(-3, 2)],
        [-1, 0, 0, 0, 0, 0, -1, 0, 0, 0, 2, 0],
        [0, -1, 0, 0, 0, 0, 0, -1, 0, 0, 0, 2],
        [0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0],
    ]
    matrix = [
        fock_physical_differential_row(
            (input_occupation, output), probe
        )
        for output, probe in specifications
    ]
    assert matrix == expected
    assert all(
        root_permanent(input_occupation, output) == (0, 0)
        for output, _ in specifications
    )
    assert rational_rank(matrix) == 9

    gauge_vectors = (
        # K_A = X01 + X03 + X12 + X23
        (1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0),
        # K_B = Y01 - Y03 + Y12 + Y23
        (0, 1, 0, 0, 0, -1, 0, 1, 0, 0, 0, 1),
        # K_C = X02 + X13
        (0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0),
    )
    assert rational_rank([list(vector) for vector in gauge_vectors]) == 3
    assert all(
        sum(entry * coordinate for entry, coordinate in zip(row, vector))
        == 0
        for row in matrix
        for vector in gauge_vectors
    )
    # Rank nine plus three independent null vectors proves that these
    # vectors are the complete nullspace.
    pivot_columns = (0, 1, 2, 3, 4, 5, 6, 7, 9)
    pivot_minor = [
        [row[column] for column in pivot_columns]
        for row in matrix
    ]
    assert rational_determinant(pivot_minor) == Fraction(81, 8)

    print("exact normalized Fock rank-nine design certified")
    print("Fock Jacobian =", matrix)
    print("rank =", rational_rank(matrix))
    print("pivot columns =", pivot_columns)
    print("pivot minor determinant =", rational_determinant(pivot_minor))
    print("nullspace basis =", gauge_vectors)


def minimum_vector_probe_set(
    vectors: list[GaussianVector],
    target_rank: int,
) -> tuple[int, ...]:
    for size in range(1, 13):
        for probes in combinations(range(12), size):
            rows = [
                vector_differential_row(vector, probe)
                for probe in probes
                for vector in vectors
            ]
            if rational_rank(rows) == target_rank:
                return probes
    return ()


def minimum_axis_probe_set(events: list[Event], target_rank: int) -> tuple[int, ...]:
    """Find the smallest subset of coordinate-axis probes reaching rank."""
    for size in range(1, 13):
        for probes in combinations(range(12), size):
            rows = [
                differential_row(event, probe)
                for probe in probes
                for event in events
            ]
            if rational_rank(rows) == target_rank:
                return probes
    return ()


def greedy_differentials(
    events: list[Event],
    probes: tuple[int, ...],
    target_rank: int,
) -> list[tuple[Event, int, list[int]]]:
    """Choose an exact independent list of event/probe differentials."""
    candidates = [
        (event, probe, differential_row(event, probe))
        for probe in probes
        for event in events
    ]
    selected: list[tuple[Event, int, list[int]]] = []
    rows: list[list[int]] = []
    rank = 0
    for candidate in candidates:
        if rational_rank(rows + [candidate[2]]) > rank:
            selected.append(candidate)
            rows.append(candidate[2])
            rank += 1
            if rank == target_rank:
                break
    return selected


def physical_row_norms_squared(event: Event) -> tuple[Fraction, Fraction]:
    denominator_squared = physical_denominator_squared(*event)
    real, imaginary = event_rows(event)
    return (
        Fraction(
            sum(value * value for value in real),
            denominator_squared,
        ),
        Fraction(
            sum(value * value for value in imaginary),
            denominator_squared,
        ),
    )


def format_coordinate(index: int) -> str:
    generator, pair = COORDINATES[index]
    return f"{generator}{pair[0]}{pair[1]}"


def print_design(events: list[Event]) -> None:
    rows: list[list[int]] = []
    print(f"events={len(events)}")
    for event in events:
        real, imaginary = event_rows(event)
        rows.extend((real, imaginary))
        left, right, determinant = best_probe_pair(event)
        print(
            f"  {event[0]} -> {event[1]} "
            f"probes=({format_coordinate(left)},{format_coordinate(right)}) "
            f"local_det={determinant} "
            f"norms_squared={physical_row_norms_squared(event)}"
        )
        print(f"    Re={primitive(real)}")
        print(f"    Im={primitive(imaginary)}")
    print(f"real_rank={rational_rank(rows)}")


def main() -> None:
    certify_exact_cat_design()
    print()
    certify_exact_fock_design()
    print()
    occupations = list(occupation_vectors(4, 4))
    dark_events = [
        (r, s)
        for r in occupations
        for s in occupations
        if root_permanent(r, s) == (0, 0)
        and rational_rank(list(event_rows((r, s)))) == 2
    ]
    print(f"rank-two dark events={len(dark_events)}")

    fixed_input_candidates: list[
        tuple[int, Occupation, list[Event]]
    ] = []
    for r in occupations:
        candidates = [event for event in dark_events if event[0] == r]
        all_rows = [
            row
            for event in candidates
            for row in event_rows(event)
        ]
        rank = rational_rank(all_rows)
        if rank:
            fixed_input_candidates.append((rank, r, candidates))

    fixed_input_candidates.sort(reverse=True)
    print("best fixed-input ranks:")
    for rank, r, _ in fixed_input_candidates[:10]:
        print(f"  {r}: {rank}")

    full_design = greedy_events(dark_events)
    print("\nglobal greedy design")
    print_design(full_design)

    rank, r, candidates = fixed_input_candidates[0]
    design = greedy_events(candidates)
    print(f"\nbest fixed-input greedy design for {r} (maximum rank {rank})")
    print_design(design)
    probes = minimum_axis_probe_set(candidates, rank)
    print(
        "minimum coordinate-axis probe set using every dark output: "
        + ", ".join(format_coordinate(index) for index in probes)
    )
    probe_rows = [
        differential_row(event, probe)
        for probe in probes
        for event in candidates
    ]
    print(f"probe-differential rank={rational_rank(probe_rows)}")
    selected_differentials = greedy_differentials(
        candidates, probes, rank
    )
    print("one exact independent fixed-input differential set:")
    for event, probe, row in selected_differentials:
        print(
            f"  output {event[1]}, probe {format_coordinate(probe)}, "
            f"row={primitive(row)}"
        )

    quotient_rows = [
        row
        for event in dark_events
        for row in event_rows(event)
    ]
    noon_vectors = [noon_dark_vector(mode) for mode in (1, 2, 3)]
    print("\ncoherent NOON references for the three gauge directions")
    for mode, vector in zip((1, 2, 3), noon_vectors):
        real, imaginary = vector_rows(vector)
        print(f"  (|4_0>-|4_{mode}>)/sqrt(2) -> |4_0>")
        print(f"    Re={primitive(real)}")
        print(f"    Im={primitive(imaginary)}")
    coherent_rows = [
        row
        for vector in noon_vectors
        for row in vector_rows(vector)
    ]
    print(
        "rank after adding coherent references="
        f"{rational_rank(quotient_rows + coherent_rows)}"
    )

    chosen_noon_rows: list[tuple[int, int, list[int]]] = []
    rows = quotient_rows.copy()
    rank = rational_rank(rows)
    for mode, vector in zip((1, 2, 3), noon_vectors):
        best: tuple[int, list[int]] | None = None
        for probe in range(12):
            row = vector_differential_row(vector, probe)
            if rational_rank(rows + [row]) > rank:
                best = probe, row
                break
        if best is not None:
            probe, row = best
            chosen_noon_rows.append((mode, probe, row))
            rows.append(row)
            rank += 1
    print("one signed probe differential per coherent reference:")
    for mode, probe, row in chosen_noon_rows:
        print(
            f"  mode {mode}: probe {format_coordinate(probe)}, "
            f"row={primitive(row)}"
        )
    print(f"combined observable rank={rank}")

    cat_outputs = (
        (3, 1, 0, 0),
        (3, 0, 1, 0),
        (3, 0, 0, 1),
    )
    cat_vectors = [
        four_mode_cat_dark_vector(output)
        for output in cat_outputs
    ]
    print("\none-input four-mode cat reference")
    for output, vector in zip(cat_outputs, cat_vectors):
        real, imaginary = vector_rows(vector)
        print(f"  output {output}")
        print(f"    Re={primitive(real)}")
        print(f"    Im={primitive(imaginary)}")
    cat_rows = [
        row for vector in cat_vectors for row in vector_rows(vector)
    ]
    print(
        "rank after all cat-output quadratures="
        f"{rational_rank(quotient_rows + cat_rows)}"
    )

    all_cat_outputs = [
        output
        for output in occupations
        if sum(mode * count for mode, count in enumerate(output)) % 4
    ]
    all_cat_vectors = [
        four_mode_cat_dark_vector(output)
        for output in all_cat_outputs
    ]
    all_cat_rows = [
        row
        for vector in all_cat_vectors
        for row in vector_rows(vector)
    ]
    all_cat_rank = rational_rank(all_cat_rows)
    print(
        f"all dark outputs of one cat input: "
        f"events={len(all_cat_outputs)}, quadrature_rank={all_cat_rank}"
    )
    cat_probes = minimum_vector_probe_set(all_cat_vectors, all_cat_rank)
    print(
        "minimum cat coordinate-axis probes: "
        + ", ".join(format_coordinate(index) for index in cat_probes)
    )


if __name__ == "__main__":
    main()
