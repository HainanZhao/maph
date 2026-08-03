# Cycle 215 / B052 preregistration: equation-(66) `E` transport

Cycle 214 found the sole frozen label-and-flow reverser
`E=((0,1),(1,0))`, but AFK covariance stopped at a transformed tuple.  This
block applies that matrix directly to the published equation-(66) lens
parameters and asks whether the transformed data remain within the verified
positive-period specialization or yield a forced conjugate-dual packet law.

<!-- research-freeze-v1
{
  "schema": "research-preregistration-freeze-v1",
  "cycle": 215,
  "parameters": {
    "equation66_source_data": {
      "kind": "expression",
      "value": "Freeze the Sarkissian--Spiridonov equation-(66) specialization audited in scripts/dimension_six_ss_evaluation_audit.py: M=A6=((-p,-s),(k,-r))=((115,-24),(24,-5)), (p,k,r,s)=(-115,24,5,24), p*r+k*s=1, beta=(5+sqrt(21))/2, omega1=k*beta-r=24*beta-5=beta^3>0, omega2=1, Q=omega1+omega2, and phase coefficient p-k*(1-s)=437.",
      "rationale": "This is the only frozen direct Gamma_M/equation-(66) source specialization."
    },
    "e_transport": {
      "kind": "expression",
      "value": "Freeze E=((0,1),(1,0)), beta_E=E*beta=beta^-1=5-beta, and E*A6*E=A6^-1. Canonicalize the inverse to k>0 by M_E=-A6^-1=((-p_E,-s_E),(k_E,-r_E)), then calculate its four lens parameters, Bezout identity, phase coefficient, and omega1_E=k_E*beta_E-r_E exactly. No independent sign, period rescaling, or replacement of the beta_E root is allowed.",
      "rationale": "It tests the actual transformed equation data before any claimed t inversion."
    },
    "packet_test": {
      "kind": "expression",
      "value": "For the frozen complete source packet P_(a,b;h)(t)=zeta_6^(5*h*a)*t^(4*b-5*a)*(1+t^6+t^12), test only the bare direct candidate P_(a,b;h)(t)=kappa_h(t)*conjugate(P_(b,a;h_prime)(t^-1)), where h_prime ranges over the six global channel images and kappa_h is independent of (a,b). Compare all 216 labelled coordinates symbolically. A label-dependent correction is not admissible unless it is explicitly derived from the transformed equation-(66) phase data.",
      "rationale": "A direct packet isomorphism must be more than a post hoc rowwise renormalization."
    },
    "acceptance_boundary": {
      "kind": "expression",
      "value": "Accept a direct E packet law only if the transformed lens data satisfy the cited equation-(66) specialization hypotheses (including k>0 and positive boundary periods) and produce a displayed source-derived phase/cocycle cancelling every packet ratio on all 216 coordinates. Otherwise record the exact parameter or all-row mismatch. No target/C198 fitting, analytic-continuation theorem beyond the frozen source, or formal dual pairing is allowed.",
      "rationale": "The claimed duality must arise from the actual Gamma_M transform rather than from C213's formal model."
    }
  },
  "resource_caps": {
    "lens_parameter_sets": {"kind":"integer","value":2,"rationale":"Original A6 and its fixed E-transport canonicalization."},
    "packet_channels": {"kind":"integer","value":6,"rationale":"All global channel images are tested."},
    "packet_coordinates": {"kind":"integer","value":216,"rationale":"Six channels times the complete 36-label packet."},
    "candidate_scalars": {"kind":"integer","value":6,"rationale":"One scalar per source channel, never per label."},
    "wall_seconds": {"kind":"integer","value":180,"rationale":"Exact integer and Laurent-exponent audit."},
    "floating_point": {"kind":"not_applicable","justification":"All calculations use Q(sqrt(21)), integer matrices, roots-of-unity exponents, and formal Laurent exponents.","rationale":"No Gamma_M value or endpoint limit is evaluated."}
  },
  "formula_families": [
    "Sarkissian--Spiridonov equation-(66) d=6 specialization",
    "Cycle-214 exact E conjugacy and root action",
    "Cycle-206 complete 36-characteristic source packet",
    "Exact global-channel direct-inversion comparison"
  ],
  "selection_rule": [
    "Verify transformed matrix, lens parameters, Bezout identity, phase coefficient, and positive-period condition before testing any packet relation.",
    "Test every global target channel and all 36 labels; retain a scalar only if its phase and t exponent are label-independent.",
    "Promote a packet isomorphism only with a source-derived equation-(66) phase/cocycle and all verified hypotheses; otherwise preserve the mismatch as a scoped obstruction."
  ],
  "failure_rule": [
    "Do not use -A6^-1 without recording why it is the k>0 canonicalization, or change beta_E/period signs to restore positivity.",
    "Do not replace a failed global scalar by a label-dependent correction, selected channel, target datum, or unproved analytic continuation.",
    "Do not infer t->t^-1 from label exchange alone or call a bare packet identity a fusion, AFK, Stark, or TCC theorem.",
    "If any matrix, parameter, source-hypothesis, phase, Laurent exponent, channel, or replay condition differs, withhold the direct-E conclusion."
  ],
  "pre_execution": {
    "timestamp_utc": "2026-08-03T06:08:32Z",
    "git_head": "a6733c0b218b0b5ad94a8f3102d7952dc55a398d",
    "git_state": "Dirty only from concurrent repository-wide PROGRAM migration and unrelated work; this cycle freezes the listed SIC--Stark inputs."
  },
  "input_paths": [
    "artifacts/cycle-213-b050-two-ended-completion-v1.json",
    "artifacts/cycle-214-b051-source-automorphy-end-exchange-v1.json",
    "proof/verify_cycle_214_source_automorphy_end_exchange.py",
    "scripts/dimension_six_ss_evaluation_audit.py",
    "proof/verify_cycle_206_projective_line_interface.py",
    "proof/verify_cycle_190_balanced_helical_reflection.py",
    "paper/sic-stark-dimension-six-boundary-fusion.tex",
    "../../tools/preregistration_check.py"
  ]
}
-->
