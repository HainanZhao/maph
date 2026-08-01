"""Exact bookkeeping for energy-only restricted-log-Farey F4F sharpness.

The theorem note uses pinned predecessors for the analytic RL4 upper and the
actual-Farey phase-lattice lower. This module freezes the architecture,
normalizations, and exact central-exponent arithmetic only.
"""
from __future__ import annotations

from fractions import Fraction


MIN_V = 8


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def scales(v: int) -> dict[str, int]:
    """Return frozen CRR scales for an admissible integral parameter."""
    require(isinstance(v, int) and v >= MIN_V, "v must be an integer at least 8")
    result = {"v": v, "H": v**12, "L": v**10, "R": v**8, "Q": v**4}
    require(result["H"] == result["Q"] ** 3, "H=Q^3 mismatch")
    require(result["R"] == result["Q"] ** 2, "R=Q^2 mismatch")
    require(result["L"] ** 2 == result["R"] * result["H"], "L^2=RH mismatch")
    return result


def architecture_rows() -> dict[str, str]:
    """Return the precise energy-only restricted-log-Farey architecture."""
    rows = {
        "farey_labels": "F_Q={(r,s): Q<=r,s<2Q, gcd(r,s)=1, 3/4<=r/s<=5/4}",
        "true_windows": "I_(r,s)={(r/s)*exp(theta/H): -3<=theta<=3}, U_v=disjoint union_(r,s in F_Q) I_(r,s)",
        "energy_only_class": "W subset [0,H], H^(1/100)-separated, v^(8-delta(v))<=|W|<=v^(8+delta(v)), and v^(20-delta(v))<=E(W)<=v^(20+delta(v))",
        "energy": "E(W)=#{(t1,t2,t3,t4) in W^4: |t1+t2-t3-t4|<=1}",
        "raw_sum": "R_W(u)=sum_(t in W)u^(it)",
        "log_functional": "J_v(W)=integral_(log U_v)|sum_(t in W)exp(i*t*x)|^4 dx=integral_(U_v)|R_W(u)|^4du/u",
        "excluded_data": "No coefficient vector b, pointwise Base value condition, RationalMass predicate, or PositiveCubic predicate belongs to the energy-only architecture.",
    }
    require(rows["log_functional"] == "J_v(W)=integral_(log U_v)|sum_(t in W)exp(i*t*x)|^4 dx=integral_(U_v)|R_W(u)|^4du/u", "log functional mismatch")
    return rows


def sharpness_rows() -> dict[str, Fraction | str]:
    """Return the predecessor-derived upper/lower and their exact conversion."""
    rows: dict[str, Fraction | str] = {
        "window_range": "U_v subset [1/2,3/2]",
        "measure_comparison": "(2/3)*integral_(U_v)|R_W|^4du<=J_v(W)<=2*integral_(U_v)|R_W|^4du",
        "global_upper": "J_v(W)<=2*H^(o(1))*E(W)<=v^(20+o(1)) on the energy-only class",
        "actual_lower_du": "For every sufficiently large even v, a sealed actual-Farey phase lattice W_v lies in the energy-only class and integral_(U_v)|R_(W_v)(u)|^4du>=(1/20)*v^20",
        "actual_lower_log": "J_v(W_v)>=(1/30)*v^20 for every sufficiently large even v",
        "limsup": "limsup_(v->infinity, v even) log(sup_(W in EO_v)J_v(W))/log(v)=20",
        "fixed_power_no_go": "For every fixed eta>0, the energy-only statement J_v(W)<=v^(20-eta) for all sufficiently large v and all W in EO_v is false.",
        "full_base_boundary": "The full Base/common-coefficient Guth--Maynard problem remains open: the phase lattice is not proved Base-admissible and no common capped coefficient is constructed.",
    }
    require(Fraction(2, 3) * Fraction(1, 20) == Fraction(1, 30), "log lower constant mismatch")
    return rows


def verify_all(v: int = MIN_V) -> dict[str, object]:
    """Run exact scale and central-exponent checks for the sealing builder."""
    data = scales(v)
    architecture = architecture_rows()
    sharpness = sharpness_rows()
    require(data["R"] ** 4 // data["H"] == data["Q"] ** 5, "phase-lattice fourth-moment exponent mismatch")
    require(data["Q"] ** 5 == v**20, "Q^5=v^20 mismatch")
    require(Fraction(1, 30) > 0, "positive log lower constant mismatch")
    return {
        "scales": data,
        "architecture_rows": architecture,
        "sharpness_rows": sharpness,
        "log_lower_constant": Fraction(1, 30),
        "central_exponent": 20,
    }
