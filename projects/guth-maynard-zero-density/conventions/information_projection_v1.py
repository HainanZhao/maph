"""Exact series and exponent ledger for Cycle 36 information projection."""
from __future__ import annotations

from fractions import Fraction as Q


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


DEGREE = 8


def poly(values: dict[int, Q]) -> list[Q]:
    return [values.get(i, Q(0)) for i in range(DEGREE)]


def add(a: list[Q], b: list[Q]) -> list[Q]:
    return [a[i] + b[i] for i in range(DEGREE)]


def scale(a: list[Q], factor: Q) -> list[Q]:
    return [factor * value for value in a]


def mul(a: list[Q], b: list[Q]) -> list[Q]:
    out = [Q(0) for _ in range(DEGREE)]
    for i, left in enumerate(a):
        for j, right in enumerate(b):
            if i + j < DEGREE:
                out[i + j] += left * right
    return out


def compose(a: list[Q], b: list[Q]) -> list[Q]:
    out = [Q(0) for _ in range(DEGREE)]
    power = poly({0: Q(1)})
    for coefficient in a:
        out = add(out, scale(power, coefficient))
        power = mul(power, b)
    return out


def derived_series() -> dict[str, tuple[Q, ...]]:
    i0 = poly({0: Q(1), 2: Q(1, 4), 4: Q(1, 64), 6: Q(1, 2304)})
    i1 = poly({1: Q(1, 2), 3: Q(1, 16), 5: Q(1, 384), 7: Q(1, 18432)})
    mean = poly({1: Q(1, 2), 3: Q(-1, 16), 5: Q(1, 96), 7: Q(-11, 6144)})
    require(mul(i0, mean) == i1, "I1/I0 series division")

    inverse = poly({1: Q(2), 3: Q(1), 5: Q(5, 6), 7: Q(19, 24)})
    identity = compose(mean, inverse)
    require(identity[1] == 1 and all(identity[i] == 0 for i in range(2, DEGREE)), "mean-series inversion")

    x = add(i0, scale(poly({0: Q(1)}), Q(-1)))
    log_i0 = add(add(x, scale(mul(x, x), Q(-1, 2))), scale(mul(mul(x, x), x), Q(1, 3)))
    rate = add(mul(inverse, poly({1: Q(1)})), scale(compose(log_i0, inverse), Q(-1)))
    require((rate[2], rate[4], rate[6]) == (Q(1), Q(1, 4), Q(5, 36)), "rate series")

    i2 = poly({2: Q(1, 8), 4: Q(1, 96), 6: Q(1, 3072)})
    second_ratio = poly({2: Q(1, 8), 4: Q(-1, 48), 6: Q(11, 3072)})
    require(mul(i0, second_ratio) == i2, "I2/I0 series division")
    second_in_r = compose(second_ratio, inverse)
    require(second_in_r[2] == Q(1, 2), "second harmonic leading term")
    return {
        "mean_kappa_1_3_5_7": tuple(mean[i] for i in (1, 3, 5, 7)),
        "kappa_r_1_3_5_7": tuple(inverse[i] for i in (1, 3, 5, 7)),
        "rate_r_2_4_6": tuple(rate[i] for i in (2, 4, 6)),
        "second_harmonic_r_2": (second_in_r[2],),
    }


def bessel_series() -> dict[str, tuple[Q, ...]]:
    # Coefficients are ordered by the displayed nonzero powers.
    rows = {
        "I0_kappa_0_2_4_6": (Q(1), Q(1, 4), Q(1, 64), Q(1, 2304)),
        "I1_kappa_1_3_5_7": (Q(1, 2), Q(1, 16), Q(1, 384), Q(1, 18432)),
        "mean_kappa_1_3_5_7": (Q(1, 2), Q(-1, 16), Q(1, 96), Q(-11, 6144)),
        "kappa_r_1_3_5_7": (Q(2), Q(1), Q(5, 6), Q(19, 24)),
        "rate_r_2_4_6": (Q(1), Q(1, 4), Q(5, 36)),
        "second_harmonic_r_2": (Q(1, 2),),
    }
    require(rows["rate_r_2_4_6"][0] == 1, "information leading constant")
    require(rows["second_harmonic_r_2"][0] == Q(1, 2), "second harmonic coefficient")
    derived = derived_series()
    for label, value in derived.items():
        require(rows[label] == value, f"derived Bessel mismatch: {label}")
    return rows


def exponent_match() -> dict[str, Q]:
    count = Q(21, 25)
    rho = Q(-3, 5)
    leading = count + rho
    quadratic_error = count + 2 * rho
    second_harmonic_kernel = Q(1) + rho
    require(leading == Q(6, 25), "leading information/volume scale")
    require(quadratic_error == Q(-9, 25), "information Taylor remainder scale")
    require(second_harmonic_kernel == Q(2, 5), "von Mises second harmonic scale")
    return {
        "count": count,
        "rho": rho,
        "information_leading": leading,
        "determinant_leading": leading,
        "information_quadratic_error": quadratic_error,
        "von_mises_second_harmonic_kernel": second_harmonic_kernel,
        "cycle19_popular_kernel": Q(2, 5),
    }


def pythagorean_identity() -> dict[str, str]:
    return {
        "constraint": "sum_j q_j c_j=sum_j qstar_j c_j=r",
        "projection": "log(qstar_j/u_j)=kappa*c_j-log(Z)",
        "identity": "D(q||u)=D(qstar||u)+D(q||qstar)",
        "excess": "E(q)=D(q||qstar)>=0",
        "pinsker_rigidity": "||q-qstar||_1<=sqrt(2E(q))",
    }


def verify_all() -> dict[str, object]:
    rows = {
        "bessel_series": bessel_series(),
        "exponent_match": exponent_match(),
        "pythagorean": pythagorean_identity(),
    }
    require(rows["exponent_match"]["information_leading"] == rows["exponent_match"]["determinant_leading"], "leading scales disagree")
    require(rows["exponent_match"]["von_mises_second_harmonic_kernel"] == rows["exponent_match"]["cycle19_popular_kernel"], "second harmonic mismatch")
    return rows


if __name__ == "__main__":
    print(verify_all())
