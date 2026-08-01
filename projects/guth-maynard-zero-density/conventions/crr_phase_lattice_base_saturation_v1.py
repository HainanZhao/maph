"""Exact bookkeeping for the CRR phase-lattice Base-saturation reduction.

The accompanying note proves the quotient and functional identities.  This
module freezes their integer scale algebra and exact alias constants only.
"""
from __future__ import annotations

from fractions import Fraction
from math import gcd


MIN_V = 8


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def scales(v: int) -> dict[str, int]:
    require(isinstance(v, int) and v >= MIN_V and v % 2 == 0, "v must be an even integer at least 8")
    q = v**4
    result = {"v": v, "Q": q, "H": v**12, "L": v**10, "R": v**8, "V": v**7}
    require(result["H"] == q**3, "phase-lattice reduction requires H=Q^3")
    require(result["R"] == q**2, "phase-lattice reduction requires R=Q^2")
    require(q % 4 == 0, "even v must make Q divisible by four")
    require(result["L"] * result["H"] == result["R"] * result["V"] ** 2, "critical sampled-energy scale mismatch")
    return result


def actual_anchor(q: int) -> dict[str, int]:
    require(isinstance(q, int) and q >= 4 and q % 4 == 0, "actual anchor requires Q divisible by four and at least four")
    r = q + 1
    s = 5 * q // 4 + 1
    require(q <= r < 2 * q and q <= s < 2 * q, "actual anchor lies outside the frozen Farey shell")
    require(gcd(r, s) == 1, "actual anchor must be reduced")
    require(5 * r > 4 * s and 6 * r <= 5 * s, "anchor ratio must lie in (4/5,5/6]")
    return {"r": r, "s": s}


def exact_rows() -> dict[str, Fraction | int | str]:
    rows: dict[str, Fraction | int | str] = {
        "beta_lower": Fraction(6, 5),
        "beta_upper_strict": Fraction(5, 4),
        "max_exact_alias_class_size": 4,
        "alias_operator_square_factor": 4,
        "alias_capped_value_factor": 4,
        "base_product_main_exponent": 12,
        "base_product_delta_loss": 3,
        "phase_lattice_efficiency": "Xi_(P,A)=m*Gamma_(P,A)^2/(N_L*lambda_(P,A))",
        "base_equivalence": "Gamma>=V_- iff lambda*Xi>=m*V_-^2/N_L",
    }
    require(rows["beta_lower"] ** 4 > 2, "five exact aliases would not be excluded")
    require(rows["alias_operator_square_factor"] == rows["max_exact_alias_class_size"], "alias operator factor mismatch")
    require(rows["alias_capped_value_factor"] == rows["max_exact_alias_class_size"], "alias cap factor mismatch")
    require(rows["base_product_main_exponent"] == 8 + 2 * 7 - 10, "Base product exponent mismatch")
    return rows


def verify_all(v: int = MIN_V) -> dict[str, object]:
    data = scales(v)
    anchor = actual_anchor(data["Q"])
    rows = exact_rows()
    require(Fraction(8) + 2 * Fraction(7) - Fraction(10) == rows["base_product_main_exponent"], "central exponent identity changed")
    require(Fraction(1) + 2 * Fraction(1) == rows["base_product_delta_loss"], "delta-loss identity changed")
    require(data["L"] - 1 >= data["L"] // 2, "support cardinality convention changed")
    return {"scales": data, "actual_anchor": anchor, "exact_rows": rows}
