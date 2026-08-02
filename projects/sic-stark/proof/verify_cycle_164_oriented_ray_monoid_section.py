#!/usr/bin/env python3
"""Exact finite prototype for Cycle 164's oriented ray-monoid section."""
from __future__ import annotations

import argparse
import ast
import json
import subprocess
import sys
from pathlib import Path


DIMENSION = 6
DISCRIMINANT = 21
ANCHORS = {(3, 5): 1, (3, 4): 2}

GP = r'''
K=bnfinit(y^2-5*y+1,1);
if(bnfcertify(K)!=1,error("base bnf certification failed"));
beta=Mod(y,y^2-5*y+1);
m=idealhnf(K,6);
oneplace=[1,0];
R6=bnrinit(K,[m,oneplace],1);
gideal=idealhnf(K,4*beta+1);
raylog(R,I)={my(v=bnrisprincipal(R,I,0));if(#v==0,return([]));return(Vec(v[1]));};
glog=raylog(R6,gideal);
positive_lift(a,b)={
  my(p=a,left);
  while(1,
    left=5*b-2*p;
    if(left>0 && left^2>21*b^2,return(p));
    p-=6;
  );
};
audit(a,b)=
{
  my(p=positive_lift(a,b),gamma=b*beta-p,gi=idealhnf(K,gamma));
  my(c=idealadd(K,m,gi),rm=idealdiv(K,m,c),ra=idealdiv(K,gi,c));
  my(R=bnrinit(K,[rm,oneplace],1),target=raylog(R,ra));
  my(matches=List(),image);
  for(e=0,5,image=raylog(R,idealpow(K,gideal,e));if(image==target,listput(matches,e)));
  my(direct=-1);
  if(idealnorm(K,c)==1,direct=raylog(R6,gi));
  print("ROW=",[a,b,p,norm(gamma),idealnorm(K,c),idealnorm(K,rm),[rm[1,1],rm[1,2],rm[2,1],rm[2,2]],[ra[1,1],ra[1,2],ra[2,1],ra[2,2]],Vec(R.cyc),target,Vec(matches),direct]);
};
for(a=0,5,for(b=0,5,audit(a,b)));
print("BASE=",[Vec(R6.cyc),glog]);
print("PARI_VERSION=",version());
quit;
'''


def is_positive_at_selected_embedding(b: int, lift: int) -> bool:
    """Exactly decide b*(5-sqrt(21))/2-lift > 0."""
    left = 5 * b - 2 * lift
    return left > 0 and left * left > DISCRIMINANT * b * b


def positive_lift(a: int, b: int) -> int:
    for candidate in range(a, a - 4 * DIMENSION, -DIMENSION):
        if is_positive_at_selected_embedding(b, candidate):
            if is_positive_at_selected_embedding(b, candidate + DIMENSION):
                raise AssertionError("positive lift was not maximal")
            return candidate
    raise AssertionError("positive lift search exceeded frozen finite range")


def run_gp() -> tuple[list[dict[str, object]], list[object], str]:
    run = subprocess.run(
        ["gp", "-q"], input=GP, text=True, capture_output=True, check=True, timeout=60
    )
    rows: list[dict[str, object]] = []
    base: list[object] | None = None
    version: str | None = None
    for line in run.stdout.splitlines():
        if line.startswith("ROW="):
            values = ast.literal_eval(line.removeprefix("ROW="))
            (a, b, lift, gamma_norm, common_norm, reduced_modulus_norm,
             reduced_modulus_hnf, reduced_ideal_hnf, reduced_ray_cyc,
             reduced_ideal_ray_log, matches, direct_full_ray_log) = values
            if lift != positive_lift(a, b):
                raise AssertionError((a, b, lift, positive_lift(a, b)))
            if gamma_norm != lift * lift - 5 * lift * b + b * b:
                raise AssertionError((a, b, lift, gamma_norm))
            if common_norm * reduced_modulus_norm != DIMENSION * DIMENSION:
                raise AssertionError((a, b, common_norm, reduced_modulus_norm))
            rows.append({
                "characteristic": [a, b], "positive_lift": lift,
                "norm_gamma": gamma_norm, "common_ideal_norm": common_norm,
                "reduced_finite_modulus_norm": reduced_modulus_norm,
                "reduced_finite_modulus_hnf": reduced_modulus_hnf,
                "reduced_ideal_hnf": reduced_ideal_hnf,
                "reduced_ray_cyc": reduced_ray_cyc,
                "reduced_ideal_ray_log": reduced_ideal_ray_log,
                "matching_source_exponents": matches,
                "least_section_exponent": matches[0] if matches else None,
                "direct_full_ray_log": direct_full_ray_log,
            })
        elif line.startswith("BASE="):
            base = ast.literal_eval(line.removeprefix("BASE="))
        elif line.startswith("PARI_VERSION="):
            version = ".".join(
                str(piece) for piece in ast.literal_eval(line.removeprefix("PARI_VERSION="))
            )
    if run.stderr:
        raise AssertionError(f"PARI stderr: {run.stderr}")
    if len(rows) != 36 or base is None or version is None:
        raise AssertionError((len(rows), base, version))
    return rows, base, version


