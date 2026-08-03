#!/usr/bin/env python3
"""Direct Shintani correspondence on local residue-sign ray data."""
from __future__ import annotations

import argparse
import ast
import json
import subprocess
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
actionset(alpha,alphat,rm)={my(ord=unitperiod(rm),M=List());for(q=0,5,if(equiv(alphat,ggen^q*alpha,rm,ord),listput(M,q)));return(Set(Vec(M)));};
kernel(rm)={my(ord=unitperiod(rm),M=List());for(q=0,5,if(equiv(1,ggen^q,rm,ord),listput(M,q)));return(Set(Vec(M)));};
rayset(ra,rm)={my(R=bnrinit(K,[rm,one],1),M=List());for(e=0,5,if(raylog(R,idealpow(K,gideal,e))==raylog(R,ra),listput(M,e)));return(Set(Vec(M)));};
diffset(A,B)={my(M=List());for(i=1,#A,for(j=1,#B,listput(M,(B[j]-A[i])%6)));return(Set(Vec(M)));};
addset(A,B)={my(M=List());for(i=1,#A,for(j=1,#B,listput(M,(A[i]+B[j])%6)));return(Set(Vec(M)));};
modulus(n2,n3)={return(idealmul(K,idealpow(K,p2,n2),idealpow(K,p3,n3)));};
transitioncheck()={my(n=0);for(n2L=0,1,for(n3L=0,2,for(n2S=0,n2L,for(n3S=0,n3L,my(large=modulus(n2L,n3L),small=modulus(n2S,n3S),oL=unitperiod(large),oS=unitperiod(small),count=0);for(e=0,5,for(f=0,5,if(equiv(ggen^e,ggen^f,large,oL)&&!equiv(ggen^e,ggen^f,small,oS),error([n2L,n3L,n2S,n3S,e,f]));count++));print("TRANS=",[n2L,n3L,n2S,n3S,count]);n++))));return(n);};
audit(a,b)={my(x=[a,b],y=T(a,b),z=T(y[1],y[2]),back=T(z[1],z[2]),d0=data(a,b),d1=data(y[1],y[2]),d2=data(z[1],z[2]),m01=idealadd(K,d0[1],d1[1]),m12=idealadd(K,d1[1],d2[1]),m20=idealadd(K,d2[1],d0[1]),m012=idealadd(K,m01,d2[1]),D0=actionset(d0[3],d1[3],m01),D1=actionset(d1[3],d2[3],m12),D2=actionset(d2[3],d0[3],m20),triple=addset(addset(D0,D1),D2),K0=kernel(m012),E0=rayset(d0[2],d0[1]),E1=rayset(d1[2],d1[1]));if(back!=x,error(["T-order",x,back]));if(D0!=diffset(E0,E1),error(["edge",x,D0,diffset(E0,E1)]));if(triple!=K0,error(["third-return",x,triple,K0,mpair(m012)]));print("ROW=",[a,b,y,mpair(d0[1]),mpair(d1[1]),mpair(d2[1]),D0,triple]);};
print("TRANSITIONS=",transitioncheck());print("BASE=",[K.no,Vec(nfalgtobasis(K,beta)),Vec(nfalgtobasis(K,ggen)),sgnsel(ggen)]);for(a=0,5,for(b=0,5,audit(a,b)));quit();
'''


def exact_payload() -> dict[str, object]:
    run = subprocess.run(["gp", "-q"], input=GP, text=True, capture_output=True, check=True, timeout=120)
    rows: list[dict[str, object]] = []
    transitions = base = None
    for line in run.stdout.splitlines():
        if line.startswith("ROW="):
            a, b, successor, modulus, successor_modulus, third_modulus, direct_relation, third_return = ast.literal_eval(line.removeprefix("ROW="))
            rows.append({"characteristic": [a, b], "successor": successor, "modulus": modulus, "successor_modulus": successor_modulus, "third_modulus": third_modulus, "direct_action_relation": direct_relation, "third_return_kernel": third_return})
        elif line.startswith("TRANSITIONS="):
            transitions = int(line.removeprefix("TRANSITIONS="))
        elif line.startswith("BASE="):
            base = ast.literal_eval(line.removeprefix("BASE="))
    if run.stderr or len(rows) != 36 or transitions != 18 or base != [1, [2, 1], [-7, 1], -1]:
        raise AssertionError({"stderr": run.stderr, "rows": len(rows), "transitions": transitions, "base": base})
    if len({tuple(row["modulus"]) for row in rows}) != 6:
        raise AssertionError("incomplete lowered-modulus support")
    if any(not row["direct_action_relation"] for row in rows):
        raise AssertionError("empty direct action relation")
    anchor_rows = {tuple(row["characteristic"]): row for row in rows if tuple(row["characteristic"]) in {(3, 5), (3, 4)}}
    if set(anchor_rows) != {(3, 5), (3, 4)}:
        raise AssertionError(anchor_rows)
    return {
        "schema": "sic-stark-cycle-181-shintani-local-action-prototype-v1",
        "epistemic_status": "PROVED",
        "claim_boundary": "This exact finite result derives a set-valued Shintani correspondence from local residue-sign/global-unit quotient data and independently validates it against ray sets. It defines no additive coefficient operation, AFK interface, regulator equality, fusion theorem, or TCC identity.",
        "conventions": {"characteristic_action": "T(a,b)=(5a+b,-a) mod 6", "oriented_generator": "(4beta+1)=(beta-9)", "direct_relation": "alpha_Tx ~ u*(beta-9)^q*alpha_x modulo m_x+m_Tx with equal selected-place sign, u in {+/-beta^k}", "third_return": "sum of three direct relations equals the kernel at the triple conductor meet"},
        "summary": {"rows_checked": len(rows), "shintani_edges_checked": len(rows), "third_returns_checked": len(rows), "conductor_transitions_checked": transitions, "all_direct_relations_equal_independent_ray_differences": True, "all_third_returns_equal_kernel": True, "orientation_anchor_rows_present": True},
        "rows": rows,
        "gate_outcome": {"set_valued_shintani_action": "EXACT_DIRECT_CORRESPONDENCE_VALIDATED", "scope": "finite arithmetic action only; no coefficient operation"},
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
