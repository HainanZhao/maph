#!/usr/bin/env python3
"""Faddeev one-kernel Fourier scope audit for Cycle 238/B075."""
from __future__ import annotations
import json
try:
 from .verify_cycle_228_f3_square_residual_block import blocks
except ImportError:  # pragma: no cover
 from verify_cycle_228_f3_square_residual_block import blocks
def audit():
 rows=[]
 for start,block in blocks().items():
  bases=[(tuple(x["alpha"]),tuple(x["beta"])) for x in block]
  assert len(bases)==4 and len(set(bases))==4
  rows.append({"start":start,"factor_count":4,"distinct_period_pair_count":len(set(bases)),"one_fixed_kernel_period_pair_applies":False,"one_factor_output_can_equal_four_factor_reversed_word":False,"published_contour":"displaced real line for one kernel"})
 assert len(rows)==2
 return {"epistemic_status":"PROVED","source_transform":{"formula":"integral_R gamma(t-omega''+i0)e^(-2*pi*i*x*t)dt=c/gamma(x+omega''-i0)","kernel_factor_count":1,"fixed_period_pair_count":1,"output_factor_count":1},"residual_blocks":rows,"source_transform_applies_to_entire_residual_word":False,"status":"FALSIFIED_BY_HETEROGENEOUS_BASES_AND_FACTOR_ARITY","conclusion":"Faddeev's one-kernel Fourier duality cannot dualize either frozen four-factor residual word: every block has four distinct period bases and requires four reversed partners, while the cited identity has one fixed period pair and one reciprocal output. No source composition theorem licenses four separate transforms."}
if __name__=="__main__":print(json.dumps(audit(),indent=2,sort_keys=True))
