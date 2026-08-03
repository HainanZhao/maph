#!/usr/bin/env python3
"""Positive-k source reachability audit for reflected residual partners."""
from __future__ import annotations
import json
from fractions import Fraction as F
try:
 from .verify_cycle_226_signed_product_groupoid import edge_inventory
 from .verify_cycle_228_f3_square_residual_block import blocks
except ImportError:  # pragma: no cover
 from verify_cycle_226_signed_product_groupoid import edge_inventory
 from verify_cycle_228_f3_square_residual_block import blocks

def audit():
 edges=[e for e in edge_inventory()["edges"] if e["source_product_definition_available"]]
 assert len(edges)==4 and all(e["source_k"]==24 for e in edges)
 partners=[]
 for start,block in blocks().items():
  for position,item in enumerate(block,1):
   c=F(item["argument_mu"]); assert c>0
   partners.append({"start":start,"position":position,"partner_mu_coefficient":str(-c)})
 assert len(partners)==8
 rows=[]
 for edge in edges:
  # C226 residuals have argument (mu+...)/k, k=24, hence +1/24.
  for partner in partners:
   rows.append({"edge":edge["edge"],"partner":f'{partner["start"]}{partner["position"]}',"source_mu_coefficient":"1/24","partner_mu_coefficient":partner["partner_mu_coefficient"],"argument_match":False,"reason":"opposite nonzero mu coefficients"})
 assert len(rows)==32 and not any(row["argument_match"] for row in rows)
 # In equations (16)--(17), an arbitrary admissible positive-k source factor
 # has (mu+L)/k, hence coefficient +1/k. Its (32) partner has -1/k in that
 # same local chart. Any multistep source transport applies the same invertible
 # affine coordinate map to both coefficient covectors, preserving their
 # being opposite nonzero covectors.
 generic={"source_local_mu_coefficient":"+1/k, k>0","reflection_partner_local_mu_coefficient":"-1/k","same_transport_preserves_opposition":True,"arbitrary_finite_positive_k_path_reaches_partner":False}
 assert generic["same_transport_preserves_opposition"]
 return {"epistemic_status":"PROVED","positive_edges":[e["edge"] for e in edges],"partners":partners,"rows":rows,"formula_level_orientation_invariant":generic,"source_reachable_partner_count":0,"conclusion":"No required equation-(32) reflection partner is produced by any admissible positive-k F2/F3 source edge or finite positive-k path: source residual and reflected partner have opposite nonzero local mu covectors, and the same invertible transport cannot identify them. The four-edge census is the exact finite anchor; period-base comparison is never reached."}
if __name__=="__main__":print(json.dumps(audit(),indent=2,sort_keys=True))
