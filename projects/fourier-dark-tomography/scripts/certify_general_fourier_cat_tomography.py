#!/usr/bin/env python3
"""Exact certificates for Fourier-cat off-diagonal error identification.

For m modes, let F_m be the discrete Fourier multiport and prepare the
charge-zero cat

    |Cat_{m,n}> = m^(-1/2) sum_j |n e_j>,       n == 0 (mod m).

For every cyclic distance c in {1,...,floor(m/2)}, this script selects the
dark occupations

    s_{p,c} = (n-1)e_p + e_{p+c}.

All indices are modulo m.  When 2c != 0 mod m, p runs over every mode.  In
the antipodal class 2c == 0, only one p from each pair is retained.  Two
fixed Hermitian probes, one real-symmetric and one oriented-imaginary,
turn the complex dark-amplitude differentials into two real contrast rows.

Everything below uses integer Gaussian arithmetic.  The common nonzero
amplitude normalization and common positive contrast factors are omitted,
because they do not affect rank.
"""

from __future__ import annotations

import argparse
from fractions import Fraction
from math import gcd


Gaussian = tuple[int, int]
Occupation = tuple[int, ...]
Coordinate = tuple[str, int, int]


def add(left: Gaussian, right: Gaussian) -> Gaussian:
    return left[0] + right[0], left[1] + right[1]


def scale(factor: int, value: Gaussian) -> Gaussian:
    return factor * value[0], factor * value[1]


def conjugate(value: Gaussian) -> Gaussian:
    return value[0], -value[1]


def real_inner(left: Gaussian, right: Gaussian) -> int:
    """Real part of conjugate(left) * right."""
    return left[0] * right[0] + left[1] * right[1]


def coordinates(modes: int) -> tuple[Coordinate, ...]:
    return tuple(
        (kind, left, right)
        for left in range(modes)
        for right in range(left + 1, modes)
        for kind in ("X", "Y")
    )


def basis_entry(
    coordinate: Coordinate,
    row: int,
    column: int,
) -> Gaussian:
    kind, left, right = coordinate
    if kind == "X":
        if (row, column) in ((left, right), (right, left)):
            return 1, 0
    elif kind == "Y":
        # Y_lr = -i |l><r| + i |r><l| for l < r.
        if (row, column) == (left, right):
            return 0, -1
        if (row, column) == (right, left):
            return 0, 1
    else:
        raise ValueError(f"unknown coordinate kind {kind!r}")
    return 0, 0


def selected_occupation(
    modes: int,
    photons: int,
    mode: int,
    charge: int,
) -> Occupation:
    result = [0] * modes
    result[mode] = photons - 1
    result[(mode + charge) % modes] += 1
    return tuple(result)


def modular_charge(occupation: Occupation) -> int:
    return sum(mode * count for mode, count in enumerate(occupation)) % len(
        occupation
    )


def amplitude_gradient(
    occupation: Occupation,
    charge: int,
) -> tuple[Gaussian, ...]:
    """Return the unnormalized vector ell_s(H)=sum_a s_a H[a,a-c].

    The omitted physical factor is

        sqrt(n! / prod_a s_a!) * m^((1-n)/2),

    which is positive and nonzero.  This formula follows directly by
    differentiating the Fourier-cat output polynomial.
    """
    modes = len(occupation)
    result = []
    for coordinate in coordinates(modes):
        total = (0, 0)
        for row in range(modes):
            total = add(
                total,
                scale(
                    occupation[row],
                    basis_entry(
                        coordinate,
                        row,
                        (row - charge) % modes,
                    ),
                ),
            )
        result.append(total)
    return tuple(result)


def real_probe_entry(row: int, column: int) -> Gaussian:
    return (0, 0) if row == column else (1, 0)


def imaginary_probe_entry(
    modes: int,
    row: int,
    column: int,
) -> Gaussian:
    """Entry of a fixed cyclic orientation of the complete graph.

    For every non-antipodal representative c < m/2 we impose
    H[a,a-c]=i.  If m is even, antipodal pairs are oriented from
    p in {0,...,m/2-1} to p+m/2, so H[p,p+m/2]=i.
    """
    if row == column:
        return 0, 0
    difference = (row - column) % modes
    half = modes // 2
    if modes % 2 == 0 and difference == half:
        return (0, 1) if row < half else (0, -1)
    if 1 <= difference <= (modes - 1) // 2:
        return 0, 1
    return 0, -1


def probe_amplitude(
    occupation: Occupation,
    charge: int,
    *,
    imaginary: bool,
) -> Gaussian:
    modes = len(occupation)
    total = (0, 0)
    for row, count in enumerate(occupation):
        if imaginary:
            entry = imaginary_probe_entry(
                modes, row, (row - charge) % modes
            )
        else:
            entry = real_probe_entry(row, (row - charge) % modes)
        total = add(total, scale(count, entry))
    return total


def contrast_rows(
    occupation: Occupation,
    charge: int,
) -> tuple[list[int], list[int]]:
    gradient = amplitude_gradient(occupation, charge)
    references = (
        probe_amplitude(occupation, charge, imaginary=False),
        probe_amplitude(occupation, charge, imaginary=True),
    )
    return tuple(
        [real_inner(reference, value) for value in gradient]
        for reference in references
    )  # type: ignore[return-value]


