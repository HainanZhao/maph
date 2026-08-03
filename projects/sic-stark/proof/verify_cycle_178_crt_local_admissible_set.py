#!/usr/bin/env python3
"""CRT local-record fibres versus intrinsic admissible ray-exponent sets."""
from __future__ import annotations

import argparse
import ast
import json
import subprocess
from pathlib import Path


GP = r'''
K=bnfinit(y^2-5*y+1,1);if(bnfcertify(K)!=1,error("uncertified K"));beta=Mod(y,y^2-5*y+1);p2=idealprimedec(K,2)[1];p3=idealprimedec(K,3)[1];pi2=nfbasistoalg(K,bnfisprincipal(K,p2)[2]);pi3=nfbasistoalg(K,bnfisprincipal(K,p3)[2]);m=idealhnf(K,6);one=[1,0];gideal=idealhnf(K,4*beta+1);
raylog(R,I)={my(v=bnrisprincipal(R,I,0));if(#v==0,return([]));return(Vec(v[1]));};
positive(a,b)={my(q=a,l);while(1,l=5*b-2*q;if(l>0&&l^2>21*b^2,return(q));q-=6;)};
audit(a,b)={my(q=positive(a,b),gamma=b*beta-q,v2=idealval(K,idealhnf(K,gamma),p2),v3=idealval(K,idealhnf(K,gamma),p3),u2=gamma/pi2^v2,u3=gamma/pi3^v3,z2=Vec(nfalgtobasis(K,u2)),z3=Vec(nfalgtobasis(K,u3)),c=idealadd(K,m,idealhnf(K,gamma)),rm=idealdiv(K,m,c),ra=idealdiv(K,idealhnf(K,gamma),c),R=bnrinit(K,[rm,one],1),M=List());for(e=0,5,if(raylog(R,idealpow(K,gideal,e))==raylog(R,ra),listput(M,e)));print("ROW=",[a,b,q,[v2,z2[1]%2,z2[2]%2,v3%3,z3[1]%3,z3[2]%3,1],Vec(M)]);};
for(a=0,5,for(b=0,5,audit(a,b)));print("PI2_VAL=",idealval(K,pi2,p2));print("PI3_VAL=",idealval(K,pi3,p3));print("G_LOG=",raylog(bnrinit(K,[m,one],1),gideal));quit();
'''


def exact_rows() -> list[dict[str, object]]:
    run = subprocess.run(["gp", "-q"], input=GP, text=True, capture_output=True, check=True)
    rows: list[dict[str, object]] = []
    checks: dict[str, object] = {}
    for line in run.stdout.splitlines():
        if line.startswith("ROW="):
            a, b, lift, record, admissible = ast.literal_eval(line.removeprefix("ROW="))
            if not admissible:
                raise AssertionError((a, b, "empty admissible set"))
            rows.append({"characteristic": [a, b], "positive_lift": lift, "crt_local_record": record, "admissible_exponents": admissible})
        elif "=" in line:
            key, value = line.split("=", 1)
            checks[key] = ast.literal_eval(value)
    if run.stderr or len(rows) != 36 or checks != {"PI2_VAL": 1, "PI3_VAL": 1, "G_LOG": [1]}:
        raise AssertionError({"stderr": run.stderr, "rows": len(rows), "checks": checks})
    return rows


def build_payload() -> dict[str, object]:
    rows = exact_rows()
    fibres: dict[tuple[int, ...], list[dict[str, object]]] = {}
    for row in rows:
        fibres.setdefault(tuple(row["crt_local_record"]), []).append(row)
    nontrivial = []
    empty_intersection = []
    for record, fibre in sorted(fibres.items()):
        if len(fibre) < 2:
            continue
        common = set(fibre[0]["admissible_exponents"])
        for row in fibre[1:]:
            common &= set(row["admissible_exponents"])
        item = {"crt_local_record": list(record), "characteristics": [row["characteristic"] for row in fibre], "admissible_sets": [row["admissible_exponents"] for row in fibre], "common_admissible_exponents": sorted(common)}
        nontrivial.append(item)
        if not common:
            empty_intersection.append(item)
    anchor_sets = {tuple(row["characteristic"]): row["admissible_exponents"] for row in rows if tuple(row["characteristic"]) in {(3, 5), (3, 4)}}
    if 1 not in anchor_sets[(3, 5)] or 2 not in anchor_sets[(3, 4)]:
        raise AssertionError(anchor_sets)
    return {
        "schema": "sic-stark-cycle-178-crt-local-admissible-set-prototype-v1",
        "epistemic_status": "PROVED",
        "claim_boundary": "This exact finite result compares a preregistered CRT local record only with conductor-lowered admissible ray-exponent sets. It defines no selected ray-label map, additive coefficient operation, AFK interface, regulator equality, fusion theorem, or TCC identity.",
        "summary": {"rows_checked": len(rows), "distinct_crt_records": len(fibres), "nontrivial_fibres": len(nontrivial), "empty_intersection_fibres": len(empty_intersection), "crt_set_compatibility": not empty_intersection, "anchor_admissible_sets": {"3,5": anchor_sets[(3, 5)], "3,4": anchor_sets[(3, 4)]}},
        "rows": rows,
        "nontrivial_fibres": nontrivial,
        "empty_intersection_fibres": empty_intersection,
        "gate_outcome": {"crt_record_to_admissible_set": "COMPATIBLE_ON_ALL_FIBRES" if not empty_intersection else "FALSIFIED_BY_EMPTY_SET_INTERSECTION", "scope": "finite source-side compatibility only; no coefficient operation"},
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
