"""Exact conventions for the Cycle 11 E1+E2 block-variance reduction."""
from __future__ import annotations

from fractions import Fraction
from itertools import product
from typing import Sequence


Q = Fraction
Matrix = list[list[Fraction]]
Vector = list[Fraction]


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def shape(a: Matrix) -> tuple[int, int]:
    require(bool(a) and bool(a[0]), "matrix must be nonempty")
    width = len(a[0])
    require(all(len(row) == width for row in a), "ragged matrix")
    return len(a), width


def transpose(a: Matrix) -> Matrix:
    rows, cols = shape(a)
    return [[a[i][j] for i in range(rows)] for j in range(cols)]


def matmul(a: Matrix, b: Matrix) -> Matrix:
    rows, inner = shape(a)
    inner_b, cols = shape(b)
    require(inner == inner_b, "matrix dimension mismatch")
    return [[sum((a[i][k] * b[k][j] for k in range(inner)), Q(0)) for j in range(cols)] for i in range(rows)]


def add(a: Matrix, b: Matrix) -> Matrix:
    rows, cols = shape(a)
    require(shape(b) == (rows, cols), "matrix addition mismatch")
    return [[a[i][j] + b[i][j] for j in range(cols)] for i in range(rows)]


def subtract(a: Matrix, b: Matrix) -> Matrix:
    rows, cols = shape(a)
    require(shape(b) == (rows, cols), "matrix subtraction mismatch")
    return [[a[i][j] - b[i][j] for j in range(cols)] for i in range(rows)]


def scale(value: Fraction, a: Matrix) -> Matrix:
    shape(a)
    return [[value * entry for entry in row] for row in a]


def outer(x: Vector) -> Matrix:
    require(bool(x), "outer vector must be nonempty")
    return [[left * right for right in x] for left in x]


def vector_add(vectors: Sequence[Vector]) -> Vector:
    require(bool(vectors), "vector family must be nonempty")
    size = len(vectors[0])
    require(size > 0 and all(len(vector) == size for vector in vectors), "vector dimension mismatch")
    return [sum((vector[i] for vector in vectors), Q(0)) for i in range(size)]


def block_variance(blocks: Sequence[Vector]) -> dict[str, object]:
    require(bool(blocks), "block family must be nonempty")
    count = len(blocks)
    total = vector_add(blocks)
    frame = [[Q(0) for _ in total] for _ in total]
    for block in blocks:
        frame = add(frame, outer(block))
    centered = [[entry - total[i] / count for i, entry in enumerate(block)] for block in blocks]
    variance = [[Q(0) for _ in total] for _ in total]
    for block in centered:
        variance = add(variance, outer(block))
    rank_one = scale(Q(1, count), outer(total))
    require(frame == add(rank_one, variance), "block-variance decomposition failed")
    diagonal = [variance[i][i] for i in range(len(total))]
    diagonal_direct = [sum(((block[i] - total[i] / count) ** 2 for block in blocks), Q(0)) for i in range(len(total))]
    require(diagonal == diagonal_direct, "block-variance diagonal mismatch")
    return {"total": total, "frame": frame, "rank_one": rank_one, "variance": variance, "variance_diagonal": diagonal}


def trace(a: Matrix) -> Fraction:
    rows, cols = shape(a)
    require(rows == cols, "trace requires square matrix")
    return sum((a[i][i] for i in range(rows)), Q(0))


def power(a: Matrix, exponent: int) -> Matrix:
    rows, cols = shape(a)
    require(rows == cols and exponent >= 1, "invalid matrix power")
    result = [row[:] for row in a]
    for _ in range(1, exponent):
        result = matmul(result, a)
    return result


def rank_one_trace_power(vector: Vector, divisor: int, exponent: int) -> Fraction:
    require(divisor >= 1 and exponent >= 1, "invalid rank-one trace parameters")
    norm_square = sum((entry * entry for entry in vector), Q(0))
    matrix = scale(Q(1, divisor), outer(vector))
    direct = trace(power(matrix, exponent))
    formula = (norm_square / divisor) ** exponent
    require(direct == formula, "rank-one trace-power formula failed")
    return direct


def rank_one_two_step(amplitudes: Sequence[Fraction]) -> dict[str, object]:
    require(len(amplitudes) >= 3, "rank-one benchmark needs at least three rows")
    require(all(value > 0 for value in amplitudes), "amplitudes must be positive")
    vector = list(amplitudes)
    p = outer(vector)
    size = len(vector)
    diagonal_values = [value * value for value in vector]
    a = [[p[i][j] if i != j else Q(0) for j in range(size)] for i in range(size)]
    a2 = matmul(a, a)
    returns = [sum((a[i][j] ** 2 for j in range(size) if j != i), Q(0)) for i in range(size)]
    c2 = [[a2[i][j] if i != j else Q(0) for j in range(size)] for i in range(size)]
    total_mass = sum(diagonal_values, Q(0))
    for i in range(size):
        for j in range(size):
            if i == j:
                require(c2[i][j] == 0, "rank-one C2 diagonal mismatch")
            else:
                expected = vector[i] * vector[j] * (total_mass - diagonal_values[i] - diagonal_values[j])
                require(c2[i][j] == expected, "rank-one C2 off-diagonal formula mismatch")
    return {"p": p, "a": a, "returns": returns, "c2": c2, "total_mass": total_mass}


