"""Pinned bookkeeping for the versioned RFDI outlier-surgery correction.

This is a self-contained v2 re-seal of the conditional actual-log/Farey
theorem. It records exact scale rows only; it does not assert that the
conditional surplus core exists or that RFDI is false.
"""
from __future__ import annotations

from fractions import Fraction


MIN_V = 64


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def scales(v: int = MIN_V) -> dict[str, int]:
    """Return the frozen central scales used in the repaired replay."""
    require(isinstance(v, int) and v >= MIN_V, "v must be an integer at least 64")
    result = {"v": v, "H": v**12, "L": v**10, "R": v**8, "Q": v**4}
    require(result["H"] == result["Q"] ** 3, "H=Q^3 mismatch")
    require(result["R"] == result["Q"] ** 2, "R=Q^2 mismatch")
    require(result["L"] ** 2 == result["R"] * result["H"], "L^2=RH mismatch")
    return result


def preservation_rows() -> dict[str, str]:
    """Return the scalar and RationalMass rows retained by surgery."""
    rows = {
        "windows": "A subset [0,H/4], tau in [3H/4,H], so pair-sum classes are more than one apart and Base separation is retained",
        "energy": "For |A|=R-1 and unit-separated A, E(A union {tau})=E(A)+4R-3",
        "rational_threshold": "T_v=v^(12-2*delta(v))",
        "smoothing_mass": "0<=psi1,psi2<=1 and supp(psi1) subset [-1,1] imply J(u)<=2",
        "rational_stability": "F_(A union {tau})(u)>=F_A(u)-2sqrt(2F_A(u))",
        "surplus_transfer": "F_A>=(1+epsilon)T_v and T_v>=max(2,8(1+epsilon)/epsilon^2) imply F_(A union {tau})>=T_v",
        "farey": "The actual K_F feature kernel and C_theta(sk,rk)=R_W((r/s)*exp(theta/H)) use the same enlarged W",
    }
    require(rows["energy"] == "For |A|=R-1 and unit-separated A, E(A union {tau})=E(A)+4R-3", "energy row mismatch")
    return rows


def selection_rows() -> dict[str, str]:
    """Return the elementary actual-log selection and block rows."""
    rows = {
        "actual_coupling": "f(tau)=u_A^*G_(A,tau)=sqrt(Lambda)sum_(L<n<2L) conjugate(x_n)w(n/L)n^(-i*tau), with sum|x_n w(n/L)|^2<=1",
        "mean_value": "On I=[3H/4,H], average_I |D_c|^2<=C_v:=1+32L(1+log L)/H",
        "large_v_mean_value": "C_v<=2 for v>=64, from log(v)<=sqrt(v) and L/H=v^(-2)",
        "core_gap": "lambda_2(G_A)<=(1-g)Lambda and S_L+sqrt(Lambda*S_L)<=gLambda/2 imply ||B||<=Lambda-gLambda/2",
        "top_coordinate": "|u_W(tau)|^2<=4C_v/(g^2Lambda) for every unit top eigenvector of G_W",
        "deletion": "DelCov(W)<=mu_top(W)<=4RC_v/(g^2Lambda)",
        "central": "Lambda>=v^(12-ell*delta(v)) and v>=64 give DelCov(W)<=8g^(-2)v^(-4+ell*delta(v))",
        "failure": "For fixed g,ell,r,s with ell+r+2s<2, the central bound is <v^(-2s*delta(v)) for all sufficiently large v",
    }
    require(rows["top_coordinate"] == "|u_W(tau)|^2<=4C_v/(g^2Lambda) for every unit top eigenvector of G_W", "top-coordinate row mismatch")
    return rows


def correction_rows() -> dict[str, str]:
    """Return the fixed scope of the v1-to-v2 correction."""
    rows = {
        "v1_artifact": "0bd2843123957ed045b1feae389467030066f572f65914032955fc4cb90bc351",
        "cause": "After v1 sealing, its convention, document, and builder were edited to clarify normalized-bump use and the ell+r+2s budget; v1 artifact bytes were not overwritten.",
        "effect": "The changed v1 inputs no longer match v1's frozen hashes, so v1 --check correctly rejects them. The underlying conditional theorem is re-sealed independently here.",
        "remedy": "v2 has its own convention, document, builder, tests, artifact, and a pinned mutation ledger; it does not rewrite the v1 artifact.",
    }
    require(len(rows["v1_artifact"]) == 64, "v1 correction hash length mismatch")
    return rows


def verify_all(v: int = MIN_V) -> dict[str, object]:
    """Run the exact finite bookkeeping checks used by the v2 builder."""
    data = scales(v)
    preservation = preservation_rows()
    selection = selection_rows()
    correction = correction_rows()
    coarse_tail_at_64 = Fraction(32, 64**2) + Fraction(320, 8**3)
    require(coarse_tail_at_64 == Fraction(81, 128), "mean-value tail mismatch")
    require(1 + coarse_tail_at_64 < 2, "mean-value constant mismatch")
    require(4 * data["R"] - 3 > 0, "energy increment must be positive")
    require(Fraction(data["H"], 4) > 1, "pair-sum window gap mismatch")
    return {
        "scales": data,
        "preservation_rows": preservation,
        "selection_rows": selection,
        "correction_rows": correction,
        "large_v_mean_value_coarse_tail_at_v64": coarse_tail_at_64,
    }
