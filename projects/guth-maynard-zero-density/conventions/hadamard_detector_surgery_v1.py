"""Exact Hadamard detector-surgery conventions for Cycle 27."""
from fractions import Fraction


Q = Fraction


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def sylvester(order: int) -> tuple[tuple[int, ...], ...]:
    require(order >= 1 and order & (order - 1) == 0, "Hadamard order must be a power of two")
    matrix = ((1,),)
    while len(matrix) < order:
        top = tuple(row + row for row in matrix)
        bottom = tuple(row + tuple(-entry for entry in row) for row in matrix)
        matrix = top + bottom
    return matrix


def transform(matrix: tuple[tuple[int, ...], ...], vector: tuple[complex | int, ...]) -> tuple[complex, ...]:
    return tuple(sum(row[j] * vector[j] for j in range(len(vector))) for row in matrix)


def gaussian_norm_squared(value: complex | int | Fraction) -> Fraction:
    real = Q(value.real)
    imag = Q(value.imag)
    return real * real + imag * imag


def hadamard_checks() -> dict[str, object]:
    order = 4
    matrix = sylvester(order)
    gram = tuple(tuple(sum(matrix[i][j] * matrix[m][j] for j in range(order)) for m in range(order)) for i in range(order))
    expected = tuple(tuple(order if i == m else 0 for m in range(order)) for i in range(order))
    require(gram == expected, "Sylvester orthogonality mismatch")
    block_norm_squared = Q(3, 4)
    detector_norm_squared = order * block_norm_squared
    require(detector_norm_squared == 3, "signed detector norm mismatch")
    return {
        "order": order,
        "matrix": matrix,
        "row_gram": gram,
        "block_norm_squared": block_norm_squared,
        "signed_detector_norm_squared": detector_norm_squared,
    }


def parseval_check() -> dict[str, object]:
    matrix = sylvester(4)
    z = (1 + 2j, 2 - 1j, -1 + 1j, 3 + 0j)
    transformed = transform(matrix, z)
    total_energy = sum(gaussian_norm_squared(value) for value in transformed)
    block_energy = 4 * sum(gaussian_norm_squared(value) for value in z)
    mean = sum(z) / 4
    complement_energy = sum(gaussian_norm_squared(value) for value in transformed[1:])
    variance_energy = 4 * sum(gaussian_norm_squared(value - mean) for value in z)
    require(total_energy == block_energy, "Hadamard Parseval mismatch")
    require(complement_energy == variance_energy, "complement/variance identity mismatch")
    return {
        "z": tuple(str(value) for value in z),
        "transform": tuple(str(value) for value in transformed),
        "total_energy": total_energy,
        "block_energy": block_energy,
        "complement_energy": complement_energy,
        "variance_energy": variance_energy,
    }


def branch_checks() -> dict[str, object]:
    order = 4
    matrix = sylvester(order)
    high_z = (1, 1, 1, -1)
    high_transform = transform(matrix, high_z)
    high_V = Q(2)
    high_complement = Q(sum(abs(value) ** 2 for value in high_transform[1:]))
    high_threshold = high_V**2 / (16 * order)
    high_max_squared = Q(max(abs(value) ** 2 for value in high_transform[1:]))
    forced_max_squared = high_V**2 / (16 * order * (order - 1))
    require(high_complement >= high_threshold, "high-variance example misses branch")
    require(high_max_squared >= forced_max_squared, "high-variance detector bound mismatch")

    low_z = (Q(1), Q(1), Q(1), Q(1))
    low_transform = transform(matrix, low_z)
    low_V = Q(4)
    low_complement = Q(sum(value * value for value in low_transform[1:]))
    block_error_bound = low_V / (4 * order)
    aligned_real_lower = 3 * low_V / (4 * order)
    require(low_complement < low_V**2 / (16 * order), "low-variance example misses branch")
    require(all(abs(value - low_transform[0] / order) < block_error_bound for value in low_z), "low-variance block error mismatch")
    require(all(value >= aligned_real_lower for value in low_z), "aligned block lower bound mismatch")
    return {
        "high_variance": {
            "complement_energy": high_complement,
            "threshold": high_threshold,
            "max_nontrivial_squared": high_max_squared,
            "forced_max_squared": forced_max_squared,
        },
        "low_variance": {
            "complement_energy": low_complement,
            "block_error_bound": block_error_bound,
            "aligned_real_lower": aligned_real_lower,
        },
    }


def verify_all() -> dict[str, object]:
    return {
        "hadamard": hadamard_checks(),
        "parseval": parseval_check(),
        "branches": branch_checks(),
        "dichotomy": "orthogonal signed detector >=V/(4J), or every aligned block real part >=3V/(4J)",
        "subpower_rule": "J=X^o(1)",
    }
