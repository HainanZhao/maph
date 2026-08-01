"""Exact conventions for the Cycle 10 E1/E2 engine block."""
from __future__ import annotations

from fractions import Fraction
from itertools import product
from typing import Iterable, Sequence


Q = Fraction
Matrix = list[list[Fraction]]
Vector = list[Fraction]


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def shape(a: Matrix) -> tuple[int, int]:
    require(bool(a), "matrix must be nonempty")
    width = len(a[0])
    require(width > 0, "matrix must have positive width")
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


def matrix_add(a: Matrix, b: Matrix) -> Matrix:
    rows, cols = shape(a)
    require(shape(b) == (rows, cols), "matrix addition dimension mismatch")
    return [[a[i][j] + b[i][j] for j in range(cols)] for i in range(rows)]


def matrix_subtract(a: Matrix, b: Matrix) -> Matrix:
    rows, cols = shape(a)
    require(shape(b) == (rows, cols), "matrix subtraction dimension mismatch")
    return [[a[i][j] - b[i][j] for j in range(cols)] for i in range(rows)]


def diagonal(values: Sequence[Fraction]) -> Matrix:
    size = len(values)
    require(size > 0, "diagonal must be nonempty")
    return [[values[i] if i == j else Q(0) for j in range(size)] for i in range(size)]


def trace(a: Matrix) -> Fraction:
    rows, cols = shape(a)
    require(rows == cols, "trace requires square matrix")
    return sum((a[i][i] for i in range(rows)), Q(0))


def matrix_power(a: Matrix, exponent: int) -> Matrix:
    rows, cols = shape(a)
    require(rows == cols, "matrix power requires square matrix")
    require(exponent >= 1, "matrix power exponent must be positive")
    result = [row[:] for row in a]
    for _ in range(1, exponent):
        result = matmul(result, a)
    return result


def frobenius_square(a: Matrix) -> Fraction:
    shape(a)
    return sum((entry * entry for row in a for entry in row), Q(0))


def outer(vector: Vector) -> Matrix:
    require(bool(vector), "outer product vector must be nonempty")
    return [[x * y for y in vector] for x in vector]


def scale_matrix(value: Fraction, a: Matrix) -> Matrix:
    shape(a)
    return [[value * entry for entry in row] for row in a]


def frame_operator(detectors: Sequence[Vector], weights: Sequence[Fraction]) -> Matrix:
    require(bool(detectors), "detector dictionary must be nonempty")
    require(len(detectors) == len(weights), "detector/weight mismatch")
    width = len(detectors[0])
    require(width > 0 and all(len(vector) == width for vector in detectors), "detector dimension mismatch")
    require(all(weight > 0 for weight in weights), "weights must be positive")
    require(sum(weights, Q(0)) == 1, "weights must sum to one")
    result = [[Q(0) for _ in range(width)] for _ in range(width)]
    for weight, vector in zip(weights, detectors, strict=True):
        result = matrix_add(result, scale_matrix(weight, outer(vector)))
    return result


def frame_kernel(matrix: Matrix, detectors: Sequence[Vector], weights: Sequence[Fraction]) -> Matrix:
    _, width = shape(matrix)
    require(all(len(vector) == width for vector in detectors), "matrix/detector width mismatch")
    b = frame_operator(detectors, weights)
    return matmul(matmul(matrix, b), transpose(matrix))


def e1_trace_rows(kernel: Matrix, exponent: int) -> dict[str, Fraction]:
    rows, cols = shape(kernel)
    require(rows == cols, "frame kernel must be square")
    require(exponent >= 1, "trace exponent must be positive")
    diagonal_power_sum = sum((kernel[i][i] ** exponent for i in range(rows)), Q(0))
    trace_power = trace(matrix_power(kernel, exponent))
    require(diagonal_power_sum <= trace_power, "E1 diagonal/trace inequality failed")
    return {"diagonal_power_sum": diagonal_power_sum, "trace_power": trace_power, "margin": trace_power - diagonal_power_sum}


def require_symmetric_zero_diagonal(a: Matrix) -> None:
    rows, cols = shape(a)
    require(rows == cols, "matrix must be square")
    require(all(a[i][i] == 0 for i in range(rows)), "matrix diagonal must vanish")
    require(all(a[i][j] == a[j][i] for i in range(rows) for j in range(rows)), "matrix must be symmetric")


