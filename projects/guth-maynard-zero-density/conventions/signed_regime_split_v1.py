"""Exact Cycle 86 signed-regime exponent contracts."""

from fractions import Fraction

Q = Fraction

D_EXP = Q(3, 5)
Q_EXP = Q(1, 3)
ATOM_EXP = D_EXP + Q_EXP
SQRT_ATOM_EXP = ATOM_EXP / 2
UNSIGNED_CUTOFF = Q(16, 25)
MOMENT_CUTOFF = Q(58, 75)
FOURIER_CEILING = Q(83, 75)
RAW_L1_TARGET = Q(31, 25)


def signed_contract(xi: Fraction) -> dict[str, Fraction]:
    unsigned_block = xi + D_EXP
    diagonal_m2 = xi + ATOM_EXP
    cauchy_l1 = xi / 2 + diagonal_m2 / 2
    return {
        "xi": xi,
        "unsigned_block": unsigned_block,
        "required_saving_from_unsigned": unsigned_block - RAW_L1_TARGET,
        "diagonal_second_moment": diagonal_m2,
        "cauchy_l1": cauchy_l1,
        "average_allowance": RAW_L1_TARGET - xi,
        "sqrt_atom": SQRT_ATOM_EXP,
    }


def verify_all() -> dict[str, object]:
    assert ATOM_EXP == Q(14, 15)
    assert SQRT_ATOM_EXP == Q(7, 15)
    assert D_EXP - SQRT_ATOM_EXP == Q(2, 15)
    assert RAW_L1_TARGET - SQRT_ATOM_EXP == MOMENT_CUTOFF
    assert signed_contract(UNSIGNED_CUTOFF)["required_saving_from_unsigned"] == 0
    assert signed_contract(MOMENT_CUTOFF)["cauchy_l1"] == RAW_L1_TARGET
    assert signed_contract(FOURIER_CEILING)["average_allowance"] == Q(2, 15)
    assert MOMENT_CUTOFF - UNSIGNED_CUTOFF == Q(2, 15)
    assert FOURIER_CEILING - MOMENT_CUTOFF == Q(1, 3)
    return {
        "projector_zero_mode": "int_(R/Z)Theta_Q(x)dx=V(0)=0",
        "atom_exponent": str(ATOM_EXP),
        "square_root_exponent": str(SQRT_ATOM_EXP),
        "signed_saving_over_unsigned": str(D_EXP - SQRT_ATOM_EXP),
        "diagonal_second_moment": "sum_(k~K)|S_k|^2<=X^(xi+14/15+o(1))",
        "cauchy_block_exponent": "xi+7/15",
        "unsigned_boundary": str(UNSIGNED_CUTOFF),
        "moment_boundary": str(MOMENT_CUTOFF),
        "moment_regime": "16/25<=xi<58/75",
        "large_value_regime": "58/75<=xi<=83/75",
        "moment_endpoint": "xi=58/75 ties 31/25 and is not promoted",
        "ceiling_average_allowance": str(
            signed_contract(FOURIER_CEILING)["average_allowance"]
        ),
        "required_saving_formula": "xi-16/25 over unsigned volume",
        "gate": "prove diagonal-strength moment below 58/75 and sparse large values above",
    }


if __name__ == "__main__":
    print(verify_all())

