# Cycle 216 / B053 preregistration: rotating-period cone continuation

Cycle 215 proves only that the frozen positive-period equation-(66)
specialization cannot implement the `E` reversal directly.  This block tries a
different, source-level construction: continue the *original* rarefied
hyperbolic-gamma kernel through the upper-half-plane path from `omega1` to
`-omega1`, with a moving separating contour.  It asks whether the resulting
endpoint comparison supplies the missing, label-dependent cocycle rather than
fitting one to the 36 packet labels.

<!-- research-freeze-v1
{
  "schema": "research-preregistration-freeze-v1",
  "cycle": 216,
  "parameters": {
    "fixed_lens_kernel": {
      "kind": "expression",
      "value": "Freeze the Sarkissian--Spiridonov equation-(66) d=6 kernel with M=((-p,-s),(k,-r))=((115,-24),(24,-5)), (p,k,r,s)=(-115,24,5,24), k=24, omega2=1, omega1=24*beta-5=beta^3=W>0, Q(u)=omega(u)+1, g=Q(u), ell=0, and the normalized Gamma_M pole formula (10). Keep this M fixed while continuing periods; do not replace it by M_E unless a cited source identity derives that comparison.",
      "rationale": "It separates period continuation from Cycle 215's direct matrix substitution."
    },
    "period_path_and_contour": {
      "kind": "expression",
      "value": "Freeze omega(u)=W*exp(pi*i*u), 0<=u<=1, approached from 0<u<1. For theta=pi*u set L_u(z)=Re(exp(-i*theta/2)*z) and C_u={z:L_u(z)=L_u(Q(u))/2}, with the fixed convention that true poles of Gamma_M(y,m) stay on the L_u<=0 side and true poles of Gamma_M(Q(u)-y,-m) stay on the L_u>=L_u(Q(u)) side. Endpoint values mean one-sided limits along this path only; no contour deformation, lower-half-plane path, or branch substitution is allowed.",
      "rationale": "The functional is the proposed concrete continuation mechanism and fixes the pole-side rule."
    },
    "divisor_audit": {
      "kind": "expression",
      "value": "For every m modulo 24 and every true-pole index j>=0, L=24*n+5*j+m>=0 in the first factor, and the analogous nonnegative L' for the Q-y factor, prove the exact cone inequalities L_u(-j*omega(u)-L)=-cos(theta/2)*(j*W+L)<=0 and L_u(Q(u)+j*omega(u)+L')=L_u(Q(u))+cos(theta/2)*(j*W+L')>=L_u(Q(u)). Record the corridor width L_u(Q(u))=(W+1)*cos(theta/2), its strict positivity on 0<u<1, and its one-sided collapse at u=1. A pole-side rule is valid only if it covers the full infinite divisor families symbolically, not a finite sample.",
      "rationale": "This is a falsifiable all-divisor control rather than a numerical contour picture."
    },
    "endpoint_cocycle_test": {
      "kind": "expression",
      "value": "Using only a source-stated Gamma_M identity valid on the frozen path (definitions (5)--(15), normalized reflection (33), shifts (38)--(39), or an explicitly cited analytic-continuation theorem), derive or fail to derive an endpoint comparison to the E-transported lens data M_E=((5,-24),(24,-115)). Test its induced all-36 packet factor against the exact defect t^(12-a-b). A label-dependent factor is admissible only when its complete formula is derived from that source identity before comparison; a fitted rowwise factor is forbidden.",
      "rationale": "Cycle 215 left precisely a source-derived label-dependent cocycle open."
    },
    "acceptance_boundary": {
      "kind": "expression",
      "value": "Advance only if a cited, hypothesis-checked source identity transports the fixed upper-half-plane continuation to M_E at the negative-period endpoint, fixes every branch and contour contribution, and yields an all-36 cocycle cancelling 12-a-b without target/C198 data. A controlled open-path cone with a collapsed endpoint corridor is not by itself an endpoint Gamma_M identity, packet duality, AFK statement, fusion theorem, Stark statement, or TCC proof.",
      "rationale": "It prevents treating existence of an interior contour family as the missing bridge."
    }
  },
  "resource_caps": {
    "discrete_channels": {"kind":"integer","value":24,"rationale":"The complete equation-(66) residue class system."},
    "packet_labels": {"kind":"integer","value":36,"rationale":"No label may be selected after the source derivation."},
    "period_paths": {"kind":"integer","value":1,"rationale":"Only the specified upper-half-plane semicircle is admissible."},
    "divisor_families": {"kind":"integer","value":2,"rationale":"The two Gamma_M factors are handled symbolically over their full index cones."},
    "wall_seconds": {"kind":"integer","value":180,"rationale":"Exact symbolic cone and exponent audit."},
    "floating_point": {"kind":"not_applicable","justification":"The path geometry is proved symbolically from W>0 and 0<u<1; no numerical Gamma_M values are evaluated.","rationale":"Numerics cannot establish divisor-side control or an endpoint cocycle."}
  },
  "formula_families": [
    "Sarkissian--Spiridonov rarefied hyperbolic gamma divisor formula (10)",
    "Sarkissian--Spiridonov normalized reflection and shift formulae (33), (38)--(39)",
    "Sarkissian--Spiridonov equation-(66) d=6 specialization",
    "Cycle-215 exact E transport and all-36 t-exponent defect"
  ],
  "selection_rule": [
    "First prove the moving-cone inequalities for the full symbolic pole families and identify the endpoint corridor limit.",
    "Then inspect only source-stated continuation/transformation identities to determine whether they compare the fixed M path endpoint with M_E.",
    "Compare a cocycle to all 36 labels only after its complete source derivation; retain an explicit failure to obtain such a law as a scoped result."
  ],
  "failure_rule": [
    "Do not infer endpoint continuation from the source's generic phrase 'analytic continuation', or replace the fixed upper path, pole-side convention, contour, M, or branch after seeing a mismatch.",
    "Do not truncate the infinite pole families, hide the collapsed endpoint corridor, or call a one-sided interior contour a valid undeformed endpoint contour.",
    "Do not import a label-dependent packet correction from C198, a formal pairing, or an unproved AFK covariance law; do not promote any result to fusion, Stark, or TCC."
  ],
  "pre_execution": {
    "timestamp_utc": "2026-08-03T06:17:39Z",
    "git_head": "cdfb2a9de532d48bf76c8dcb46b363488dbc8b5b",
    "git_state": "Dirty only from concurrent repository-wide PROGRAM migration and unrelated work; this cycle freezes the listed SIC--Stark inputs."
  },
  "input_paths": [
    "artifacts/cycle-215-b052-equation66-e-transport-v1.json",
    "scripts/dimension_six_ss_evaluation_audit.py",
    "proof/verify_cycle_190_balanced_helical_reflection.py",
    "proof/verify_cycle_215_equation66_e_transport.py",
    "paper/sic-stark-dimension-six-boundary-fusion.tex",
    "docs/cycle-188-stabilizer-covariance-preregistration-v1.md",
    "../../tools/preregistration_check.py"
  ]
}
-->
