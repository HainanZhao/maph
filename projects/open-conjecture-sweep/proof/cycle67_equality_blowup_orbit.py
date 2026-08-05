#!/usr/bin/env python3
"""Fast invariant-route construction of C67 radial blow-up charts."""

from __future__ import annotations

import argparse
import csv
import json
from collections import defaultdict
from fractions import Fraction
from pathlib import Path

from cycle67_equality_blowup import charts, add, scale, mul, power, const, evaluate


def actual_values(family, z):
    if family == "cycle_equal":
        return z[0],z[1],z[2],z[3],scale(z[4],Fraction(1,2)),scale(z[4],Fraction(1,2))
    if family == "cycle_zero":
        return z[0],z[1],z[2],z[3],z[4],{}
    if family == "trans_equal":
        return z[0],scale(z[1],Fraction(1,2)),scale(z[1],Fraction(1,2)),z[2],z[3],z[4]
    if family == "trans_zero":
        return z[0],z[1],z[2],{},z[3],z[4]
    raise ValueError(family)


def invariant_forms(family,z):
    e,q1,q2,q3,v1,v2=actual_values(family,z)
    t=scale(add(q1,q2,q3),Fraction(1,3));c=scale(add(v1,v2),Fraction(1,2))
    x,y,zz=add(q1,scale(t,-1)),add(q2,scale(t,-1)),add(q3,scale(t,-1))
    r2=add(mul(x,x),mul(y,y),mul(zz,zz));u=mul(mul(x,y),zz);s2=mul(scale(add(v1,scale(v2,-1)),Fraction(1,2)),scale(add(v1,scale(v2,-1)),Fraction(1,2)))
    return e,t,c,r2,u,s2


def load_orbit(path):
    rows=[]
    with path.open(newline="",encoding="utf-8") as handle:
        for row in csv.DictReader(handle,delimiter="\t"):
            assert int(row["w"])==0
            rows.append((tuple(int(row[name]) for name in ("e","t","c","r2","u","s2")),Fraction(int(row["numerator"]),int(row["denominator"]))))
    return rows


def substitute(rows,forms):
    powers=[[power(form,k) for k in range(16)] for form in forms];out=defaultdict(Fraction)
    for exponent,coefficient in rows:
        term=const(coefficient)
        for i,k in enumerate(exponent):
            if k:term=mul(term,powers[i][k])
        for e,c in term.items():out[e]+=c
    return {e:c for e,c in out.items() if c}


def main():
    p=argparse.ArgumentParser();p.add_argument("orbit",type=Path);p.add_argument("output_dir",type=Path);p.add_argument("names",nargs="*");a=p.parse_args();a.output_dir.mkdir(parents=True,exist_ok=True);rows=load_orbit(a.orbit);summary={};selected=set(a.names)
    for name,(family,zforms) in charts().items():
        if selected and name not in selected: continue
        full=substitute(rows,invariant_forms(family,zforms));minimum=min(e[2] for e in full);assert minimum>=2
        quotient={tuple(k-(2 if i==2 else 0) for i,k in enumerate(e)):c for e,c in full.items()}
        with (a.output_dir/f"{name}.tsv").open("w",newline="",encoding="utf-8") as handle:
            w=csv.writer(handle,delimiter="\t",lineterminator="\n");w.writerow(("x","y","r","h","numerator","denominator"));[w.writerow((*e,c.numerator,c.denominator)) for e,c in sorted(quotient.items())]
        summary[name]={"family":family,"terms":len(quotient),"multidegrees":[max(e[i] for e in quotient) for i in range(4)],"minimum_removed_radial_degree":minimum,"positive_coefficients":sum(c>0 for c in quotient.values()),"negative_coefficients":sum(c<0 for c in quotient.values())}
    payload={"status":"PASS","epistemic_status":"PROVED","orbit_rows":len(rows),"charts":summary,"claim_boundary":"Exact invariant-route radial factor and quotient; sign remains unproved."};(a.output_dir/"blowup-summary.json").write_text(json.dumps(payload,indent=2,sort_keys=True)+"\n",encoding="utf-8");print(json.dumps(payload,sort_keys=True));return 0


if __name__=="__main__":raise SystemExit(main())
