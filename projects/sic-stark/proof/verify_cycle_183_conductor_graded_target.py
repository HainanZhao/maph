#!/usr/bin/env python3
"""Exact deterministic Shintani action test on the conductor-graded target."""
from __future__ import annotations

import argparse
import ast
import json
import subprocess
from collections import defaultdict
from pathlib import Path


GP = r'''
K=bnfinit(y^2-5*y+1,1);if(bnfcertify(K)!=1||K.no!=1,error("base field certification or class number failed"));beta=Mod(y,y^2-5*y+1);p2=idealprimedec(K,2)[1];p3=idealprimedec(K,3)[1];m6=idealhnf(K,6);one=[1,0];gideal=idealhnf(K,4*beta+1);ggen=nfbasistoalg(K,bnfisprincipal(K,gideal)[2]);
T(a,b)={return([(5*a+b)%6,(-a)%6]);};
raylog(R,I)={my(v=bnrisprincipal(R,I,0));if(#v==0,return([]));return(Vec(v[1]));};
positive(a,b)={my(q=a,l);while(1,l=5*b-2*q;if(l>0&&l^2>21*b^2,return(q));q-=6;)};
sgnsel(x)={my(p=lift(x),a=polcoeff(p,0),b=polcoeff(p,1),t=2*a+5*b);if(b==0,return(if(t>0,1,-1)));if(b>0,return(if(t>0&&t^2>21*b^2,1,-1)));return(if(t>0||t^2<21*b^2,1,-1));};
cong0(x,rm)={my(n2=idealval(K,rm,p2),n3=idealval(K,rm,p3));if(x==0,return(1));return(idealval(K,idealhnf(K,x),p2)>=n2&&idealval(K,idealhnf(K,x),p3)>=n3);};
unitperiod(rm)={for(k=1,36,if(cong0(beta^k-1,rm)&&sgnsel(beta^k)==1,return(k)));error("unit image period exceeds cap");};
equiv(x,y,rm,ord)={for(k=0,ord-1,forstep(s=-1,1,2,if(cong0(s*beta^k*x-y,rm)&&sgnsel(s*beta^k*x)==sgnsel(y),return(1))));return(0);};
data(a,b)={my(q=positive(a,b),gamma=b*beta-q,gi=idealhnf(K,gamma),c=idealadd(K,m6,gi),rm=idealdiv(K,m6,c),ra=idealdiv(K,gi,c),alpha=nfbasistoalg(K,bnfisprincipal(K,ra)[2]));return([rm,ra,alpha]);};
mpair(rm)={return([idealval(K,rm,p2),idealval(K,rm,p3)]);};
assembled(alpha,rm)={my(ord=unitperiod(rm),M=List());for(e=0,5,if(equiv(alpha,ggen^e,rm,ord),listput(M,e)));return(Set(Vec(M)));};
rayset(ra,rm)={my(R=bnrinit(K,[rm,one],1),M=List());for(e=0,5,if(raylog(R,idealpow(K,gideal,e))==raylog(R,ra),listput(M,e)));return(Set(Vec(M)));};
audit(a,b)={my(y=T(a,b),d=data(a,b),A=assembled(d[3],d[1]),B=rayset(d[2],d[1]));if(A!=B,error([a,b,A,B]));print("ROW=",[a,b,y,mpair(d[1]),A]);};
print("BASE=",[K.no,Vec(nfalgtobasis(K,beta)),Vec(nfalgtobasis(K,ggen)),sgnsel(ggen)]);for(a=0,5,for(b=0,5,audit(a,b)));quit();
'''


EXPECTED_GRADES = {(0, 0), (0, 1), (0, 2), (1, 0), (1, 1), (1, 2)}
EXPECTED_DIMENSION = 14


