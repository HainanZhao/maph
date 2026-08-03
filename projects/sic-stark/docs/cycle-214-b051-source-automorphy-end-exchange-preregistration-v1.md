# Cycle 214 / B051 preregistration: source automorphy and end exchange

Cycle 213 showed that a merely formal two-ended space has no nonzero strictly
scalar complex-bilinear invariant pairing.  This block tests the concrete
source candidate for supplying the missing anti/dual structure: the
determinant-negative coordinate swap assembled from the documented theta and
conjugation transformations.

<!-- research-freeze-v1
{
  "schema": "research-preregistration-freeze-v1",
  "cycle": 214,
  "parameters": {
    "published_source_covariance": {
      "kind": "expression",
      "value": "Use only AFK arXiv:2501.03970v2 Theorems 7.7--7.8 as pinned in Cycle 188: for M in GL_2(Z), l=sgn(j_(M^-1)(rho_t)), normalized ghost overlaps transform from t_M to t by nu_p(t_M)=nu_(l*M*p)(t), while determinant -1 conjugates the underlying B_t cocycle factors. No statement about the Cycle-211 asymptotic packet coordinate t=exp(-pi*D*Lambda/(36*omega)) may be inferred unless it is explicitly supplied by those frozen source statements.",
      "rationale": "Separates genuine AFK tuple covariance from an invented action on the analytic packet ends."
    },
    "candidate_automorphisms": {
      "kind": "expression",
      "value": "Freeze J0=diag(1,-1), S=((0,1),(-1,0)), and E=J0*S=((0,1),(1,0)).  Freeze beta=(5+sqrt(21))/2, A6=((115,-24),(24,-5)), and cusp labels c_infinity=(0,5), c_zero=(5,0) modulo 6. Check label images, determinants, Mobius root images, j_(M^-1)(beta) signs, Q(a,b)=a^2-5ab+b^2 invariance, and conjugation of A6.",
      "rationale": "E is the smallest documented conjugation-theta composite that can exchange the two frozen labels."
    },
    "same_object_and_duality_criterion": {
      "kind": "expression",
      "value": "Accept a source-derived end exchange or dual line only if a frozen source theorem both acts on the same beta-oriented Cycle-211/212 packet (or explicitly identifies its transformed tuple with it) and maps its two actual asymptotic sections. Accept a scalar dual/sesquilinear pairing only if that same theorem supplies the anti/dual action and its coefficient-line cancellation. A label permutation, a transformed root beta^-1, a transformed-tuple ghost-overlap equality, or a formal Hermitian form alone fails acceptance.",
      "rationale": "This prevents transformed-tuple covariance from being mislabeled as a same-packet fusion mechanism."
    },
    "claim_boundary": {
      "kind": "expression",
      "value": "The block can prove only the exact relationship of the three frozen GL_2 matrices to the two labels, A6, beta, and the stated AFK covariance domain. It cannot prove a new AFK theorem, an action on the axis/logarithmic coordinate, analytic endpoint gluing, a multiplier trivialization, C198 comparison, fusion, Stark, or TCC statement.",
      "rationale": "The intended result is a discriminating source-domain test."
    }
  },
  "resource_caps": {
    "candidate_matrices": {"kind":"integer","value":3,"rationale":"Exactly J0, S, and their frozen composite E."},
    "cusp_labels": {"kind":"integer","value":2,"rationale":"Exactly the Cycle-211 extrema."},
    "matrix_identity_checks": {"kind":"integer","value":12,"rationale":"Fixed finite determinant, action, root, form, and conjugacy checks."},
    "source_theorems": {"kind":"integer","value":2,"rationale":"Only the pinned AFK covariance theorems."},
    "wall_seconds": {"kind":"integer","value":180,"rationale":"Exact quadratic-field and integer-matrix audit."},
    "floating_point": {"kind":"not_applicable","justification":"All root identities are represented in Q(sqrt(21)) and all label actions are integral.","rationale":"No numerical packet limit is evaluated."}
  },
  "formula_families": [
    "AFK GL_2 transformed-tuple covariance and determinant-negative conjugation",
    "Cycle-188 source covariance provenance",
    "Cycle-211 cusp-label and A6 multiplier data",
    "Exact Q(sqrt(21)) Mobius action and binary-quadratic-form identities"
  ],
  "selection_rule": [
    "Check all matrix and root identities before interpreting a covariance statement.",
    "Treat E as an end-exchange candidate only if it maps c_infinity to c_zero and reverses the frozen A6 step exactly.",
    "Promote an analytic end exchange or scalar dual pairing only on the exact same-object-and-duality criterion; otherwise record the domain mismatch as the result."
  ],
  "failure_rule": [
    "Do not call E a same-tuple map merely because Q_E=Q; beta and beta^-1 must be compared explicitly.",
    "Do not turn determinant-negative cocycle conjugation into an action on the Cycle-211 packet, Lambda, s, or packet t without a frozen theorem.",
    "Do not construct a formal Hermitian pairing to cure the C213 obstruction, fit C198, or claim fusion from a label exchange.",
    "If any matrix, label, root, sign, source-domain, or replay condition disagrees, withhold the candidate conclusion."
  ],
  "pre_execution": {
    "timestamp_utc": "2026-08-03T06:01:02Z",
    "git_head": "e1c67b19f7e708765ad70d6606b96f51092f5063",
    "git_state": "Dirty only from concurrent repository-wide PROGRAM migration and unrelated work; this cycle freezes the listed SIC--Stark inputs."
  },
  "input_paths": [
    "artifacts/cycle-188-stabilizer-covariance-v1.json",
    "artifacts/cycle-211-b048-cusp-asymptotic-flat-sections-v1.json",
    "artifacts/cycle-213-b050-two-ended-completion-v1.json",
    "docs/cycle-188-stabilizer-covariance-preregistration-v1.md",
    "proof/verify_cycle_188_stabilizer_covariance.py",
    "proof/verify_cycle_211_cusp_asymptotic_flat_sections.py",
    "scripts/dimension_six_stabilizer_ledger.py",
    "../../tools/preregistration_check.py"
  ]
}
-->
