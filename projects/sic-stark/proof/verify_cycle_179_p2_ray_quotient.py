#!/usr/bin/env python3
"""Exact p2 ray-factor derivation and CRT admissible-set fibre test."""
from __future__ import annotations

import argparse
import ast
import json
import subprocess
from collections import Counter
from pathlib import Path


GP = r'''
K=bnfinit(y^2-5*y+1,1);if(bnfcertify(K)!=1,error("uncertified K"));beta=Mod(y,y^2-5*y+1);p2=idealprimedec(K,2)[1];p3=idealprimedec(K,3)[1];pi3=nfbasistoalg(K,bnfisprincipal(K,p3)[2]);m6=idealhnf(K,6);one=[1,0];gideal=idealhnf(K,4*beta+1);
raylog(R,I)={my(v=bnrisprincipal(R,I,0));if(#v==0,return([]));return(Vec(v[1]));};
positive(a,b)={my(q=a,l);while(1,l=5*b-2*q;if(l>0&&l^2>21*b^2,return(q));q-=6;)};
audit(a,b)={my(q=positive(a,b),gamma=b*beta-q,gi=idealhnf(K,gamma),c=idealadd(K,m6,gi),rm=idealdiv(K,m6,c),n2=idealval(K,rm,p2),v2=idealval(K,gi,p2),v3=idealval(K,gi,p3),z2=Vec(nfalgtobasis(K,gamma)),u3=gamma/pi3^v3,z3=Vec(nfalgtobasis(K,u3)),q2,ra,R,M=List());if(n2<0||n2>1,error("bad p2 exponent"));if(n2!=if(v2==0,1,0),error("lowered p2 exponent mismatch"));if(n2==1,q2=[z2[1]%2,z2[2]%2];if(q2==[0,0],error("nonunit p2 residue")),q2=[0,0]);ra=idealdiv(K,gi,c);R=bnrinit(K,[rm,one],1);for(e=0,5,if(raylog(R,idealpow(K,gideal,e))==raylog(R,ra),listput(M,e)));print("ROW=",[a,b,q,n2,q2,[v3%3,z3[1]%3,z3[2]%3,1],Vec(M)]);};
for(a=0,5,for(b=0,5,audit(a,b)));print("CHECK=",[idealval(K,m6,p2),idealnorm(K,p2),idealnorm(K,p3),raylog(bnrinit(K,[m6,one],1),gideal)]);quit();
'''

SENTINEL = (0, 0)
P2_UNITS = {(1, 0), (0, 1), (1, 1)}


def exact_rows() -> tuple[list[dict[str, object]], list[object]]:
    run = subprocess.run(["gp", "-q"], input=GP, text=True, capture_output=True, check=True, timeout=90)
    rows: list[dict[str, object]] = []
    checks: list[object] | None = None
    for line in run.stdout.splitlines():
        if line.startswith("ROW="):
            a, b, lift, n2, q2, p3, admissible = ast.literal_eval(line.removeprefix("ROW="))
            if not admissible:
                raise AssertionError((a, b, "empty admissible set"))
            q2_tuple = tuple(q2)
            if n2 == 1 and q2_tuple not in P2_UNITS:
                raise AssertionError((a, b, n2, q2))
            if n2 == 0 and q2_tuple != SENTINEL:
                raise AssertionError((a, b, n2, q2))
            rows.append({
                "characteristic": [a, b], "positive_lift": lift,
                "p2_conductor_exponent": n2, "p2_ray_factor_class": q2,
                "p3_local_record": p3, "admissible_exponents": admissible,
            })
        elif line.startswith("CHECK="):
            checks = ast.literal_eval(line.removeprefix("CHECK="))
    if run.stderr or len(rows) != 36 or checks != [1, 4, 3, [1]]:
        raise AssertionError({"stderr": run.stderr, "rows": len(rows), "checks": checks})
    return rows, checks


