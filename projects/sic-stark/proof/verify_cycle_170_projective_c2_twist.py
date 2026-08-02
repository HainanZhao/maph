#!/usr/bin/env python3
"""Exact Cycle-170 C3 central-C2 projective-twist barrier."""
from __future__ import annotations
import argparse, json
from itertools import product
from pathlib import Path
Q = range(3)
def plus(a,b): return (a+b)%3
def normalized(values):
    return {(a,b): 0 if a == 0 or b == 0 else values[(a,b)] for a in Q for b in Q}
def cocycle(c): return all((c[a,b]+c[plus(a,b),d]-c[b,d]-c[a,plus(b,d)])%2 == 0 for a in Q for b in Q for d in Q)
def coboundary(f): return {(a,b):(f[plus(a,b)]-f[a]-f[b])%2 for a in Q for b in Q}
def build_payload():
    cells=((1,1),(1,2),(2,1),(2,2)); cocycles=[]
    for bits in product(range(2), repeat=4):
        c=normalized(dict(zip(cells,bits,strict=True)))
        if cocycle(c): cocycles.append(c)
    coboundaries=[]
    for values in product(range(2),repeat=2):
        f={0:0,1:values[0],2:values[1]}; coboundaries.append(coboundary(f))
    cocycle_keys={tuple(c[a,b] for a in Q for b in Q) for c in cocycles}; coboundary_keys={tuple(c[a,b] for a in Q for b in Q) for c in coboundaries}
    characters=[]
    for image in range(2):
        chi={q:(q*image)%2 for q in Q}
        if all(chi[plus(a,b)] == (chi[a]+chi[b])%2 for a in Q for b in Q): characters.append(chi)
    return {"schema":"sic-stark-cycle-170-projective-c2-twist-prototype-v1","epistemic_status":"PROVED","claim_boundary":"This exact finite result concerns only C3 central extensions and C3-to-C2 scalar characters from the certified projective scalar kernel. It defines no coefficient-to-logarithm operation, AFK interface, Stark identity, fusion theorem, or TCC identity.","summary":{"normalized_2cochains_checked":16,"group_triples_checked":len(Q)**3,"normalized_cocycle_count":len(cocycles),"normalized_coboundary_count":len(coboundary_keys),"nontrivial_extension_class_count":len(cocycle_keys-coboundary_keys),"generator_images_checked":2,"character_count":len(characters),"nontrivial_character_count":sum(any(chi[q] for q in Q) for chi in characters),"projective_scalar_twist_exists":bool(cocycle_keys-coboundary_keys) or any(any(chi[q] for q in Q) for chi in characters)},"normalized_cocycles":[[c[a,b] for a,b in cells] for c in cocycles],"normalized_coboundaries":[[c[a,b] for a,b in cells] for c in coboundaries],"characters":[[chi[q] for q in Q] for chi in characters],"gate_outcome":{"projective_c2_scalar_twist":"SURVIVES_EXACT_FINITE_TEST" if cocycle_keys-coboundary_keys else "FALSIFIED_EXACT_FINITE_CLASS","scope":"C3 central C2 extensions and C3-to-C2 scalar characters only"}}
def main():
    p=argparse.ArgumentParser();p.add_argument("--output",type=Path);a=p.parse_args();text=json.dumps(build_payload(),indent=2,sort_keys=True)+"\n";a.output.write_text(text) if a.output else print(text,end="")
if __name__=="__main__":main()
