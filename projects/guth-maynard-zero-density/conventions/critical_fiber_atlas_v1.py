"""Cycle 100 exact oriented critical-fiber divisor switch."""

from __future__ import annotations

from dataclasses import dataclass
from math import gcd


def divisor_count(n: int) -> int:
    if n <= 0:
        raise ValueError("positive integer required")
    count = 1
    prime = 2
    remaining = n
    while prime * prime <= remaining:
        exponent = 0
        while remaining % prime == 0:
            remaining //= prime
            exponent += 1
        if exponent:
            count *= exponent + 1
        prime += 1
    if remaining > 1:
        count *= 2
    return count


def prime_powers(n: int) -> dict[int, int]:
    result: dict[int, int] = {}
    prime = 2
    remaining = n
    while prime * prime <= remaining:
        while remaining % prime == 0:
            result[prime] = result.get(prime, 0) + 1
            remaining //= prime
        prime += 1
    if remaining > 1:
        result[remaining] = result.get(remaining, 0) + 1
    return result


@dataclass(frozen=True)
class FiberAtlas:
    w: int
    N: int
    R: int
    Q: int

    def __post_init__(self) -> None:
        if self.w == 0 or min(self.N, self.R, self.Q) <= 0:
            raise ValueError("nonzero w and positive label/scale required")
        if gcd(self.N, self.R) != 1:
            raise ValueError("label must be reduced")
        if abs(self.w) < 2:
            raise ValueError("opposite nonzero modes require |w|>=2")

    @property
    def W(self) -> int:
        return abs(self.w)

    def split(self, s: int) -> dict[str, object]:
        if not 1 <= s < self.W:
            raise ValueError("split outside 1..W-1")
        t = self.W - s
        g0 = gcd(s, t)
        cross_r = gcd(s // g0, self.R)
        cross_n = gcd(t // g0, self.N)
        total_gcd = gcd(s * self.N, t * self.R)
        factored_gcd = g0 * cross_r * cross_n
        if total_gcd != factored_gcd:
            raise AssertionError("gcd factorization failed")
        base_B = t * self.R // total_gcd
        base_C = s * self.N // total_gcd
        lambda_max = self.Q // max(base_B, base_C)
        return {
            "s": s,
            "t": t,
            "g0": g0,
            "cross_R": cross_r,
            "cross_N": cross_n,
            "cross_R_prime_powers": prime_powers(cross_r),
            "cross_N_prime_powers": prime_powers(cross_n),
            "total_gcd": total_gcd,
            "base_B": base_B,
            "base_C": base_C,
            "lambda_max": lambda_max,
            "generic": cross_r == 1 and cross_n == 1,
        }

    def exact_fiber_count(self) -> int:
        return sum(int(self.split(s)["lambda_max"]) for s in range(1, self.W))

    def generic_fiber_count(self) -> int:
        return sum(
            int(row["lambda_max"])
            for s in range(1, self.W)
            if (row := self.split(s))["generic"]
        )

    def generic_bound(self) -> float:
        return 2.0 * self.Q * divisor_count(self.W) / min(self.N, self.R)

    def enumerate_solutions(self) -> list[tuple[int, int, int, int]]:
        rows: list[tuple[int, int, int, int]] = []
        for s in range(1, self.W):
            split = self.split(s)
            for scale in range(1, int(split["lambda_max"]) + 1):
                rows.append(
                    (
                        s,
                        self.W - s,
                        scale * int(split["base_B"]),
                        scale * int(split["base_C"]),
                    )
                )
        return rows


def theorem_record() -> dict[str, object]:
    return {
        "orientation": "signed w fixes orientation; s=abs(a), t=abs(b), s+t=abs(w)",
        "fiber_equation": "C*t*R=B*s*N",
        "solutions": (
            "B=lambda*t*R/g, C=lambda*s*N/g, "
            "lambda<=Q*g/max(s*N,t*R)"
        ),
        "exact_count": (
            "sum_{s=1}^{W-1} floor(Q*gcd(s*N,(W-s)*R)/max(s*N,(W-s)*R))"
        ),
        "gcd_factorization": (
            "gcd(s*N,t*R)=g0*gcd(s/g0,R)*gcd(t/g0,N), g0=gcd(s,t)"
        ),
        "generic_bound": "F_generic<=2*Q*tau(W)/min(N,R)",
        "exceptional_web": (
            "gcd(s/g0,R)>1 or gcd(t/g0,N)>1, with side and prime powers retained"
        ),
        "sign_boundary": (
            "no Mobius sign is inherited; later work must reinsert actual stationary phases/amplitudes"
        ),
        "boundary": "no bound for the cross-valuation web or weak near-double rows",
    }
