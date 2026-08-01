"""Pinned exact bookkeeping for the CRR row-deletion inverse reduction.

This module records finite algebra and frozen-scale arithmetic only.  It does
not assert that RationalMass controls a row-deletion statistic or that an
actual CRR witness exists.
"""
from __future__ import annotations

from fractions import Fraction


MIN_V = 8
SCALE_EXPONENTS = {
    "local_height_H": 12,
    "polynomial_length_L": 10,
    "cardinality_R": 8,
    "rational_height_Q": 4,
}


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def scales(v: int) -> dict[str, int]:
    """Return frozen scales used by the deletion/Gram reduction."""
    require(isinstance(v, int) and v >= MIN_V, "v must be an integer at least 8")
    result = {
        "v": v,
        "H": v**SCALE_EXPONENTS["local_height_H"],
        "L": v**SCALE_EXPONENTS["polynomial_length_L"],
        "R": v**SCALE_EXPONENTS["cardinality_R"],
        "Q": v**SCALE_EXPONENTS["rational_height_Q"],
    }
    require(result["H"] == result["Q"] ** 3, "H=Q^3 mismatch")
    require(result["R"] == result["Q"] ** 2, "R=Q^2 mismatch")
    return result


def plateau_l2_bounds(v: int = MIN_V) -> dict[str, Fraction | int | str]:
    """Return exact L2-mass bounds from the frozen plateau of w.

    The source/conventions fix ``0<=w<=1`` and ``w=1`` on [6/5,9/5].
    The number of integers in that interval is at least 3L/5-1, which is at
    least L/2 at every frozen v.
    """
    data = scales(v)
    L = data["L"]
    plateau_integer_lower = Fraction(3 * L, 5) - 1
    require(plateau_integer_lower >= Fraction(L, 2), "plateau lower count must dominate L/2")
    return {
        "L": L,
        "weight_range": "0<=w<=1 on L<n<2L",
        "plateau": "w=1 on [6/5,9/5]",
        "plateau_integer_count_lower": plateau_integer_lower,
        "gram_diagonal_S_lower": Fraction(L, 2),
        "gram_diagonal_S_upper": Fraction(L),
        "derivation": "S_L=sum_(L<n<2L)w(n/L)^2; plateau gives S_L>=3L/5-1>=L/2",
    }


def deletion_rows() -> dict[str, str]:
    """Return the exact row-deletion and phase-projection statements."""
    rows = {
        "deletion_deficit": "d_t=lambda-lambda_max(G_(W minus {t}))",
        "off_row_correlation": "beta_t=||G_(W minus {t},t)||_2",
        "coordinate_lower": "|u_t|^2>=d_t^2/(d_t^2+beta_t^2), with 0/0 interpreted as 0",
        "deletion_coverage": "DelCov(W)=|W|*min_t d_t^2/(d_t^2+beta_t^2)<=mu_top(W)",
        "phase_projection": "chi_ph^2<=eta_ph*max_t(G_tt/(lambda|u_t|^2)-1)",
        "actual_constant_diagonal": "G_tt=S_L for M_W(t,n)=w(n/L)n^(it)",
        "combined_projection": "chi_ph^2<=eta_ph*(|W|*S_L/(lambda*DelCov(W))-1) when DelCov(W)>0",
        "closure": "DelCov>=v^(-2*s*delta), combined_projection<=kappa^2, and ell+r+2*s<=2-gamma imply the prior all-row gate",
    }
    require(rows["coordinate_lower"] == "|u_t|^2>=d_t^2/(d_t^2+beta_t^2), with 0/0 interpreted as 0", "deletion row mismatch")
    return rows


def rank_one_sharpness() -> dict[str, Fraction | int | list[Fraction] | str]:
    """Return a rational rank-one example where the deletion bound is equal."""
    coordinates = [Fraction(1), Fraction(2), Fraction(3)]
    squares = [value * value for value in coordinates]
    lam = sum(squares, Fraction())
    ratios = []
    for square in squares:
        d = square
        beta_square = square * (lam - square)
        ratios.append(d * d / (d * d + beta_square))
    require(ratios == [square / lam for square in squares], "rank-one deletion equality mismatch")
    return {
        "coordinates": coordinates,
        "lambda": lam,
        "coordinate_squares": [square / lam for square in squares],
        "deletion_lower_bounds": ratios,
        "minimum_top_leverage": Fraction(3) * min(ratios),
        "statement": "For G=a a^*, d_t=|a_t|^2 and beta_t^2=|a_t|^2(lambda-|a_t|^2), so the deletion lower bound is exact.",
    }


def cancellation_projection_calibration() -> dict[str, Fraction | str]:
    """Return exact equality data for the phase-cancellation model.

    These values are inherited algebraically from the two-row countermodel in
    the preceding phase-flatness reduction and show that the projection bound
    can be sharp.
    """
    eta = Fraction(243, 169)
    row_diagonal = Fraction(206, 243)
    rows = Fraction(2)
    lam = Fraction(1)
    mu_top = Fraction(1)
    projection_factor = rows * row_diagonal / (lam * mu_top) - 1
    require(eta * projection_factor == 1, "cancellation projection equality mismatch")
    return {
        "eta_ph": eta,
        "row_diagonal_S": row_diagonal,
        "rows": rows,
        "lambda": lam,
        "mu_top": mu_top,
        "projection_factor": projection_factor,
        "chi_ph_square": Fraction(1),
        "statement": "eta_ph*(m*S/(lambda*mu_top)-1)=chi_ph^2=1 in the exact cancellation family.",
    }


def farey_deletion_rows() -> dict[str, str]:
    """Return exact identities for the actual-Farey deletion bookkeeping."""
    rows = {
        "kernel": "(K_F)_(t,t')=sum_(a in F_Q) integral_(-3)^3 (a*exp(theta/H))^(i(t-t')) dtheta",
        "mass": "Mcal_v(W)=1^*K_F*1",
        "deletion": "Delta_F(t)=Mcal_v(W)-Mcal_v(W minus {t})=(K_F)_(t,t)+2*Re sum_(s!=t)(K_F)_(t,s)",
        "sum": "sum_t Delta_F(t)=2*Mcal_v(W)-tr(K_F)",
        "trace": "tr(K_F)=6*|W|*|F_Q|",
        "rationalmass_average": "RationalMass gives Mcal_v(W)>=(75/2)*H*v^(8-3*delta), hence average Delta_F>=75*v^(12-3*delta)-6*v^8",
    }
    require(rows["trace"] == "tr(K_F)=6*|W|*|F_Q|", "Farey trace row mismatch")
    return rows


def verify_all(v: int = MIN_V) -> dict[str, object]:
    """Run all exact checks used by the sealing builder."""
    data = scales(v)
    plateau = plateau_l2_bounds(v)
    deletion = deletion_rows()
    rank_one = rank_one_sharpness()
    cancellation = cancellation_projection_calibration()
    farey = farey_deletion_rows()
    require(data["R"] * plateau["gram_diagonal_S_lower"] == Fraction(v**18, 2), "central RS lower scale mismatch")
    require(rank_one["minimum_top_leverage"] == Fraction(3, 14), "rank-one leverage mismatch")
    require(cancellation["chi_ph_square"] == Fraction(1), "cancellation chi mismatch")
    return {
        "scales": data,
        "plateau_l2_bounds": plateau,
        "deletion_rows": deletion,
        "rank_one_sharpness": rank_one,
        "cancellation_projection_calibration": cancellation,
        "farey_deletion_rows": farey,
    }
