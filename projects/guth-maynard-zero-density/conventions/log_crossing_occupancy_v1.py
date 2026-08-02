"""Exact Cycle 85 logarithmic crossing-occupancy ledger."""

from fractions import Fraction

Q = Fraction

D_EXP = Q(3, 5)
Q_EXP = Q(1, 3)
XI_MIN = Q(43, 75)
XI_MAX = Q(16, 25)
RAW_L1_TARGET = Q(31, 25)
SCHWARTZ_POWER = 5


def hs_terms(xi: Fraction, nu: Fraction) -> dict[str, Fraction]:
    lam = D_EXP - 3 * nu
    delta = D_EXP - nu - xi
    return {
        "lambda": lam,
        "delta": delta,
        "derivative": nu + lam / 6,
        "tube": nu + delta / 3,
        "ratio": (delta - lam) / 3,
        "constant": Q(0),
    }


def crossing_exponent(xi: Fraction, nu: Fraction) -> Fraction:
    row = hs_terms(xi, nu)
    hs = max(row[key] for key in ("derivative", "tube", "ratio", "constant"))
    return min(nu, hs)


def dyadic_l1_exponent(xi: Fraction, nu: Fraction) -> Fraction:
    return xi + nu + crossing_exponent(xi, nu)


def dominance_margins(xi: Fraction, nu: Fraction) -> dict[str, Fraction]:
    row = hs_terms(xi, nu)
    return {
        "over_tube": row["derivative"] - row["tube"],
        "over_ratio": row["derivative"] - row["ratio"],
        "over_constant": row["derivative"],
    }


def verify_all() -> dict[str, object]:
    corners = [
        (xi, nu)
        for xi in (XI_MIN, XI_MAX)
        for nu in (Q(0), Q(1, 5), Q_EXP)
    ]
    for xi, nu in corners:
        margins = dominance_margins(xi, nu)
        assert all(value > 0 for value in margins.values())
        assert hs_terms(xi, nu)["derivative"] == Q(1, 10) + nu / 2
        assert crossing_exponent(xi, nu) == min(nu, Q(1, 10) + nu / 2)
    assert dominance_margins(XI_MIN, Q_EXP)["over_tube"] == Q(8, 225)
    assert dyadic_l1_exponent(XI_MIN, Q_EXP) == XI_MIN + D_EXP
    endpoint = dyadic_l1_exponent(XI_MAX, Q_EXP)
    assert endpoint == RAW_L1_TARGET
    assert XI_MAX - XI_MIN == Q(1, 15)
    assert Q_EXP + crossing_exponent(XI_MIN, Q_EXP) == D_EXP
    ell = Q(1, 30)
    annular_top_nu = Q_EXP - ell
    annular = (
        XI_MIN
        + annular_top_nu
        + crossing_exponent(XI_MIN, annular_top_nu)
        + (1 - SCHWARTZ_POWER) * ell
    )
    central = dyadic_l1_exponent(XI_MIN, Q_EXP)
    assert annular < central
    return {
        "crossing_curve": "g_j(r)=D/(2*pi)*log(r/(j*c0))",
        "tolerance": "delta=D/(j*K)",
        "hs_terms": {
            "derivative": "1/10+nu/2",
            "tube": "1/5+2nu/3-xi/3",
            "ratio": "(2nu-xi)/3",
            "constant": "0",
        },
        "minimum_derivative_over_tube_margin": "8/225",
        "crossing_exponent": "min(nu,1/10+nu/2)",
        "max_j_plus_crossing": "3/5 at nu=1/3",
        "block_l1_exponent": "xi+3/5",
        "old_cutoff": str(XI_MIN),
        "new_cutoff": str(XI_MAX),
        "new_band": "43/75<=xi<16/25",
        "band_width": str(XI_MAX - XI_MIN),
        "endpoint": "xi=16/25 ties 31/25 and is not promoted",
        "annular_decay_power": SCHWARTZ_POWER,
        "gate": "unsigned incidence reaches volume limit; signed high-frequency cancellation open",
    }


if __name__ == "__main__":
    print(verify_all())

