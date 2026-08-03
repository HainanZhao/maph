# Cycle 210 / B047 preregistration: logarithmic projective connection

Cycle 209 makes a moving source transport unavoidable for the complete packet.
This block derives the only diagonal logarithmic transport forced by the
Cycle-206 exponents, audits its `A6`/multiplier covariance, and tests whether
it has a basepoint-free canonical comparison to C198.

<!-- research-freeze-v1
{
  "schema": "research-preregistration-freeze-v1",
  "cycle": 210,
  "parameters": {
    "source_connection": {
      "kind": "expression",
      "value": "For P_(a,b;h)(t)=zeta_6^(5*h*a)*t^E_(a,b) with E_(a,b)=4*b-5*a, on either connected admissible component t>1 or 0<t<1, freeze the diagonal logarithmic connection nabla=d-diag(E_(a,b))*dlog(t). Its parallel transport from t0 to t1 is diag((t1/t0)^E_(a,b)). Work projectively, modulo common scalar transport only.",
      "rationale": "It is forced by the exact source exponent array, without a target fit."
    },
    "gauge_and_base_data": {
      "kind": "expression",
      "value": "No basepoint t0, source fibre, affine coordinate, target ratio, or transport normalization may be selected. Compare two formal admissible basepoints t0 and u0 in the same component; their transports differ by diag((u0/t0)^E_(a,b)). Test labels (0,0),(0,1), whose exponent difference is 4.",
      "rationale": "A projective connection is only a relative transport until base data are supplied."
    },
    "a6_multiplier_audit": {
      "kind": "expression",
      "value": "Audit all 36 labels: A6 is identity modulo 6 and its frozen multiplier action is diagonal by the exact Kopp/AFK ledger. Since the exponent connection is also diagonal and label-fixed, the two actions commute. This is covariance of transport only, not an amplitude identification.",
      "rationale": "It tests the required finite symmetry without inventing a target map."
    },
    "acceptance_rule": {
      "kind": "expression",
      "value": "Accept only if the 36 exponent connection, exact transport law, all-36 A6/multiplier commutation, and the basepoint-change non-scalar witness are checked. The no-canonical-comparison conclusion requires that the basepoint-change ratio at labels (0,1)/(0,0) equals (u0/t0)^4 and is nonconstant for exact admissible pairs (t0,u0)=(2,3).",
      "rationale": "It separates a valid moving connection from an unsupported C198 endpoint identification."
    },
    "claim_boundary": {
      "kind": "expression",
      "value": "This block may prove a source logarithmic projective connection and a basepoint-free normalization obstruction. It does not rule out a separately source-authorized canonical base datum, non-diagonal connection, target-side theorem, AFK identity, fusion, Stark, or TCC statement.",
      "rationale": "A missing normalization is a design boundary, not a universal no-go."
    }
  },
  "resource_caps": {
    "label_count": {"kind":"integer","value":36,"rationale":"All C6xC6 characteristics."},
    "source_channel_count": {"kind":"integer","value":6,"rationale":"All h channels remain in the source derivation."},
    "basepoint_pairs": {"kind":"integer","value":1,"rationale":"The exact admissible pair (2,3) witnesses non-scalar basepoint change."},
    "wall_seconds": {"kind":"integer","value":180,"rationale":"Exact finite exponent and multiplier audit."},
    "floating_point": {"kind":"not_applicable","justification":"Only integer exponents, rational witnesses, and exact finite multiplier phases are used.","rationale":"No target endpoint is evaluated."}
  },
  "formula_families": [
    "Cycle-206 denominator-free projective normal packet",
    "dimension-six A6 stabilizer and multiplier ledger",
    "Cycle-209 admissible all-fibre fixed-diagonal no-go"
  ],
  "selection_rule": [
    "Retain all labels and h channels, with no selected source fibre or target coordinate.",
    "Use the source-forced diagonal exponent connection only; do not add a fitted scalar or target-dependent gauge.",
    "Use only the exact same-component basepoint witness (t0,u0)=(2,3)."
  ],
  "failure_rule": [
    "Do not promote A6/multiplier commutation to C198 amplitude equality or AFK covariance.",
    "Do not turn the basepoint-free obstruction into a no-go for a source-authorized base datum or broader connection class.",
    "If any exponent, projective quotient, multiplier action, basepoint domain, or witness ratio disagrees, withhold every connection or obstruction claim."
  ],
  "pre_execution": {
    "timestamp_utc": "2026-08-03T05:33:46Z",
    "git_head": "eae17aea7d571b4748d8e9d90e6b153db4073f3e",
    "git_state": "Dirty only from concurrent repository-wide PROGRAM migration outside this new cycle; Cycle 210 freezes the listed SIC--Stark mathematical inputs."
  },
  "input_paths": [
    "artifacts/cycle-209-b046-fixed-diagonal-projective-interface-v1.json",
    "artifacts/cycle-206-b043-projective-line-interface-v1.json",
    "proof/verify_cycle_209_fixed_diagonal_projective_interface.py",
    "proof/verify_cycle_206_projective_line_interface.py",
    "scripts/dimension_six_stabilizer_ledger.py",
    "../../tools/preregistration_check.py"
  ]
}
-->
