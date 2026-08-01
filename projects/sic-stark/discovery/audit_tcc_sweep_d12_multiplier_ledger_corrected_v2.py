#!/usr/bin/env python3
"""Correct D12 phase ledger with fixed-point-positive characteristic lifts."""

from __future__ import annotations

from fractions import Fraction
from hashlib import sha256
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "discovery" / "tcc-sweep-d12-multiplier-ledger-corrected-v2.json"
A = (1189, 360, 360, 109)


def mod_one(value: Fraction) -> Fraction:
    return value % 1


def positive_lift(p: int, q: int) -> int:
    value = p
    while True:
        left = 3*q - 2*value
        if (q == 0 and left > 0) or (q > 0 and left > 0 and left*left > 13*q*q):
            return value
        value -= 12


def dedekind_sum(a: int, c: int) -> Fraction:
    return sum((Fraction(n, c)-Fraction(1,2))*(Fraction((n*a) % c, c)-Fraction(1,2)) for n in range(1,c))


def theta(ptilde: int, q: int) -> Fraction:
    a,b,c,d=A; r1,r2=Fraction(ptilde,12),Fraction(q,12)
    return Fraction(1,2)*((c-d+1)*r1+(-a+b+1)*r2-c*d*r1*r1+2*(a-1)*d*r1*r2-(a-2)*b*r2*r2)


def Q(p: int, q: int) -> int:
    return p*p-3*p*q-q*q


def digest(path: Path) -> str:
    return sha256(path.read_bytes()).hexdigest()


def main() -> None:
    a,b,c,d=A
    psi=Fraction(a+d,c)-3-12*dedekind_sum(a,c)
    if psi != 0 or a*d-b*c != 1 or (a%12,b%12,c%12,d%12)!=(1,0,0,1): raise AssertionError((psi,A))
    records=[]
    for p in range(12):
        for q in range(12):
            if not (p or q): continue
            lift=positive_lift(p,q); tv=mod_one(theta(lift,q)); target=mod_one(Fraction(Q(p,q),4))
            if tv != target: raise AssertionError((p,q,lift,tv,target))
            records.append({"characteristic":[p,q],"fixed_point_positive_lift":lift,"quadratic_form":Q(p,q),"theta_character_exponent_mod_1":str(tv),"afk_phase_square_exponent_mod_1":str(mod_one(-target)),"kopp_multiplier_exponent_mod_1":str(mod_one(-psi/12-tv)),"match":True})
    if len(records)!=143: raise AssertionError(len(records))
    payload={"schema":"tcc-sweep-d12-multiplier-ledger-corrected-v2","claim_tag":"EXPLORATORY","claim_boundary":"Exact phase-square multiplier comparison with corrected AFK/Kopp fixed-point positive lifts; no ray-value identification, signs, reconstruction, minors, or TCC conclusion.","correction_of":"tcc-sweep-d12-multiplier-ledger-v1.json","candidate":{"d":12,"r":1,"form":"<1,-3,-1>","rho":"(3+sqrt(13))/2"},"stabilizer":{"A_t":[[a,b],[c,d]],"rademacher_invariant":str(psi)},"nonzero_characteristic_count":len(records),"all_multiplier_comparisons_match":True,"records":records,"replay":{"command":"python3 discovery/audit_tcc_sweep_d12_multiplier_ledger_corrected_v2.py"},"source_hashes":{"audit_script":digest(Path(__file__))}}
    OUTPUT.write_text(json.dumps(payload,indent=2,sort_keys=True)+"\n")
    print("TCC_SWEEP_D12_MULTIPLIER_LEDGER_CORRECTED_V2=PASS")


if __name__=="__main__": main()
