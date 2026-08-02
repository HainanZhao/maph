"""Exact rank-J residual spectral-shift conventions for Cycle 28."""
from fractions import Fraction


Q = Fraction


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def determinant_example() -> dict[str, object]:
    # B=I_2, S=diag(1,2), L=S* S=diag(1,4).
    B_det = Q(1)
    L_diagonal = (Q(1), Q(4))
    det_identity_plus_L = (1 + L_diagonal[0]) * (1 + L_diagonal[1])
    D_squared = (Q(1, 2), Q(1, 5))
    D_product = D_squared[0] * D_squared[1]
    H_diagonal = (
        D_squared[0] * (1 + L_diagonal[0]),
        D_squared[1] * (1 + L_diagonal[1]),
    )
    H_det = H_diagonal[0] * H_diagonal[1]
    require(det_identity_plus_L == 10, "finite leverage determinant mismatch")
    require(H_diagonal == (Q(1), Q(1)), "finite normalized Gram diagonal mismatch")
    require(H_det / B_det == D_product * det_identity_plus_L, "rank-J determinant identity mismatch")
    return {
        "B_det": B_det,
        "L_diagonal": L_diagonal,
        "det_I_plus_L": det_identity_plus_L,
        "D_squared": D_squared,
        "D_product": D_product,
        "H_diagonal": H_diagonal,
        "H_det": H_det,
    }


def reconstruction_example() -> dict[str, object]:
    top_eigenvalue = Q(4)
    y = (Q(0), Q(1))
    c = (Q(0), Q(2))
    c_star_S = (Q(0), Q(4))
    residual_norm_squared = c[0] ** 2 + c[1] ** 2
    error_squared = residual_norm_squared / top_eigenvalue**2
    require(c_star_S == tuple(top_eigenvalue * entry for entry in y), "top-direction reconstruction mismatch")
    require(residual_norm_squared == top_eigenvalue, "rank-J residual norm mismatch")
    require(error_squared == Q(1, 4), "rank-J reconstruction error mismatch")
    return {
        "top_eigenvalue": top_eigenvalue,
        "y": y,
        "c": c,
        "c_star_S": c_star_S,
        "residual_norm_squared": residual_norm_squared,
        "error_squared": error_squared,
    }


def singular_examples() -> dict[str, object]:
    # B=diag(1,0), null vector c=(0,1).
    null_vector = (Q(0), Q(1))
    reconstructing_c_star_S = (Q(0), Q(2))
    annihilating_c_star_S = (Q(0), Q(0))
    require(any(reconstructing_c_star_S), "singular reconstruction example vanished")
    require(not any(annihilating_c_star_S), "singular annihilation example nonzero")
    return {
        "B_diagonal": (Q(1), Q(0)),
        "null_vector": null_vector,
        "reconstructing_c_star_S": reconstructing_c_star_S,
        "annihilating_c_star_S": annihilating_c_star_S,
    }


def critical_ledger() -> dict[str, Fraction | str]:
    rows = Q(21, 25)
    base_rho = Q(-3, 5)
    base_shift = rows + base_rho
    frame_rho_constant = Q(1, 16)
    negative_shift_constant = frame_rho_constant / 2
    reconstruction_constant = frame_rho_constant / 4
    require(base_shift == Q(6, 25), "critical rank-J scale mismatch")
    require(negative_shift_constant == Q(1, 32), "negative-shift constant mismatch")
    require(reconstruction_constant == Q(1, 64), "reconstruction constant mismatch")
    return {
        "rows": rows,
        "base_rho": base_rho,
        "k_rho": base_shift,
        "frame_rho": "rho/(16J^2)",
        "K_lower": "k rho/(16J^2)",
        "negative_shift_lower": "k rho/(32J^2)",
        "reconstruction_error_upper": "sqrt(2) exp(-k rho/(64J^3))",
        "frame_rho_constant": frame_rho_constant,
        "negative_shift_constant": negative_shift_constant,
        "reconstruction_constant": reconstruction_constant,
        "subpower_dimension": "J=X^o(1)",
        "retained_exponential_scale": "X^(6/25-o(1))",
    }


def verify_all() -> dict[str, object]:
    return {
        "determinant_example": determinant_example(),
        "reconstruction_example": reconstruction_example(),
        "singular_examples": singular_examples(),
        "critical_ledger": critical_ledger(),
        "determinant_identity": "det(XX*)/det(B)=product(1-rho_t) det(I_J+S*B^(-1)S)",
        "singular_identity": "c in ker(B) implies c*D^(-1)X=(c*S)E*",
    }
