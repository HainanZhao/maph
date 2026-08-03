# Cycle 223 / B060 preregistration: explicit parity-corrected signed product

Cycle 222 identifies a complete parity-cocycle torsor but no source sign
bridge. This block performs the distinct construction it leaves open: define
the negative-`k` product explicitly and test it against the frozen direct
continuation identities.

<!-- research-freeze-v1
{
  "schema":"research-preregistration-freeze-v1",
  "cycle":223,
  "parameters":{
    "candidate_state_space":{"kind":"expression","value":"Freeze M_+=(-5,24,115,24), raw M_-=-M_+, the two survivors sigma in {+1,-1}, and epsilon=lambda(0) in {+1,-1}. Set lambda_epsilon(m)=epsilon*(-1)^m on Z/24Z. Set z=exp(2*pi*i*tilde-u_-), C(z;qtilde)=(qtilde*z;qtilde)_infinity/(qtilde*z^(-1);qtilde)_infinity, and define H_(sigma,epsilon)(mu,m)=lambda_epsilon(m)*C(z;qtilde)*Gamma_M+(sigma*mu,-m;sigma*omega1,-sigma*omega2).","rationale":"This is a complete, finite, independently constructed negative-k product family; no source attribution is made."},
    "normalization_and_identity_requirements":{"kind":"expression","value":"Freeze formal raw reflection label involution m->4-m and require lambda(m)lambda(4-m)=1, which restricts epsilon^2=1. Test every one of the four candidates against: unnormalized product-sector agreement; this reflection condition; the direct signed continuations of both normalized shifts; and equations (16)--(17) retaining all ordinary-gamma residual factors. Do not identify a positive-k source theorem with any negative-k result.","rationale":"The construction is accepted only when its full prescribed algebra closes."},
    "second_shift_algebra":{"kind":"expression","value":"For the raw second shift (mu,m)->(mu+omega2,m-1), freeze z->qtilde^(-1)z, C(z)->(1-z)(1-qtilde/z)C(z), and use the source positive backward shift for Gamma_M+ exactly. Compare the resulting multiplier with the direct raw signed continuation before considering factorization.","rationale":"This is the first nontrivial compatibility test after the parity repair."},
    "acceptance_boundary":{"kind":"expression","value":"Accept only if all four candidates are checked and at least one passes every listed condition with no fitted term. A failure of a shift contains this explicit product construction and makes later factorization tests inapplicable. Do not claim a source-defined signed Gamma_M law, packet cocycle, AFK covariance, fusion, Stark, or TCC.","rationale":"A new construction may fail, but cannot be repaired after seeing the result."}
  },
  "resource_caps":{"candidates":{"kind":"integer","value":4,"rationale":"Two survivor lifts times two reflection-normalized constants."},"label_states":{"kind":"integer","value":24,"rationale":"Complete label quotient."},"identity_families":{"kind":"integer","value":5,"rationale":"Product/reflection, two shifts, and two factorization arrows counted as one family after shifts."},"wall_seconds":{"kind":"integer","value":240,"rationale":"Exact product and trigonometric algebra only."},"floating_point":{"kind":"not_applicable","justification":"The construction uses formal q-products, exact signs, and symbolic finite factors.","rationale":"No numerical Gamma_M evaluation is admissible."}},
  "formula_families":["Sarkissian--Spiridonov normalized reflection (33), shifts (38)--(39), and factorization identities (16)--(17)","q-Pochhammer inversion under z->qtilde^(-1)z","Cycle-221 forced tilde factor","Cycle-222 parity cocycle"],
  "selection_rule":["Use exactly all four frozen candidates and both label/parity choices.","Derive the second-shift multiplier before assessing an equality.","Stop the candidate branch at the first failed required identity; preserve its residual factor."],
  "failure_rule":["Do not change epsilon, add a period-dependent scalar, alter lambda(m), add a correction factor, shift, swap, branch, or relabel after a mismatch.","Do not turn formal raw continuation requirements into source theorems or suppress ordinary-gamma residual factors.","Do not infer any packet, AFK, fusion, Stark, or TCC consequence."],
  "pre_execution":{"timestamp_utc":"2026-08-03T07:44:00Z","git_head":"0c2dec39e4ab43d90198d51be31add6e87608631","git_state":"Dirty only from the concurrent repository-wide PROGRAM migration and unrelated work; this cycle freezes the listed SIC--Stark inputs."},
  "input_paths":["artifacts/cycle-222-b059-z-label-cocycle-v1.json","proof/verify_cycle_222_z_label_cocycle.py","proof/verify_cycle_221_tilde_inversion.py","proof/verify_cycle_217_source_transformation_groupoid.py","scripts/dimension_six_ss_evaluation_audit.py","paper/sic-stark-dimension-six-boundary-fusion.tex","../../tools/preregistration_check.py"]
}
-->
