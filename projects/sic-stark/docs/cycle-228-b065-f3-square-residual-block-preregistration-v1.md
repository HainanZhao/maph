# Cycle 228 / B065 preregistration: `F3^2` residual block

Cycle 227 isolates the only source-defined product-node return: the label-zero
`F3^2` path from A or C, up to positive common scaling.  This block tests its
four ordered ordinary-gamma residual factors using only explicitly cited
ordinary-gamma identities.

Amendment — 2026-08-03: source equation (32) was checked before reduction.
For the unnormalized ordinary `gamma`, reflection leaves
`exp(pi*i*B_2,2)`; it is not the normalized identity with right side one.

<!-- research-freeze-v1
{
  "schema":"research-preregistration-freeze-v1",
  "cycle":228,
  "parameters":{
    "frozen_blocks":{"kind":"expression","value":"Freeze starts A=(-115,24,5,24) and C=(115,24,-5,24), initial label m=0, and the two successive F3 residual blocks from S--S (17). Retain the four ordinary-gamma factors in their source order, with every argument and period pair transported exactly.","rationale":"These are the only C227 source-defined zero-label product-node returns."},
    "allowed_identities":{"kind":"expression","value":"Admit only the ordinary unnormalized hyperbolic-gamma reflection identity gamma(alpha+beta-z;alpha,beta) gamma(z;alpha,beta)=exp(pi*i*B_2,2(z;alpha,beta)) from S--S equation (32), and multiplication/product decompositions explicitly stated in S--S equation (15) or directly cited source formulas, after their period and argument hypotheses are checked. No unreferenced modular, swap, signed-k, normalization, or fitted scalar identity is allowed.","rationale":"The residual word may be reduced only by a known identity with matching bases and its explicit Bernoulli factor."},
    "acceptance_boundary":{"kind":"expression","value":"Accept a scalar/cocycle reduction only if all four factors are consumed or a fully displayed nonconstant remainder is identified, with order and all bases retained until a cited identity applies. A nonmatching reflection partner, incompatible bases, or unreduced factor is failure of this reduction engine. Do not turn a product-node scaling return into a factorization/cochain loop.","rationale":"The object tested is the residual block, not a projective matrix loop."}
  },
  "resource_caps":{"start_states":{"kind":"integer","value":2,"rationale":"A and C only."},"paths_per_start":{"kind":"integer","value":1,"rationale":"The frozen F3 squared path."},"ordinary_gamma_factors_per_block":{"kind":"integer","value":4,"rationale":"Two residual factors at each step."},"identity_families":{"kind":"integer","value":2,"rationale":"Reflection and cited multiplication/decomposition only."},"floating_point":{"kind":"not_applicable","justification":"Arguments and period bases are exact symbolic linear forms.","rationale":"Numerics cannot authorize a special-function identity."},"wall_seconds":{"kind":"integer","value":300,"rationale":"Exact basis/argument matching."}},
  "formula_families":["Sarkissian--Spiridonov equation (17)","ordinary hyperbolic-gamma reflection","S--S equation (15) product decomposition"],
  "selection_rule":["Use both frozen starts and no other path or label.","Compare reflection partners only at identical ordered period bases.","Apply a multiplication/decomposition only after its exact source hypotheses and every resulting factor are tracked."],
  "failure_rule":["Do not reorder factors, identify swapped bases, insert a scalar, use negative-k data, or suppress an unreduced factor.","Do not extend the identity list or start/path/label set after inspecting a mismatch.","Do not claim a signed extension, packet cocycle, AFK covariance, fusion, Stark, or TCC."],
  "pre_execution":{"timestamp_utc":"2026-08-03T10:15:00Z","git_head":"f04c41b27fa171ebfb1dba04cb887a8ecf2e3871","git_state":"Dirty only from the concurrent repository-wide PROGRAM migration and unrelated work; this cycle freezes the listed SIC--Stark inputs."},
  "input_paths":["artifacts/cycle-227-b064-augmented-transport-normal-forms-v1.json","proof/verify_cycle_227_augmented_transport_normal_forms.py","proof/verify_cycle_226_signed_product_groupoid.py","paper/sic-stark-dimension-six-boundary-fusion.tex","scripts/dimension_six_ss_evaluation_audit.py","../../tools/preregistration_check.py"]
}
-->
