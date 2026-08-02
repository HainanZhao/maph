# Cycle 167 preregistration: bilinear torsor convolution

Can the graph of the sealed fibre-resolved torsor be multiplicative for an
independently specified translation-invariant bilinear `C6`-twisted
convolution, while its frozen Shintani transport is an algebra automorphism?

This is an exact finite algebra test only. A pass neither defines a
coefficient-to-logarithm map nor proves AFK identification, Stark, fusion, or
TCC.

<!-- research-freeze-v1
{
  "schema": "research-preregistration-freeze-v1",
  "cycle": 167,
  "parameters": {
    "base": {
      "kind": "expression",
      "value": "X=(Z/6Z)^2; Y=XxC6; s:X->C6 and d:X->C6 are the sealed Cycle-166 graph and transport",
      "rationale": "The test retains the full fibre-resolved construction and no quotient or fitted section is allowed."
    },
    "source_product": {
      "kind": "expression",
      "value": "delta_x * delta_y = delta_(x+y) on Q[X]",
      "rationale": "This is the fixed additive source algebra whose graph is tested."
    },
    "candidate_family": {
      "kind": "expression",
      "value": "for every M in Mat_2(Z/6Z), B_M((a,b),(c,d))=(a,b)M(c,d)^T mod 6 and delta_(x,e) star_M delta_(y,f)=delta_(x+y,e+f+B_M(x,y))",
      "rationale": "The complete 6^4 translation-invariant bilinear C6-twist family is fixed before evaluation."
    },
    "graph_and_transport": {
      "kind": "expression",
      "value": "J(delta_x)=delta_(x,s(x)); T_tilde(delta_(x,e))=delta_(Tx,e+d(x)); require J(delta_x*delta_y)=J(delta_x) star_M J(delta_y) and T_tilde(u star_M v)=T_tilde(u) star_M T_tilde(v) on all basis pairs",
      "rationale": "These are the preregistered multiplicativity and transport-automorphism identities."
    },
    "coefficient_ring": {
      "kind": "expression",
      "value": "Q-vector spaces with basis indexed by X or Y; all label equations are in C6",
      "rationale": "No floating-point phase, branch, or analytic target enters this finite test."
    }
  },
  "resource_caps": {
    "base_elements": {
      "kind": "integer",
      "value": 36,
      "rationale": "All characteristics are required."
    },
    "basis_pairs_per_candidate": {
      "kind": "integer",
      "value": 1296,
      "rationale": "Every ordered X-pair is checked for each identity."
    },
    "bilinear_matrices": {
      "kind": "integer",
      "value": 1296,
      "rationale": "This exhausts Mat_2(Z/6Z) without selection."
    },
    "identity_evaluations_per_family": {
      "kind": "integer",
      "value": 3359232,
      "rationale": "Two identities on 1296 pairs for each of 1296 matrices."
    },
    "wall_seconds": {
      "kind": "integer",
      "value": 30,
      "rationale": "The bounded exact census must remain a finite engine."
    },
    "floating_point": {
      "kind": "not_applicable",
      "justification": "All calculations are modular integer identities.",
      "rationale": "Numerical fitting would create an unfrozen operation."
    }
  },
  "formula_families": [
    "Cycle-166 sealed C6 torsor graph and Shintani transport",
    "complete translation-invariant bilinear C6-twisted convolution family",
    "basis-level graph multiplicativity and transport automorphism identities"
  ],
  "selection_rule": [
    "Enumerate every 2-by-2 matrix over Z/6Z and every ordered X-pair in lexicographic order.",
    "Accept a matrix only if both frozen identities hold on every pair; do not select a coboundary, nonlinear twist, or product after inspecting the graph defect.",
    "Report every passing matrix or, if none pass, the exact failure counts and first lexicographic witnesses."
  ],
  "failure_rule": [
    "If no matrix passes both identities, falsify only this translation-invariant bilinear C6-twisted convolution class.",
    "A passing matrix proves only the stated finite algebra construction, not a coefficient-to-logarithm operation, AFK interface, Stark identity, fusion theorem, or TCC.",
    "A failure does not rule out non-bilinear, non-translation-invariant, higher-fibre, or analytic operations."
  ],
  "pre_execution": {
    "timestamp_utc": "2026-08-02T16:24:41Z",
    "git_head": "d2e999b5554316aa3e802346d3629d19164c2361",
    "git_state": "?? docs/cycle-167-bilinear-convolution-preregistration-v1.md"
  },
  "input_paths": [
    "AGENTS.md",
    "PLAN.md",
    "artifacts/cycle-166-fibre-torsor-v1.json",
    "discovery/cycle-166-fibre-torsor-prototype-v1.json",
    "proof/verify_cycle_166_fibre_torsor.py",
    "../../tools/preregistration_check.py"
  ]
}
-->
