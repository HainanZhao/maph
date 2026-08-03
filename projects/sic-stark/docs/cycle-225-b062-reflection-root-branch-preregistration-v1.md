# Cycle 225 / B062 preregistration: reflection-root signed-product branch

Cycle 224 leaves exactly two reflection roots. This block tests the full
`c=±i` branch, including how simultaneous sign reversal acts on that branch,
before treating it as a possible signed state.

<!-- research-freeze-v1
{
  "schema":"research-preregistration-freeze-v1",
  "cycle":225,
  "parameters":{
    "frozen_product_roots":{"kind":"expression","value":"Freeze the Cycle-224 product H_(sigma,c)=c*(-1)^m*C(z;qtilde)*exp(pi*i*tilde-u_-)*Gamma_M+(sigma*mu,-m;sigma*omega1,-sigma*omega2), sigma in {+1,-1}, with exactly c in {+i,-i}. These and only these constants solve the combined reflection equation -c^2=1.","rationale":"The roots are forced by the sealed reflection residual and are a new explicit branch, not a source-derived choice."},
    "sign_reversal_actions":{"kind":"expression","value":"Freeze both possible actions of simultaneous sign reversal on the two constants: preserve c, or conjugate c (equivalently c->-c). Test double-sign involutivity for each action; retain an action only if the exact branch constants and product factors make the double transform the identity.","rationale":"The branch involution cannot be assumed from the root equation alone."},
    "identity_tests":{"kind":"expression","value":"For all four (sigma,c) candidates, verify both frozen signed shifts, raw reflection, and the surviving double-sign action. Then test whether equations (16)--(17) have defined pullbacks on every signed state required by their raw arrows, retaining ordinary-gamma factors and full period/argument/label data. An unavailable state or pullback fails the extension acceptance condition.","rationale":"A one-state product is not a signed Gamma_M theory unless it closes under the required transformations."},
    "acceptance_boundary":{"kind":"expression","value":"Accept only if a branch/action passes both shifts, reflection, double sign, and both factorization identities. Do not identify an algebraically selected branch with a source theorem, or a one-state closure with a full factorization law. Do not claim a packet cocycle, AFK covariance, fusion, Stark, or TCC.","rationale":"This is the final acceptance boundary for this branch construction."}
  },
  "resource_caps":{"product_candidates":{"kind":"integer","value":4,"rationale":"Two survivor signs times two reflection roots."},"sign_actions":{"kind":"integer","value":2,"rationale":"Preserve or conjugate the root."},"identity_families":{"kind":"integer","value":5,"rationale":"Two shifts, reflection, double sign, and paired factorization."},"wall_seconds":{"kind":"integer","value":240,"rationale":"Exact sign and state-space algebra."},"floating_point":{"kind":"not_applicable","justification":"All roots, phases, and state transitions are exact symbolic values.","rationale":"No numerical Gamma_M evaluation is admissible."}},
  "formula_families":["Sarkissian--Spiridonov normalized reflection (33), shifts (38)--(39), and factorization identities (16)--(17)","Cycle-224 unique shift cochain","Cycle-217 full raw transformation-state audit","Exact root-branch involutivity"],
  "selection_rule":["Use exactly c=+i,-i and both frozen sign-reversal actions.","Preserve the exact Cycle-224 cochain and all C223 product factors.","Require a defined factorization pullback for every raw signed state; retain all residual factors."],
  "failure_rule":["Do not choose a new root, change the sign action, add any multiplier, modify the state space, or drop a residual factor after a failed identity.","Do not call c=±i source-derived or a matrix projective equivalence a Gamma_M arrow.","Do not infer any packet, AFK, fusion, Stark, or TCC consequence."],
  "pre_execution":{"timestamp_utc":"2026-08-03T08:15:00Z","git_head":"3c2a323a0619f3da2aafaf788ae399b353331a7b","git_state":"Dirty only from the concurrent repository-wide PROGRAM migration and unrelated work; this cycle freezes the listed SIC--Stark inputs."},
  "input_paths":["artifacts/cycle-224-b061-shift-cohomology-v1.json","proof/verify_cycle_224_shift_cohomology.py","proof/verify_cycle_223_explicit_signed_product.py","proof/verify_cycle_217_source_transformation_groupoid.py","scripts/dimension_six_ss_evaluation_audit.py","paper/sic-stark-dimension-six-boundary-fusion.tex","../../tools/preregistration_check.py"]
}
-->
