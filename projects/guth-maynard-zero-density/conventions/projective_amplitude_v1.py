"""Cycle 121 projective stationary-amplitude conventions."""

from __future__ import annotations

from dataclasses import dataclass
from math import exp


@dataclass(frozen=True)
class ProjectiveAmplitudeData:
    D: int
    B: int
    C: int
    q0: int
    m: int
    v: int

    def __post_init__(self) -> None:
        if min(self.D, self.B, self.C, self.q0, self.m) <= 0:
            raise ValueError("positive stationary data required")
        if self.C != self.q0 * self.m:
            raise ValueError("C=q0*m convention violated")

    @property
    def c(self) -> float:
        return self.D / (2.0 * 3.141592653589793)

    @property
    def g(self) -> float:
        return exp(1.0 / self.c)

    @property
    def z_saddle(self) -> float:
        return self.C * self.g**self.v / (self.B + self.C * self.g**self.v)

    @property
    def leading_amplitude(self) -> float:
        return self.c * self.z_saddle / self.m

    @property
    def simplified_amplitude(self) -> float:
        return self.c * self.q0 * self.g**self.v / (self.B + self.C * self.g**self.v)


def theorem_record() -> dict[str, object]:
    return {
        "input_symbol": (
            "A*=c^(3/2)sqrt(Delta)/(m sqrt(H(H-Delta))) becomes "
            "c^(3/2)sqrt(z)/(m sqrt(1-z)sqrt(H))"
        ),
        "jacobian": (
            "dH dDelta=H dH dz, so the projective integrand amplitude is "
            "c^(3/2)H^(1/2)sqrt(z/(1-z))/m"
        ),
        "stationary_factor": (
            "for parameter Hc and normalized curvature 1/[z(1-z)], the "
            "positive-signature factor is e(1/8)sqrt(z(1-z)/(Hc))"
        ),
        "amplitude_collapse": (
            "the leading z-saddle amplitude is e(1/8)c z_v/m; since C=q0m, "
            "c z_v/m=c q0 g^v/(B+Cg^v), with no remaining power of H"
        ),
        "cutoffs": (
            "V(n/Q),V(n'/Q), W(beta^-1 log(m/(n z c0))), and "
            "W(beta^-1 log((1-z)m/(n' z c0))) are independent of H"
        ),
        "radial_profile": (
            "for a dyadic U(H/H0), the leading radial factor is "
            "H0 hat(U)(-H0 P(z_v))"
        ),
        "remainder": (
            "on a fixed compact z-chart with fixed smooth symbol norms, the "
            "z-stationary remainder is O(1/(mH)); integration over H~H0 is O(1/m)"
        ),
        "boundary": (
            "no arithmetic cancellation in the radial-profile sum, simple-root "
            "closure, complete moment, density, or prime intervals is proved"
        ),
    }
