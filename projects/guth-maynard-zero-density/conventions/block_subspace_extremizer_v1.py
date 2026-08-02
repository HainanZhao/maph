"""Exact block-subspace saturation conventions for Cycle 30."""
from fractions import Fraction


Q = Fraction


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def finite_extremizer() -> dict[str, Fraction | int | str]:
    k = 4
    rho = Q(1, 4)
    one_minus_rho = 1 - rho
    leverage_target = one_minus_rho ** (-k) - 1
    epsilon = k * rho / (one_minus_rho * leverage_target)
    residual_off_diagonal = (epsilon - 1) / (k - 1)
    full_gram_off_diagonal = rho + one_minus_rho * residual_off_diagonal
    residual_other_eigenvalue = (k - epsilon) / (k - 1)
    leverage = rho / one_minus_rho * k / epsilon
    determinant_ratio = one_minus_rho**k * (1 + leverage)
    reconstruction_error_squared = 1 / leverage
    require(leverage_target == Q(175, 81), "finite leverage target mismatch")
    require(epsilon == Q(108, 175), "finite residual eigenvalue mismatch")
    require(residual_off_diagonal == Q(-67, 525), "finite residual off-diagonal mismatch")
    require(full_gram_off_diagonal == Q(27, 175), "finite full Gram off-diagonal mismatch")
    require(leverage == leverage_target, "finite inverse leverage mismatch")
    require(determinant_ratio == 1, "finite determinant shift did not cancel")
    require(0 < epsilon < 1 < residual_other_eigenvalue, "finite residual spectrum invalid")
    return {
        "k": k,
        "rho": rho,
        "one_minus_rho": one_minus_rho,
        "L_target": leverage_target,
        "epsilon": epsilon,
        "residual_off_diagonal": residual_off_diagonal,
        "residual_other_eigenvalue": residual_other_eigenvalue,
        "full_gram_off_diagonal": full_gram_off_diagonal,
        "leverage": leverage,
        "multiplicative_determinant_ratio": determinant_ratio,
        "reconstruction_error_squared": reconstruction_error_squared,
    }


def block_synchronization_check() -> dict[str, object]:
    J = 4
    # The detector block contribution is represented after dividing by
    # sqrt(rho): every block is 1/J, while nontrivial Hadamard sums vanish.
    contributions = (Q(1, J),) * J
    hadamard = (
        (1, 1, 1, 1),
        (1, -1, 1, -1),
        (1, 1, -1, -1),
        (1, -1, -1, 1),
    )
    signed = tuple(sum(row[j] * contributions[j] for j in range(J)) for row in hadamard)
    require(signed == (Q(1), Q(0), Q(0), Q(0)), "block synchronization mismatch")
    return {
        "J": J,
        "contributions_divided_by_sqrt_rho": contributions,
        "signed_values_divided_by_sqrt_rho": signed,
        "nontrivial_hadamard_values": signed[1:],
    }


def critical_exponents() -> dict[str, Fraction | str]:
    rows = Q(21, 25)
    rho = Q(-3, 5)
    detector_dimension = Q(1, 25)
    k_rho = rows + rho
    k_rho_squared = rows + 2 * rho
    require(k_rho == Q(6, 25), "critical extremizer scale mismatch")
    require(k_rho_squared == Q(-9, 25), "quadratic correction scale mismatch")
    return {
        "rows": rows,
        "rho": rho,
        "detector_dimension": detector_dimension,
        "k_rho": k_rho,
        "k_rho_squared": k_rho_squared,
        "epsilon": "exp(-X^(6/25+o(1)))",
        "reconstruction_error": "exp(-X^(6/25+o(1))/2)",
        "label_spacing": "arbitrary, including X^(3/5)",
    }


def verify_all() -> dict[str, object]:
    return {
        "finite_extremizer": finite_extremizer(),
        "block_synchronization": block_synchronization_check(),
        "critical_exponents": critical_exponents(),
        "construction": "x_t=sqrt(rho)b+sqrt(1-rho)r_t with Gram(r)=B_epsilon",
        "scope": "arbitrary Hilbert rows and separated labels; actual prime phase curve excluded",
    }
