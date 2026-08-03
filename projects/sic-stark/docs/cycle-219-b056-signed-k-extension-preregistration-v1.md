# Cycle 219 / B056 preregistration: signed-`k` extension prototype

Cycle 218 shows that the raw endpoint's negative `k` is outside the source
domain. This block attempts the smallest genuine extension: a sign-lift from
the raw negative-`k` coordinates to the positive-`k` product coordinates.

<!-- research-freeze-v1
{
  "schema":"research-preregistration-freeze-v1",
  "cycle":219,
  "parameters":{
    "positive_and_negative_states":{"kind":"expression","value":"Freeze a positive state (p,k,r,s) with k=24 and its raw signed representative (-p,-k,-r,-s) with k=-24. Freeze u=(mu+m*omega2)/(k*omega2), tau=(omega1+r*omega2)/(k*omega2), and tilde-u=(mu-p*m*omega1)/(k*omega1) from equations (5)--(8).","rationale":"The extension must respect both q-product sectors, not just the modular matrix."},
    "sign_lift_family":{"kind":"expression","value":"Enumerate the 16 diagonal sign lifts (mu,m,omega1,omega2)->(a*mu,b*m,c*omega1,d*omega2), a,b,c,d in {+1,-1}, while matrix coordinates negate. Require equality of tau, u, and tilde-u as formal affine rational expressions. Do not allow shifts, scalars, theta factors, reflection substitutions, swaps, or label redefinitions.","rationale":"This is the smallest falsifiable signed-k construction."},
    "extension_axioms":{"kind":"expression","value":"For every surviving lift require agreement with the source k>0 product under double sign application, involutivity, normalized reflection (33), shifts (38)--(39), and factorization identities (16)--(17), retaining normalization and residual factors. If no lift preserves every product coordinate, record that these axioms cannot be tested for this diagonal family.","rationale":"A convention is not an extension unless it preserves defining identities."},
    "acceptance_boundary":{"kind":"expression","value":"Accept only an explicitly defined signed-k function with every axiom checked. A no-survivor result contains diagonal sign lifts only; it does not exclude a non-diagonal reflection/theta/product extension, a new source theorem, a packet cocycle, AFK covariance, fusion, Stark, or TCC.","rationale":"The prototype must not be confused with an exhaustion of signed-k constructions."}
  },
  "resource_caps":{"sign_lifts":{"kind":"integer","value":16,"rationale":"All diagonal sign assignments."},"product_coordinates":{"kind":"integer","value":3,"rationale":"tau, u, and tilde-u must agree."},"downstream_axiom_families":{"kind":"integer","value":4,"rationale":"Involutivity, reflection, shifts, factorization."},"wall_seconds":{"kind":"integer","value":180,"rationale":"Exact sign-coefficient census."},"floating_point":{"kind":"not_applicable","justification":"The comparison is exact symbolic sign algebra.","rationale":"No numerical Gamma_M value is relevant."}},
  "formula_families":["Sarkissian--Spiridonov equations (3), (5)--(8), (16)--(17), (29)--(33), and (38)--(39)","Cycle-218 signed-period product-domain boundary","Exact diagonal sign-lift census"],
  "selection_rule":["Derive three product-coordinate constraints before interpreting a matrix equality.","Enumerate all 16 sign lifts and retain every survivor or inconsistency.","Test downstream axioms only for surviving product-coordinate lifts."],
  "failure_rule":["Do not add shifts, swaps, theta factors, reflections, label changes, or branches to rescue a failed diagonal lift.","Do not call a lift preserving fewer than all three coordinates an extension.","Do not infer packet, AFK, fusion, Stark, or TCC statements."],
  "pre_execution":{"timestamp_utc":"2026-08-03T06:39:54Z","git_head":"ad265e43bad09a683234d69d4d991d49e66c89bc","git_state":"Dirty only from concurrent repository-wide PROGRAM migration and unrelated work; this cycle freezes the listed SIC--Stark inputs."},
  "input_paths":["artifacts/cycle-218-b055-signed-period-cover-v1.json","proof/verify_cycle_218_signed_period_cover.py","scripts/dimension_six_ss_evaluation_audit.py","paper/sic-stark-dimension-six-boundary-fusion.tex","../../tools/preregistration_check.py"]
}
-->
