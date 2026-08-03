#!/usr/bin/env python3
"""Exact compressed AFK-phase refinement of the local ray correspondence."""
from __future__ import annotations

import argparse
import ast
import json
import subprocess
from collections import defaultdict
from pathlib import Path


GP = r'''
K=bnfinit(y^2-5*y+1,1);if(bnfcertify(K)!=1||K.no!=1,error("base"));beta=Mod(y,y^2-5*y+1);p2=idealprimedec(K,2)[1];p3=idealprimedec(K,3)[1];m6=idealhnf(K,6);one=[1,0];gideal=idealhnf(K,4*beta+1);ggen=nfbasistoalg(K,bnfisprincipal(K,gideal)[2]);
T(a,b)={return([(5*a+b)%6,(-a)%6]);};
raylog(R,I)={my(v=bnrisprincipal(R,I,0));if(#v==0,return([]));return(Vec(v[1]));};
pos(a,b)={my(q=a,l);while(1,l=5*b-2*q;if(l>0&&l^2>21*b^2,return(q));q-=6;)};
sgn(x)={my(z=lift(x),a=polcoeff(z,0),b=polcoeff(z,1),t=2*a+5*b);if(b==0,return(if(t>0,1,-1)));if(b>0,return(if(t>0&&t^2>21*b^2,1,-1)));return(if(t>0||t^2<21*b^2,1,-1));};
zero(x,m)={my(a=idealval(K,m,p2),b=idealval(K,m,p3));if(x==0,return(1));return(idealval(K,idealhnf(K,x),p2)>=a&&idealval(K,idealhnf(K,x),p3)>=b);};
per(m)={for(k=1,36,if(zero(beta^k-1,m)&&sgn(beta^k)==1,return(k)));error("period");};
eq(x,y,m,o)={for(k=0,o-1,forstep(s=-1,1,2,if(zero(s*beta^k*x-y,m)&&sgn(s*beta^k*x)==sgn(y),return(1))));return(0);};
data(a,b)={my(q=pos(a,b),z=b*beta-q,i=idealhnf(K,z),c=idealadd(K,m6,i),m=idealdiv(K,m6,c),r=idealdiv(K,i,c),u=nfbasistoalg(K,bnfisprincipal(K,r)[2]));return([m,r,u]);};
pair(m)={return([idealval(K,m,p2),idealval(K,m,p3)]);};
set(u,m)={my(o=per(m),L=List());for(e=0,5,if(eq(u,ggen^e,m,o),listput(L,e)));return(Set(Vec(L)));};
rset(r,m)={my(R=bnrinit(K,[m,one],1),L=List());for(e=0,5,if(raylog(R,idealpow(K,gideal,e))==raylog(R,r),listput(L,e)));return(Set(Vec(L)));};
rel(u,v,m)={my(o=per(m),L=List());for(e=0,5,if(eq(v,ggen^e*u,m,o),listput(L,e)));return(Set(Vec(L)));};
setsum(A,B)={my(L=List());for(i=1,#A,for(j=1,#B,listput(L,(A[i]+B[j])%6)));return(Set(Vec(L)));};
diffset(A,B)={my(L=List());for(i=1,#A,for(j=1,#B,listput(L,(B[j]-A[i])%6)));return(Set(Vec(L)));};
audit(a,b)={my(y=T(a,b),z=T(y[1],y[2]),d=data(a,b),e=data(y[1],y[2]),f=data(z[1],z[2]),m1=idealadd(K,d[1],e[1]),m2=idealadd(K,e[1],f[1]),m3=idealadd(K,f[1],d[1]),mt=idealadd(K,m1,f[1]),E=set(d[3],d[1]),Ey=set(e[3],e[1]),A=rel(d[3],e[3],m1),B=rel(e[3],f[3],m2),C=rel(f[3],d[3],m3),K0=rel(1,1,mt),pa=(24*(6+7*(1+a)*(1+b))-12-28*(a^2-5*a*b+b^2))%48,py=(24*(6+7*(1+y[1])*(1+y[2]))-12-28*(y[1]^2-5*y[1]*y[2]+y[2]^2))%48,pz=(24*(6+7*(1+z[1])*(1+z[2]))-12-28*(z[1]^2-5*z[1]*z[2]+z[2]^2))%48,q=(py-pa)%48,q1=(pz-py)%48,q2=(pa-pz)%48);if(E!=rset(d[2],d[1])||Ey!=rset(e[2],e[1])||A!=diffset(E,Ey)||setsum(setsum(A,B),C)!=K0||(q+q1+q2)%48,error([a,b]));print("ROW=",[a,b,y,pair(d[1]),E,pa,A,q]);};
for(a=0,5,for(b=0,5,audit(a,b)));quit();
'''


