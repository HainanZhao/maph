# Cycle 245 / B082 preregistration: A-word principal coefficients

This live block replaces C244's formal coefficient line by the exact
double-pole principal coefficients of the source-defined A residual product.
It neither supplies an A-to-C identity nor makes the constructed current
source-authorized.

Amendment — 2026-08-03: corrected the frozen Git commit hash before any
discovery, proof, test, or replay executable was created or run.

<!-- research-freeze-v1
{
  "schema": "research-preregistration-freeze-v1",
  "cycle": 245,
  "parameters": {
    "source_gamma": {
      "kind": "expression",
      "value": "Freeze Sarkissian--Spiridonov arXiv:1910.11747v4 equation (14) gamma(z;alpha,beta)=(qtilde*exp(2*pi*i*z/alpha);qtilde)_infty/(exp(2*pi*i*z/beta);q)_infty, with q=exp(2*pi*i*alpha/beta), qtilde=exp(-2*pi*i*beta/alpha), and the two shift relations obtained directly from that frozen product: gamma(z+alpha)=(1-exp(2*pi*i*z/beta))*gamma(z), gamma(z+beta)=(1-exp(2*pi*i*z/alpha))*gamma(z).", "rationale": "This is the source convention for every retained ordinary-gamma factor."},
    "principal_coefficients": {
      "kind": "expression",
      "value": "Freeze R_A as the ordered C228 A product. For N>=1 set mu_N=N*a, a=115*t-1, and define kappa_N=Coeff_{(mu-mu_N)^(-2)} R_A(mu). Normalize only by the source-defined ratio kappa_N/kappa_1; do not assign a numerical or fitted value to kappa_1.", "rationale": "C243 proves exactly the relevant two-pole family and C244 requires its actual coefficient recurrence."},
    "shift_lattice": {
      "kind": "expression",
      "value": "Freeze the exact a decompositions: for A2/A3, a=-beta; for A1/A4, a=115*alpha-24*beta. Derive the finite shift-product recurrence factor-by-factor, including the limiting two-pole factors, with no modular, reflection, or period sign replacement.", "rationale": "These identities determine whether the source product itself fixes a recurrence."},
    "growth_criterion": {
      "kind": "expression",
      "value": "A canonical tempered coefficient result requires an exact recurrence, Galois-swap rule, and a proved polynomial bound |kappa_N/kappa_1|<=C*(1+N)^d on the frozen upper-half-plane regularization with C,d fixed before evaluation. If the recurrence contains an unbounded or unproved small-divisor factor, withhold temperedness rather than fit C,d.", "rationale": "Local finiteness alone does not provide a tempered current."},
    "claim_boundary": {
      "kind": "expression",
      "value": "Any result is only about the A-word coefficient line and its recurrence/growth under the frozen regularization. It does not source-authorize the constructed current, define a contour identity, or imply a mixed-base transform, B-Fourier covariance, AFK, fusion, Stark, or TCC.", "rationale": "The missing interface remains separate."}
  },
  "resource_caps": {
    "residual_words": {"kind": "integer", "value": 1, "rationale": "The C228 A word only."},
    "ordinary_gamma_factors": {"kind": "integer", "value": 4, "rationale": "Every A factor remains present."},
    "pole_factors": {"kind": "integer", "value": 2, "rationale": "A2 and A3 only."},
    "shift_decompositions": {"kind": "integer", "value": 2, "rationale": "The two frozen shift forms of a."},
    "regularizations": {"kind": "integer", "value": 1, "rationale": "The fixed common upper-half-plane tilt only."},
    "floating_point": {"kind": "not_applicable", "justification": "Recurrence and any bound must be exact.", "rationale": "Numerical gamma samples cannot establish temperedness."},
    "wall_seconds": {"kind": "integer", "value": 300, "rationale": "Exact four-factor recurrence audit."}
  },
  "formula_families": ["Sarkissian--Spiridonov ordinary gamma product and shifts", "Cycle-228 A residual word", "Cycle-243 double-pole family", "exact finite q-Pochhammer/sine shift products"],
  "selection_rule": ["Derive each shift factor from the frozen product before combining factors.", "Treat the A2/A3 double-pole coefficient by an explicit Laurent limit.", "Separate a proved recurrence from any unproved asymptotic growth estimate."],
  "failure_rule": ["Do not evaluate or choose kappa_1, change the tilt, omit A1/A4, cancel a zero/pole without the exact limit, fit a recurrence, or assert a numerical growth rate.", "Do not infer source authorization, a contour identity, mixed-base transform, B-Fourier covariance, AFK, fusion, Stark, or TCC."],
  "pre_execution": {"timestamp_utc": "2026-08-03T11:26:00Z", "git_head": "7596a6185858cfb8fda19c8f2afcfaff85628b5e", "git_state": "Dirty only from concurrent repository-wide PROGRAM migration and unrelated work; this cycle freezes the listed SIC--Stark inputs."},
  "input_paths": ["artifacts/cycle-228-b065-f3-square-residual-block-v1.json", "proof/verify_cycle_228_f3_square_residual_block.py", "artifacts/cycle-243-b080-two-chamber-crossing-v1.json", "proof/verify_cycle_243_two_chamber_crossing.py", "artifacts/cycle-244-b081-constructed-abel-current-v1.json", "../../tools/preregistration_check.py"]
}
-->

Claim boundary: this is the actual coefficient-normalization question for one
constructed A current only.
