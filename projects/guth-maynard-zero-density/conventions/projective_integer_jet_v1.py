"""Cycle 96 integer-jet trichotomy for projective Laurent residuals."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from math import exp


@dataclass(frozen=True)
class JetData:
    A: int
    B: int
    C: int
    a: int
    b: int
    x: float

    def __post_init__(self) -> None:
        if min(self.A, self.B, self.C) <= 0:
            raise ValueError("A, B, C must be positive integers")
        if self.a == 0 and self.b == 0:
            raise ValueError("the mode must be noncentral")
        if self.x <= 0:
            raise ValueError("x must be positive")

    @property
    def j0(self) -> int:
        return self.A - self.B - self.C

    @property
    def j1(self) -> int:
        return self.B * self.a + self.C * self.b

    @property
    def mode_radius(self) -> int:
        return max(abs(self.a), abs(self.b))

    @property
    def s1(self) -> int:
        return self.B * abs(self.a) + self.C * abs(self.b)

    @property
    def s2(self) -> int:
        return self.B * self.a * self.a + self.C * self.b * self.b

    @property
    def residual(self) -> float:
        return self.A - self.B * exp(self.a * self.x) - self.C * exp(self.b * self.x)

    def case(self) -> str:
        if self.j0 != 0:
            return "NONZERO_CONSTANT_JET"
        if self.j1 > 0:
            return "NEGATIVE_MONOTONE_LINEAR_JET"
        if self.j1 < 0:
            return "POSITIVE_CONTROLLED_LINEAR_JET"
        return "QUADRATIC_CONCAVITY_JET"

    def sector_condition(self) -> bool:
        envelope = exp(self.x * self.mode_radius)
        if self.j0 != 0:
            return self.x * envelope * self.s1 <= 0.5
        if self.j1 > 0:
            return True
        if self.j1 < 0:
            return self.x * envelope * self.s2 <= 0.5
        return True

    def proved_lower_bound(self) -> float:
        if not self.sector_condition():
            raise ValueError("row lies outside its registered sector")
        if self.j0 != 0:
            return 0.5
        if self.j1 > 0:
            return self.x
        if self.j1 < 0:
            return self.x / 2.0
        return exp(-self.x * self.mode_radius) * self.x * self.x * self.s2 / 2.0

    def record(self) -> dict[str, object]:
        return {
            **asdict(self),
            "J0": self.j0,
            "J1": self.j1,
            "M": self.mode_radius,
            "S1": self.s1,
            "S2": self.s2,
            "case": self.case(),
            "sector_condition": self.sector_condition(),
        }


def theorem_record() -> dict[str, object]:
    return {
        "residual": "f(x)=A-B*exp(a*x)-C*exp(b*x)",
        "integer_jets": ["J0=A-B-C", "J1=B*a+C*b"],
        "derivatives": [
            "f'(t)=-B*a*exp(a*t)-C*b*exp(b*t)",
            "f''(t)=-B*a^2*exp(a*t)-C*b^2*exp(b*t)<0",
        ],
        "actual_substitution": (
            "(A,B,C,a,b,x)=(p0*n,p0*n',q0*m,u,u+v,2*pi/D)"
        ),
        "cases": {
            "J0_nonzero": "x*exp(x*M)*S1<=1/2 implies |f(x)|>=1/2",
            "J0_zero_J1_positive": "|f(x)|>=x",
            "J0_zero_J1_negative": (
                "x*exp(x*M)*S2<=1/2 implies |f(x)|>=x/2"
            ),
            "both_jets_zero": "|f(x)|>=exp(-x*M)*x^2*S2/2",
        },
        "boundary": (
            "no claim that registered sectors exhaust the projective Poisson support"
        ),
    }
