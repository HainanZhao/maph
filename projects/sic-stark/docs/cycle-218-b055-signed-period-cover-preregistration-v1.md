# Cycle 218 / B055 preregistration: signed-period product cover

Cycle 217 proves that the raw two-step source word reaches `-M_E` only
projectively and ends at `576*(omega2,omega1)` with label zero.  This block
does not repair that state by convention.  It derives the available scaling,
period-swap, and sign laws directly from the rarefied-gamma product definition
and asks whether any *legal* lifted state reaches the E data.

<!-- research-freeze-v1
{
  "schema": "research-preregistration-freeze-v1",
  "cycle": 218,
  "parameters": {
    "frozen_raw_endpoint": {
      "kind": "expression",
      "value": "Freeze Cycle-217 raw endpoint: matrix state -S_E=(5,-24,-115,-24), projective matrix -M_E, periods (Omega1,Omega2)=576*(omega2,omega1), continuous argument 576*(mu+m*omega2), and discrete label 0. Freeze the E target as S_E=(-5,24,115,24), periods (-omega1,omega2), with the packet defect t^(12-a-b).",
      "rationale": "The cover must compare the complete affine state, not merely its matrix projection."
    },
    "product_definition_cover": {
      "kind": "expression",
      "value": "Freeze the S--S unnormalized product definition (5), its modular parameters (6)--(8), and finite ordinary-gamma product (15), together with normalized factor (29)--(33). The cover state is (signed matrix representative, ordered period pair up to a positive common scale, affine continuous argument, discrete label modulo 24, normalization/branch factor, and unsuppressed ordinary-gamma residual list). A law is legal only if it is derived from these frozen formulae with all denominators and product-index relabelings checked.",
      "rationale": "It makes sign and ordering part of the state instead of silently quotienting them away."
    },
    "candidate_laws": {
      "kind": "expression",
      "value": "Test exactly three proposed laws: (i) positive common scaling by 576; (ii) ordered-period swap via a Delta(k,p,m) index relabeling using pr=1 mod k, including the induced p/r and discrete-label change; (iii) simultaneous projective matrix/period sign reversal. The first two are candidates to prove from the products; the third is a candidate to derive or contain. No other modular transformation, contour move, or recurrence word is allowed.",
      "rationale": "The three operations are precisely the discrepancies exposed by Cycle 217."
    },
    "legal_lift_test": {
      "kind": "expression",
      "value": "Apply only derived legal laws to the frozen raw endpoint and compare every state coordinate to the E target: representative, ordered periods modulo allowed positive scale, affine argument, discrete label, normalization/branch, and residual list. A matrix match with any other coordinate unmatched is a failure. Test packet t^(12-a-b) only if every coordinate matches and a source-derived map to all 36 (a,b) labels exists.",
      "rationale": "It blocks projective or scalar-only pseudo-progress."
    },
    "acceptance_boundary": {
      "kind": "expression",
      "value": "Advance only if product-derived laws legalize a complete raw-endpoint-to-E lift and supply a source formula for every residual/normalization factor; then, and only then, test an unfitted all-36 cocycle. If a proposed law is undefined, changes a forbidden state coordinate, or leaves a residual factor, record it exactly. No result proves AFK covariance, fusion, Stark, or TCC.",
      "rationale": "The missing bridge is a fully oriented source transformation, not a formal period quotient."
    }
  },
  "resource_caps": {
    "candidate_laws": {"kind":"integer","value":3,"rationale":"Only scaling, swap, and simultaneous sign are frozen."},
    "finite_product_indices": {"kind":"integer","value":24,"rationale":"Complete Delta(k,p,m) reindexing at k=24."},
    "endpoint_states": {"kind":"integer","value":2,"rationale":"The raw Cycle-217 endpoint and E target only."},
    "packet_labels": {"kind":"integer","value":36,"rationale":"Used only after a full legal lift."},
    "wall_seconds": {"kind":"integer","value":240,"rationale":"Exact finite index and affine-state audit."},
    "floating_point": {"kind":"not_applicable","justification":"All product-index, matrix, period-basis, and label computations are exact; no Gamma_M values are numerically evaluated.","rationale":"Numerics cannot establish a sign or branch law."}
  },
  "formula_families": [
    "Sarkissian--Spiridonov equations (5)--(15) and (29)--(33)",
    "Cycle-217 raw two-step affine endpoint",
    "Exact Delta(k,p,m) reindexing at k=24",
    "Cycle-215 E target and all-36 packet exponent defect"
  ],
  "selection_rule": [
    "Prove or contain positive scaling, swap, and simultaneous-sign candidates separately from the frozen products before composing them.",
    "Check all 24 finite Delta indices for any swap law and retain every phase/normalization/residual factor.",
    "Declare a legal lift only after every frozen cover coordinate agrees; otherwise do not run a packet-cocycle fit."
  ],
  "failure_rule": [
    "Do not identify -M_E with M_E, swap periods, divide by 576, or alter a discrete label by convention without the corresponding derived product law.",
    "Do not suppress an ordinary-gamma factor, choose an unregistered branch, introduce another source transformation, or expand the cover state after a mismatch.",
    "Do not call a partial cover match, a matrix equality, or a fitted label factor a Gamma_M, AFK, fusion, Stark, or TCC theorem."
  ],
  "pre_execution": {
    "timestamp_utc": "2026-08-03T06:34:29Z",
    "git_head": "b1d3786db41bbbfab1ae985dcf20d26008337339",
    "git_state": "Dirty only from concurrent repository-wide PROGRAM migration and unrelated work; this cycle freezes the listed SIC--Stark inputs."
  },
  "input_paths": [
    "artifacts/cycle-215-b052-equation66-e-transport-v1.json",
    "artifacts/cycle-217-b054-source-transformation-groupoid-v1.json",
    "scripts/dimension_six_ss_evaluation_audit.py",
    "proof/verify_cycle_217_source_transformation_groupoid.py",
    "proof/verify_cycle_190_balanced_helical_reflection.py",
    "paper/sic-stark-dimension-six-boundary-fusion.tex",
    "docs/cycle-188-stabilizer-covariance-preregistration-v1.md",
    "../../tools/preregistration_check.py"
  ]
}
-->
