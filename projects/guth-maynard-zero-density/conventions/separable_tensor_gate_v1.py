"""Exact ordered tensor-square and separable gate conventions, Cycle 16."""
from __future__ import annotations

from fractions import Fraction


Q = Fraction


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def transpose(a: list[list[Fraction]]) -> list[list[Fraction]]:
    return [list(column) for column in zip(*a)]


def matmul(a: list[list[Fraction]], b: list[list[Fraction]]) -> list[list[Fraction]]:
    require(a and b and len(a[0]) == len(b), "matrix dimension mismatch")
    bt = transpose(b)
    return [[sum((x * y for x, y in zip(row, column)), Q(0)) for column in bt] for row in a]


def matvec(a: list[list[Fraction]], x: list[Fraction]) -> list[Fraction]:
    require(a and len(a[0]) == len(x), "matrix-vector dimension mismatch")
    return [sum((u * v for u, v in zip(row, x)), Q(0)) for row in a]


def dot(x: list[Fraction], y: list[Fraction]) -> Fraction:
    require(len(x) == len(y), "dot dimension mismatch")
    return sum((u * v for u, v in zip(x, y)), Q(0))


def tensor(x: list[Fraction], y: list[Fraction]) -> list[Fraction]:
    return [u * v for u in x for v in y]


def tensor_rows(u: list[list[Fraction]]) -> list[list[Fraction]]:
    return [tensor(row, row) for row in u]


def identity_rows(u: list[list[Fraction]], a: list[Fraction]) -> dict[str, object]:
    require(u and all(len(row) == len(a) for row in u), "sampling dimensions mismatch")
    s = tensor_rows(u)
    z = tensor(a, a)
    p = matvec(u, a)
    sz = matvec(s, z)
    require(sz == [value * value for value in p], "tensor evaluation identity mismatch")
    h = matmul(transpose(s), s)
    c = matmul(s, transpose(s))
    hz = matvec(h, z)
    quadratic = dot(z, hz)
    fourth = sum((value**4 for value in p), Q(0))
    require(quadratic == fourth, "fourth-form identity mismatch")
    require(dot(z, z) == dot(a, a) ** 2, "rank-one norm identity mismatch")
    gram = matmul(u, transpose(u))
    hadamard_square = [[value * value for value in row] for row in gram]
    require(c == hadamard_square, "row Gram Hadamard-square mismatch")
    return {"U": u, "a": a, "P": p, "S_z": sz, "H_2": h, "C_2": c, "quadratic": quadratic, "fourth": fourth}


def identical_row_rows(r: int, m: int) -> dict[str, object]:
    require(1 <= r <= 4 and 1 <= m <= 4, "registered identical-row range exceeded")
    u = [Q(index + 1) for index in range(m)]
    sampling = [list(u) for _ in range(r)]
    s = tensor_rows(sampling)
    h = matmul(transpose(s), s)
    z = tensor(u, u)
    z_norm = dot(z, z)
    quotient = dot(z, matvec(h, z)) / z_norm
    lambda_max = Q(r) * z_norm
    require(quotient == lambda_max, "identical-row separable quotient mismatch")
    return {"R": r, "m": m, "u_norm_squared": dot(u, u), "lambda_max": lambda_max, "separable_witness": quotient}


def spectral_overlap_row(eigenvalues: list[Fraction], vector: list[Fraction], cutoff: Fraction) -> dict[str, Fraction]:
    require(len(eigenvalues) == len(vector) and eigenvalues, "spectral dimensions mismatch")
    require(dot(vector, vector) == 1, "registered vector must be unit")
    maximum = max(eigenvalues)
    require(cutoff < maximum, "cutoff must lie below top eigenvalue")
    quadratic = sum((lam * value * value for lam, value in zip(eigenvalues, vector)), Q(0))
    overlap = sum((value * value for lam, value in zip(eigenvalues, vector) if lam > cutoff), Q(0))
    upper = cutoff + (maximum - cutoff) * overlap
    require(quadratic <= upper, "spectral-overlap upper bound failed")
    if quadratic > cutoff:
        lower = (quadratic - cutoff) / (maximum - cutoff)
        require(overlap >= lower, "spectral-overlap certificate failed")
    else:
        lower = Q(0)
    return {"cutoff": cutoff, "lambda_max": maximum, "quadratic": quadratic, "overlap": overlap, "upper": upper, "certified_lower": lower}


def exponent_rows() -> dict[str, Fraction]:
    count = Q(36, 25)
    threshold_fourth = Q(14, 5)
    coefficient_norm_squared = Q(2)
    required_sep = count + threshold_fourth - coefficient_norm_squared
    generic_sep = Q(12, 5)
    saving = generic_sep - required_sep
    require(required_sep == Q(56, 25), "required separable exponent mismatch")
    require(saving == Q(4, 25), "separable saving mismatch")
    return {"count": count, "threshold_fourth": threshold_fourth, "coefficient_norm_squared": coefficient_norm_squared, "required_sep": required_sep, "generic_sep": generic_sep, "saving": saving}


def verify_all() -> dict[str, object]:
    examples = [
        identity_rows([[Q(1), Q(2)], [Q(3), Q(-1)]], [Q(2), Q(-3)]),
        identity_rows([[Q(1), Q(0), Q(2)], [Q(-2), Q(1), Q(1)], [Q(3), Q(2), Q(-1)]], [Q(1), Q(-1), Q(2)]),
    ]
    identical = [identical_row_rows(r, m) for r in range(1, 5) for m in range(1, 5)]
    spectral = [
        spectral_overlap_row([Q(1), Q(3)], [Q(3, 5), Q(4, 5)], Q(2)),
        spectral_overlap_row([Q(0), Q(2), Q(5)], [Q(0), Q(3, 5), Q(4, 5)], Q(3)),
    ]
    require(len(examples) + len(identical) + len(spectral) < 1_000, "finite-row cap exceeded")
    return {"tensor_examples": examples, "identical_row_countermodels": identical, "spectral_overlap_examples": spectral, "exponents": exponent_rows()}
