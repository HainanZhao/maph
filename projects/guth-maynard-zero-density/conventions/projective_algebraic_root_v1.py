"""Cycle 97 algebraic-root and near-double-root inverse conventions."""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from math import exp, log, sqrt


@dataclass(frozen=True)
class RootData:
    A: int
    B: int
    C: int
    a: int
    b: int

    def __post_init__(self) -> None:
        if min(self.A, self.B, self.C) <= 0:
            raise ValueError("A, B, C must be positive")
        if self.a == 0 and self.b == 0:
            raise ValueError("the mode must be noncentral")

    @property
    def mode_radius(self) -> int:
        return max(abs(self.a), abs(self.b))

    @property
    def shift(self) -> int:
        return max(0, -self.a, -self.b)

    @property
    def weight(self) -> int:
        return self.A + self.B + self.C

    @property
    def s2(self) -> int:
        return self.B * self.a * self.a + self.C * self.b * self.b

    def polynomial(self) -> dict[int, int]:
        terms: dict[int, int] = {}
        for exponent, coefficient in (
            (self.shift, self.A),
            (self.shift + self.a, -self.B),
            (self.shift + self.b, -self.C),
        ):
            if exponent < 0:
                raise AssertionError("negative exponent after clearing")
            terms[exponent] = terms.get(exponent, 0) + coefficient
        return {exponent: coefficient for exponent, coefficient in terms.items() if coefficient}

    def polynomial_degree(self) -> int:
        return max(self.polynomial())

    def polynomial_l1(self) -> int:
        return sum(abs(value) for value in self.polynomial().values())

    def value(self, t: float) -> float:
        return self.A - self.B * exp(self.a * t) - self.C * exp(self.b * t)

    def derivative(self, t: float) -> float:
        return -self.B * self.a * exp(self.a * t) - self.C * self.b * exp(self.b * t)

    def second_derivative(self, t: float) -> float:
        return (
            -self.B * self.a * self.a * exp(self.a * t)
            - self.C * self.b * self.b * exp(self.b * t)
        )

    def critical_contract(self) -> dict[str, object]:
        if self.a * self.b >= 0:
            return {"exists": False, "reason": "modes do not have opposite signs"}
        ratio = Fraction(-self.C * self.b, self.B * self.a)
        if ratio <= 0:
            raise AssertionError("critical ratio must be positive")
        t_star = log(float(ratio)) / (self.a - self.b)
        return {
            "exists": True,
            "ratio_numerator": ratio.numerator,
            "ratio_denominator": ratio.denominator,
            "root_exponent": self.a - self.b,
            "t_star": t_star,
            "positive": t_star > 0,
        }

    def local_inverse(self, x: float) -> dict[str, object]:
        if x <= 0:
            raise ValueError("x must be positive")
        delta = abs(self.value(x))
        eta = abs(self.derivative(x))
        radius = self.mode_radius
        upper_curvature = self.s2 * exp(radius * (x + 1.0))
        lower_curvature = self.s2 * exp(-radius * (x + 1.0))
        tau = max(2.0 * delta, 2.0 * sqrt(upper_curvature * delta))
        if delta == 0:
            branch = "EXACT_ALGEBRAIC_ROOT"
        elif eta >= tau:
            branch = "SIMPLE_ALGEBRAIC_ROOT"
        else:
            branch = "NEAR_DOUBLE_ROOT"
        result: dict[str, object] = {
            "branch": branch,
            "delta": delta,
            "eta": eta,
            "L": upper_curvature,
            "ell": lower_curvature,
            "tau": tau,
        }
        if branch == "SIMPLE_ALGEBRAIC_ROOT":
            result["root_distance_bound"] = 2.0 * delta / eta
        if branch == "NEAR_DOUBLE_ROOT" and eta <= lower_curvature / 2.0:
            result["localized_critical"] = True
            result["critical_distance_bound"] = 2.0 * eta / lower_curvature
            result["critical_value_bound"] = (
                delta
                + 2.0 * eta * eta / lower_curvature
                + 2.0 * upper_curvature * eta * eta / (lower_curvature**2)
            )
        else:
            result["localized_critical"] = False
        return result


def theorem_record() -> dict[str, object]:
    return {
        "cleared_polynomial": "P(Y)=A*Y^s-B*Y^(s+a)-C*Y^(s+b), s=max(0,-a,-b)",
        "identity": "f(t)=exp(-s*t)*P(exp(t))",
        "polynomial_contract": {
            "nonzero": True,
            "degree": "deg(P)<=2*M",
            "coefficient_l1": "||P||_1<=W=A+B+C",
            "root_degree": "deg(alpha)<=2*M",
            "root_height": "h(alpha)<=log(W)+log(2*M+1)/2",
        },
        "shape": {
            "strict_concavity": "f''(t)<0",
            "root_count": "at most two real roots",
            "critical_count": "at most one real critical point",
            "critical_equation": "exp((a-b)*t*)=-C*b/(B*a), requiring a*b<0",
        },
        "inverse": {
            "tau": "max(2*delta,2*sqrt(L*delta))",
            "simple": "eta>=tau gives |r-x|<=2*delta/eta for an algebraic root",
            "near_double": "eta<tau records simultaneous small value and derivative",
            "localized_critical": (
                "eta<=ell/2 gives a*b<0 and |t*-x|<=2*eta/ell"
            ),
        },
        "entropy_linear_form": "x=2*pi/D gives |D*log(alpha)-2*pi|<=2*D*delta/eta",
        "boundary": "no effective lower bound for the entropy linear form is proved",
    }
