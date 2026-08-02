"""Cycle 123 joint radial/Poisson-alias saddle conventions."""

from __future__ import annotations

from dataclasses import dataclass
from math import exp, log, pi


@dataclass(frozen=True)
class JointAliasData:
    D: int
    p0: int
    q0: int
    n_prime: int
    m: int
    u: int
    v: int
    ell: int

    def __post_init__(self) -> None:
        if min(self.D, self.p0, self.q0, self.n_prime, self.m, self.ell) <= 0:
            raise ValueError("positive stationary data required")

    @property
    def c(self) -> float:
        return self.D / (2.0 * pi)

    @property
    def g(self) -> float:
        return exp(1.0 / self.c)

    @property
    def B(self) -> int:
        return self.p0 * self.n_prime

    @property
    def C(self) -> int:
        return self.q0 * self.m

    @property
    def S(self) -> float:
        return self.B * self.g**self.u + self.C * self.g ** (self.u + self.v)

    @property
    def n_saddle(self) -> float:
        return self.S / self.p0

    @property
    def H_saddle(self) -> float:
        return self.ell * self.S / (self.p0 * self.c)

    @property
    def z_saddle(self) -> float:
        return self.C * self.g**self.v / (self.B + self.C * self.g**self.v)

    @property
    def stationary_value(self) -> float:
        return -self.ell * self.S / self.p0

    @property
    def hessian_determinant(self) -> float:
        return -(self.c / self.n_saddle) ** 2

    @property
    def joint_amplitude(self) -> float:
        return self.n_saddle / self.c

    @property
    def total_amplitude(self) -> float:
        return self.c * self.z_saddle / self.m * self.joint_amplitude

    @property
    def simplified_amplitude(self) -> float:
        return (self.q0 / self.p0) * self.g ** (self.u + self.v)

    def phase(self, H: float, n: float) -> float:
        return H * self.c * log(self.p0 * n / self.S) - self.ell * n


def theorem_record() -> dict[str, object]:
    return {
        "phase": (
            "Phi_ell(H,n)=Hc log(p0n/S)-ell n, "
            "S=p0n'g^u+q0m g^(u+v)"
        ),
        "joint_saddle": (
            "n*=S/p0 and H*=ell S/(p0c); interior support forces ell~K"
        ),
        "hessian": (
            "Hess=[[0,c/n],[c/n,-Hc/n^2]], det=-(c/n)^2; it has one "
            "positive and one negative eigenvalue, hence signature zero"
        ),
        "stationary_value": (
            "Phi_ell(H*,n*)=-ell S/p0=-ell n'g^u-ell(q0/p0)m g^(u+v)"
        ),
        "joint_amplitude": "|det Hess|^(-1/2)=n*/c=S/(p0c)",
        "total_amplitude": (
            "multiplying the Cycle-121 factor e(1/8)c z_v/m gives "
            "e(1/8)(q0/p0)g^(u+v)"
        ),
        "cutoffs": (
            "at the saddle, V(n/Q)=V(S/(p0Q)); the logarithmic W arguments "
            "are -(u+v)/D and -v/D; U is evaluated at ell S/(p0cH0)"
        ),
        "factorization": (
            "e(-ell S/p0)=e(-ell n'g^u)e(-ell(q0/p0)m g^(u+v))"
        ),
        "remainder": (
            "after H=H0 h,n=Qx, the large parameter is H0c~KQ and the "
            "fixed-chart two-dimensional remainder is smaller than the leading "
            "stationary scale by O((KQ)^(-1))"
        ),
        "boundary": (
            "no bilinear estimate for the ell~K operator, simple-root closure, "
            "complete moment, density, or prime intervals is proved"
        ),
    }
