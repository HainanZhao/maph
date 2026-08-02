"""Exact Cycle 83 Fejer--second-derivative resonance ledger."""

from fractions import Fraction

Q = Fraction

D_EXP = Q(3, 5)
Q_EXP = Q(1, 3)
OLD_CUTOFF = Q(94, 225)
NEW_CUTOFF = Q(37, 75)
RAW_L1_TARGET = Q(31, 25)
SCHWARTZ_POWER = 5


def resonance_terms(xi: Fraction, ell: Fraction = Q(0)) -> dict[str, Fraction]:
    """Counts at radius L/Q with L=X^ell and Fejer bandwidth Q/L."""
    bandwidth = Q_EXP - ell
    return {
        "bandwidth": bandwidth,
        "volume": D_EXP - bandwidth,
        "derivative": (xi + bandwidth) / 2,
        "reciprocal": D_EXP - (xi + bandwidth) / 2,
        "second_derivative_ceiling": xi + bandwidth - 2 * D_EXP,
    }


def central_resonance(xi: Fraction) -> Fraction:
    row = resonance_terms(xi)
    return max(row["volume"], row["derivative"], row["reciprocal"])


def block_ledger(xi: Fraction) -> dict[str, object]:
    resonance = central_resonance(xi)
    per_k = Q_EXP + resonance
    block = xi + per_k
    return {
        "xi": xi,
        "resonance": resonance,
        "per_k": per_k,
        "block_l1": block,
        "strictly_closed": block < RAW_L1_TARGET,
        "margin": RAW_L1_TARGET - block,
    }


def annular_net_terms(xi: Fraction, ell: Fraction) -> dict[str, Fraction]:
    row = resonance_terms(xi, ell)
    return {
        key: Q_EXP - SCHWARTZ_POWER * ell + row[key]
        for key in ("volume", "derivative", "reciprocal")
    }


def verify_all() -> dict[str, object]:
    bottom = resonance_terms(OLD_CUTOFF)
    top = resonance_terms(NEW_CUTOFF)
    assert bottom["second_derivative_ceiling"] < 0
    assert top["second_derivative_ceiling"] == Q(-28, 75)
    for xi in (OLD_CUTOFF, Q(9, 20), NEW_CUTOFF):
        row = resonance_terms(xi)
        assert row["derivative"] >= row["volume"]
        assert row["derivative"] >= row["reciprocal"]
        assert central_resonance(xi) == xi / 2 + Q(1, 6)
    assert block_ledger(OLD_CUTOFF)["strictly_closed"]
    assert not block_ledger(NEW_CUTOFF)["strictly_closed"]
    assert block_ledger(NEW_CUTOFF)["margin"] == 0
    assert NEW_CUTOFF - OLD_CUTOFF == Q(17, 225)
    ell = Q(1, 10)
    central_net = annular_net_terms(Q(9, 20), Q(0))
    annular_net = annular_net_terms(Q(9, 20), ell)
    assert all(annular_net[key] < central_net[key] for key in central_net)
    return {
        "fejer": "R_k(L)<<D*L/Q+(Q/L)^(-1)*sum_(j<=Q/L)|E_j|",
        "vdc": "E_j<<sqrt(j*k)+D/sqrt(j*k)",
        "central_resonance": "R_k<<D/Q+sqrt(kQ)+D/sqrt(kQ)",
        "active_dominant_exponent": "xi/2+1/6",
        "per_k_exponent": "xi/2+1/2",
        "block_exponent": "3xi/2+1/2",
        "old_cutoff": str(OLD_CUTOFF),
        "new_cutoff": str(NEW_CUTOFF),
        "new_band": "94/225<=xi<37/75",
        "band_width": str(NEW_CUTOFF - OLD_CUTOFF),
        "endpoint": "xi=37/75 ties 31/25 and is not promoted",
        "derivative_ceiling_at_endpoint": str(top["second_derivative_ceiling"]),
        "annular_decay_power": SCHWARTZ_POWER,
        "gate": "Fejer-VdC band closed; higher-frequency exponent-pair or averaging gain open",
    }


if __name__ == "__main__":
    print(verify_all())

