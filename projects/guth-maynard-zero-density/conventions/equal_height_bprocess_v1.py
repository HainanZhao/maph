"""Exact Cycle 90 equal-height B-process and saddle ledger."""

from fractions import Fraction

QF = Fraction

D_EXP = QF(3, 5)
DENOM_EXP = QF(1, 3)
ATOM_EXP = D_EXP + DENOM_EXP
XI_MIN = QF(16, 25)
XI_MAX = QF(58, 75)


def support(xi: Fraction) -> dict[str, Fraction]:
    h = xi + DENOM_EXP - D_EXP
    t = h + D_EXP
    dual_n = t - xi
    stationary_amplitude = t / 2 - dual_n
    leading_amplitude = D_EXP - xi
    dual_cell_amplitude = leading_amplitude + stationary_amplitude
    return {
        "xi": xi,
        "h": h,
        "t": t,
        "dual_n": dual_n,
        "sample_surplus": h - dual_n,
        "stationary_amplitude": stationary_amplitude,
        "leading_amplitude": leading_amplitude,
        "dual_cell_amplitude": dual_cell_amplitude,
    }


def moment_ledger(xi: Fraction) -> dict[str, Fraction]:
    row = support(xi)
    diagonal = xi + row["h"] + row["dual_n"] + 2 * row["dual_cell_amplitude"]
    one_cell_remainder = xi + row["h"] + 2 * row["dual_cell_amplitude"]
    target = xi + ATOM_EXP
    return {
        "diagonal": diagonal,
        "target": target,
        "one_cell_remainder": one_cell_remainder,
        "remainder_margin": target - one_cell_remainder,
    }


def collision_ledger(xi: Fraction) -> dict[str, Fraction]:
    volume = D_EXP + DENOM_EXP - xi
    target = DENOM_EXP
    return {
        "a": D_EXP,
        "n": DENOM_EXP,
        "vertical_tolerance": -xi,
        "volume": volume,
        "target": target,
        "target_over_volume_margin": target - volume,
    }


def formulas() -> dict[str, str]:
    return {
        "same_h_form": "sum_k U(k/K) sum_h |sum_r A_(k,h,r)|^2",
        "mellin_phase": "-t*log(r), t=h*D/beta",
        "poisson_phase": "-t*log(r)+n*r",
        "stationary_point": "r=t/n",
        "stationary_value": "t*(1-log(t/n))",
        "stationary_hessian": "n^2/t",
        "stationary_amplitude": "sqrt(t)/n",
        "dual_cross_phase": "(h*D/beta)*log(n/n')",
        "collision": "|n'-n*exp(beta*a/D)|<<1/K",
        "collision_surface": "F(a,n)=n*exp(beta*a/D)",
        "surface_hessian": (
            "F_aa=(beta^2*n/D^2)exp(beta*a/D), "
            "F_an=(beta/D)exp(beta*a/D), F_nn=0"
        ),
        "surface_determinant": "-(beta^2/D^2)*exp(2*beta*a/D)",
    }


def verify_all() -> dict[str, object]:
    for xi in (XI_MIN, QF(7, 10), XI_MAX):
        row = support(xi)
        moment = moment_ledger(xi)
        collision = collision_ledger(xi)
        assert row["dual_n"] == DENOM_EXP
        assert row["sample_surplus"] == xi - D_EXP
        assert row["stationary_amplitude"] == (xi - DENOM_EXP) / 2
        assert moment["diagonal"] == xi + ATOM_EXP
        assert moment["remainder_margin"] == DENOM_EXP
        assert collision["volume"] == ATOM_EXP - xi
        assert collision["target_over_volume_margin"] == xi - D_EXP
    assert support(XI_MIN)["sample_surplus"] == QF(1, 25)
    assert support(XI_MAX)["sample_surplus"] == QF(13, 75)
    values = formulas()
    assert values["stationary_point"] == "r=t/n"
    assert values["surface_determinant"].startswith("-(beta^2/D^2)")
    return {
        **values,
        "range": "16/25<=xi<58/75",
        "h_exponent": "xi-4/15",
        "dual_length_exponent": "1/3",
        "sample_surplus": "xi-3/5",
        "minimum_sample_surplus": "1/25",
        "dual_diagonal_exponent": "xi+14/15",
        "bprocess_remainder_exponent": "xi+3/5",
        "bprocess_remainder_margin": "1/3",
        "collision_volume_exponent": "14/15-xi",
        "collision_target_exponent": "1/3",
        "collision_margin": "xi-3/5",
        "analytic_target": (
            "Schwartz-weighted saddle collisions are <=X^(1/3+o(1)) "
            "on every fixed annulus"
        ),
        "gate": "prove two-dimensional saddle discrepancy or export a collision web",
    }


if __name__ == "__main__":
    print(verify_all())

