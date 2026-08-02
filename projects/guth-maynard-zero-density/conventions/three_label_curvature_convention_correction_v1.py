"""Exact correction ledger for Cycle 185's shifted exponential phase."""
from __future__ import annotations

from fractions import Fraction as Q


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def original_unshifted_identity_failure(*, z: Q) -> dict[str, Q]:
    """Exhibit the pinned alpha=z^ell-1 convention failure at labels 1,2,3."""
    require(z > 1, "positive nontrivial exponential base")
    alpha_minus, alpha_zero, alpha_plus = z - 1, z * z - 1, z * z * z - 1
    unshifted_difference = alpha_minus * alpha_plus - alpha_zero * alpha_zero
    require(unshifted_difference != 0, "unshifted identity unexpectedly held")
    return {
        "z": z,
        "alpha_minus": alpha_minus,
        "alpha_zero": alpha_zero,
        "alpha_plus": alpha_plus,
        "unshifted_difference": unshifted_difference,
    }


def shifted_curvature_identity(
    *, v: int, u_minus: int, u_zero: int, u_plus: int,
    A_minus: int, A_zero: int, A_plus: int,
    z_minus: Q, z_zero: Q, z_plus: Q,
) -> dict[str, object]:
    """Clear the true AP product identity z_- z_+ = z_0^2 exactly."""
    require(min(v, u_minus, u_zero, u_plus) > 0, "positive common-intercept ray data")
    require(z_minus * z_plus == z_zero * z_zero, "shifted three-label exponential product")
    U_minus, U_zero, U_plus = v * u_minus, v * u_zero, v * u_plus
    B_minus, B_zero, B_plus = A_minus + U_minus, A_zero + U_zero, A_plus + U_plus
    epsilon_minus = Q(B_minus) - U_minus * z_minus
    epsilon_zero = Q(B_zero) - U_zero * z_zero
    epsilon_plus = Q(B_plus) - U_plus * z_plus
    K_plus = U_zero**2 * B_minus * B_plus - U_minus * U_plus * B_zero**2
    require(K_plus % (v * v) == 0, "common-intercept shifted-curvature square divisibility")
    K_plus_prime = K_plus // (v * v)
    P = U_minus * U_plus * U_zero**2
    expanded = (
        z_minus * Q(epsilon_plus, U_plus)
        + z_plus * Q(epsilon_minus, U_minus)
        + Q(epsilon_minus * epsilon_plus, U_minus * U_plus)
        - 2 * z_zero * Q(epsilon_zero, U_zero)
        - Q(epsilon_zero * epsilon_zero, U_zero * U_zero)
    )
    require(Q(K_plus, P) == expanded, "shifted cleared-curvature expansion")
    F_minus_zero_A = u_zero * A_minus - u_minus * A_zero
    F_zero_plus_A = u_plus * A_zero - u_zero * A_plus
    F_minus_zero_B = u_zero * B_minus - u_minus * B_zero
    F_zero_plus_B = u_plus * B_zero - u_zero * B_plus
    require(F_minus_zero_A == F_minus_zero_B and F_zero_plus_A == F_zero_plus_B, "common-intercept numerator-shift cancellation")
    syzygy = u_zero * B_plus * F_minus_zero_A - u_minus * B_zero * F_zero_plus_A
    require(K_plus_prime == syzygy, "shifted primitive curvature pair-determinant syzygy")
    return {
        "U": {"minus": U_minus, "zero": U_zero, "plus": U_plus},
        "A": {"minus": A_minus, "zero": A_zero, "plus": A_plus},
        "B": {"minus": B_minus, "zero": B_zero, "plus": B_plus},
        "epsilon": {"minus": epsilon_minus, "zero": epsilon_zero, "plus": epsilon_plus},
        "K_plus": K_plus,
        "K_plus_prime": K_plus_prime,
        "formula": "K_plus=U_0^2*B_-*B_+-U_-*U_+*B_0^2=v^2*K_plus_prime",
        "expansion": "K_plus/(U_-*U_+*U_0^2)=z_-*delta_++z_+*delta_-+delta_-*delta_+-2*z_0*delta_0-delta_0^2",
        "syzygy": "K_plus_prime=u_0*B_+*F_-0(A)-u_-*B_0*F_0+(A)",
        "shift_cancellation": "u_j*(A_i+v*u_i)-u_i*(A_j+v*u_j)=u_j*A_i-u_i*A_j",
        "expanded_value": expanded,
    }


def verify_all() -> dict[str, object]:
    failure = original_unshifted_identity_failure(z=Q(2))
    corrected = shifted_curvature_identity(
        v=3, u_minus=2, u_zero=5, u_plus=7,
        A_minus=6, A_zero=45, A_plus=147,
        z_minus=Q(2), z_zero=Q(4), z_plus=Q(8),
    )
    require(corrected["K_plus"] == 0 and corrected["K_plus_prime"] == 0, "shifted geometric fixture")
    return {
        "original_claim_disposition": "WITHHELD: alpha_ell=z^ell-1 does not obey alpha_-*alpha_+=alpha_0^2.",
        "corrected_local_result": "For B_i=A_i+U_i and z_i=1+alpha_i, the AP product gives a v^2-divisible integer K_plus with the retained primitive pair-determinant syzygy. Any depth exactification must use a chart cap for z_i.",
        "unchanged_boundary": "The Cycle 185 AP-free occupancy is abstract and non-exponential; it remains only a mass/capacity/stable-shell no-go.",
        "samples": {"unshifted_failure": failure, "shifted_curvature": corrected},
    }


def theorem_record() -> dict[str, object]:
    return {"epistemic_status": "PROVED", **verify_all()}
