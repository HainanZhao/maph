"""Exact phase-synchronization and recurrence-graph conventions, Cycle 19."""
from fractions import Fraction


Q = Fraction


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def critical_exponents() -> dict[str, Fraction]:
    coefficient_norm = Q(1)
    row_norm = Q(1)
    threshold = Q(7, 10)
    target_rows = Q(21, 25)
    correlation = 2 * threshold - coefficient_norm
    diagonal_transition = row_norm - correlation
    popular_pairs = 2 * target_rows + correlation - row_norm
    average_degree = popular_pairs - target_rows
    two_step_paths = 2 * popular_pairs - target_rows
    require(correlation == Q(2, 5), "critical correlation mismatch")
    require(diagonal_transition == Q(3, 5), "diagonal transition mismatch")
    require(popular_pairs == Q(27, 25), "popular-pair exponent mismatch")
    require(average_degree == Q(6, 25), "average-degree exponent mismatch")
    require(two_step_paths == Q(33, 25), "two-step exponent mismatch")
    return {
        "coefficient_norm_squared": coefficient_norm,
        "row_norm_squared": row_norm,
        "threshold": threshold,
        "correlation_scale": correlation,
        "diagonal_transition": diagonal_transition,
        "target_rows": target_rows,
        "popular_ordered_pairs": popular_pairs,
        "average_degree": average_degree,
        "ordered_two_step_paths": two_step_paths,
    }


def finite_simplex() -> dict[str, Fraction | int]:
    # This is the exact Gram data of the common-component construction.
    A = Q(25)
    M = Q(16)
    w = Q(4)
    R = 9
    V_squared = A * w
    diagonal_sum = R * M
    off_diagonal_sum = R * (R - 1) * w
    synchronized_sum = diagonal_sum + off_diagonal_sum
    cauchy_lower = R * R * w
    off_diagonal_lower = cauchy_lower - diagonal_sum
    half_lower = Q(R * R, 2) * w
    popular_ordered_pairs = R * (R - 1)
    registered_pair_lower = Q(R * R) * w / (4 * M)
    ordered_two_step_paths = R * (R - 1) ** 2
    path_lower = Q(popular_ordered_pairs**2, R)
    small_eigenvalue = M - w
    large_eigenvalue = M + (R - 1) * w
    require(R * w >= 2 * M, "finite model misses off-diagonal regime")
    require(off_diagonal_sum >= half_lower, "off-diagonal half bound fails")
    require(popular_ordered_pairs >= registered_pair_lower, "popular-pair bound fails")
    require(ordered_two_step_paths == path_lower, "regular graph path identity fails")
    require(small_eigenvalue > 0 and large_eigenvalue > 0, "simplex Gram matrix is not positive definite")
    return {
        "A": A,
        "M": M,
        "w": w,
        "R": R,
        "V_squared": V_squared,
        "diagonal_sum": diagonal_sum,
        "off_diagonal_sum": off_diagonal_sum,
        "synchronized_sum": synchronized_sum,
        "cauchy_lower": cauchy_lower,
        "off_diagonal_lower": off_diagonal_lower,
        "half_lower": half_lower,
        "popular_ordered_pairs": popular_ordered_pairs,
        "registered_pair_lower": registered_pair_lower,
        "ordered_two_step_paths": ordered_two_step_paths,
        "path_lower": path_lower,
        "small_gram_eigenvalue": small_eigenvalue,
        "large_gram_eigenvalue": large_eigenvalue,
        "phase_code_entropy": Q(0),
    }


def verify_all() -> dict[str, object]:
    return {
        "critical_exponents": critical_exponents(),
        "finite_common_component_simplex": finite_simplex(),
        "synchronization_identity": "R^2 V^2/A <= sum_(t,s) z_t conjugate(z_s) K(t,s)",
        "popular_pair_bound": "if Rw>=2M then E_(Re phase*K>=w/4) >= R^2w/(4M)",
        "two_generation_bound": "sum_t d_t^2 >= E^2/R",
        "closure_gap": "two popular edges sharing a vertex do not abstractly force their endpoint pair to be popular",
    }
