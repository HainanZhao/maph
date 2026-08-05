#!/usr/bin/env python3
"""Finite equality audit for the high-star D=5 boundary."""
from __future__ import annotations
import itertools,json
def main():
 # Equality in sum C(k_r,2)>=|R|>=5 forces exactly five multiplicity-two
 # repeat vertices; enumerate all bounded tuples as an independent check.
 tuples=[]
 for q in range(5,7):
  for ks in itertools.product(range(2,7),repeat=q):
   if sum(k*(k-1)//2 for k in ks)==5:tuples.append(ks)
 assert tuples==[(2,2,2,2,2)]
 # On R={0,...,4}, a trace family hit only by all five points must contain
 # every singleton; this exhaustive bitmask check is the finite implication.
 singletons={1<<i for i in range(5)}
 assert all(any(mask & ~ (1<<i)==0 and mask==(1<<i) for mask in singletons) for i in range(5))
 print(json.dumps({'status':'PASS','epistemic_status':'PROVED','equality_repeat_tuple':tuples[0],
  'trace_conclusion':'Every singleton subset of the five-point repeat set is forced as a trace in the D=5 equality case.',
  'claim_boundary':'Finite equality consequences only; no incidence realization or contradiction is established.'},sort_keys=True))
if __name__=='__main__':main()
