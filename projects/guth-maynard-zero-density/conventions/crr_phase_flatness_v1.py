"""Pinned exact bookkeeping for the CRR all-row phase-flatness gate.

The accompanying note proves finite-dimensional statements. This module
records only exact scale rows and rational countermodel bounds; it does not
assert that the displayed matrices arise from a Dirichlet polynomial or that
an actual CRR set has the required row statistics.
"""
from __future__ import annotations

from fractions import Fraction


MIN_V = 8
SCALE_EXPONENTS = {
    "local_height_H": 12,
    "polynomial_length_L": 10,
    "cardinality_R": 8,
    "large_value_V": 7,
}


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def scales(v: int) -> dict[str, int]:
    """Return the frozen central scales used by the phase-flatness gate."""
    require(isinstance(v, int) and v >= MIN_V, "v must be an integer at least 8")
    result = {
        "v": v,
        "H": v**SCALE_EXPONENTS["local_height_H"],
        "L": v**SCALE_EXPONENTS["polynomial_length_L"],
        "R": v**SCALE_EXPONENTS["cardinality_R"],
        "V": v**SCALE_EXPONENTS["large_value_V"],
    }
    require(result["L"] * result["H"] == result["R"] * result["V"] ** 2, "critical scale mismatch")
    return result


def phase_flatness_rows() -> dict[str, str]:
    """Return the exact affine-in-delta closure rows.

    ``mu_top`` is the square of the usable phase-flatness lower bound, up to
    a fixed factor depending only on the relative phase-leakage cap kappa.
    """
    rows = {
        "top_eigenvalue": "lambda>=v^(12-ell*delta)",
        "right_delocalization": "rho>=v^(-r*delta)",
        "minimum_top_leverage": "mu_top>=v^(-2*s*delta)",
        "relative_phase_leakage": "chi_ph<=kappa<1",
        "derived_flatness": "phi>=((1-kappa)/sqrt(1+kappa^2))*sqrt(mu_top)",
        "strict_closure": "ell+r+2*s<=2-gamma for fixed gamma>0",
        "conclusion": "Gamma(W)>=v^(7-delta(v)) for all sufficiently large v",
    }
    require(rows["strict_closure"] == "ell+r+2*s<=2-gamma for fixed gamma>0", "closure row mismatch")
    return rows


def block_countermodel_bounds(
    m: int = 101,
    tau: Fraction = Fraction(1, 100),
    epsilon: Fraction = Fraction(1, 100),
) -> dict[str, Fraction | int | str]:
    """Return exact bounds for the full-rank equal-diagonal block family.

    With n=m-1, start from ``J_n direct_sum [1]`` with cross block
    ``tau*1_n`` and regularize by ``epsilon*I``. The displayed quantities
    bound the top-eigenvector coordinate ratio d and hence phi^2. No square
    root is evaluated here.
    """
    require(isinstance(m, int) and m >= 3, "m must be an integer at least 3")
    require(isinstance(tau, Fraction) and 0 < tau < 1, "tau must lie in (0,1)")
    require(isinstance(epsilon, Fraction) and epsilon > 0, "epsilon must be positive")
    n = m - 1
    require(tau < Fraction(n - 1, n), "tau must make the last top coordinate minimal")
    d_square_upper = Fraction(n) * tau * tau / Fraction((n - 1) ** 2)
    phi_square_upper = Fraction(m) * d_square_upper
    left_participation_lower = Fraction(n, m) / (1 + d_square_upper)
    lambda_lower = Fraction(n, 1) / (1 + epsilon)
    require(phi_square_upper > 0, "countermodel flatness bound must be positive")
    require(left_participation_lower < 1, "participation lower bound must be nontrivial")
    return {
        "m": m,
        "n": n,
        "tau": tau,
        "epsilon": epsilon,
        "lambda_top_lower": lambda_lower,
        "right_rho": Fraction(1),
        "row_diagonal": Fraction(1),
        "top_coordinate_ratio_square_upper": d_square_upper,
        "phi_square_upper": phi_square_upper,
        "left_l1_participation_lower": left_participation_lower,
        "relative_phase_leakage": Fraction(0),
        "scope": "abstract finite matrix only; not asserted to be a Dirichlet measurement matrix",
    }


def cancellation_countermodel() -> dict[str, Fraction | int | str]:
    """Return exact data for a two-row cancellation countermodel.

    The top left singular vector is perfectly flat and the Gram diagonal is
    constant, but the phase-rounded top direction cancels one output row.
    """
    rho = Fraction(169, 412)
    second_ratio = Fraction(169, 243)
    row_diagonal = (1 + second_ratio) / 2
    require(0 < second_ratio < 1, "top eigenvalue must be simple")
    require(rho < Fraction(1, 2), "cancellation construction requires rho below one half")
    return {
        "rows_m": 2,
        "columns_N": 4,
        "lambda_top": Fraction(1),
        "lambda_second": second_ratio,
        "spectral_gap": 1 - second_ratio,
        "right_rho": rho,
        "minimum_top_leverage": Fraction(1),
        "row_diagonal": row_diagonal,
        "relative_phase_leakage": Fraction(1),
        "phi_square": Fraction(0),
        "scope": "abstract finite matrix only; not asserted to be a Dirichlet measurement matrix",
    }


def verify_all(v: int = MIN_V) -> dict[str, object]:
    """Run all exact checks used by the sealing builder."""
    central = scales(v)
    rows = phase_flatness_rows()
    block = block_countermodel_bounds()
    cancellation = cancellation_countermodel()
    require(central["L"] - 1 >= central["L"] // 2, "support factor mismatch")
    require(block["phi_square_upper"] == Fraction(101, 980100), "block phi bound mismatch")
    require(block["left_l1_participation_lower"] == Fraction(98010000, 98990201), "block participation mismatch")
    require(cancellation["spectral_gap"] == Fraction(74, 243), "cancellation gap mismatch")
    require(cancellation["row_diagonal"] == Fraction(206, 243), "cancellation row diagonal mismatch")
    return {
        "scales": central,
        "phase_flatness_rows": rows,
        "block_countermodel": block,
        "cancellation_countermodel": cancellation,
    }
