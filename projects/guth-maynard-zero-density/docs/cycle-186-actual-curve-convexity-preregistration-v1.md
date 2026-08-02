# Cycle 186 preregistration: actual-curve convexity grid exclusion

## Frozen question

Can the actual positive-exponential curve exclude a locally clustered triple
of deep rational rays even when the labels contain no arithmetic progression?
The engine uses the weighted additive convexity of
`z^ell=1+alpha_ell`, exact rational grids from three retained denominators,
and the row-depth approximation errors.

<!-- research-freeze-v1
{
  "cycle": 186,
  "failure_rule": [
    "Seal NO_GO_OR_LOCAL_ONLY if the exact weighted second difference cannot be placed strictly between its retained approximation error and its rational denominator grid.",
    "Do not promote an AP-only identity, a mass/capacity argument, a scalar denominator count, or an unweighted convexity slogan.",
    "A local three-point exclusion without a quantified critical-box population saving is local-only and does not advance density."
  ],
  "formula_families": [
    "pinned actual curve z^ell=exp(2*pi*ell/Delta)=1+alpha_ell",
    "weighted convexity C=p*z^a+q*z^c-(p+q)*z^b for a<b<c, q=b-a, p=c-b",
    "three rational shifted slopes B_i/U_i approximating z^i with retained row-depth errors",
    "integer denominator grid after clearing U_a*U_b*U_c",
    "C182 full-fibre capacity U_i<=H/(N_i-1)"
  ],
  "input_paths": [
    "artifacts/cycle-182-fibre-line-rigidity-v1.json",
    "artifacts/cycle-183-intercept-cleared-ray-box-v1.json",
    "artifacts/cycle-185-three-label-curvature-convention-correction-v1.json",
    "proof/cycle_seal_v1.py",
    "../../tools/preregistration_check.py"
  ],
  "parameters": {
    "phase": {
      "kind": "expression",
      "rationale": "This engine must use the pinned shifted phase, not the invalid unshifted C185 identity.",
      "value": "z=exp(2*pi/Delta), alpha_i=z^i-1, B_i=A_i+U_i"
    },
    "triple": {
      "kind": "symbolic",
      "rationale": "No arithmetic progression is assumed.",
      "value": "a<b<c, q=b-a, p=c-b, r=p+q"
    },
    "strict_gate": {
      "kind": "expression",
      "rationale": "Exact rationality is useful only in the forbidden sandwich between curve curvature and denominator spacing.",
      "value": "E < C_curve and C_curve+E < 1/(U_a*U_b*U_c)"
    },
    "retained_state": {
      "kind": "symbolic",
      "rationale": "All errors must remain row-depth-sensitive and denominator-labelled.",
      "value": "(a,b,c,p,q,U_a,U_b,U_c,N_a,N_b,N_c,A_i,B_i,full fibres,residuals,stable shells)"
    }
  },
  "pre_execution": {
    "git_head": "1a7d3552434cea520ee08f46618df12cb5b24b39",
    "git_state": "clean worktree; C186 preregistration and one working ledger created before executable code",
    "timestamp_utc": "2026-08-02T14:22:28Z"
  },
  "resource_caps": {
    "candidate_engine_count": {
      "kind": "integer",
      "rationale": "Use one three-point actual-curve engine; do not branch into another occupancy argument.",
      "value": 1
    },
    "label_dimension": {
      "kind": "integer",
      "rationale": "Three labels are the first configuration with additive curvature while avoiding the AP restriction.",
      "value": 3
    },
    "new_executable_code": {
      "kind": "not_applicable",
      "justification": "The first task is an exact inequality specification and failure criterion; code follows after this freeze validates.",
      "rationale": "Preflight precedes executable derivation, tests, and replay code."
    }
  },
  "schema": "research-preregistration-freeze-v1",
  "selection_rule": [
    "Prove the convexity-grid lemma with exact cleared integers and a separately checked analytic curvature envelope.",
    "Count an advance only if the lemma, together with frozen box parameters, forces a strict populated-box saving, a seeded recurrence, or a genuine critical actual saturator."
  ]
}
-->

