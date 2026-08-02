"""Cycle 99 critical rational-ray compiler conventions."""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from math import exp, log


@dataclass(frozen=True)
class CriticalRay:
    B: int
    C: int
    a: int
    b: int
    Q: int
    M: int

    def __post_init__(self) -> None:
        if min(self.B, self.C, self.Q, self.M) <= 0:
            raise ValueError("positive parameters required")
        if self.B > self.Q or self.C > self.Q:
            raise ValueError("coefficient exceeds Q")
        if self.a * self.b >= 0:
            raise ValueError("modes must be nonzero and opposite in sign")
        if max(abs(self.a), abs(self.b)) > self.M:
            raise ValueError("mode exceeds M")

    @property
    def w(self) -> int:
        return self.a - self.b

    @property
    def label(self) -> Fraction:
        return Fraction(-self.C * self.b, self.B * self.a)

    @property
    def height_budget(self) -> int:
        return self.Q * self.M

    @property
    def critical_point(self) -> float:
        return log(float(self.label)) / self.w

    def compile(self, x: float) -> dict[str, object]:
        if x <= 0:
            raise ValueError("x must be positive")
        t_star = self.critical_point
        rho = abs(t_star - x)
        envelope_exponent = max(abs(self.w * x), abs(self.w * t_star))
        envelope = exp(envelope_exponent)
        ray_error = envelope * abs(self.w) * rho
        height = self.height_budget
        farey_threshold = 1.0 / (2.0 * height * height)
        exponential_threshold = (
            exp(-envelope_exponent) * (exp(x) - 1.0) / 2.0
        )
        return {
            "w": self.w,
            "label_numerator": self.label.numerator,
            "label_denominator": self.label.denominator,
            "height_budget": height,
            "t_star": t_star,
            "rho": rho,
            "L": envelope_exponent,
            "E": envelope,
            "ray_error_bound": ray_error,
            "farey_threshold": farey_threshold,
            "exponential_threshold": exponential_threshold,
            "unique_fixed_w": ray_error < farey_threshold,
            "injective_across_w": ray_error < exponential_threshold,
            "strong_compiler": ray_error < min(farey_threshold, exponential_threshold),
            "factorization_fiber": (
                "C*abs(b)*R=B*abs(a)*N with a-b=w and sign orientation retained"
            ),
        }


def farey_spacing(left: Fraction, right: Fraction) -> Fraction:
    return abs(left - right)


def theorem_record() -> dict[str, object]:
    return {
        "critical_label": "r=-C*b/(B*a)=C*abs(b)/(B*abs(a))=exp(w*t*)",
        "mode": "w=a-b, 1<=abs(w)<=2*M",
        "height": "reduced numerator and denominator are <=H=Q*M",
        "ray_error": "|r-exp(w*x)|<=E*abs(w)*rho",
        "fixed_w_uniqueness": "E*abs(w)*rho<1/(2*H^2)",
        "cross_w_injectivity": (
            "E*abs(w)*rho<exp(-L)*(exp(x)-1)/2 for every row"
        ),
        "cycle97_substitution": (
            "rho<=2*eta/ell gives 2*E*abs(w)*eta/ell below both thresholds"
        ),
        "fiber": "C*abs(b)*R=B*abs(a)*N, a-b=w, orientation retained",
        "boundary": "no bound for the factorization fiber or weak near-double rows",
    }
