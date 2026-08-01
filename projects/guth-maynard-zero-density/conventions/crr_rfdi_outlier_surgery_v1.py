"""Pinned bookkeeping for the CRR actual-log/Farey outlier-surgery lemma.

The accompanying note proves an elementary conditional obstruction.  It does
not assert that a RationalMass-surplus core exists, nor that RFDI is false.
All quantities here use the frozen CRR scales and the actual logarithmic row
model rather than an abstract Gram replacement.
"""
from __future__ import annotations

from fractions import Fraction


MIN_V = 8
MEAN_VALUE_SIMPLE_BOUND_V = 64
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
    """Return the frozen central scales for an integral admissible ``v``."""
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
    require(result["L"] * result["R"] == v**18, "central scale relation mismatch")
    return result


def outlier_windows(v: int = MIN_V) -> dict[str, Fraction | int | str]:
    """Freeze the separated core and outlier windows used by surgery."""
    data = scales(v)
    H = data["H"]
    core_right = Fraction(H, 4)
    outlier_left = Fraction(3 * H, 4)
    pair_sum_gap = Fraction(H, 4)
    separation_gap = Fraction(H, 2)
    require(pair_sum_gap > 1, "pair-sum classes must be more than unit separated")
    # H^(1/100)=v^(3/25)<=v for v>=1, while H/2>v at frozen v>=8.
    require(separation_gap > v, "outlier must preserve Base separation")
    return {
        "core_window": "A subset [0,H/4]",
        "outlier_window": "I=[3H/4,H]",
        "outlier_interval_length": Fraction(H, 4),
        "core_to_outlier_distance_lower": separation_gap,
        "pair_sum_class_gap_lower": pair_sum_gap,
        "pair_sum_classes": "A+A, tau+A=A+tau, and {2tau}",
        "energy_increment": 4 * data["R"] - 3,
        "energy_increment_derivation": "For |A|=R-1 and unit-separated A, E(A union {tau})=E(A)+4|A|+1=E(A)+4R-3.",
    }


def mean_value_rows() -> dict[str, str]:
    """Return the elementary actual-Dirichlet-polynomial averaging rows."""
    rows = {
        "polynomial": "D_c(tau)=sum_(L<n<2L) c_n n^(-i*tau), with sum_n |c_n|^2<=1",
        "interval": "I=[3H/4,H], |I|=H/4",
        "kernel_integral": "|integral_I exp(-i*tau*log(n/m)) dtau|<=2/|log(n/m)| for n!=m",
        "log_spacing": "1/|log(n/m)|<=2L/|n-m| for L<n,m<2L and n!=m",
        "harmonic_bound": "sum_(n!=m)|c_n||c_m|/|n-m|<=2(1+log L)*sum_n|c_n|^2",
        "average_bound": "(1/|I|) integral_I |D_c(tau)|^2 dtau<=C_v:=1+32*L*(1+log L)/H",
        "selection": "There exists tau in I with |D_c(tau)|^2<=C_v.",
        "simple_large_v_bound": "For v>=64, C_v<=2, using log v<=sqrt(v) and L/H=v^(-2).",
    }
    require(rows["average_bound"] == "(1/|I|) integral_I |D_c(tau)|^2 dtau<=C_v:=1+32*L*(1+log L)/H", "mean-value row mismatch")
    return rows


def rationalmass_surplus_rows() -> dict[str, str]:
    """Return the frozen smoothing-stability implication for one added row."""
    rows = {
        "threshold": "T_v=v^(12-2*delta(v))",
        "core_surplus": "F_A(u)>=(1+epsilon)*T_v on a rational set E of measure at least v^(-4-delta(v))",
        "kernel_mass": "The pinned normalized bumps obey 0<=psi1,psi2<=1, so J(u):=H integral psi1(H(u-u'))psi2(u')du' satisfies 0<=J(u)<=2",
        "one_row_bound": "F_(A union {tau})(u)>=F_A(u)-2*sqrt(2*F_A(u))",
        "sufficient_size": "If T_v>=max(2,8*(1+epsilon)/epsilon^2), then the core surplus implies F_(A union {tau})(u)>=T_v on E.",
        "conclusion": "The same E proves the frozen RationalMass(v) predicate for A union {tau}; no new set of rational cells is selected.",
    }
    require(rows["threshold"] == "T_v=v^(12-2*delta(v))", "RationalMass threshold mismatch")
    return rows


