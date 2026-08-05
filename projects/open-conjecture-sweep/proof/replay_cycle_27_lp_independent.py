#!/usr/bin/env python3
"""Independent streamed cutting-plane replay of Cycle 27's target LPs."""
from __future__ import annotations
import csv,itertools,json,multiprocessing,time
from pathlib import Path
import sys
import numpy as np
from scipy.optimize import linprog
from scipy.sparse import csr_matrix

ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/"discovery"))
import lrc_coupled_incidence as coupled
import lrc_pair_choice as direct
import lrc_width_four_stage_a as width4
import lrc_width_five_lp as original
OUT=ROOT/"discovery/out/cycle27-width-five-lp"
TOL=1e-9; ROUND_CAP=512

def read(path):
 with path.open(newline="",encoding="utf-8") as h:return list(csv.DictReader(h,delimiter="\t"))
def mask(block,option,coverage):return np.logical_or.reduce([coverage[:,c,d] for c,d in zip(block,option,strict=True)])
def count(block,allowed):
 x=1
 for c in block:x*=len(allowed[c])
 return x
def maximum(block,allowed,coverage,weights):
 # Independent state batching: enumerate a three-coordinate prefix, stream
 # penultimate suffixes, then score the final digit batch.
 p=block[:3];tail=block[3:];states=np.zeros((1,coverage.shape[0]),dtype=bool);prefixes=[()]
 for c in p:
  digits=tuple(allowed[c]); states=np.logical_or(states[:,None,:],coverage[:,c,list(digits)].T[None,:,:]).reshape(-1,coverage.shape[0]);prefixes=[a+(d,) for a in prefixes for d in digits]
 best=(-float("inf"),None,None); total=0
 if len(tail)==0: heads=[()];last=None;digits=((),)
 elif len(tail)==1: heads=[()];last=tail[0];digits=tuple(allowed[last])
 else: heads=itertools.product(*[tuple(allowed[c]) for c in tail[:-1]]);last=tail[-1];digits=tuple(allowed[last])
 for head in heads:
  base=states
  for c,d in zip(tail[:-1] if tail else (),head,strict=True):base=base|coverage[:,c,d]
  cand=base[:,None,:] if last is None else np.logical_or(base[:,None,:],coverage[:,last,list(digits)].T[None,:,:])
  flat=cand.reshape(-1,coverage.shape[0]);scores=flat@weights;i=int(np.argmax(scores));a,b=divmod(i,len(digits));option=prefixes[a]+head+(() if last is None else (digits[b],));value=float(scores[i])
  if value>best[0] or (value==best[0] and option<best[1]):best=(value,option,flat[i].copy())
  total+=len(flat)
 if total!=count(block,allowed):raise AssertionError("option census")
 return best
def solve(job):
 base,ordinal=job;allowed=direct.allowed_digits(coupled.read_bases()[base],ordinal);blocks=original.target_partition(allowed);coverage=width4.raw_coverage(direct.CNFS[base]);n=len(coverage);cuts=[];seen=[set() for _ in blocks]
 for i,b in enumerate(blocks):
  o=tuple(allowed[c][0] for c in b);cuts.append((i,o,mask(b,o,coverage)));seen[i].add(o)
 eq=csr_matrix((np.ones(n),(np.zeros(n,dtype=int),np.arange(n))),shape=(1,n+len(blocks)));objective=np.r_[np.zeros(n),np.ones(len(blocks))]
 for rnd in range(1,ROUND_CAP+1):
  data=[];rr=[];cc=[]
  for r,(bi,_o,m) in enumerate(cuts):
   ix=np.flatnonzero(m);rr.extend([r]*len(ix));cc.extend(ix);data.extend([1.0]*len(ix));rr.append(r);cc.append(n+bi);data.append(-1.0)
  solved=linprog(objective,A_ub=csr_matrix((data,(rr,cc)),shape=(len(cuts),n+len(blocks))),b_ub=np.zeros(len(cuts)),A_eq=eq,b_eq=np.array([1.0]),bounds=(0,None),method="highs-ds",options={"presolve":True})
  if solved.status!=0:raise AssertionError(solved.message)
  added=[]
  for bi,b in enumerate(blocks):
   value,o,m=maximum(b,allowed,coverage,solved.x[:n])
   if value>solved.x[n+bi]+TOL:
    if o in seen[bi]:raise AssertionError("repeat")
    added.append((bi,o,m))
  if not added:return base,ordinal,float(solved.fun),rnd,len(cuts)
  for bi,o,m in added:cuts.append((bi,o,m));seen[bi].add(o)
 raise AssertionError("cap")
def audit():
 observed=read(OUT/"results.tsv");jobs=[(int(r["base_index"]),int(r["leaf_ordinal"])) for r in observed]
 with multiprocessing.Pool(processes=3) as pool: replay=pool.map(solve,jobs,chunksize=1)
 for row,(base,ordinal,value,rnd,cuts) in zip(observed,replay,strict=True):
  assert (base,ordinal)==(int(row["base_index"]),int(row["leaf_ordinal"])) and abs(value-float(row["objective"]))<=1e-8 and rnd==int(row["separation_rounds"]) and cuts==int(row["cuts"])
 return {"status":"PASS","epistemic_status":"OBSERVED","targets":60,"independent_separator_replays":60}
if __name__ == "__main__":
 result = audit()
 # The external timing wrapper records duration even if Python exits with an
 # error.  Persist a successful audit atomically so a completed replay has
 # evidence independent of terminal scrollback.
 target = OUT / "independent-replay.json"
 temporary = target.with_suffix(".json.tmp")
 temporary.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
 temporary.replace(target)
 print(json.dumps(result, indent=2, sort_keys=True))
