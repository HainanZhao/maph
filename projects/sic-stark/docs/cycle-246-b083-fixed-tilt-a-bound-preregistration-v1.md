# Cycle 246 / B083 preregistration: fixed-tilt A coefficient bound

This distinct block asks whether C245's source-defined A-word principal-
coefficient recurrence is bounded at one explicit common upper regularization.
It does not promote the constructed C244 current to a canonical current.

<!-- research-freeze-v1
{
  "schema": "research-preregistration-freeze-v1",
  "cycle": 246,
  "parameters": {
    "regularization": {
      "kind": "expression",
      "value": "Freeze w_sigma=t_sigma+i for both real embeddings t_+=55+12*sqrt(21), t_-=55-12*sqrt(21); every C228 affine period and mu_N=N*(115*w_sigma-1) is re-evaluated at that same w_sigma.",
      "rationale": "epsilon=1 is a fixed common upper chamber, not a post-result tilt choice."
    },
    "coefficient_norm": {
      "kind": "expression",
      "value": "Freeze ||kappa_N/kappa_1||_infinity=max(|kappa_N^+/kappa_1^+|,|kappa_N^-/kappa_1^-|), where each component is the C245 source-product recurrence at w_sigma.",
      "rationale": "This bounds the two embedding components without asserting an arithmetic action on gamma values."
    },
    "bound_target": {
      "kind": "expression",
      "value": "For every N>=1 prove ||kappa_N/kappa_1||_infinity <= C*(1+N)^d with C=2^40000000 and d=0.",
      "rationale": "The deliberately conservative constants are fixed before evaluation; no fitted constants are allowed."
    },
    "bound_engine": {
      "kind": "expression",
      "value": "Use only C245's exact finite-product multiplier. Prove each source factor is bounded by r^N with r=exp(-1/50000), then bound the 230 numerator and 50 inverse-denominator factors by sum r^N<50000 and sum -log(1-r^N)<100000. Do not use numerical gamma values or a fitted asymptotic.",
      "rationale": "A factorwise exact upper bound is a falsifiable replacement for the previously missing uniform small-divisor control."
    },
    "claim_boundary": {
      "kind": "expression",
      "value": "A pass proves only the stated normalized A-word coefficient bound at w_sigma=t_sigma+i. It neither removes C244's regulator-normalization ambiguity nor source-authorizes a current, defines a contour identity, or implies a mixed-base transform, B-Fourier covariance, AFK, fusion, Stark, or TCC.",
      "rationale": "Fixed-tilt boundedness is strictly weaker than a canonical bridge."
    }
  },
  "resource_caps": {
    "residual_words": {"kind": "integer", "value": 1, "rationale": "C228 A word only."},
    "ordinary_gamma_factors": {"kind": "integer", "value": 4, "rationale": "No factor omission."},
    "embeddings": {"kind": "integer", "value": 2, "rationale": "Both fixed real embeddings are required."},
    "factor_classes": {"kind": "integer", "value": 3, "rationale": "A1/A4 numerator, A1/A4 inverse denominator, and A2/A3 inverse pole factors."},
    "floating_point": {"kind": "not_applicable", "justification": "All inequalities use rational/algebraic estimates and analytic inequalities.", "rationale": "Numerical sampling cannot certify the all-N bound."},
    "wall_seconds": {"kind": "integer", "value": 300, "rationale": "Exact inequality audit and replay."}
  },
  "formula_families": ["C245 finite gamma-shift multiplier", "exact quadratic-field embedding bounds", "elementary exponential/product inequalities"],
  "selection_rule": ["Verify every factor class and both embeddings before multiplying bounds.", "Use the frozen r, factor counts, C, and d exactly.", "If a required lower bound fails, classify the target as falsified or unresolved; do not change the tilt, r, C, d, or method family."],
  "failure_rule": ["Do not use approximate gamma values, numerical sampling, a different regularization, a different norm, a smaller or fitted constant, an omitted factor, or a bound only for finite N.", "Do not infer a canonical current, source authorization, a contour identity, mixed-base transform, B-Fourier covariance, AFK, fusion, Stark, or TCC."],
  "pre_execution": {"timestamp_utc": "2026-08-03T12:20:00Z", "git_head": "38cc3a97bc51ff043b3a887fd6b912a27350761e", "git_state": "Dirty only from concurrent repository-wide PROGRAM migration and unrelated work; this cycle freezes the listed SIC--Stark inputs."},
  "input_paths": ["artifacts/cycle-228-b065-f3-square-residual-block-v1.json", "artifacts/cycle-245-b082-a-principal-coefficients-v1.json", "proof/verify_cycle_245_a_principal_coefficients.py", "../../tools/preregistration_check.py"]
}
-->

Claim boundary: this is a fixed-regularization coefficient bound for one
source-defined A word only.