def payload() -> dict[str, object]:
    run = subprocess.run(["gp", "-q"], input=GP, text=True, capture_output=True, check=True, timeout=120)
    rows = []
    for line in run.stdout.splitlines():
        if line.startswith("ROW="):
            a,b,succ,grade,coset,phase,relation,delta=ast.literal_eval(line[4:])
            rows.append({"characteristic":[a,b],"successor":succ,"grade":grade,"coset":coset,"phase_mod_48":phase,"relation":relation,"phase_delta_mod_48":delta})
    if run.stderr or len(rows)!=36: raise AssertionError({"stderr":run.stderr,"rows":len(rows)})
    key=lambda r:(tuple(r["grade"]),tuple(r["coset"]),r["phase_mod_48"])
    states=sorted({key(r) for r in rows})
    if not 0<len(states)<36: raise AssertionError(len(states))
    by={tuple(r["characteristic"]):r for r in rows}; edges=defaultdict(set)
    for r in rows: edges[key(r)].add(key(by[tuple(r["successor"])]))
    conflicts=[{"state":[list(s[0]),list(s[1]),s[2]],"successors":[[list(t[0]),list(t[1]),t[2]] for t in sorted(ts)]} for s,ts in sorted(edges.items()) if len(ts)>1]
    anchors={tuple(r["characteristic"]):key(r) for r in rows if tuple(r["characteristic"]) in {(3,5),(3,4)}}
    return {"schema":"sic-stark-cycle-184-multiplier-refined-correspondence-prototype-v1","epistemic_status":"PROVED","claim_boundary":"This exact finite result constructs a compressed multiplier-refined local ray correspondence and composition law only. It defines no AFK coefficient identification, Stark regulator equality, fusion theorem, or TCC identity.","summary":{"rows_checked":36,"compressed_state_count":len(states),"phase_value_count":len({r['phase_mod_48'] for r in rows}),"direct_ray_difference_validations":36,"all_direct_relations_equal_independent_ray_differences":True,"edge_compositions_checked":36,"third_compositions_checked":36,"strict_compression":len(states)<36,"deterministic_successor_conflict_count":len(conflicts),"anchors":{"3,5":[list(anchors[(3,5)][0]),list(anchors[(3,5)][1]),anchors[(3,5)][2]],"3,4":[list(anchors[(3,4)][0]),list(anchors[(3,4)][1]),anchors[(3,4)][2]]},"composition":"C6 set addition plus Z/48 addition; all third labels equal (kernel,0)"},"states":[[list(g),list(c),p] for g,c,p in states],"conflicts":conflicts,"rows":rows,"gate_outcome":{"multiplier_refined_correspondence":"COMPOSITION_VALIDATED","scope":"finite correspondence only"}}


def main() -> None:
    parser=argparse.ArgumentParser();parser.add_argument("--output",type=Path);args=parser.parse_args()
    text=json.dumps(payload(),indent=2,sort_keys=True)+"\n"
    if args.output:args.output.write_text(text)
    else:print(text,end="")


if __name__=="__main__":main()
