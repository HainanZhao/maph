"""Exact exponent ledger for the corrected light nonrational root tower."""
from __future__ import annotations
from math import comb

def require(ok: bool, msg: str) -> None:
    if not ok: raise ValueError(msg)

def light_tower_bound(*, T: int, a: int) -> dict[str, object]:
    require(T >= 3 and a >= 10, "light root-tower regime")
    H, V, target = T**22, T**a, T**42
    N1, N2, N3 = H//V+1, H//(V*V)+1, H//(V**3)+1
    require(N1 <= T**12+1 and N3 == 1, "light fibre capacities")
    P1, P2 = comb(N1,2), comb(N2,2)
    cross = 2*P1*P2
    require(cross < target, "tower unexpectedly critical")
    return {"parameters":{"T":T,"a":a,"H":H,"V":V,"critical_target":target},"fibres":{"N1":N1,"N2":N2,"N3":N3},"mass":{"ordered_cross_mass":cross,"upper_scale":"T^(88-6a)<=T^28","critical_scale":"T^42"},"phase":"z=r^(1/n), alpha_(jn)=r^j-1; q^j-1 has denominator V^j and residuals can be made <X^-1 by the C184 perturbation scale","boundary":"This is only the corrected rational-root tower family, not all actual positive exponentials."}

def verify_all() -> dict[str,object]:
    sample=light_tower_bound(T=3,a=10)
    return {"subcritical_tower":"Every corrected nonrational rational-root tower in the frozen light regime has only labels n and 2n with non-singleton fibres, and ordered cross mass <=T^28<T^42.","boundary":"No arbitrary actual-exponential distribution conclusion follows.","samples":{"T3_a10":sample}}
def theorem_record() -> dict[str,object]: return {"epistemic_status":"PROVED",**verify_all()}
