# Cycle 227 / B064 preregistration: augmented transport normal forms

Cycle 226 proves that raw `F2/F3` matrix loops are not loops of the factorization
state. This block derives the exact transport semigroup before assigning any
signed product or edge cochain.

<!-- research-freeze-v1
{
  "schema":"research-preregistration-freeze-v1",
  "cycle":227,
  "parameters":{
    "augmented_generators":{"kind":"expression","value":"Freeze raw states A=(-115,24,5,24), B=(-5,-24,115,-24), C=(115,24,-5,24), D=(5,-24,-115,-24). For F2 and F3 retain the raw-state map, the integral 2-by-2 period-basis map, affine argument in (mu,m*omega2), target label 0, and the two ordinary-gamma residual factors from S--S (16)/(17). No negative-k formal transition is called a source identity.","rationale":"These are exactly the C226 augmented interfaces."},
    "normal_form_test":{"kind":"expression","value":"Enumerate all 2^12 words of length at most 12 from each frozen raw start, then derive and verify an inductive normal-form reduction using the exact paired F2/F3 transports. A normal form records raw endpoint, positive scaling exponent, swap flag, affine argument coefficients, label, source-domain path class, and unsimplified residual-factor word.","rationale":"The finite census is a discovery check; the induction, not a bounded search, is the acceptance route."},
    "quotient_rule":{"kind":"expression","value":"A 576 positive-scaling quotient may be considered only on a path all of whose product inputs have k>0, only after checking the exact C218 scaling hypotheses, and only if it preserves the full affine argument/label state. Do not use it across B,D, to erase label loss, to identify a period swap, or to cancel ordinary-gamma residuals.","rationale":"C218 proves a restricted product law, not a signed-k or raw-loop quotient."},
    "acceptance_boundary":{"kind":"expression","value":"Accept only an exact normal-form theorem plus a complete classification of any admissible scaling quotient and of all remaining nonclosed transports. If no quotient makes a full augmented loop close, record that containment. Do not construct cochains, use residual cancellation, claim a source signed-k law, affine E closure, packet cocycle, AFK covariance, fusion, Stark, or TCC.","rationale":"The state space must close before cohomology is meaningful."}
  },
  "resource_caps":{"word_length":{"kind":"integer","value":12,"rationale":"Complete finite discovery census before the inductive proof."},"raw_start_states":{"kind":"integer","value":4,"rationale":"The frozen orbit."},"generators":{"kind":"integer","value":2,"rationale":"Only F2,F3."},"maximum_words_per_start":{"kind":"integer","value":8191,"rationale":"All nonempty binary words through length 12."},"scaling_candidates":{"kind":"integer","value":2,"rationale":"Identity or the C218 576 scaling at a normal-form reduction step."},"floating_point":{"kind":"not_applicable","justification":"All transport and normal forms are exact integral/symbolic data.","rationale":"No special-function evaluation can legalize a quotient."},"wall_seconds":{"kind":"integer","value":600,"rationale":"Exact word census and inductive normal-form algebra."}},
  "formula_families":["Sarkissian--Spiridonov equations (16)--(17) with both residual factors retained","Cycle-218 positive 576-scaling law in its k>0 source domain","Cycle-226 augmented F2/F3 transport","Exact semigroup normal forms"],
  "selection_rule":["Include every word through the frozen cap and every raw start.","Retain pathwise source-domain flags and ordered residual-factor words.","Apply a scaling quotient only after all three frozen quotient conditions pass."],
  "failure_rule":["Do not identify matrix return with an augmented loop, quotient a negative-k path, drop an argument/label defect, commute/cancel residual factors, or fit a cochain.","Do not extend the generator set, quotient class, word cap, or source law after inspecting the census.","Do not infer any AFK, fusion, Stark, or TCC result."],
  "pre_execution":{"timestamp_utc":"2026-08-03T09:20:00Z","git_head":"80478aa8934d3ab198a36f79fa7f9b1f4851c685","git_state":"Dirty only from the concurrent repository-wide PROGRAM migration and unrelated work; this cycle freezes the listed SIC--Stark inputs."},
  "input_paths":["artifacts/cycle-218-b055-signed-period-cover-v1.json","artifacts/cycle-226-b063-signed-product-groupoid-v1.json","proof/verify_cycle_226_signed_product_groupoid.py","proof/verify_cycle_218_signed_period_cover.py","scripts/dimension_six_ss_evaluation_audit.py","paper/sic-stark-dimension-six-boundary-fusion.tex","../../tools/preregistration_check.py"]
}
-->
