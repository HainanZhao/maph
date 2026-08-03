# Cycle 251 / B088 preregistration: residue-dual cross-sign test

This block tests whether C250's positive graded action canonically generates
an orientation-reversing action on its dual jet space. It is distinct from
C219's diagonal sign lifts because the candidate is derived from the
finite-rank residue pairing and the full graded transfer operator.

<!-- research-freeze-v1
{
  "schema": "research-preregistration-freeze-v1",
  "cycle": 251,
  "parameters": {
    "jet_pairing": {
      "kind": "expression",
      "value": "Freeze V=C[mu]/(mu^4) with ordered basis (1,mu,mu^2,mu^3) and residue pairing <f,g>=[mu^3]f(mu)g(mu), whose Gram matrix J has ones on the anti-diagonal. For an operator X define X^dagger=J^(-1)X^T J. Derive the adjoints of every lower-triangular multiplication M_h and pullback P_24 from this pairing; no fitted bilinear form or degree gauge is allowed.",
      "rationale": "This is the canonical Frobenius pairing on the exact C250 jet algebra."
    },
    "contragredient_candidate": {
      "kind": "expression",
      "value": "For C250 T_e^(n)=24^(-2n) M_h P_24, freeze the derived reverse candidate T_e^sharp=(T_e^dagger)^(-1). Compute it exactly through degree three, retaining its grading scalar, coordinate pullback, inverse multiplier, source/target, periods, affine coordinate, and label. Do not declare it a Gamma_M edge unless the source-state comparison passes.",
      "rationale": "The reverse map is forced by positive functoriality and the pairing rather than postulated as a negative-k product."
    },
    "orientation_test": {
      "kind": "expression",
      "value": "Freeze orientation reversal R:(omega1,omega2)->(-omega1,omega2). Compare R applied factorwise to the ordered C228 A block with C, and R(C) with A, at C249's w_sigma=t_sigma+i chamber. First test exact argument slopes, alpha/beta coefficient pairs, determinant signs, q/qtilde product domains, period/affine/label state, and only if all pass test the degree-0:3 contragredient matrix coefficients.",
      "rationale": "A source cross-sign law must remain in a defined analytic state before coefficient duality can be asserted."
    },
    "acceptance": {
      "kind": "expression",
      "value": "Accept a derived cross-sign intertwiner only if one canonical residue pairing makes both A-to-C and C-to-A reverse candidates agree with the opposite source states and all ordered degree-0:3 matrices. Falsify on the first exact state or chamber mismatch and stop before inspecting later coefficients; do not repair a failed comparison by multiplying a period or factor by -1, changing chamber, adding a Bernoulli gauge, or selecting another pairing.",
      "rationale": "The frozen engine is the canonical contragredient itself, not an after-the-fact signed continuation."
    },
    "claim_boundary": {
      "kind": "expression",
      "value": "Failure excludes only the canonical residue-dual cross-sign candidate on C250's fixed rank-four chamber. Passing would construct only that finite-jet cross-sign action and would not establish an endpoint limit, full Gamma_M continuation, packet map, canonical current, contour identity, mixed-base transform, B-Fourier covariance, AFK, fusion, Stark, or TCC.",
      "rationale": "The finite jet candidate is narrower than the full interface."
    }
  },
  "resource_caps": {
    "jet_rank": {"kind": "integer", "value": 4, "rationale": "C250's rank."},
    "pairings": {"kind": "integer", "value": 1, "rationale": "The canonical residue pairing only."},
    "orientation_maps": {"kind": "integer", "value": 1, "rationale": "omega1 sign reversal only."},
    "residual_blocks": {"kind": "integer", "value": 2, "rationale": "A and C."},
    "ordinary_gamma_factors": {"kind": "integer", "value": 8, "rationale": "Every C228 factor."},
    "embeddings": {"kind": "integer", "value": 2, "rationale": "Both C249 embeddings."},
    "floating_point": {"kind": "not_applicable", "justification": "Adjoints, sign maps, determinants, and chamber membership are exact.", "rationale": "Sampling cannot source-authorize orientation reversal."},
    "wall_seconds": {"kind": "integer", "value": 240, "rationale": "Exact rank-four and eight-factor audit."}
  },
  "formula_families": ["C250 graded positive-F3 jet representation", "Frobenius residue pairing on truncated polynomials", "contragredient representation", "C228 exact period pairs", "C249 q-product chamber"],
  "selection_rule": ["Derive J-adjoints before comparing any A/C factor.", "Apply R to both coefficients of each period pair exactly and compare factor order without sign repair.", "Stop at the first failed source-state or chamber prerequisite; do not continue to a fitted coefficient pairing."],
  "failure_rule": ["Do not choose another pairing, degree gauge, factor sign, Bernoulli correction, analytic continuation path, tilt, or negative-k definition after a mismatch.", "Do not infer a general signed-period no-go, endpoint theorem, packet map, canonical current, AFK, fusion, Stark, or TCC."],
  "pre_execution": {"timestamp_utc": "2026-08-03T10:27:50Z", "git_head": "e2408c4a505b863d7378fcf14c4334045ed78af8", "git_state": "Dirty only from concurrent repository-wide PROGRAM migration and unrelated work; this cycle freezes only the listed SIC--Stark inputs."},
  "input_paths": ["artifacts/cycle-219-b056-signed-k-extension-v1.json", "artifacts/cycle-228-b065-f3-square-residual-block-v1.json", "proof/verify_cycle_228_f3_square_residual_block.py", "artifacts/cycle-249-b086-common-jet-chamber-v1.json", "proof/verify_cycle_249_common_jet_chamber.py", "artifacts/cycle-250-b087-graded-f3-jet-representation-v1.json", "proof/verify_cycle_250_graded_f3_jet_representation.py", "paper/sic-stark-dimension-six-boundary-fusion.tex", "../../tools/preregistration_check.py"]
}
-->

Claim boundary: this is the canonical residue-dual candidate only, not a
general signed-period obstruction.
