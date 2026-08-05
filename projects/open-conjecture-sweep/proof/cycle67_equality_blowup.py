#!/usr/bin/env python3
"""Construct exact radial blow-up charts for the four C67 endpoint families."""

from __future__ import annotations

import argparse
import csv
import json
from collections import defaultdict
from fractions import Fraction
from pathlib import Path

N=4
Exponent=tuple[int,...]
Poly=dict[Exponent,Fraction]


def const(value=1): return {(0,)*N:Fraction(value)} if value else {}
def var(index):
    e=[0]*N;e[index]=1;return {tuple(e):Fraction(1)}
def add(*polys):
    out=defaultdict(Fraction)
    for p in polys:
        for e,c in p.items():out[e]+=c
    return {e:c for e,c in out.items() if c}
def scale(p,c): return {e:v*c for e,v in p.items() if v*c}
def mul(a,b):
    out=defaultdict(Fraction)
    for ea,ca in a.items():
        for eb,cb in b.items():out[tuple(x+y for x,y in zip(ea,eb))]+=ca*cb
    return {e:c for e,c in out.items() if c}
def power(p,n):
    out=const();base=p
    while n:
        if n&1:out=mul(out,base)
        n//=2
        if n:base=mul(base,base)
    return out
def one_minus(p): return add(const(),scale(p,-1))


X,Y,R,H=(var(i) for i in range(4))
ONE=const()


def stick_base():
    rest=one_minus(X)
    return X,mul(rest,Y),mul(rest,one_minus(Y))


def trans_distribution(total,radial,shape):
    center=scale(one_minus(radial),Fraction(1,3))
    p1=add(center,mul(radial,shape))
    p2=add(center,mul(radial,one_minus(shape)))
    p3=center
    return mul(total,p1),mul(total,p2),mul(total,p3)


def charts():
    result={}
    # cycle_equal: X,Y are the class-mass stick variables; R radial; H shape.
    e,t,c=stick_base();q1,q2,q3=trans_distribution(t,R,H)
    result["cycle_equal"]=("cycle_equal",[e,q1,q2,q3,c])

    # cycle_zero: X is e/(e+T), Y is trans boundary shape.
    for mode in ("cycle_dominant","trans_dominant"):
        cycle_mass=R if mode=="cycle_dominant" else mul(R,H)
        trans_radial=mul(R,H) if mode=="cycle_dominant" else R
        remaining=one_minus(cycle_mass)
        e=mul(remaining,X);t=mul(remaining,one_minus(X))
        q1,q2,q3=trans_distribution(t,trans_radial,Y)
        result[f"cycle_zero_{mode}"]=("cycle_zero",[e,q1,q2,q3,cycle_mass])

    # trans_equal: X,Y are class-mass stick variables. Two radial rectangles
    # and the two inequivalent directions on the two-equal line.
    for mode in ("trans_dominant","cycle_dominant"):
        tr=R if mode=="trans_dominant" else mul(R,H)
        cr=mul(R,H) if mode=="trans_dominant" else R
        e,t,c=stick_base()
        for direction in ("pair_large","singleton_large"):
            if direction=="pair_large":
                pair_mass=mul(t,add(FractionPoly(2,3),scale(tr,Fraction(1,3))))
                singleton=mul(t,scale(one_minus(tr),Fraction(1,3)))
            else:
                pair_mass=mul(t,scale(one_minus(tr),Fraction(2,3)))
                singleton=mul(t,add(FractionPoly(1,3),scale(tr,Fraction(2,3))))
            v1=mul(c,scale(add(ONE,cr),Fraction(1,2)))
            v2=mul(c,scale(one_minus(cr),Fraction(1,2)))
            result[f"trans_equal_{mode}_{direction}"]=("trans_equal",[e,pair_mass,singleton,v1,v2])

    # trans_zero: X is e/(e+C), Y splits the two positive transpositions.
    for mode in ("trans_mass_dominant","cycle_deviation_dominant"):
        t=R if mode=="trans_mass_dominant" else mul(R,H)
        cr=mul(R,H) if mode=="trans_mass_dominant" else R
        remaining=one_minus(t);e=mul(remaining,X);c=mul(remaining,one_minus(X))
        q1=mul(t,Y);q2=mul(t,one_minus(Y))
        v1=mul(c,scale(add(ONE,cr),Fraction(1,2)))
        v2=mul(c,scale(one_minus(cr),Fraction(1,2)))
        result[f"trans_zero_{mode}"]=("trans_zero",[e,q1,q2,v1,v2])
    return result


def FractionPoly(n,d): return const(Fraction(n,d))


def load(path):
    out={}
    with path.open(newline="",encoding="utf-8") as handle:
        for row in csv.DictReader(handle,delimiter="\t"):
            e=tuple(int(row[f"z{i}"]) for i in range(5))
            out[e]=Fraction(int(row["numerator"]),int(row["denominator"]))
    return out


def substitute(poly,forms):
    powers=[[power(form,k) for k in range(16)] for form in forms]
    out=defaultdict(Fraction)
    for exponent,coefficient in poly.items():
        term=const(coefficient)
        for i,k in enumerate(exponent):
            if k:term=mul(term,powers[i][k])
        for e,c in term.items():out[e]+=c
    return {e:c for e,c in out.items() if c}


def evaluate(poly,point):
    pp=[[x**k for k in range(32)] for x in point]
    return sum(c*__import__("math").prod(pp[i][k] for i,k in enumerate(e)) for e,c in poly.items())


def main():
    parser=argparse.ArgumentParser();parser.add_argument("pullback_dir",type=Path);parser.add_argument("output_dir",type=Path);args=parser.parse_args();args.output_dir.mkdir(parents=True,exist_ok=True)
    loaded={name:load(args.pullback_dir/f"{name}.tsv") for name in ("cycle_equal","cycle_zero","trans_equal","trans_zero")}
    summary={}
    control=(Fraction(2,7),Fraction(3,8),Fraction(1,3),Fraction(4,9))
    for name,(family,forms) in charts().items():
        full=substitute(loaded[family],forms)
        minimum_r=min(e[2] for e in full)
        assert minimum_r>=2
        quotient={tuple(value-(2 if i==2 else 0) for i,value in enumerate(e)):c for e,c in full.items()}
        # Check P(chart)=R^2 Q at one interior rational point.
        zpoint=tuple(evaluate(form,control) for form in forms)
        assert evaluate(loaded[family],zpoint)==control[2]**2*evaluate(quotient,control)
        with (args.output_dir/f"{name}.tsv").open("w",newline="",encoding="utf-8") as handle:
            w=csv.writer(handle,delimiter="\t",lineterminator="\n");w.writerow(("x","y","r","h","numerator","denominator"))
            for e,c in sorted(quotient.items()):w.writerow((*e,c.numerator,c.denominator))
        degrees=[max(e[i] for e in quotient) for i in range(4)]
        summary[name]={"family":family,"terms":len(quotient),"multidegrees":degrees,"minimum_removed_radial_degree":minimum_r,"positive_coefficients":sum(c>0 for c in quotient.values()),"negative_coefficients":sum(c<0 for c in quotient.values())}
    payload={"status":"PASS","epistemic_status":"PROVED","charts":summary,"claim_boundary":"Exact radial factor R^2 on nine charts covering equality neighborhoods; quotient sign remains unproved."}
    (args.output_dir/"blowup-summary.json").write_text(json.dumps(payload,indent=2,sort_keys=True)+"\n",encoding="utf-8");print(json.dumps(payload,sort_keys=True));return 0


if __name__=="__main__": raise SystemExit(main())
