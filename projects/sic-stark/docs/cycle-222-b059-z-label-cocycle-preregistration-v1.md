# Cycle 222 / B059 preregistration: source-normalization label cocycle

Cycle 221 leaves a residual minus sign under the first signed shift. This
block asks whether the source normalization `Z(m)` determines a mod-24 label
cocycle that repairs it, without inventing a negative-`k` multiplier.

<!-- research-freeze-v1
{
  "schema":"research-preregistration-freeze-v1",
  "cycle":222,
  "parameters":{
    "frozen_positive_normalization":{"kind":"expression","value":"Freeze M_+=(p,k,r,s)=(-5,24,115,24), its source-defined Z_+(m) from equation (29)/(31), and labels m in Z/24Z. Freeze the raw projective negative M_-=-M_+ as outside the source product domain; no value called Z_-(m) is admitted unless derived from a source identity.","rationale":"The cycle tests whether source normalization supplies the missing sign bridge rather than assuming it."},
    "coboundary_requirement":{"kind":"expression","value":"Freeze a prospective root-of-unity label multiplier lambda:Z/24Z->C^x only through the Cycle-221 first-shift repair equation lambda(m-115)/lambda(m)=-1, equivalently lambda(m+5)/lambda(m)=-1. Enumerate the complete mod-24 solution torsor before imposing any source selection rule. Do not impose a guessed Z_- formula.","rationale":"This gives the exact finite freedom required by the known residual sign, without fitting an individual multiplier."},
    "source_selection_and_identity_tests":{"kind":"expression","value":"Derive every mod-24 phase relation actually supplied by Z_+(m), its source quasiperiodicity, normalized reflection, and the cited factorization arrows. Check whether any relation connects a positive-k Z_+ label to a negative-k raw label, selects one lambda solution, or defines factorization pullbacks for lambda. If no source relation supplies such a bridge, record nonselection; do not evaluate an invented signed product.","rationale":"A solution of the abstract coboundary is not source-derived unless the source identifies it across the sign boundary."},
    "acceptance_boundary":{"kind":"expression","value":"Accept only an explicitly source-derived lambda with its sign bridge, reflection, both shifts, and both factorization identities proved. A finite solution torsor or positive-domain Z relation alone is not an extension. Do not claim a signed-k Gamma_M extension, packet cocycle, AFK covariance, fusion, Stark, or TCC.","rationale":"The exact source/domain boundary is the central falsifiable condition."}
  },
  "resource_caps":{"label_states":{"kind":"integer","value":24,"rationale":"Complete modulus-24 state space."},"first_shift_orbit":{"kind":"integer","value":24,"rationale":"Step 5 generates Z/24Z."},"source_identity_families":{"kind":"integer","value":4,"rationale":"Z formula/quasiperiodicity, reflection, and two factorization arrows."},"wall_seconds":{"kind":"integer","value":180,"rationale":"Finite exact phase and graph computation."},"floating_point":{"kind":"not_applicable","justification":"All phases are exact roots of unity and modular arithmetic.","rationale":"No numerical Gamma_M evaluation is admissible."}},
  "formula_families":["Sarkissian--Spiridonov normalized multiplier Z(m), normalized reflection (33), quasiperiodicity (34), shifts (38)--(39), and factorization identities (16)--(17)","Cycle-217 raw source transformation orbit","Cycle-221 signed first-shift mismatch","Exact Z/24 cocycle algebra"],
  "selection_rule":["Enumerate every solution of the first-shift equation on Z/24Z before reading a selection from source phases.","Use only identities valid on the source positive-k domain to seek a sign bridge.","Treat a missing cross-domain relation as nonselection, not as permission to choose lambda."],
  "failure_rule":["Do not define Z_- by simultaneous sign substitution, fit lambda from the failed shift, use a post-result root choice, or call a positive-domain phase an inter-representative law.","Do not suppress residual ordinary-gamma factors or use matrix-level projective equality as factorization compatibility.","Do not infer any packet, AFK, fusion, Stark, or TCC consequence."],
  "pre_execution":{"timestamp_utc":"2026-08-03T07:32:00Z","git_head":"6906ae87f7c87ec33e61b79b3879b6ec0fd8429f","git_state":"Dirty only from the concurrent repository-wide PROGRAM migration and unrelated work; this cycle freezes the listed SIC--Stark inputs."},
  "input_paths":["artifacts/cycle-221-b058-tilde-inversion-v1.json","proof/verify_cycle_221_tilde_inversion.py","proof/verify_cycle_217_source_transformation_groupoid.py","scripts/dimension_six_ss_evaluation_audit.py","paper/sic-stark-dimension-six-boundary-fusion.tex","../../tools/preregistration_check.py"]
}
-->