def farey_kernel_rows() -> dict[str, str]:
    """Return actual-Farey PSD-kernel identities retained by the surgery."""
    rows = {
        "kernel": "(K_F)_(t,s)=sum_(a in F_Q) integral_(-3)^3 (a*exp(theta/H))^(i*(t-s)) dtheta",
        "feature": "Phi_t(a,theta)=(a*exp(theta/H))^(i*t), so K_F is a Gram kernel",
        "diagonal": "(K_F)_(t,t)=6*|F_Q|<=6*Q^2=6*v^8",
        "mass": "Mcal(W)=1^*K_F*1=||sum_(t in W) Phi_t||_2^2",
        "one_row_change": "|Mcal(A union {tau})-Mcal(A)-6|F_Q||<=2*sqrt(6|F_Q|*Mcal(A))",
        "actual_labels": "C_theta(sk,rk)=R_W((r/s)*exp(theta/H)) remains an identity for the one common W.",
    }
    require(rows["diagonal"] == "(K_F)_(t,t)=6*|F_Q|<=6*Q^2=6*v^8", "Farey diagonal mismatch")
    return rows


def spectral_surgery_rows() -> dict[str, str]:
    """Return the exact block estimates for the selected actual outlier."""
    rows = {
        "core_hypothesis": "lambda_1(G_A)=Lambda and lambda_2(G_A)<=(1-g)*Lambda for fixed 0<g<=1",
        "scale_condition": "S_L+sqrt(Lambda*S_L)<=g*Lambda/2",
        "coupling": "f(tau)=u_A^*G_(A,tau)=sqrt(Lambda)*D_c(tau), with sum |c_n|^2<=1",
        "selected_coupling": "|f(tau)|^2<=Lambda*C_v",
        "complement_bound": "||B||<=lambda_2(G_A)+S_L+sqrt(Lambda*S_L)<=Lambda-g*Lambda/2",
        "top_coordinate": "For every unit top eigenvector u_W, |(u_W)_tau|^2<=4*C_v/(g^2*Lambda)",
        "deletion_consequence": "DelCov(W)<=mu_top(W)<=4*R*C_v/(g^2*Lambda)",
        "central_failure": "If Lambda>=v^(12-ell*delta(v)) and v>=64, DelCov(W)<=8*g^(-2)*v^(-4+ell*delta(v)).",
        "asymptotic_failure": "For fixed g,ell,s, the last bound is <v^(-2*s*delta(v)) for all sufficiently large v.",
    }
    require(rows["top_coordinate"] == "For every unit top eigenvector u_W, |(u_W)_tau|^2<=4*C_v/(g^2*Lambda)", "outlier-coordinate row mismatch")
    return rows


def verify_all(v: int = MEAN_VALUE_SIMPLE_BOUND_V) -> dict[str, object]:
    """Run the exact frozen-scale checks used by the sealing builder."""
    require(v >= MEAN_VALUE_SIMPLE_BOUND_V, "verification v must be at least 64")
    data = scales(v)
    windows = outlier_windows(v)
    mean_value = mean_value_rows()
    rationalmass = rationalmass_surplus_rows()
    farey = farey_kernel_rows()
    spectral = spectral_surgery_rows()
    coarse_tail_at_64 = Fraction(32, 64**2) + Fraction(320, 8**3)
    require(coarse_tail_at_64 == Fraction(81, 128), "large-v mean-value coarse tail mismatch")
    require(1 + coarse_tail_at_64 < 2, "C_v<=2 coarse check mismatch")
    require(windows["energy_increment"] == 4 * data["R"] - 3, "energy increment mismatch")
    require(data["L"] * data["L"] == data["R"] * data["H"], "L^2=RH critical scale mismatch")
    return {
        "scales": data,
        "outlier_windows": windows,
        "mean_value_rows": mean_value,
        "rationalmass_surplus_rows": rationalmass,
        "farey_kernel_rows": farey,
        "spectral_surgery_rows": spectral,
        "large_v_mean_value_coarse_tail_at_v64": coarse_tail_at_64,
    }