def constant_rank_one_rows(row_count: int, a: Fraction) -> dict[str, object]:
    require(row_count >= 3 and a > 0, "invalid constant rank-one benchmark")
    # Avoid irrational arithmetic: construct directly from P_ij=a.
    p = [[a for _ in range(row_count)] for _ in range(row_count)]
    centered = [[a if i != j else Q(0) for j in range(row_count)] for i in range(row_count)]
    returns = [(row_count - 1) * a * a for _ in range(row_count)]
    a2 = matmul(centered, centered)
    c2 = [[a2[i][j] if i != j else Q(0) for j in range(row_count)] for i in range(row_count)]
    top_c2 = (row_count - 1) * (row_count - 2) * a * a
    top_vector = [Q(1) for _ in range(row_count)]
    c2_on_top = [sum((c2[i][j] * top_vector[j] for j in range(row_count)), Q(0)) for i in range(row_count)]
    require(all(value == top_c2 for value in c2_on_top), "constant rank-one C2 top eigenvalue mismatch")
    return {
        "lambda_p": row_count * a,
        "return": returns[0],
        "lambda_a_top": (row_count - 1) * a,
        "lambda_a_other": -a,
        "lambda_c2_top": top_c2,
        "lambda_c2_other": (2 - row_count) * a * a,
    }


def colouring_frame(evaluation: Matrix, coefficients: Vector, colouring: Sequence[int], colour_count: int) -> Matrix:
    rows, width = shape(evaluation)
    require(len(coefficients) == width and len(colouring) == width, "colouring input mismatch")
    require(colour_count >= 2 and all(0 <= colour < colour_count for colour in colouring), "invalid colouring")
    block_values = [[Q(0) for _ in range(rows)] for _ in range(colour_count)]
    for colour in range(colour_count):
        for row in range(rows):
            block_values[colour][row] = sum((evaluation[row][n] * coefficients[n] for n in range(width) if colouring[n] == colour), Q(0))
    frame = [[Q(0) for _ in range(rows)] for _ in range(rows)]
    for values in block_values:
        frame = add(frame, outer(values))
    return frame


def verify_random_colouring(evaluation: Matrix, coefficients: Vector, colour_count: int) -> dict[str, object]:
    rows, width = shape(evaluation)
    require(2 <= width <= 5 and colour_count in (2, 3), "outside registered colouring range")
    total = colour_count ** width
    accumulated = [[Q(0) for _ in range(rows)] for _ in range(rows)]
    for colouring in product(range(colour_count), repeat=width):
        accumulated = add(accumulated, colouring_frame(evaluation, coefficients, colouring, colour_count))
    expectation = scale(Q(1, total), accumulated)
    detector = [sum((evaluation[row][n] * coefficients[n] for n in range(width)), Q(0)) for row in range(rows)]
    gram = [[sum((evaluation[i][n] * coefficients[n] ** 2 * evaluation[j][n] for n in range(width)), Q(0)) for j in range(rows)] for i in range(rows)]
    formula = add(scale(Q(1, colour_count), outer(detector)), scale(Q(colour_count - 1, colour_count), gram))
    require(expectation == formula, "random-colouring expectation failed")
    return {"width": width, "colour_count": colour_count, "colourings": total, "expectation": expectation, "formula": formula}


def verify_all() -> dict[str, object]:
    blocks = [[Q(2), Q(-1), Q(3)], [Q(0), Q(4), Q(-2)], [Q(1), Q(2), Q(1)]]
    decomposition = block_variance(blocks)
    zero_variance = block_variance([[Q(1), Q(2), Q(-1)] for _ in range(3)])
    require(all(entry == 0 for row in zero_variance["variance"] for entry in row), "zero-variance model failed")
    trace_powers = {str(exponent): rank_one_trace_power(decomposition["total"], len(blocks), exponent) for exponent in range(1, 5)}
    constant = constant_rank_one_rows(5, Q(7, 3))
    nonconstant = rank_one_two_step([Q(1), Q(2), Q(3), Q(4)])
    evaluations = {
        2: [[Q(1), Q(2)], [Q(-1), Q(3)], [Q(2), Q(1)]],
        3: [[Q(1), Q(2), Q(-1)], [Q(0), Q(3), Q(2)], [Q(2), Q(-1), Q(1)]],
        4: [[Q(1), Q(0), Q(2), Q(-1)], [Q(2), Q(1), Q(-1), Q(3)], [Q(-1), Q(2), Q(1), Q(1)]],
        5: [[Q(1), Q(2), Q(0), Q(-1), Q(3)], [Q(2), Q(-1), Q(1), Q(0), Q(2)], [Q(0), Q(1), Q(3), Q(2), Q(-2)]],
    }
    colouring_rows: dict[str, object] = {}
    for width, evaluation in evaluations.items():
        coefficients = [Q(index + 1) for index in range(width)]
        for colour_count in (2, 3):
            key = f"n{width}_k{colour_count}"
            colouring_rows[key] = verify_random_colouring(evaluation, coefficients, colour_count)
    return {
        "decomposition": decomposition,
        "zero_variance": zero_variance,
        "rank_one_trace_powers": trace_powers,
        "constant_rank_one": constant,
        "nonconstant_rank_one": nonconstant,
        "random_colouring": colouring_rows,
    }
