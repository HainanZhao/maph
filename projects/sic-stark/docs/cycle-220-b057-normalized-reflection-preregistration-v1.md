# Cycle 220 / B057 preregistration: normalized-reflection signed-`k` candidate

Cycle 219 excludes only diagonal sign lifts. This block tests the smallest
source-derived non-diagonal alternative: compose the normalized S--S
reflection with the required simultaneous-sign representative change.

<!-- research-freeze-v1
{
  "schema":"research-preregistration-freeze-v1",
  "cycle":220,
  "parameters":{
    "positive_and_raw_states":{"kind":"expression","value":"Freeze the positive E representative M_+=(p,k,r,s)=(-5,24,115,24) and its raw projective negative M_-=(-p,-k,-r,-s)=(5,-24,-115,-24). The raw product coordinates are those obtained by substituting M_- in source equations (5)--(8), while the candidate evaluates the positive M_+ product.","rationale":"The source fixes k>0, so only M_+ supplies a source-defined normalized Gamma_M."},
    "reflection_candidate_family":{"kind":"expression","value":"For each (a,b,c,d) in {+1,-1}^4, set Q_cd=c*omega1+d*omega2 and define the sole candidate H_abcd(mu,m;omega1,omega2)=Gamma_{M_+}(Q_cd-a*mu,r-1-b*m;c*omega1,d*omega2)^(-1). Use only source normalized reflection Gamma_M(Q-x,r-1-y)*Gamma_M(x,y)=1. No additional scalar, shift, theta/Pochhammer factor, swap, branch, label redefinition, or fitted correction is permitted.","rationale":"This is the companion-approved smallest source-derived non-diagonal candidate; its inverse and affine reflection are fixed before calculation."},
    "coordinate_and_identity_tests":{"kind":"expression","value":"First derive exactly whether source reflection reduces H_abcd to the diagonal Gamma_{M_+}(a*mu,b*m;c*omega1,d*omega2). Then enumerate all 16 candidates against raw tau,u,tilde-u as formal affine rational expressions. For a coordinate survivor only, test involutivity, reflection, shifts (38)--(39), and both factorization identities (16)--(17), retaining every normalization and residual factor.","rationale":"The reflection candidate earns downstream testing only if it reaches the raw product-coordinate state."},
    "acceptance_boundary":{"kind":"expression","value":"Accept only a source-defined H_abcd with all three raw coordinates and all listed identities checked. If normalized reflection collapses to the sealed Cycle-219 diagonal family, contain this particular reflection-plus-sign construction only. Do not infer a general signed-k nonexistence, a Gamma_M product extension, a packet cocycle, AFK covariance, fusion, Stark, or TCC.","rationale":"An exact reduction is useful only at its stated construction scope."}
  },
  "resource_caps":{"reflection_sign_candidates":{"kind":"integer","value":16,"rationale":"All diagonal signs beneath the one frozen affine reflection."},"product_coordinates":{"kind":"integer","value":3,"rationale":"tau, u, and tilde-u are the two product sectors and modular parameter."},"downstream_axiom_families":{"kind":"integer","value":4,"rationale":"Involutivity, reflection, shifts, and factorization."},"wall_seconds":{"kind":"integer","value":180,"rationale":"Exact symbolic coefficient comparison."},"floating_point":{"kind":"not_applicable","justification":"Only source identities and exact integer/sign algebra are used.","rationale":"No numerical Gamma_M evaluation is admissible."}},
  "formula_families":["Sarkissian--Spiridonov equations (3), (5)--(8), normalized reflection (33), shifts (38)--(39), and factorization identities (16)--(17)","Cycle-218 signed-period domain boundary","Cycle-219 diagonal sign-lift census","Exact affine reflection/sign reduction"],
  "selection_rule":["Derive the normalized-reflection reduction symbolically before any coordinate census.","Enumerate all 16 frozen reflection-plus-sign candidates and preserve each outcome.","Run downstream functional identities only for a candidate preserving all raw product coordinates."],
  "failure_rule":["Do not add a post-result correction factor, shift, theta/Pochhammer term, swap, branch, scalar, or label map to rescue this frozen family.","Do not call a reflected candidate a signed-k extension merely because its matrix is projectively equivalent.","Do not infer any packet, AFK, fusion, Stark, or TCC consequence."],
  "pre_execution":{"timestamp_utc":"2026-08-03T07:05:00Z","git_head":"0272936daaf041451871109f196edb65475caa22","git_state":"Dirty only from the concurrent repository-wide PROGRAM migration and unrelated work; this cycle freezes the listed SIC--Stark inputs."},
  "input_paths":["artifacts/cycle-219-b056-signed-k-extension-v1.json","proof/verify_cycle_219_signed_k_extension.py","scripts/dimension_six_ss_evaluation_audit.py","paper/sic-stark-dimension-six-boundary-fusion.tex","../../tools/preregistration_check.py"]
}
-->
