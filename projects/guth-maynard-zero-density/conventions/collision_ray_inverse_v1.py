"""Exact Cycle 92 collision-ray inverse exponent ledger."""

from fractions import Fraction

QF = Fraction

D_EXP = QF(3, 5)
DENOM_EXP = QF(1, 3)
XI_MIN = QF(16, 25)
XI_MAX = QF(58, 75)


def separation_margins(xi: Fraction) -> dict[str, Fraction]:
    return {
        "same_a_farey": xi - DENOM_EXP,
        "cross_a_injectivity": xi + DENOM_EXP - D_EXP,
    }


def web_exponents(mu: Fraction, epsilon: Fraction = QF(0)) -> dict[str, Fraction]:
    """Ignore logarithms: multiplicity X^mu from excess Q X^epsilon."""
    return {
        "multiplicity": mu,
        "primitive_denominator_ceiling": DENOM_EXP - mu,
        "distinct_a_floor": DENOM_EXP + epsilon - mu,
    }


def verify_all() -> dict[str, object]:
    bottom = separation_margins(XI_MIN)
    top = separation_margins(XI_MAX)
    assert bottom["same_a_farey"] == QF(23, 75)
    assert bottom["cross_a_injectivity"] == QF(28, 75)
    assert top["same_a_farey"] == QF(11, 25)
    assert top["cross_a_injectivity"] == QF(38, 75)
    for mu in (QF(0), QF(1, 10), DENOM_EXP):
        row = web_exponents(mu)
        assert row["primitive_denominator_ceiling"] + mu == DENOM_EXP
        assert row["distinct_a_floor"] + mu == DENOM_EXP
    return {
        "collision": "|n'-n*exp(beta*a/D)|<=C/K",
        "primitive_label": "(p,q)=(n'/g,n/g), g=gcd(n,n')",
        "same_a_rigidity": (
            "Farey spacing Omega(Q^-2) and error O((KQ)^-1) force one "
            "primitive rational label for each a"
        ),
        "cross_a_injectivity": (
            "spacing Omega(D^-1) of exp(beta*a/D) and error O((KQ)^-1) "
            "prevent one label from serving distinct a"
        ),
        "multiplicity_contract": "class degree M implies primitive denominator q<<Q/M",
        "dyadic_extraction": (
            "C_tot collisions yield some dyadic M with >>C_tot/(M log Q) "
            "distinct a and injective labels q<<Q/M"
        ),
        "minimum_same_a_margin": str(bottom["same_a_farey"]),
        "minimum_cross_a_margin": str(bottom["cross_a_injectivity"]),
        "analytic_or_web": (
            "either C_tot<=Q*X^epsilon or a dyadic rational-ray web is "
            "exported; the web is not yet a transport seed"
        ),
        "gate": "equal-height collision count or rational-ray web to E16",
    }


if __name__ == "__main__":
    print(verify_all())

