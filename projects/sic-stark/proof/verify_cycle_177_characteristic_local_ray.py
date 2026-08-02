#!/usr/bin/env python3
"""Direct arithmetic local-record-to-ray collision test on all 36 rows."""
from __future__ import annotations

import argparse
import ast
import json
import subprocess
from pathlib import Path


GP = r'''
K=bnfinit(y^2-5*y+1,1);if(bnfcertify(K)!=1,error("uncertified K"));beta=Mod(y,y^2-5*y+1);p3=idealprimedec(K,3)[1];pi=nfbasistoalg(K,bnfisprincipal(K,p3)[2]);m=idealhnf(K,6);one=[1,0];gideal=idealhnf(K,4*beta+1);
raylog(R,I)={my(v=bnrisprincipal(R,I,0));if(#v==0,return([]));return(Vec(v[1]));};
positive(a,b)={my(q=a,l);while(1,l=5*b-2*q;if(l>0&&l^2>21*b^2,return(q));q-=6;)};
audit(a,b)={my(q=positive(a,b),gamma=b*beta-q,v=idealval(K,idealhnf(K,gamma),p3),u=gamma/pi^v,z=Vec(nfalgtobasis(K,u)),c=idealadd(K,m,idealhnf(K,gamma)),rm=idealdiv(K,m,c),ra=idealdiv(K,idealhnf(K,gamma),c),R=bnrinit(K,[rm,one],1),M=List());for(e=0,5,if(raylog(R,idealpow(K,gideal,e))==raylog(R,ra),listput(M,e)));print("ROW=",[a,b,q,[v%3,z[1]%3,z[2]%3,1],Vec(M)]);};
for(a=0,5,for(b=0,5,audit(a,b)));print("PI_VAL=",idealval(K,pi,p3));print("G_LOG=",raylog(bnrinit(K,[m,one],1),gideal));quit();
'''


def exact_rows() -> list[dict[str, object]]:
    run = subprocess.run(["gp", "-q"], input=GP, text=True, capture_output=True, check=True)
    rows = []
    pi_val = generator_log = None
    for line in run.stdout.splitlines():
        if line.startswith("ROW="):
            a, b, lift, record, matches = ast.literal_eval(line.removeprefix("ROW="))
            if not matches:
                raise AssertionError((a, b, "no ray representative"))
            rows.append({"characteristic": [a, b], "positive_lift": lift, "local_record": record, "ray_label": matches[0], "all_matching_exponents": matches})
        elif line.startswith("PI_VAL="):
            pi_val = int(line.removeprefix("PI_VAL="))
        elif line.startswith("G_LOG="):
            generator_log = ast.literal_eval(line.removeprefix("G_LOG="))
    if run.stderr or len(rows) != 36 or pi_val != 1 or generator_log != [1]:
        raise AssertionError({"stderr": run.stderr, "rows": len(rows), "pi_val": pi_val, "generator_log": generator_log})
    return rows


def build_payload() -> dict[str, object]:
    rows = exact_rows()
    records: dict[tuple[int, ...], set[int]] = {}
    for row in rows:
        records.setdefault(tuple(row["local_record"]), set()).add(row["ray_label"])
    collisions = [
        {"local_record": list(record), "ray_labels": sorted(labels)}
        for record, labels in sorted(records.items()) if len(labels) > 1
    ]
    anchors = {tuple(row["characteristic"]): row["ray_label"] for row in rows if tuple(row["characteristic"]) in {(3, 5), (3, 4)}}
    if anchors != {(3, 5): 1, (3, 4): 2}:
        raise AssertionError(anchors)
    return {
        "schema": "sic-stark-cycle-177-characteristic-local-ray-prototype-v1",
        "epistemic_status": "PROVED",
        "claim_boundary": "This exact finite result tests only whether the preregistered ramified local record determines the conductor-lowered ray label. It defines no additive coefficient operation, AFK interface, regulator equality, fusion theorem, or TCC identity.",
        "summary": {"rows_checked": len(rows), "distinct_local_records": len(records), "collision_count": len(collisions), "map_determinacy": not collisions, "orientation_anchors": {"3,5": 1, "3,4": 2}},
        "rows": [{**row, "local_pairing_value_mod_3": (2 * row["ray_label"]) % 3} for row in rows],
        "collisions": collisions,
        "gate_outcome": {"local_record_to_ray_map": "DETERMINES_ALL_LABELS" if not collisions else "FALSIFIED_BY_LOCAL_RECORD_COLLISION", "scope": "finite arithmetic determinacy only; no coefficient operation"},
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
