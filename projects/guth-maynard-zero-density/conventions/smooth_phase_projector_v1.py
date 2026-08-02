"""Exact exponent ledger for Cycle 82 smooth phase projection."""

from fractions import Fraction

Q = Fraction

Q_EXP = Q(1, 3)
OCCUPANCY_EXP = Q(22, 45)
OLD_CUTOFF = Q(163, 450)
RAW_L1_TARGET = Q(31, 25)


def projector_ledger(xi: Fraction) -> dict[str, object]:
    per_k = Q_EXP + OCCUPANCY_EXP
    block = xi + per_k
    return {
        "xi": xi,
        "q_prefactor": Q_EXP,
        "occupancy": OCCUPANCY_EXP,
        "per_k": per_k,
        "block_l1": block,
        "strictly_closed": block < RAW_L1_TARGET,
        "margin": RAW_L1_TARGET - block,
    }


def verify_all() -> dict[str, object]:
    per_k = Q_EXP + OCCUPANCY_EXP
    cutoff = RAW_L1_TARGET - per_k
    width = cutoff - OLD_CUTOFF
    assert per_k == Q(37, 45)
    assert cutoff == Q(94, 225)
    assert width == Q(1, 18)
    assert projector_ledger(OLD_CUTOFF)["strictly_closed"]
    assert not projector_ledger(cutoff)["strictly_closed"]
    assert projector_ledger(cutoff)["margin"] == 0
    return {
        "projector": "Theta_Q(x)=Q*sum_m hatV(Q*(m-x)); |Theta_Q(x)|<<Q*(1+Q*||x||)^(-A)",
        "occupancy_sum": "sum_d |Theta_Q(x_d)|<<Q*A_k",
        "per_k_exponent": str(per_k),
        "old_cutoff": str(OLD_CUTOFF),
        "new_cutoff": str(cutoff),
        "new_band": "163/450<=xi<94/225",
        "band_width": str(width),
        "endpoint": "xi=94/225 ties 31/25 and is not promoted",
        "gate": "smooth projector band closed; fixed-center resonance occupancy open",
    }


if __name__ == "__main__":
    print(verify_all())