def source_rows() -> list[dict[str, object]]:
    run = subprocess.run(["gp", "-q"], input=GP, text=True, capture_output=True, check=True, timeout=120)
    rows: list[dict[str, object]] = []
    base = None
    for line in run.stdout.splitlines():
        if line.startswith("ROW="):
            a, b, successor, grade, coset = ast.literal_eval(line.removeprefix("ROW="))
            rows.append({"characteristic": [a, b], "successor": successor, "grade": grade, "coset": coset})
        elif line.startswith("BASE="):
            base = ast.literal_eval(line.removeprefix("BASE="))
    if run.stderr or len(rows) != 36 or base != [1, [2, 1], [-7, 1], -1]:
        raise AssertionError({"stderr": run.stderr, "rows": len(rows), "base": base})
    if {tuple(row["grade"]) for row in rows} != EXPECTED_GRADES:
        raise AssertionError("grade support drift")
    return rows


def state(row: dict[str, object]) -> tuple[tuple[int, int], tuple[int, ...]]:
    return tuple(row["grade"]), tuple(row["coset"])


def build_payload() -> dict[str, object]:
    rows = source_rows()
    by_point = {tuple(row["characteristic"]): row for row in rows}
    states = sorted({state(row) for row in rows})
    if len(states) != EXPECTED_DIMENSION:
        raise AssertionError({"states": states, "dimension": len(states)})
    edges: dict[tuple[tuple[int, int], tuple[int, ...]], set[tuple[tuple[int, int], tuple[int, ...]]]] = defaultdict(set)
    for row in rows:
        edges[state(row)].add(state(by_point[tuple(row["successor"])]))
    conflicts = [
        {"source_state": {"grade": list(source[0]), "coset": list(source[1])}, "target_states": [{"grade": list(target[0]), "coset": list(target[1])} for target in sorted(targets)]}
        for source, targets in sorted(edges.items()) if len(targets) > 1
    ]
    anchors = {tuple(row["characteristic"]): state(row) for row in rows if tuple(row["characteristic"]) in {(3, 5), (3, 4)}}
    if anchors[(3, 5)][1] != (1,) or anchors[(3, 4)][1] != (2,):
        raise AssertionError(anchors)
    summary: dict[str, object] = {
        "rows_checked": len(rows), "graded_target_dimension": len(states), "graded_components": len({grade for grade, _coset in states}),
        "all_source_states_observed": len(states) == EXPECTED_DIMENSION, "deterministic_state_conflict_count": len(conflicts),
        "orientation_anchors": {"3,5": {"grade": list(anchors[(3, 5)][0]), "coset": list(anchors[(3, 5)][1])}, "3,4": {"grade": list(anchors[(3, 4)][0]), "coset": list(anchors[(3, 4)][1])}},
    }
    if conflicts:
        status = "CONDUCTOR_GRADED_DETERMINISTIC_ACTION_FALSIFIED"
    else:
        action = {source: next(iter(targets)) for source, targets in edges.items()}
        if set(action) != set(states) or set(action.values()) != set(states):
            raise AssertionError("action is not a graded-state permutation")
        for source in states:
            current = source
            for _ in range(3):
                current = action[current]
            if current != source:
                raise AssertionError(("third return", source, current))
        status = "CONDUCTOR_GRADED_DETERMINISTIC_ACTION_EXISTS"
        summary["all_third_returns_identity"] = True
    return {
        "schema": "sic-stark-cycle-183-conductor-graded-target-prototype-v1",
        "epistemic_status": "PROVED",
        "claim_boundary": "This exact finite result tests only whether the source-built conductor-graded coset states admit one deterministic Shintani action. It defines no AFK coefficient identification, Stark regulator equality, fusion theorem, or TCC identity.",
        "conventions": {"source": "Q[(Z/6Z)^2] with T(a,b)=(5a+b,-a)", "target": "direct sum of six Q[C6/K_m] components", "state": "(conductor grade, assembled exponent coset) without an exponent representative"},
        "summary": summary, "states": [{"grade": list(grade), "coset": list(coset)} for grade, coset in states], "conflicts": conflicts, "rows": rows,
        "gate_outcome": {"conductor_graded_deterministic_action": status, "scope": "finite graded deterministic action only"},
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    rendered = json.dumps(build_payload(), indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.write_text(rendered)
    else:
        print(rendered, end="")


if __name__ == "__main__":
    main()
