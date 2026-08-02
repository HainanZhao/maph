"""Corrected weighted continuum-frame conventions, Cycle 21 v2."""
from fractions import Fraction


Q = Fraction


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def harmonic(n: int) -> Fraction:
    return sum((Q(1, j) for j in range(1, n + 1)), Q(0))


def critical_exponents() -> dict[str, Fraction | str]:
    rows = Q(21, 25)
    separation = Q(3, 5)
    rho = Q(-3, 5)
    volume = rows + rho
    require(volume == Q(6, 25), "corrected volume exponent mismatch")
    return {
        "rows": rows,
        "separation": separation,
        "rho": rho,
        "weighted_continuum_error_power": -separation,
        "weighted_continuum_log_improvement": "1/log X",
        "volume_collapse_scale": volume,
        "required_prime_operator_discrepancy": "o(X^(-3/5))",
    }


def finite_weighted_check() -> dict[str, Fraction | int | str]:
    k = 5
    separation = Q(100)
    harmonic_number = harmonic(k - 1)
    kernel_numerator_bound = Q(3)
    row_sum = 2 * kernel_numerator_bound * harmonic_number / separation
    eta = Q(1, 8)
    total_error = row_sum + eta
    determinant_lower = (1 - total_error) ** k
    require(row_sum == Q(1, 8), "weighted row-sum constant mismatch")
    require(total_error == Q(1, 4), "weighted perturbation mismatch")
    require(total_error < Q(1, 2), "weighted finite model misses perturbative regime")
    return {
        "k": k,
        "separation": separation,
        "harmonic_number": harmonic_number,
        "kernel_numerator_bound": kernel_numerator_bound,
        "weighted_row_sum": row_sum,
        "prime_operator_discrepancy": eta,
        "total_error": total_error,
        "determinant_lower_factor": determinant_lower,
        "reference_measure": "e^y dy on [0,log 2]",
    }


def verify_all() -> dict[str, object]:
    return {
        "critical_exponents": critical_exponents(),
        "finite_weighted_check": finite_weighted_check(),
        "corrected_kernel": "H_nu(h)=(2^(1-ih)-1)/(1-ih)",
        "corrected_kernel_bound": "|H_nu(h)|<=3/|h|",
        "corrected_gershgorin_bound": "epsilon_nu<=6H_(k-1)/Delta",
        "correction_scope": "v1 uniform-frame theorem remains valid; its reference measure is superseded for prime comparison",
    }
