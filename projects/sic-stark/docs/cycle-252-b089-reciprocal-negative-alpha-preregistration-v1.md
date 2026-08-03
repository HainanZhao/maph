# Cycle 252 / B089 preregistration: reciprocal-base negative-alpha continuation

This block tests the explicit reciprocal-base extension left open by C251. It
asks whether that formula is a canonical analytic continuation of the source
ordinary hyperbolic gamma and whether it supplies all eight reflected factors.

<!-- research-freeze-v1
{
  "schema": "research-preregistration-freeze-v1",
  "cycle": 252,
  "parameters": {
    "source_formula": {
      "kind": "expression",
      "value": "Freeze Sarkissian--Spiridonov arXiv:1910.11747v4 equation (5): gamma(z;alpha,beta)=((qtilde*exp(2*pi*i*z/alpha);qtilde)_infinity)/((exp(2*pi*i*z/beta);q)_infinity), q=exp(2*pi*i*alpha/beta), qtilde=exp(-2*pi*i*beta/alpha), in its stated |q|<1 and |qtilde|<1 product chamber. Freeze the principal exponential ratios exactly; no numerical logarithm is used.",
      "rationale": "The proposed cross-sign law must start from the published normalization used by the existing source interfaces."
    },
    "reciprocal_base_rule": {
      "kind": "expression",
      "value": "For |Q|>1 define the candidate (x;Q)_out := 1/(Q^(-1)*x;Q^(-1))_infinity. Under alpha -> -alpha this gives F(z;-alpha,beta)=(q*exp(2*pi*i*z/beta);q)_infinity/(exp(-2*pi*i*z/alpha);qtilde)_infinity. Treat this as a candidate separate-chamber definition until path-independent meromorphic continuation from the source chamber is proved.",
      "rationale": "This is the unique frozen engine; no post-comparison correction or fitted Bernoulli factor is allowed."
    },
    "ordered_tests": {
      "kind": "expression",
      "value": "In order: (1) derive F algebraically from the reciprocal-base rule; (2) derive both alpha and beta shift equations and the double alpha-sign operation; (3) derive the exact reflection product as a Jacobi-theta ratio and any Bernoulli/monodromy factor with its branch; (4) determine from a cited theorem or a direct locally uniform argument whether F is path-independent meromorphic continuation of the source gamma across the signed-period cover; (5) only after all four pass, compare periods, arguments, labels, normalized degree-0:3 jets, and ordered factor products for all eight C251 reflected factors at both C249 embeddings.",
      "rationale": "Algebraic functional equations alone do not prove analytic continuation or source authorization."
    },
    "acceptance": {
      "kind": "expression",
      "value": "Accept only if the frozen F is proved to be a path-independent source continuation with fixed branch/monodromy, satisfies both source shifts and double-sign consistency, and matches every one of the eight opposite A/C factor states and normalized degree-0:3 jets without a fitted scalar. Stop and preserve the first exact failed prerequisite. A source theorem must have its hypotheses checked in this run.",
      "rationale": "The result must be strong enough to act on C250 rather than merely define another formal q-series."
    },
    "claim_boundary": {
      "kind": "expression",
      "value": "Passing constructs only the frozen negative-alpha ordinary-gamma continuation and its eight-factor finite-jet action. Failure excludes only this reciprocal-base rule. Neither outcome alone proves the full Gamma_M interface, boundary value, AFK identity, fusion continuity, Stark claim, or dimension-six TCC.",
      "rationale": "C252 is the first of the final three closeout blocks, not a downstream proof by itself."
    }
  },
  "resource_caps": {
    "candidate_rules": {"kind": "integer", "value": 1, "rationale": "The frozen reciprocal-base rule only."},
    "ordinary_gamma_factors": {"kind": "integer", "value": 8, "rationale": "Every C228/C251 reflected factor."},
    "embeddings": {"kind": "integer", "value": 2, "rationale": "Both C249 embeddings."},
    "jet_degree": {"kind": "integer", "value": 3, "rationale": "The complete C250 graded jet space."},
    "primary_sources": {"kind": "integer", "value": 2, "rationale": "Sarkissian--Spiridonov and one direct q-product/theta reference if required."},
    "floating_point": {"kind": "not_applicable", "justification": "Product transformations, shifts, theta ratios, state comparisons, and continuation hypotheses are symbolic or theorem-based.", "rationale": "Numerical agreement cannot prove path independence."},
    "wall_seconds": {"kind": "integer", "value": 1200, "rationale": "Symbolic eight-factor audit plus bounded primary-source verification."}
  },
  "formula_families": ["Sarkissian--Spiridonov equation (5) ordinary hyperbolic gamma", "inside- and reciprocal-base q-Pochhammer products", "Jacobi theta product and modular transformation", "C249 common chamber and normalized jets", "C250 graded F3 representation", "C251 reflected A/C factor states"],
  "selection_rule": ["Execute the five tests in their frozen order.", "Do not inspect or fit jet corrections after a failed source-continuation prerequisite.", "Check theorem hypotheses against the signed periods rather than citing a formula outside its domain."],
  "failure_rule": ["Do not substitute a different reciprocal convention, elliptic multiplier, continuation path, Bernoulli gauge, tilt, branch, or factor sign after execution.", "Do not infer a general negative-period no-go, full interface obstruction, AFK statement, fusion result, Stark claim, or TCC conclusion."],
  "pre_execution": {"timestamp_utc": "2026-08-03T10:37:13Z", "git_head": "d0d5f53a1c5878552e8455e07c69bcd34d1c5de7", "git_state": "Dirty from the existing repository-wide PROGRAM migration and unrelated work; this cycle freezes only the listed SIC--Stark inputs."},
  "input_paths": ["artifacts/cycle-228-b065-f3-square-residual-block-v1.json", "proof/verify_cycle_228_f3_square_residual_block.py", "artifacts/cycle-249-b086-common-jet-chamber-v1.json", "proof/verify_cycle_249_common_jet_chamber.py", "artifacts/cycle-250-b087-graded-f3-jet-representation-v1.json", "proof/verify_cycle_250_graded_f3_jet_representation.py", "artifacts/cycle-251-b088-residue-dual-cross-sign-v1.json", "proof/verify_cycle_251_residue_dual_cross_sign.py", "paper/sic-stark-dimension-six-boundary-fusion.tex", "../../tools/preregistration_check.py"]
}
-->

Claim boundary: this tests one explicit reciprocal-base continuation only; it
does not assume that a separate-chamber product is an analytic continuation.
