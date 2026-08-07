#!/usr/bin/env python3
"""Independent integer checks of C105's symbolic arithmetic skeleton."""
from __future__ import annotations
import json

def row(q: int) -> dict[str, object]:
    lower, upper=(q-1)//2,(q+1)//2
    roots=[k for k in range(q+1) if k*(k-1)==(q-1)*(k-(q+1)//4)]
    k=upper; lam=k-(q+1)//4
    assert roots==[lower,upper]
    assert lower%2==1 and upper%2==0
    assert k%2==0 and lam==(q+1)//4 and lam%2==0
    # These are the two rearrangements in (2), for 1_A(t)=0,1.
    assert 2*lam+q-2*k==lower
    assert 1+2*lam+q-2*k==upper
    return {"q":q,"roots":roots,"lambda":lam,"parity_targets":[lower%2,upper%2]}

def main() -> None:
    rows=[row(q) for q in range(7,100,8)]
    print(json.dumps({"status":"PASS","symbolic_rows":rows,"identity":"P(t) mod 2 = 1_A(t/2) by the fixed-point involution"},sort_keys=True))

if __name__=="__main__":main()
