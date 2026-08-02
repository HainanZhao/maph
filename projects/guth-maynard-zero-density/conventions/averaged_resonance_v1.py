"""Exact Cycle 84 averaged-resonance exponent ledger."""

from fractions import Fraction

Q = Fraction

D_EXP = Q(3, 5)
Q_EXP = Q(1, 3)
OLD_CUTOFF = Q(37, 75)
NEW_CUTOFF = Q(43, 75)
VOLUME_CUTOFF = Q(16, 25)
RAW_L1_TARGET = Q(31, 25)
SCHWARTZ_POWER = 5


def incidence_terms(xi: Fraction, ell: Fraction = Q(0)) -> dict[str, Fraction]:
    """I_L terms before the outer Q projector factor."""
    return {
        "volume": xi + D_EXP + ell - Q_EXP,
        "length": D_EXP,
        "crossing": xi + Q_EXP - ell,
    }


def l1_terms(xi: Fraction, ell: Fraction = Q(0)) -> dict[str, Fraction]:
    incidence = incidence_terms(xi, ell)
    return {
        key: Q_EXP - SCHWARTZ_POWER * ell + value
        for key, value in incidence.items()
    }


def block_ledger(xi: Fraction) -> dict[str, object]:
    terms = l1_terms(xi)
    bound = max(terms.values())
    return {
        "xi": xi,
        **terms,
        "bound": bound,
        "strictly_closed": bound < RAW_L1_TARGET,
        "margin": RAW_L1_TARGET - bound,
    }


def verify_all() -> dict[str, object]:
    bottom = block_ledger(OLD_CUTOFF)
    endpoint = block_ledger(NEW_CUTOFF)
    assert bottom["crossing"] > bottom["volume"]
    assert bottom["crossing"] > bottom["length"]
    assert bottom["strictly_closed"]
    assert not endpoint["strictly_closed"]
    assert endpoint["margin"] == 0
    assert endpoint["crossing"] == RAW_L1_TARGET
    assert NEW_CUTOFF - OLD_CUTOFF == Q(2, 25)
    assert VOLUME_CUTOFF - NEW_CUTOFF == Q(1, 15)
    ell = Q(1, 20)
    central = l1_terms(Q(8, 15), Q(0))
    annular = l1_terms(Q(8, 15), ell)
    assert all(annular[key] < central[key] for key in central)
    return {
        "joint_fejer": "I_L<<K*D*L/Q+(L/Q)*sum_(j<=Q/L)|B_j|",
        "bilinear_sum": "B_j=sum_(k~K,d~D)e(j*k*c0*exp(2*pi*d/D))",
        "crossing_bound": "|B_j|<<D+j*K",
        "incidence": "I_L<<K*D*L/Q+D+K*Q/L",
        "l1_terms_at_L1": {
            "volume": "xi+3/5",
            "length": "14/15",
            "crossing": "xi+2/3",
        },
        "old_cutoff": str(OLD_CUTOFF),
        "new_cutoff": str(NEW_CUTOFF),
        "new_band": "37/75<=xi<43/75",
        "band_width": str(NEW_CUTOFF - OLD_CUTOFF),
        "endpoint": "xi=43/75 ties 31/25 and is not promoted",
        "volume_only_cutoff": str(VOLUME_CUTOFF),
        "crossing_gap_to_volume": str(VOLUME_CUTOFF - NEW_CUTOFF),
        "annular_decay_power": SCHWARTZ_POWER,
        "gate": "averaged resonance band closed; crossing-discretization inverse theorem open",
    }


if __name__ == "__main__":
    print(verify_all())

