#!/usr/bin/env python3
"""Exact local-global assembly of lowered ray-exponent sets."""
from __future__ import annotations

import argparse
import ast
import json
import subprocess
from pathlib import Path


GP = r'''
K=bnfinit(y^2-5*y+1,1);if(bnfcertify(K)!=1||K.no!=1,error("base field certification or class number failed"));beta=Mod(y,y^2-5*y+1);p2=idealprimedec(K,2)[1];p3=idealprimedec(K,3)[1];m6=idealhnf(K,6);one=[1,0];gideal=idealhnf(K,4*beta+1);ggen=nfbasistoalg(K,bnfisprincipal(K,gideal)[2]);
raylog(R,I)={my(v=bnrisprincipal(R,I,0));if(#v==0,return([]));return(Vec(v[1]));};
positive(a,b)={my(q=a,l);while(1,l=5*b-2*q;if(l>0&&l^2>21*b^2,return(q));q-=6;)};
sgnsel(x)={my(p=lift(x),a=polcoeff(p,0),b=polcoeff(p,1),t=2*a+5*b);if(b==0,return(if(t>0,1,-1)));if(b>0,return(if(t>0&&t^2>21*b^2,1,-1)));return(if(t>0||t^2<21*b^2,1,-1));};
cong0(x,rm)={my(n2=idealval(K,rm,p2),n3=idealval(K,rm,p3));if(x==0,return(1));return(idealval(K,idealhnf(K,x),p2)>=n2&&idealval(K,idealhnf(K,x),p3)>=n3);};
unitperiod(rm)={for(k=1,36,if(cong0(beta^k-1,rm)&&sgnsel(beta^k)==1,return(k)));error("unit image period exceeds cap");};
equiv(x,y,rm,ord)={for(k=0,ord-1,forstep(s=-1,1,2,if(cong0(s*beta^k*x-y,rm)&&sgnsel(s*beta^k*x)==sgnsel(y),return(1))));return(0);};
modulus(n2,n3)={return(idealmul(K,idealpow(K,p2,n2),idealpow(K,p3,n3)));};
rayorder(R)={my(v=Vec(R.cyc),z=1);for(i=1,#v,z*=v[i]);return(z);};
phi(n2,n3)={my(z=1);if(n2>0,z*=3);if(n3==1,z*=2);if(n3==2,z*=6);return(z);};
imageorder(rm,ord)={my(z=0);for(e=0,5,my(new=1);for(f=0,e-1,if(equiv(ggen^e,ggen^f,rm,ord),new=0));if(new,z++));return(z);};
power_set(alpha,rm,ord)={my(M=List());for(e=0,5,if(equiv(alpha,ggen^e,rm,ord),listput(M,e)));return(Vec(M));};
audit(a,b)={my(q=positive(a,b),gamma=b*beta-q,gi=idealhnf(K,gamma),c=idealadd(K,m6,gi),rm=idealdiv(K,m6,c),ra=idealdiv(K,gi,c),n2=idealval(K,rm,p2),n3=idealval(K,rm,p3),alpha=nfbasistoalg(K,bnfisprincipal(K,ra)[2]),R=bnrinit(K,[rm,one],1),ord=unitperiod(rm),A=power_set(alpha,rm,ord),B=List());for(e=0,5,if(raylog(R,idealpow(K,gideal,e))==raylog(R,ra),listput(B,e)));if(A!=Vec(B),error([a,b,n2,n3,alpha,A,Vec(B)]));print("ROW=",[a,b,q,n2,n3,ord,A]);};
for(n2=0,1,for(n3=0,2,my(rm=modulus(n2,n3),R=bnrinit(K,[rm,one],1),ord=unitperiod(rm),o=rayorder(R),im=imageorder(rm,ord),f=phi(n2,n3));if(f/ord!=o||im!=o,error([n2,n3,f,ord,o,im]));print("MOD=",[n2,n3,f,ord,o,Vec(R.cyc)])));
for(n2L=0,1,for(n3L=0,2,for(n2S=0,n2L,for(n3S=0,n3L,my(large=modulus(n2L,n3L),small=modulus(n2S,n3S),RL=bnrinit(K,[large,one],1),RS=bnrinit(K,[small,one],1),oL=unitperiod(large),oS=unitperiod(small),count=0);for(e=0,5,for(f=0,5,my(AL=equiv(ggen^e,ggen^f,large,oL),AS=equiv(ggen^e,ggen^f,small,oS),BL=(raylog(RL,idealpow(K,gideal,e))==raylog(RL,idealpow(K,gideal,f))),BS=(raylog(RS,idealpow(K,gideal,e))==raylog(RS,idealpow(K,gideal,f))));if(AL!=BL||AS!=BS||AL&&!AS,error([n2L,n3L,n2S,n3S,e,f,AL,AS,BL,BS]));count++));print("TRANS=",[n2L,n3L,n2S,n3S,count])))));
print("BASE=",[K.no,Vec(nfalgtobasis(K,beta)),Vec(nfalgtobasis(K,ggen)),sgnsel(ggen)]);for(a=0,5,for(b=0,5,audit(a,b)));quit();
'''