def selected_events(
    modes: int,
    photons: int,
) -> list[tuple[int, int, Occupation]]:
    if photons % modes:
        raise ValueError("the explicit family requires photons == 0 mod modes")
    result = []
    for charge in range(1, modes // 2 + 1):
        antipodal = modes % 2 == 0 and charge == modes // 2
        mode_range = range(modes // 2) if antipodal else range(modes)
        for mode in mode_range:
            occupation = selected_occupation(
                modes, photons, mode, charge
            )
            if modular_charge(occupation) != charge:
                raise AssertionError("selected outcome has wrong charge")
            result.append((charge, mode, occupation))
    return result


def certificate_matrix(modes: int, photons: int) -> list[list[int]]:
    rows: list[list[int]] = []
    for charge, _, occupation in selected_events(modes, photons):
        rows.extend(contrast_rows(occupation, charge))
    return rows


def fourth_root_power(exponent: int) -> Gaussian:
    """Return i**exponent exactly as a Gaussian integer."""
    return ((1, 0), (0, 1), (-1, 0), (0, -1))[exponent % 4]


def f4_spam_matrix(
    photons: int = 4,
    *,
    include_amplitudes: bool = True,
    include_phases: bool = True,
) -> list[list[int]]:
    """Selected-contrast Jacobian for relative F4-cat coefficient errors.

    The three columns in either family use the relative perturbation bases
    e_j-e_0, j=1,2,3.  Real coefficient perturbations model amplitude
    imbalance; multiplication by i models phase perturbations.  Common
    nonzero factors are omitted.
    """
    if not include_amplitudes and not include_phases:
        return [[] for _ in range(12)]
    events = selected_events(4, photons)
    columns: list[tuple[str, int]] = []
    if include_amplitudes:
        columns.extend(("amplitude", mode) for mode in range(1, 4))
    if include_phases:
        columns.extend(("phase", mode) for mode in range(1, 4))
    rows: list[list[int]] = []
    for charge, _, occupation in events:
        references = (
            probe_amplitude(occupation, charge, imaginary=False),
            probe_amplitude(occupation, charge, imaginary=True),
        )
        for reference in references:
            row = []
            for family, mode in columns:
                leakage = add(
                    fourth_root_power(mode * charge),
                    scale(-1, fourth_root_power(0)),
                )
                if family == "phase":
                    leakage = -leakage[1], leakage[0]
                row.append(real_inner(reference, leakage))
            rows.append(row)
    return rows


def rational_rank(rows: list[list[int]]) -> int:
    matrix = [[Fraction(value) for value in row] for row in rows]
    rank = 0
    columns = len(matrix[0]) if matrix else 0
    for column in range(columns):
        pivot = next(
            (
                index
                for index in range(rank, len(matrix))
                if matrix[index][column]
            ),
            None,
        )
        if pivot is None:
            continue
        matrix[rank], matrix[pivot] = matrix[pivot], matrix[rank]
        pivot_value = matrix[rank][column]
        for entry in range(column, columns):
            matrix[rank][entry] /= pivot_value
        for index in range(len(matrix)):
            if index == rank:
                continue
            factor = matrix[index][column]
            if not factor:
                continue
            for entry in range(column, columns):
                matrix[index][entry] -= factor * matrix[rank][entry]
        rank += 1
        if rank == len(matrix):
            break
    return rank


def primitive(row: list[int]) -> list[int]:
    divisor = 0
    for value in row:
        divisor = gcd(divisor, abs(value))
    return [value // divisor for value in row] if divisor else row


def verify(modes: int, photons: int) -> dict[str, int]:
    if modes < 2:
        raise ValueError("this certificate requires at least two modes")
    if photons <= 2 or photons % modes:
        raise ValueError("photons must be a multiple of modes and exceed two")
    dimension = modes * (modes - 1)
    events = selected_events(modes, photons)
    matrix = certificate_matrix(modes, photons)
    rank = rational_rank(matrix)
    assert len(events) == dimension // 2
    assert len(matrix) == dimension
    assert all(len(row) == dimension for row in matrix)
    assert rank == dimension

    # Check the two closed-form probe references used in the proof.
    for charge, mode, occupation in events:
        real_reference = probe_amplitude(
            occupation, charge, imaginary=False
        )
        imaginary_reference = probe_amplitude(
            occupation, charge, imaginary=True
        )
        assert real_reference == (photons, 0)
        antipodal = modes % 2 == 0 and charge == modes // 2
        expected_imaginary = photons - 2 if antipodal else photons
        assert imaginary_reference == (0, expected_imaginary)
        if antipodal:
            assert mode < modes // 2
    return {
        "modes": modes,
        "photons": photons,
        "dimension": dimension,
        "events": len(events),
        "rows": len(matrix),
        "rank": rank,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--min-modes", type=int, default=3)
    parser.add_argument("--max-modes", type=int, default=9)
    parser.add_argument(
        "--photon-multiple",
        type=int,
        default=1,
        help="use n = photon_multiple * m",
    )
    args = parser.parse_args()
    for modes in range(args.min_modes, args.max_modes + 1):
        result = verify(modes, args.photon_multiple * modes)
        print(
            "m={modes} n={photons} dim={dimension} "
            "events={events} rows={rows} rank={rank}".format(**result)
        )


if __name__ == "__main__":
    main()
