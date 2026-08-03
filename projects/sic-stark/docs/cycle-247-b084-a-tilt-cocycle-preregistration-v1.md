# Cycle 247 / B084 preregistration: A-word tilt cocycle

This block tests a source-derived necessary condition for regulator-independent
normalization: whether a scalar base normalization can make the normalized
A-word principal-coefficient line independent of the common upper tilt.

<!-- research-freeze-v1
{
  "schema": "research-preregistration-freeze-v1",
  "cycle": 247,
  "parameters": {
    "tilt_state": {
      "kind": "expression",
      "value": "Freeze t=t_+=55+12*sqrt(21), epsilon in (0,infinity), w_epsilon=t+i*epsilon, q_epsilon=exp(2*pi*i*(w_epsilon+5)/24), and r_N^(epsilon)=kappa_N^(epsilon)/kappa_1^(epsilon) from the C245 source recurrence. The branch is the ordinary complex exponential; no logarithm branch is selected.",
      "rationale": "The plus embedding alone is a sufficient falsifier of simultaneous two-embedding tilt stability."
    },
    "comparison_invariant": {
      "kind": "expression",
      "value": "Freeze H_N(epsilon,epsilon')=r_N^(epsilon)/r_N^(epsilon'). Base-only normalization means replacing every kappa_N^(epsilon) by b(epsilon)*kappa_N^(epsilon), so it leaves every H_N unchanged. Freeze the C245-derived candidate multiplier T_N(q)=[ product_{j=115*N}^{115*N+114}(1-q^j) / ((1-q^(N+1))*product_{j=24*N+1}^{24*N+24}(1-q^j)) ]^2.",
      "rationale": "This is the exact comparison cocycle to be derived from all four retained A factors before testing stability."
    },
    "criterion": {
      "kind": "expression",
      "value": "Accept base-only tilt stability only if H_N(epsilon,epsilon')=1 for every N>=1 and every epsilon,epsilon'>0; equivalently every T_N(q_epsilon) is tilt-independent. Falsify it if the derived T_1(q) is a nonconstant analytic function on the open unit disk, using its exact q-series coefficient rather than sampled tilts.",
      "rationale": "A scalar base cannot change normalized recurrence ratios."
    },
    "claim_boundary": {
      "kind": "expression",
      "value": "A failure proves only that no base-only scalar normalization makes the C245 normalized A-word recurrence tilt-independent. It does not identify C244's constructed-current coefficients with the source line, prove a regulator-independent source current, or imply a contour identity, mixed-base transform, B-Fourier covariance, AFK, fusion, Stark, or TCC.",
      "rationale": "The source-to-current interface remains absent."
    }
  },
  "resource_caps": {
    "residual_words": {"kind": "integer", "value": 1, "rationale": "C228 A word only."},
    "ordinary_gamma_factors": {"kind": "integer", "value": 4, "rationale": "Every retained factor is used in the cocycle collapse."},
    "embeddings": {"kind": "integer", "value": 1, "rationale": "A plus-embedding counterexample suffices for the frozen base-only stability criterion."},
    "multiplier_indices": {"kind": "integer", "value": 1, "rationale": "N=1 is the preregistered analytic nonconstancy witness after the all-N formula is derived."},
    "q_series_degree": {"kind": "integer", "value": 2, "rationale": "The q^2 coefficient is the only allowed nonconstancy witness."},
    "floating_point": {"kind": "not_applicable", "justification": "The criterion is an exact analytic identity/nonidentity.", "rationale": "Tilt sampling cannot prove or refute the all-tilt statement."},
    "wall_seconds": {"kind": "integer", "value": 300, "rationale": "Exact four-factor collapse and q^2 coefficient audit."}
  },
  "formula_families": ["C245 finite ordinary-gamma shift multiplier", "C228 A period pairs", "analytic q-product and identity theorem"],
  "selection_rule": ["First derive the same q_epsilon in every retained factor and the exact all-N T_N(q) formula.", "Then inspect only the frozen N=1, q^2 coefficient for analytic nonconstancy.", "If the collapse, coefficient, or identity-theorem hypothesis fails, record that exact failure without choosing another cocycle or normalization family."],
  "failure_rule": ["Do not choose a tilt-dependent N-dependent gauge, compare arbitrary constructed C244 coefficients to the source line, sample q or gamma values, alter the tilt range, use another embedding, or inspect q-series degree other than 2.", "Do not infer a canonical current, source authorization, a contour identity, mixed-base transform, B-Fourier covariance, AFK, fusion, Stark, or TCC."],
  "pre_execution": {"timestamp_utc": "2026-08-03T13:05:00Z", "git_head": "49deaf3535775b94fe375f79462fb2e4df029e42", "git_state": "Dirty only from concurrent repository-wide PROGRAM migration and unrelated work; this cycle freezes the listed SIC--Stark inputs."},
  "input_paths": ["artifacts/cycle-228-b065-f3-square-residual-block-v1.json", "artifacts/cycle-244-b081-constructed-abel-current-v1.json", "artifacts/cycle-245-b082-a-principal-coefficients-v1.json", "proof/verify_cycle_245_a_principal_coefficients.py", "../../tools/preregistration_check.py"]
}
-->

Claim boundary: this is a scoped no-go for base-only tilt stability of one
source-defined A-word coefficient line.
