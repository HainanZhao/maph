"""Exact Cycle 95 projective entropy mode classification."""

from dataclasses import dataclass


@dataclass(frozen=True)
class ModeClass:
    name: str
    exact_stationarity_possible: bool
    reason: str


def mode_class(u: int, v: int) -> ModeClass:
    if u == 0 and v == 0:
        return ModeClass(
            "CENTRAL",
            True,
            "all exponents coincide; coefficient equation is p0*(n-n')=q0*m",
        )
    if u == 0:
        return ModeClass(
            "U_ZERO_V_NONZERO",
            False,
            "the g^v coefficient is -q0*m and cannot vanish",
        )
    if u + v == 0:
        return ModeClass(
            "SUM_ZERO_U_NONZERO",
            False,
            "the g^u coefficient is -p0*n' and cannot vanish",
        )
    if v == 0:
        return ModeClass(
            "EQUAL_NONZERO_EXPONENTS",
            False,
            "the constant coefficient p0*n is isolated and cannot vanish",
        )
    return ModeClass(
        "THREE_DISTINCT_EXPONENTS",
        False,
        "the constant coefficient p0*n is isolated and cannot vanish",
    )


def laurent_coefficients(
    u: int, v: int, p0: int, q0: int, n: int, n_prime: int, m: int
) -> dict[int, int]:
    if min(p0, q0, n, n_prime, m) <= 0:
        raise ValueError("positive anchor and stationary indices required")
    result: dict[int, int] = {}
    for exponent, coefficient in (
        (0, p0 * n),
        (u, -p0 * n_prime),
        (u + v, -q0 * m),
    ):
        result[exponent] = result.get(exponent, 0) + coefficient
    return {exponent: coefficient for exponent, coefficient in result.items() if coefficient}


def verify_all() -> dict[str, object]:
    for u in range(-8, 9):
        for v in range(-8, 9):
            row = mode_class(u, v)
            assert row.exact_stationarity_possible == (u == 0 and v == 0)
            if (u, v) != (0, 0):
                for values in ((1, 1, 1, 1, 1), (3, 2, 5, 4, 7)):
                    assert laurent_coefficients(u, v, *values)
    assert laurent_coefficients(0, 0, 3, 2, 5, 3, 3) == {}
    assert laurent_coefficients(0, 0, 3, 2, 5, 4, 3) == {0: -3}
    return {
        "poisson_phase": "c*F-u*h-v*Delta, c=D/(2*pi)",
        "stationary_derivatives": "F_h=2*pi*u/D, F_Delta=2*pi*v/D",
        "g": "g=exp(2*pi/D)",
        "exponentiated_relation": "c0*n-c0*n'*g^u-m*g^(u+v)=0",
        "integer_laurent_relation": "p0*n-p0*n'*g^u-q0*m*g^(u+v)=0",
        "transcendence": (
            "Gelfond-Schneider with (-1)^(-2i/D) proves g transcendental"
        ),
        "exact_mode_classification": (
            "exact stationarity iff u=v=0 and p0*(n-n')=q0*m"
        ),
        "noncentral_boundary": (
            "qualitative transcendence gives no uniform lower bound for "
            "near-zero Laurent trinomials as D grows"
        ),
        "gate": "exact noncentral stationary modes excluded; quantitative near-modes open",
    }


if __name__ == "__main__":
    print(verify_all())
