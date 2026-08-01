"""Exact continuum-frame and prime-discrepancy conventions, Cycle 21."""
from fractions import Fraction


Q = Fraction


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def harmonic(n: int) -> Fraction:
    return sum((Q(1, j) for j in range(1, n + 1)), Q(0))


def critical_exponents() -> dict[str, Fraction | str]:
    skeleton = Q(21, 25)
    separation = Q(3, 5)
    rho = Q(-3, 5)
    color_loss = Q(0)  # L=(log X)^2 is subpower.
    colored_rows = skeleton - color_loss
    colored_separation = separation + color_loss
    continuum_error = -colored_separation
    volume_scale = colored_rows + rho
    require(continuum_error == rho, "continuum row-sum power mismatch")
    require(volume_scale == Q(6, 25), "colored volume scale mismatch")
    return {
        "skeleton_rows": skeleton,
        "base_separation": separation,
        "color_loss": color_loss,
        "colored_rows": colored_rows,
        "colored_separation": colored_separation,
        "rho": rho,
        "continuum_error_power": continuum_error,
        "continuum_log_improvement": "1/log X",
        "volume_collapse_scale": volume_scale,
        "required_prime_operator_discrepancy": "o(X^(-3/5))",
    }


def finite_frame_check() -> dict[str, Fraction | int]:
    B = Q(1)
    k = 5
    separation = Q(100)
    harmonic_number = harmonic(k - 1)
    epsilon = 4 * harmonic_number / (B * separation)
    eta = Q(1, 12)
    total_error = epsilon + eta
    determinant_lower = (1 - total_error) ** k
    require(harmonic_number == Q(25, 12), "harmonic number mismatch")
    require(epsilon == Q(1, 12), "row-sum bound mismatch")
    require(total_error == Q(1, 6), "total perturbation mismatch")
    require(total_error < Q(1, 2), "finite model misses logarithmic lower-bound regime")
    return {
        "B": B,
        "k": k,
        "separation": separation,
        "harmonic_number": harmonic_number,
        "continuum_row_sum": epsilon,
        "prime_operator_discrepancy": eta,
        "total_error": total_error,
        "determinant_lower_factor": determinant_lower,
    }


def verify_all() -> dict[str, object]:
    return {
        "critical_exponents": critical_exponents(),
        "finite_frame_check": finite_frame_check(),
        "kernel_bound": "|B^-1 integral_0^B exp(-ihy)dy| <= 2/(B|h|)",
        "gershgorin_bound": "epsilon <= 4H_(k-1)/(B Delta)",
        "perturbed_determinant": "det(H_P)>=(1-epsilon-eta)^k",
        "conditional_bridge": "eta=o(X^(-3/5)) gives log det(H_P)=-o(kX^(-3/5)) and contradicts Cycle 20",
    }
