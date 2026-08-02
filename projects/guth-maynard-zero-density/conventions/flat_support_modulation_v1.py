"""Exact flat-support modulation conventions for Cycle 32."""
from fractions import Fraction


Q = Fraction
LAMBDAS = tuple(Q(j, 25) for j in range(5))


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def finite_dyadic_check() -> dict[str, object]:
    J = 16
    discard_threshold_squared = Q(1, 4 * J)
    squared_magnitudes = (Q(1, 128),) * 8 + (Q(3, 64),) * 4 + (Q(3, 16),) * 4
    require(sum(squared_magnitudes, Q(0)) == 1, "finite vector is not unit")
    discarded = sum((value for value in squared_magnitudes if value < discard_threshold_squared), Q(0))
    require(discarded == Q(1, 16) <= Q(1, 4), "discarded mass mismatch")
    selected_indices = tuple(index for index, value in enumerate(squared_magnitudes) if value == Q(3, 16))
    selected_mass = sum((squared_magnitudes[index] for index in selected_indices), Q(0))
    s = len(selected_indices)
    normalized_squared = tuple(squared_magnitudes[index] / selected_mass for index in selected_indices)
    lower_squared = Q(1, 4 * s)
    upper_squared = Q(4, s)
    require(selected_mass == Q(3, 4), "selected dyadic mass mismatch")
    require(all(lower_squared <= value <= upper_squared for value in normalized_squared), "flat-support bounds mismatch")
    error_amplification_squared = 1 / selected_mass
    require(error_amplification_squared == Q(4, 3), "projected error amplification mismatch")
    return {
        "J": J,
        "discard_threshold_squared": discard_threshold_squared,
        "squared_magnitudes": squared_magnitudes,
        "discarded_mass": discarded,
        "selected_indices": selected_indices,
        "selected_mass": selected_mass,
        "support_size": s,
        "normalized_squared_magnitudes": normalized_squared,
        "flat_lower_squared": lower_squared,
        "flat_upper_squared": upper_squared,
        "error_amplification_squared": error_amplification_squared,
    }


def support_row(lam: Fraction) -> dict[str, Fraction]:
    block_count = Q(4, 25)
    block_size = Q(21, 25)
    rows = Q(21, 25)
    require(0 <= lam <= block_count, "support lambda outside self-dual range")
    coordinate_support = block_size + lam
    per_prime_magnitude = -coordinate_support / 2
    coordinate_excess = coordinate_support - rows
    require(coordinate_excess == lam, "coordinate excess mismatch")
    return {
        "lambda": lam,
        "support_blocks": lam,
        "prime_coordinate_support": coordinate_support,
        "rows": rows,
        "coordinate_excess": coordinate_excess,
        "per_prime_magnitude": per_prime_magnitude,
    }


def support_ladder() -> list[dict[str, Fraction]]:
    rows = [support_row(lam) for lam in LAMBDAS]
    require(rows[0]["prime_coordinate_support"] == rows[0]["rows"], "lambda-zero square scale mismatch")
    require(rows[-1]["prime_coordinate_support"] == 1, "full-support endpoint mismatch")
    return rows


def verify_all() -> dict[str, object]:
    return {
        "finite_dyadic": finite_dyadic_check(),
        "support_ladder": support_ladder(),
        "bin_count": "L=ceil(log_2(2sqrt(J)))+1=O(log X)",
        "selected_mass_lower": "mu^2>=3/(4L)",
        "normalized_error": "sqrt(4L/3) exp(-X^(2/25-o(1)))=exp(-X^(2/25-o(1)))",
    }
