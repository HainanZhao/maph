#!/usr/bin/env python3
"""Cycle 25 twelve-class quadratic-character refinement of Cycle 24."""
from __future__ import annotations
import csv, math, multiprocessing, json, time
from pathlib import Path
import sys
import numpy as np

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"discovery"))
import lrc_crt_fourier_class as core
import lrc_coupled_incidence as cycle21
import lrc_pair_choice as direct
import lrc_width_four_stage_a as width4

OUT=ROOT/"discovery/out/cycle25-quadratic-crt"
PRIOR=ROOT/"discovery/out/cycle24-crt-fourier-class/results.tsv"
P,C,K=cycle21.P,cycle21.C,cycle21.K
CLASSES=tuple((alpha,beta) for alpha in (0,1,2) for beta in (1,2,7,14))
INDEX={v:i for i,v in enumerate(CLASSES)}
STAGE_SECONDS=3000

def alpha_type(alpha):
    if alpha==0:return 0
    return 1 if pow(alpha,(P-1)//2,P)==1 else 2
def class_of_time(point): return alpha_type(point%P),math.gcd(point%C,C)
def class_indices(): return np.asarray([INDEX[class_of_time(t)] for t in range(P*C)],dtype=np.int8)
def class_cardinalities():
    v=np.bincount(class_indices(),minlength=12).astype(np.int64)
    if tuple(v)!=(6,6,1,1,594,594,99,99,594,594,99,99):raise AssertionError(tuple(v))
    return v

def quadratic_ramanujan_basis():
    """Integer evaluation matrix for the prescribed twelve class functions.

    The alpha factors are 1, the quadratic character extended by zero, and
    the alpha-zero indicator; the beta factors are the four divisor
    Ramanujan functions.  Their tensor evaluations must span the full
    class-constant space before the LP family is interpreted.
    """
    rows=[]
    for atype, divisor in CLASSES:
        alpha=(1,0 if atype==0 else (1 if atype==1 else -1),1 if atype==0 else 0)
        beta=0 if divisor==14 else divisor
        beta_basis=tuple(core.ramanujan_sum(modulus,beta) for modulus in (1,2,7,14))
        rows.append([left*right for left in alpha for right in beta_basis])
    determinant=core.bareiss_determinant(rows)
    if determinant==0: raise AssertionError("quadratic/Ramanujan class basis is singular")
    return rows
def targets():
    with PRIOR.open(newline="",encoding="utf-8") as h:r=list(csv.DictReader(h,delimiter="\t"))
    if len(r)!=60 or any(x["status"]!="UNRESOLVED" for x in r):raise AssertionError("target boundary")
    return r
def control():
    counts=class_cardinalities()
    for base_index in (3,4):
      base=cycle21.read_bases()[base_index]; coverage=width4.raw_coverage(direct.CNFS[base_index])
      for t in range(P*C):
       for j in range(K):
        for d in range(C):
         if bool(coverage[t,j,d])!=cycle21.crt_is_bad(K,P,C,base[j]+P*d,t):raise AssertionError(f"CRT mismatch {base_index},{t},{j},{d}")
    return {"status":"PASS","cardinalities":list(map(int,counts)),"quadratic_counts":{"zero":1,"residue":99,"nonresidue":99},"basis_determinant":core.bareiss_determinant(quadratic_ramanujan_basis())}

# Rebind only this process's imported module; no sealed Cycle-24 source changes.
core.CLASSES=CLASSES; core.CLASS_INDEX=INDEX; core.class_of_time=class_of_time
core.class_indices=class_indices; core.class_cardinalities=class_cardinalities

def main():
    OUT.mkdir(parents=True,exist_ok=True); (OUT/"control.json").write_text(json.dumps(control(),indent=2,sort_keys=True)+"\n")
    start=time.monotonic(); deadline=start+STAGE_SECONDS
    with multiprocessing.Pool(processes=3) as pool: rows=pool.map(core.solve,[(r,deadline) for r in targets()],chunksize=1)
    (OUT/"results.tsv").write_text("\t".join(core.Result._fields)+"\n"+"\n".join("\t".join(map(str,r)) for r in rows)+"\n")
    counts={s:sum(r.status==s for r in rows) for s in sorted({r.status for r in rows})}
    text="targets=60 "+" ".join(f"{s.lower()}={n}" for s,n in counts.items())+f" wall_seconds={time.monotonic()-start:.6f}"
    (OUT/"result.txt").write_text(text+"\n"); print(text)
if __name__=="__main__":main()
