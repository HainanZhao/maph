#!/usr/bin/env python3
"""Replay Cycle 25's quadratic CRT selector and finite output boundary."""
from __future__ import annotations
import csv,json
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/"discovery"))
import lrc_quadratic_crt_class as q
import lrc_coupled_incidence as c
import lrc_pair_choice as direct
import lrc_width_four_stage_a as width4
OUT=ROOT/"discovery/out/cycle25-quadratic-crt"
def read(path):
 with path.open(newline="",encoding="utf-8") as h:return list(csv.DictReader(h,delimiter="\t"))
def audit():
 assert len(c.interface_controls())==295
 control=q.control();assert control["status"]=="PASS" and control["basis_determinant"]!=0
 for base_index in (3,4):
  coverage=width4.raw_coverage(direct.CNFS[base_index]);base=c.read_bases()[base_index]
  for point in range(c.P*c.C):
   for coordinate in range(c.K):
    for digit in range(c.C):
     assert bool(coverage[point,coordinate,digit])==c.crt_is_bad(c.K,c.P,c.C,base[coordinate]+c.P*digit,point)
 rows=read(OUT/"results.tsv");prior=read(ROOT/"discovery/out/cycle24-crt-fourier-class/results.tsv")
 assert len(rows)==60 and [(x["base_index"],x["leaf_ordinal"]) for x in rows]==[(x["base_index"],x["leaf_ordinal"]) for x in prior]
 assert all(x["status"]=="UNRESOLVED" for x in rows)
 indices=q.class_indices()
 for x in rows:
  b,o=int(x["base_index"]),int(x["leaf_ordinal"]); allowed=direct.allowed_digits(c.read_bases()[b],o); coverage=width4.raw_coverage(direct.CNFS[b])
  score,part=q.core.select_partition(q.core.exact_savings(allowed,coverage,indices))
  assert int(x["oracle_score"])==score and x["partition"]==q.core.partition_text(part) and 1<=int(x["separation_rounds"])<=512
 vals=[float(x["objective"]) for x in rows];assert min(vals)>=1-1e-9
 return {"status":"PASS","epistemic_status":"OBSERVED","targets":60,"class_cardinalities":control["cardinalities"],"basis_determinant":control["basis_determinant"],"objective_min":min(vals),"objective_max":max(vals),"certified_leaves":[]}
if __name__=="__main__":print(json.dumps(audit(),indent=2,sort_keys=True))