EXPECTED_MODULI = {(0, 0), (0, 1), (0, 2), (1, 0), (1, 1), (1, 2)}


def exact_payload() -> dict[str, object]:
    run = subprocess.run(["gp", "-q"], input=GP, text=True, capture_output=True, check=True, timeout=120)
    rows: list[dict[str, object]] = []
    moduli: list[dict[str, object]] = []
    transitions: list[dict[str, object]] = []
    base: list[object] | None = None
    for line in run.stdout.splitlines():
        if line.startswith("ROW="):
            a, b, lift, n2, n3, period, assembled = ast.literal_eval(line.removeprefix("ROW="))
            rows.append({"characteristic": [a, b], "positive_lift": lift, "conductor_exponents": [n2, n3], "positive_unit_period": period, "assembled_admissible_exponents": assembled})
        elif line.startswith("MOD="):
            n2, n3, finite_order, period, quotient_order, ray_cyc = ast.literal_eval(line.removeprefix("MOD="))
            moduli.append({"conductor_exponents": [n2, n3], "finite_local_unit_order": finite_order, "positive_unit_image_period": period, "exact_sequence_quotient_order": quotient_order, "ray_cyc": ray_cyc})
        elif line.startswith("TRANS="):
            n2l, n3l, n2s, n3s, checks = ast.literal_eval(line.removeprefix("TRANS="))
            transitions.append({"from": [n2l, n3l], "to": [n2s, n3s], "source_power_pairs_checked": checks})
        elif line.startswith("BASE="):
            base = ast.literal_eval(line.removeprefix("BASE="))
    if run.stderr or len(rows) != 36 or len(moduli) != 6 or base != [1, [2, 1], [-7, 1], -1]:
        raise AssertionError({"stderr": run.stderr, "rows": len(rows), "moduli": moduli, "base": base})
    if {tuple(item["conductor_exponents"]) for item in moduli} != EXPECTED_MODULI:
        raise AssertionError(moduli)
    expected_transitions = sum((n2 + 1) * (n3 + 1) for n2, n3 in EXPECTED_MODULI)
    if len(transitions) != expected_transitions or any(item["source_power_pairs_checked"] != 36 for item in transitions):
        raise AssertionError(transitions)
    anchors = {tuple(row["characteristic"]): row["assembled_admissible_exponents"] for row in rows if tuple(row["characteristic"]) in {(3, 5), (3, 4)}}
    if anchors != {(3, 5): [1], (3, 4): [2]}:
        raise AssertionError(anchors)
    return {
        "schema": "sic-stark-cycle-180-local-global-artin-assembly-prototype-v1",
        "epistemic_status": "PROVED",
        "claim_boundary": "This exact finite result reconstructs conductor-lowered ray-exponent sets from local residue-sign classes modulo the exact global-unit image, and independently compares them with ray arithmetic. It defines no additive coefficient operation, AFK interface, regulator equality, fusion theorem, or TCC identity.",
        "unit_theorem": {"ordinary_class_number": base[0], "fundamental_unit": "beta", "full_unit_group": "{+/- beta^k : k in Z}", "oriented_source_generator": "(4beta+1)=(beta-9)", "selected_place_sign_of_generator": base[3]},
        "summary": {"rows_checked": len(rows), "distinct_lowered_moduli": len(moduli), "transition_maps_checked": len(transitions), "source_power_pairs_per_transition": 36, "all_assembled_sets_equal_independent_ray_sets": True, "orientation_anchors": {"3,5": anchors[(3, 5)], "3,4": anchors[(3, 4)]}},
        "moduli": moduli, "transitions": transitions, "rows": rows,
        "gate_outcome": {"local_global_assembly": "EXACT_ASSEMBLY_VALIDATED", "scope": "finite ray-class assembly only; no coefficient operation"},
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    rendered = json.dumps(exact_payload(), indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.write_text(rendered)
    else:
        print(rendered, end="")


if __name__ == "__main__":
    main()
