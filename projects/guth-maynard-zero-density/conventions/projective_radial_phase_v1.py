"""Cycle 120 exact projective/radial entropy phase conventions."""

from __future__ import annotations

from dataclasses import dataclass
from math import exp, log


@dataclass(frozen=True)
class RadialPhaseData:
    D: int
    p0: int
    q0: int
    n: int
    n_prime: int
    m: int
    u: int
    v: int

    def __post_init__(self) -> None:
        if min(self.D, self.p0, self.q0, self.n, self.n_prime, self.m) <= 0:
            raise ValueError("positive scale and arithmetic data required")

    @property
    def c(self) -> float:
        return self.D / (2.0 * 3.141592653589793)

    @property
    def g(self) -> float:
        return exp(1.0 / self.c)

    @property
    def A(self) -> int:
        return self.p0 * self.n

    @property
    def B(self) -> int:
        return self.p0 * self.n_prime

    @property
    def C(self) -> int:
        return self.q0 * self.m

    @property
    def z_saddle(self) -> float:
        return self.C * self.g**self.v / (self.B + self.C * self.g**self.v)

    @property
    def residual(self) -> float:
        return self.A - self.B * self.g**self.u - self.C * self.g ** (self.u + self.v)

    def projective_phase(self, z: float) -> float:
        if not 0.0 < z < 1.0:
            raise ValueError("projective coordinate must lie in (0,1)")
        c0 = self.p0 / self.q0
        entropy = (
            z * log(c0 * z / self.m)
            + log(self.n)
            + (1.0 - z) * log((1.0 - z) / self.n_prime)
        )
        return self.c * entropy - self.u - self.v * z

    @property
    def radial_frequency(self) -> float:
        denominator = self.B * self.g**self.u + self.C * self.g ** (self.u + self.v)
        return self.c * log(self.A / denominator)

    @property
    def projective_curvature(self) -> float:
        z = self.z_saddle
        return self.c / (z * (1.0 - z))


def theorem_record() -> dict[str, object]:
    return {
        "normal_form": (
            "with Delta=zH, cF(H,Delta)-uH-vDelta=H P_(u,v)(z), "
            "P=c[z log(c0 z/m)+log n+(1-z)log((1-z)/n')]-u-vz"
        ),
        "projective_saddle": (
            "P'(z)=0 iff z=z_v=C g^v/(B+C g^v), for "
            "(A,B,C)=(p0 n,p0 n',q0 m)"
        ),
        "curvature": "P''(z_v)=c/[z_v(1-z_v)]>0",
        "radial_frequency": (
            "P(z_v)=c log(A/(B g^u+C g^(u+v)))"
        ),
        "residual_orientation": (
            "for R=A-Bg^u-Cg^(u+v) and |R|<=A/2, sign(P(z_v))=sign(R) "
            "and (2c/(3A))|R|<=|P(z_v)|<=2c|R|/A"
        ),
        "coherence": (
            "on H~H0~KQ/D with A~Q and c~D, H0|P(z_v)|=O(1) "
            "is equivalent up to fixed constants to |R|=O(1/K)"
        ),
        "signed_kernel": (
            "after projective stationary phase the radial factor is a smooth "
            "Fourier transform evaluated at H0 P(z_v), retaining residual sign"
        ),
        "boundary": (
            "no cancellation estimate for the radial kernel, simple-root sum, "
            "complete moment, density, or prime intervals is proved"
        ),
    }
