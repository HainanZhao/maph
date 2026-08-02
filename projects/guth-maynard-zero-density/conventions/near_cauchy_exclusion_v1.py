"""Exact exponent and constant-flow conventions for Cycle 25."""
from fractions import Fraction


Q = Fraction


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def critical_exponents() -> dict[str, Fraction | int]:
    rows = Q(21, 25)
    rho = Q(-3, 5)
    k_rho = rows + rho
    delta_fraction = Q(1, 8)
    square_root_delta_fraction = delta_fraction / 2
    height_exponent = Q(1)
    coefficient_exponent = Q(12, 5)
    matveev_log_power = 3
    require(k_rho == Q(6, 25), "critical recurrence scale mismatch")
    require(square_root_delta_fraction == Q(1, 16), "square-root delta constant mismatch")
    return {
        "rows": rows,
        "rho": rho,
        "k_rho": k_rho,
        "delta_exponent_fraction": delta_fraction,
        "phase_error_exponent_fraction": square_root_delta_fraction,
        "rational_height_exponent": height_exponent,
        "integer_coefficient_exponent": coefficient_exponent,
        "matveev_log_power": matveev_log_power,
    }


def concentration_constants() -> dict[str, Fraction | int | str]:
    mean_deficit_multiplier = 2
    squared_distance_multiplier = 2 * mean_deficit_multiplier
    pointwise_distance_multiplier = 2
    ratio_distance_multiplier = 2 * pointwise_distance_multiplier
    angular_multiplier = "pi/2"
    require(squared_distance_multiplier == 4, "mean-to-square constant mismatch")
    require(ratio_distance_multiplier == 4, "point-to-ratio constant mismatch")
    return {
        "mean_modulus_lower": "1-2 delta",
        "sum_squared_distance_upper": "4 M delta",
        "pointwise_distance_upper": "2 sqrt(M delta)",
        "ratio_distance_upper": "4 sqrt(M delta)",
        "angular_error_upper": "2 pi sqrt(M delta)",
        "mean_deficit_multiplier": mean_deficit_multiplier,
        "squared_distance_multiplier": squared_distance_multiplier,
        "pointwise_distance_multiplier": pointwise_distance_multiplier,
        "ratio_distance_multiplier": ratio_distance_multiplier,
        "angular_multiplier": angular_multiplier,
    }


def prime_intervals() -> dict[str, tuple[Fraction, Fraction] | str]:
    q_interval = (Q(1), Q(11, 10))
    p_interval = (Q(7, 5), Q(3, 2))
    r_interval = (Q(9, 5), Q(19, 10))
    require(q_interval[1] < p_interval[0] < p_interval[1] < r_interval[0], "prime intervals overlap")
    require(r_interval[1] < 2, "prime intervals leave dyadic range")
    return {
        "q_over_X": q_interval,
        "p_over_X": p_interval,
        "r_over_X": r_interval,
        "alpha_bounds": "log(14/11)<=log(p/q)<=log(3/2)",
        "beta_bounds": "log(18/11)<=log(r/q)<=log(19/10)",
    }


def asymptotic_separation() -> dict[str, str | bool]:
    return {
        "upper_log_form": "exp(-k rho/16+O(log X))",
        "lower_log_form": "exp(-O((log X)^3))",
        "dominance": "X^(6/25-o(1))/(log X)^3 tends to infinity",
        "contradiction_for_large_X": True,
    }


def verify_all() -> dict[str, object]:
    return {
        "critical_exponents": critical_exponents(),
        "concentration_constants": concentration_constants(),
        "prime_intervals": prime_intervals(),
        "asymptotic_separation": asymptotic_separation(),
        "multiplicative_form": "(p/q)^n (r/q)^(-m) != 1 by unique factorization",
    }
