"""Exact prime-atom integer and fractional moment envelope, Cycle 14."""
from fractions import Fraction


Q = Fraction


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def moment_row(k: Fraction) -> dict[str, Fraction]:
    require(k >= 0, "moment half-order must be nonnegative")
    diagonal = 12 + 5 * k
    length = 10 * k
    moment_upper = max(diagonal, length)
    threshold = 7 * k
    local_rows = moment_upper - threshold
    return {
        "k": k,
        "moment_order": 2 * k,
        "diagonal_branch": diagonal,
        "length_branch": length,
        "moment_upper": moment_upper,
        "threshold": threshold,
        "local_rows": local_rows,
        "delta_loss": 2 * k,
    }


def integer_census() -> dict[str, object]:
    rows = [moment_row(Q(k)) for k in range(1, 13)]
    optimum = min(rows, key=lambda row: (row["local_rows"], row["k"]))
    require(optimum["k"] == 2 and optimum["local_rows"] == 8, "integer optimum mismatch")
    require(rows[2]["local_rows"] == 9, "sixth moment mismatch")
    return {"rows": rows, "optimum_k": optimum["k"], "optimum_local_rows": optimum["local_rows"]}


def continuous_optimum() -> dict[str, Fraction]:
    crossing = Q(12, 5)
    row = moment_row(crossing)
    require(row["diagonal_branch"] == row["length_branch"] == 24, "continuous crossing mismatch")
    require(row["local_rows"] == Q(36, 5), "continuous optimum mismatch")
    integer_penalty = Q(8) - row["local_rows"]
    require(integer_penalty == Q(4, 5), "integer penalty mismatch")
    return {**row, "integer_penalty": integer_penalty}


def interpolation_row() -> dict[str, Fraction]:
    p = Q(24, 5)
    i4 = Q(22)
    i6 = Q(30)
    norm_theta = Q(1, 2)
    effective_i4_weight = p * norm_theta / 4
    effective_i6_weight = p * norm_theta / 6
    require(effective_i4_weight == Q(3, 5), "L4 effective weight mismatch")
    require(effective_i6_weight == Q(2, 5), "L6 effective weight mismatch")
    moment_upper = effective_i4_weight * i4 + effective_i6_weight * i6
    threshold = p * Q(7, 2)
    local_rows = moment_upper - threshold
    require(moment_upper == Q(126, 5), "interpolated moment exponent mismatch")
    require(threshold == Q(84, 5), "fractional threshold mismatch")
    require(local_rows == Q(42, 5), "interpolated local exponent mismatch")
    return {
        "moment_order": p,
        "norm_theta": norm_theta,
        "effective_i4_weight": effective_i4_weight,
        "effective_i6_weight": effective_i6_weight,
        "moment_upper": moment_upper,
        "threshold": threshold,
        "local_rows": local_rows,
    }


def target_row() -> dict[str, Fraction]:
    p = Q(24, 5)
    target_moment = Q(24)
    threshold = p * Q(7, 2)
    local_rows = target_moment - threshold
    require(local_rows == Q(36, 5), "target local exponent mismatch")
    return {"moment_order": p, "target_moment": target_moment, "threshold": threshold, "local_rows": local_rows, "gain": Q(8) - local_rows}


def verify_all() -> dict[str, object]:
    return {
        "integer_census": integer_census(),
        "continuous_optimum": continuous_optimum(),
        "ordinary_interpolation": interpolation_row(),
        "fractional_prime_target": target_row(),
    }
