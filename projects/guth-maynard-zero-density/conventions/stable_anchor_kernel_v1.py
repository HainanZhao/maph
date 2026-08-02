"""Exact stable-anchor prime-kernel conventions for Cycle 34."""
from fractions import Fraction


Q = Fraction


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def one_anchor_constants() -> dict[str, Fraction]:
    evaluation_floor = Q(3, 5)
    epsilon = Q(1, 20)
    gamma_upper = 1 + epsilon
    kernel_lower = (evaluation_floor - epsilon) / gamma_upper
    coarse_lower = evaluation_floor / 2
    require(kernel_lower == Q(11, 21), "one-anchor exact lower mismatch")
    require(kernel_lower >= coarse_lower, "one-anchor coarse lower failed")
    return {
        "evaluation_floor": evaluation_floor,
        "epsilon": epsilon,
        "gamma_upper": gamma_upper,
        "kernel_lower": kernel_lower,
        "coarse_lower": coarse_lower,
    }


def multi_anchor_constants() -> dict[str, object]:
    coefficients = (Q(1, 2), Q(1, 3), Q(1, 6))
    l1_norm = sum((abs(value) for value in coefficients), Q(0))
    weighted_sum_lower = Q(3, 5)
    forced_kernel = weighted_sum_lower / l1_norm
    require(l1_norm == 1, "stable anchor l1 norm mismatch")
    require(forced_kernel == weighted_sum_lower, "stable anchor pigeonhole mismatch")
    return {
        "coefficients": coefficients,
        "l1_norm": l1_norm,
        "weighted_sum_lower": weighted_sum_lower,
        "forced_kernel": forced_kernel,
        "colour_cost": "|A|=X^o(1)",
    }


def exponent_ledger() -> dict[str, Fraction | str]:
    prime_mass = Q(1)
    rho = Q(-3, 5)
    normalized_kernel = rho / 2
    unnormalized_kernel = prime_mass + normalized_kernel
    generic_skeleton = Q(1)
    target_skeleton = Q(21, 25)
    missing_saving = generic_skeleton - target_skeleton
    require(normalized_kernel == Q(-3, 10), "normalized kernel exponent mismatch")
    require(unnormalized_kernel == Q(7, 10), "unnormalized kernel exponent mismatch")
    require(missing_saving == Q(4, 25), "stable-anchor saving mismatch")
    return {
        "prime_mass": prime_mass,
        "rho": rho,
        "normalized_kernel": normalized_kernel,
        "unnormalized_kernel": unnormalized_kernel,
        "separation": Q(3, 5),
        "height": Q(12, 5),
        "generic_skeleton": generic_skeleton,
        "target_skeleton": target_skeleton,
        "missing_saving": missing_saving,
        "target_statement": "unweighted prime-kernel large-value count <=X^(21/25+o(1))",
    }


def verify_all() -> dict[str, object]:
    return {
        "one_anchor": one_anchor_constants(),
        "multi_anchor": multi_anchor_constants(),
        "exponents": exponent_ledger(),
        "kernel_identity": "H(t,a)=M^(-1)K(t-a)",
    }