def canonical_transition(n2: int, q2: tuple[int, int]) -> tuple[int, int]:
    """The unique map Q2(p2) or Q2(1) to the trivial Q2(1) factor."""
    if n2 not in {0, 1}:
        raise AssertionError(n2)
    if n2 == 1 and q2 not in P2_UNITS:
        raise AssertionError(q2)
    if n2 == 0 and q2 != SENTINEL:
        raise AssertionError(q2)
    return SENTINEL


def build_payload() -> dict[str, object]:
    rows, checks = exact_rows()
    fibres: dict[tuple[int, ...], list[dict[str, object]]] = {}
    for row in rows:
        record = (row["p2_conductor_exponent"], *row["p2_ray_factor_class"], *row["p3_local_record"])
        fibres.setdefault(record, []).append(row)
        if canonical_transition(row["p2_conductor_exponent"], tuple(row["p2_ray_factor_class"])) != SENTINEL:
            raise AssertionError(row)
    nontrivial: list[dict[str, object]] = []
    empty: list[dict[str, object]] = []
    for record, fibre in sorted(fibres.items()):
        if len(fibre) < 2:
            continue
        common = set(fibre[0]["admissible_exponents"])
        for row in fibre[1:]:
            common &= set(row["admissible_exponents"])
        item = {
            "local_record": list(record),
            "characteristics": [row["characteristic"] for row in fibre],
            "admissible_sets": [row["admissible_exponents"] for row in fibre],
            "common_admissible_exponents": sorted(common),
        }
        nontrivial.append(item)
        if not common:
            empty.append(item)
    anchors = {tuple(row["characteristic"]): row["admissible_exponents"] for row in rows if tuple(row["characteristic"]) in {(3, 5), (3, 4)}}
    if 1 not in anchors[(3, 5)] or 2 not in anchors[(3, 4)]:
        raise AssertionError(anchors)
    p2_exp_counts = Counter(str(row["p2_conductor_exponent"]) for row in rows)
    p2_class_counts = Counter(f"{row['p2_conductor_exponent']}:{row['p2_ray_factor_class']}" for row in rows)
    return {
        "schema": "sic-stark-cycle-179-p2-ray-quotient-prototype-v1",
        "epistemic_status": "PROVED",
        "claim_boundary": "This exact finite result derives and tests only the prime-2 factor of the conductor-lowered ray exact sequence and its CRT fibres. It defines no additive coefficient operation, AFK interface, regulator equality, fusion theorem, or TCC identity.",
        "local_exact_sequence": {
            "statement": "For lowered m=p2^n2*m' with n2 in {0,1}, the p2 local finite ray factor is trivial for n2=0 and (O_K/p2)^times for n2=1; lowering p2 to 1 induces its unique projection to the trivial factor.",
            "verified_base_data": {"v_p2((6))": checks[0], "Norm(p2)": checks[1], "Norm(p3)": checks[2], "full_ray_generator_log": checks[3]},
            "unit_classes_mod_p2": sorted([list(v) for v in P2_UNITS]),
            "trivial_factor_sentinel": list(SENTINEL),
            "transition": "Q2(p2) -> Q2(1) is the canonical projection; all tested classes map to the sentinel.",
        },
        "summary": {
            "rows_checked": len(rows), "p2_conductor_exponent_counts": dict(sorted(p2_exp_counts.items())),
            "p2_factor_class_counts": dict(sorted(p2_class_counts.items())),
            "distinct_crt_records": len(fibres), "nontrivial_fibres": len(nontrivial),
            "empty_intersection_fibres": len(empty), "crt_set_compatibility": not empty,
            "anchor_admissible_sets": {"3,5": anchors[(3, 5)], "3,4": anchors[(3, 4)]},
        },
        "rows": rows, "nontrivial_fibres": nontrivial, "empty_intersection_fibres": empty,
        "gate_outcome": {"p2_quotient_to_admissible_set": "COMPATIBLE_ON_ALL_FIBRES" if not empty else "FALSIFIED_BY_EMPTY_SET_INTERSECTION", "scope": "finite local ray-factor compatibility only; singleton-fibre compatibility is vacuous"},
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