def e2_rows(a: Matrix) -> dict[str, object]:
    require_symmetric_zero_diagonal(a)
    size, _ = shape(a)
    a2 = matmul(a, a)
    row_returns = [sum((a[i][j] ** 2 for j in range(size) if j != i), Q(0)) for i in range(size)]
    require([a2[i][i] for i in range(size)] == row_returns, "two-step return diagonal mismatch")
    c2 = matrix_subtract(a2, diagonal(row_returns))
    a4_trace = trace(matrix_power(a, 4))
    return_square = sum((value * value for value in row_returns), Q(0))
    c2_square = frobenius_square(c2)
    require(c2_square == a4_trace - return_square, "return-deleted Frobenius identity failed")
    edge_fourth = sum((a[i][j] ** 4 for i in range(size) for j in range(size) if i != j), Q(0))
    nb4_formula = a4_trace - 2 * return_square + edge_fourth
    nb4_direct = Q(0)
    for i0 in range(size):
        for i1 in range(size):
            for i2 in range(size):
                for i3 in range(size):
                    if i1 == i0 or i2 == i1 or i3 == i2 or i0 == i3:
                        continue
                    if i2 == i0 or i3 == i1:
                        continue
                    nb4_direct += a[i0][i1] * a[i1][i2] * a[i2][i3] * a[i3][i0]
    require(nb4_direct == nb4_formula, "NB4 inclusion-exclusion identity failed")
    return {
        "row_returns": row_returns,
        "c2": c2,
        "trace_a4": a4_trace,
        "return_square_sum": return_square,
        "c2_frobenius_square": c2_square,
        "edge_fourth_sum": edge_fourth,
        "nb4": nb4_formula,
    }


def symmetric_matrix_from_edges(size: int, edges: Sequence[int]) -> Matrix:
    require(size >= 2, "matrix order must be at least two")
    require(len(edges) == size * (size - 1) // 2, "edge count mismatch")
    result = [[Q(0) for _ in range(size)] for _ in range(size)]
    cursor = 0
    for i in range(size):
        for j in range(i + 1, size):
            value = Q(edges[cursor])
            cursor += 1
            result[i][j] = value
            result[j][i] = value
    return result


def search_nb4_countermodel(
    orders: Iterable[int] = range(3, 7),
    alphabet: Sequence[int] = (-2, -1, 0, 1, 2),
    cap_per_order: int = 250_000,
) -> dict[str, object]:
    require(cap_per_order > 0, "search cap must be positive")
    counts: dict[str, int] = {}
    for size in orders:
        edge_count = size * (size - 1) // 2
        checked = 0
        for edges in product(alphabet, repeat=edge_count):
            if checked >= cap_per_order:
                break
            checked += 1
            matrix = symmetric_matrix_from_edges(size, edges)
            rows = e2_rows(matrix)
            if rows["nb4"] < 0:
                counts[str(size)] = checked
                return {"status": "NB4_SIGN_COUNTERMODEL", "order": size, "edges": list(edges), "matrix": matrix, "nb4": rows["nb4"], "counts": counts}
        counts[str(size)] = checked
    return {"status": "NO_COUNTERMODEL_WITHIN_CAP", "counts": counts}


def verify_all() -> dict[str, object]:
    matrix = [[Q(1), Q(0), Q(2)], [Q(0), Q(1), Q(1)], [Q(1), Q(1), Q(0)]]
    detectors = [[Q(1), Q(0), Q(1)], [Q(0), Q(1), Q(-1)]]
    weights = [Q(1, 3), Q(2, 3)]
    kernel = frame_kernel(matrix, detectors, weights)
    e1 = {str(exponent): e1_trace_rows(kernel, exponent) for exponent in range(1, 5)}
    e2_example = e2_rows(symmetric_matrix_from_edges(4, (1, 1, 0, 1, 1, -1)))
    countermodel = search_nb4_countermodel()
    require(countermodel["status"] == "NB4_SIGN_COUNTERMODEL", "registered NB4 countermodel search did not close")
    return {"frame_kernel": kernel, "e1_rows": e1, "e2_example": e2_example, "nb4_search": countermodel}
