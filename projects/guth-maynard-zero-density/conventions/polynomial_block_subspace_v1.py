"""Exact polynomial block-subspace conventions for Cycle 29."""
from fractions import Fraction


Q = Fraction


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def exponent_ledger() -> dict[str, Fraction | str]:
    kappa = Q(1, 25)
    block_length = 1 - kappa
    pnt_endpoint = Q(17, 30)
    rows = Q(21, 25)
    rho = Q(-3, 5)
    k_rho = rows + rho
    reconstruction = k_rho - kappa
    delta_fraction = Q(1, 8)
    point_error_fraction = delta_fraction / 4
    require(block_length == Q(24, 25), "block-length exponent mismatch")
    require(block_length > pnt_endpoint, "block length outside checked PNT range")
    require(k_rho == Q(6, 25), "base block-subspace shift mismatch")
    require(reconstruction == Q(1, 5), "polynomial-rank reconstruction exponent mismatch")
    require(point_error_fraction == Q(1, 32), "point-error constant mismatch")
    return {
        "kappa": kappa,
        "block_count": "J=X^(1/25+o(1))",
        "block_length": block_length,
        "checked_pnt_endpoint": pnt_endpoint,
        "rows": rows,
        "rho": rho,
        "k_rho": k_rho,
        "reconstruction_exponent": reconstruction,
        "delta_exponent_fraction": delta_fraction,
        "point_error_exponent_fraction": point_error_fraction,
        "negative_shift": "-k rho/4",
        "reconstruction_error": "sqrt(2) exp(-k rho/(8J))",
    }


def no_loss_projection_check() -> dict[str, Fraction | str]:
    # Squared masses of four equal blocks; the normalized original detector
    # has block-basis coordinate squares A_j/A.
    block_mass_fractions = (Q(1, 4),) * 4
    detector_projection_energy = sum(block_mass_fractions, Q(0))
    extra_orthogonal_energy = Q(3, 20)
    full_subspace_projection = detector_projection_energy + extra_orthogonal_energy
    require(detector_projection_energy == 1, "detector missing from block subspace")
    require(full_subspace_projection >= detector_projection_energy, "subspace projection lost detector energy")
    return {
        "block_mass_fractions": block_mass_fractions,
        "original_detector_energy_in_subspace": detector_projection_energy,
        "generic_projection_monotonicity": "||E*x||^2>=|<x,b>|^2 because b is in range(E)",
    }


def markov_check() -> dict[str, Fraction | int]:
    block_size = 120
    mean_squared_error = Q(1, 144)
    total_squared_error = block_size * mean_squared_error
    squared_bad_threshold = Q(1, 12)  # sqrt(mean_squared_error)
    bad_count_upper = total_squared_error / squared_bad_threshold
    bad_fraction_upper = bad_count_upper / block_size
    subinterval_size = 40
    good_per_subinterval_lower = subinterval_size - bad_count_upper
    require(bad_count_upper == 10, "Markov bad-count mismatch")
    require(bad_fraction_upper == Q(1, 12), "Markov bad-fraction mismatch")
    require(good_per_subinterval_lower == 30, "subinterval good-prime check mismatch")
    return {
        "block_size": block_size,
        "mean_squared_error": mean_squared_error,
        "point_error_threshold": "mean_squared_error^(1/4)",
        "squared_bad_threshold": squared_bad_threshold,
        "bad_count_upper": bad_count_upper,
        "bad_fraction_upper": bad_fraction_upper,
        "subinterval_size": subinterval_size,
        "good_per_subinterval_lower": good_per_subinterval_lower,
    }


def asymptotic_alternatives() -> dict[str, str]:
    return {
        "near_subspace_upper_form": "exp(-k rho/32+O(log X))",
        "matveev_lower_form": "exp(-O((log X)^3))",
        "near_subspace_status": "EXCLUDED_FOR_SUFFICIENTLY_LARGE_X",
        "regular_alternatives": "shift<=-k rho/4, approximate/exact block-modulated detector reconstruction, or exact scaled-row dependence",
    }


def verify_all() -> dict[str, object]:
    return {
        "exponents": exponent_ledger(),
        "no_loss_projection": no_loss_projection_check(),
        "markov": markov_check(),
        "asymptotic_alternatives": asymptotic_alternatives(),
    }