def build_payload() -> dict[str, object]:
    rows, base, version = run_gp()
    if version != "2.15.4":
        raise AssertionError(f"expected PARI/GP 2.15.4, found {version}")
    source_cyc, generator_log = base
    if source_cyc != [6] or generator_log != [1]:
        raise AssertionError((source_cyc, generator_log))
    if any(not row["matching_source_exponents"] for row in rows):
        raise AssertionError("a reduced ideal lies outside the projected source image")
    full_rows = [row for row in rows if row["common_ideal_norm"] == 1]
    for row in full_rows:
        direct = row["direct_full_ray_log"]
        if not isinstance(direct, list) or len(direct) != 1:
            raise AssertionError(("missing direct full-ray coordinate", row))
        if row["least_section_exponent"] != direct[0]:
            raise AssertionError(("full-modulus recovery failed", row))
    by_point = {tuple(row["characteristic"]): row for row in rows}
    for point, expected in ANCHORS.items():
        if by_point[point]["least_section_exponent"] != expected:
            raise AssertionError(("orientation anchor failed", point, by_point[point]))
    return {
        "schema": "sic-stark-cycle-164-oriented-ray-monoid-section-prototype-v1",
        "epistemic_status": "PROVED",
        "claim_boundary": (
            "This exact finite computation constructs and tests a conductor-lowered "
            "ray-monoid section only. It defines no additive coefficient-to-logarithm "
            "operation, finite part, AFK cocycle, Stark identity, fusion theorem, or TCC identity."
        ),
        "conventions": {
            "field": "Q(sqrt(21)); beta^2-5*beta+1=0",
            "selected_embedding": "beta'=(5-sqrt(21))/2",
            "positive_lift": "largest p*=a mod 6 with b*beta'-p*>0",
            "principal_representative": "gamma=b*beta-p*",
            "lowering": "c=(6)+(gamma); m_ab=(6)/c; a_ab=(gamma)/c",
            "one_place_modulus": "the beta' real place, PARI selector [1,0]",
            "common_target": "G6=Cl_{(6)infinity_2} with g=[(4beta+1)]",
            "section": "least e in {0,...,5} with pi_ab(g^e)=[a_ab]",
        },
        "source": {"ray_cyc": source_cyc, "generator_log": generator_log},
        "summary": {
            "rows_checked": len(rows), "full_modulus_rows": len(full_rows),
            "lowered_modulus_rows": len(rows) - len(full_rows),
            "all_rows_in_projected_source_image": True,
            "full_modulus_recovery": True,
            "orientation_anchors": {
                f"{a},{b}": by_point[(a, b)]["least_section_exponent"] for a, b in ANCHORS
            },
            "section_exponent_histogram": {
                str(exponent): sum(row["least_section_exponent"] == exponent for row in rows)
                for exponent in range(DIMENSION)
            },
        },
        "rows": rows,
        "replay": {
            "command": "python3 proof/verify_cycle_164_oriented_ray_monoid_section.py",
            "python_version": sys.version.split()[0], "pari_version": version,
        },
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    payload = build_payload()
    encoded = json.dumps(payload, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.write_text(encoded, encoding="utf-8")
    else:
        print(encoded, end="")


if __name__ == "__main__":
    main()
