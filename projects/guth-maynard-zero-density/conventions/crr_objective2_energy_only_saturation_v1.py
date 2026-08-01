"""Frozen bookkeeping for the Objective-2 energy-only CRR saturation audit.

This module records the exact critical scales and the epsilon absorption used
to turn Guth--Maynard's ``RL4`` subpower estimate into the uniform upper side
of the scoped actual-log-Farey theorem.  It does not assert Base
compatibility, RationalMass, PositiveCubic, AFARI, CFARI, or CRR-U.
"""
from __future__ import annotations

from fractions import Fraction
from math import log, sqrt


MIN_V = 8
LOCAL_LOWER_CONSTANT = Fraction(1, 20)


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def scales(v: int) -> dict[str, int]:
    """Return the frozen CRR critical scales for an even audit scale."""
    require(isinstance(v, int) and v >= MIN_V and v % 2 == 0, "v must be an even integer at least 8")
    result = {"v": v, "H": v**12, "L": v**10, "Q": v**4, "R": v**8}
    require(result["H"] == result["Q"] ** 3, "EO-LF4 needs H=Q^3")
    require(result["R"] == result["Q"] ** 2, "EO-LF4 needs R=Q^2")
    return result


def delta(v: int) -> float:
    """Return the frozen subpower slack delta(v)=1/sqrt(log v)."""
    require(isinstance(v, int) and v >= MIN_V, "v must be an integer at least 8")
    return 1.0 / sqrt(log(v))


def epsilon_absorption(epsilon: float) -> dict[str, float | str]:
    """Give a safe source-loss allocation for the sharp-exponent theorem.

    ``RL4`` permits an ``H^eta`` loss for every fixed eta>0.  Choosing
    eta=epsilon/24 turns this into v^(epsilon/2), while eventually
    delta(v)<=epsilon/2.  The two losses total at most epsilon.
    """
    require(isinstance(epsilon, (int, float)) and epsilon > 0.0, "epsilon must be positive")
    epsilon_value = float(epsilon)
    source_eta = epsilon_value / 24.0
    height_exponent_loss = 12.0 * source_eta
    delta_cap = epsilon_value / 2.0
    # This real threshold is an explanatory sufficient condition.  The
    # theorem uses "sufficiently large v", so integer rounding is harmless.
    sufficient_log_v = 4.0 / (epsilon_value * epsilon_value)
    require(abs(height_exponent_loss - epsilon_value / 2.0) < 1e-15, "RL4 loss allocation mismatch")
    require(abs(delta_cap - epsilon_value / 2.0) < 1e-15, "delta allocation mismatch")
    return {
        "source_eta": source_eta,
        "H_to_v_exponent_loss": height_exponent_loss,
        "delta_cap": delta_cap,
        "sufficient_log_v": sufficient_log_v,
        "sufficient_integer_v_description": "any integer v with log(v)>=4/epsilon^2",
        "conclusion": "H^(epsilon/24)*v^(20+delta(v))<=v^(20+epsilon) once delta(v)<=epsilon/2",
    }


def extremizer_rows(v: int) -> dict[str, int | Fraction | str]:
    """Return the exact central exponent rows for the phase-lattice family."""
    data = scales(v)
    require(data["R"] ** 4 // data["H"] == data["Q"] ** 5, "local fourth-moment exponent mismatch")
    require(data["Q"] ** 5 == v**20, "Q^5 must equal v^20")
    return {
        "local_lower_constant": LOCAL_LOWER_CONSTANT,
        "local_lower": "I_v(W_v)>=(1/20)*R^4/H=(1/20)*Q^5=(1/20)*v^20",
        "energy_lower": "E(W_v)>=R^4/H=Q^5=v^20",
        "energy_upper": "E(W_v)<=2^16*Q^5=2^16*v^20",
        "cardinality": data["R"],
        "central_exponent": 20,
    }


def base_bridge_rows(v: int) -> dict[str, int | str]:
    """Return the exact phase-lattice condition absent from EO-LF4."""
    data = scales(v)
    return {
        "N_L": data["L"] - 1,
        "m": data["R"],
        "V_minus": "v^(7-delta(v))",
        "exact_condition": "Gamma_(P,A)>=V_- iff lambda_(P,A)*Xi_(P,A)>=m*V_-^2/N_L",
        "threshold_with_m_R": "R*v^(14-2*delta(v))/(L-1)",
        "scope": "This is the missing common capped-coefficient/Base bridge; EO-LF4 does not establish either side for the extremizing A.",
    }


def verify_all(v: int = 8) -> dict[str, object]:
    """Run the finite identities used by the audit replay."""
    data = scales(v)
    rows = extremizer_rows(v)
    bridge = base_bridge_rows(v)
    allocation = epsilon_absorption(0.2)
    require(data["H"] == v**12 and data["L"] == v**10, "critical scale convention changed")
    require(rows["central_exponent"] == 20, "central local-moment exponent changed")
    require(rows["local_lower_constant"] == LOCAL_LOWER_CONSTANT, "local lower constant changed")
    require(bridge["N_L"] == v**10 - 1, "coefficient support convention changed")
    require(allocation["conclusion"].startswith("H^(epsilon/24)"), "epsilon-absorption conclusion changed")
    return {
        "scales": data,
        "extremizer_rows": rows,
        "base_bridge": bridge,
        "epsilon_absorption_at_1_5": epsilon_absorption(1.5),
    }
