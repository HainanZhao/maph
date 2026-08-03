# Cycle 207 / B044 preregistration: target-binomial recurrence audit

Cycle 206 constructed a denominator-free source projective packet.  Its
elementary source binomials can match C198 only if the corresponding target
binomials admit a genuine identity.  This block tests the first exact
mechanism: the complete standard factorwise `Gamma_M` shift/reflection
relation basis.  A failure of this basis is not a numerical nonvanishing claim.

<!-- research-freeze-v1
{
  "schema": "research-preregistration-freeze-v1",
  "cycle": 207,
  "parameters": {
    "target_binomials": {
      "kind": "expression",
      "value": "For every 0<=a,b<5, form Delta_(a,b)=L_(a,b)L_(a+1,b+1)-L_(a,b+1)L_(a+1,b) from exactly the C198 endpoint formula L_(a,b)=24*Gamma_M(Q,0)*Gamma_M(alpha_(a,b),N_(a,b))*Gamma_M(-alpha_(a,b),4-N_(a,b)). All 25 squares are mandatory; the common scalar may cancel only after both products are formed.",
      "rationale": "These are precisely the target relations necessary for the 25 source elementary binomials of C206."
    },
    "factorwise_relation_basis": {
      "kind": "expression",
      "value": "Admit only the standard factorwise S--S/C190 relation basis T1:(u,v,m)->(u+1,v,m+5), T2:(u,v,m)->(u,v+1,m-1), and normalized reflection (u,v,m)->(1-u,1-v,4-m) with reciprocal Gamma_M factor. For mu=u*omega+v, use the exact class c=3*(m-5*u+v) mod72; T1,T2 preserve c and reflection sends c to -c. Compare each four-factor target product by the sorted multiset of unoriented classes min(c mod72,-c mod72). Do not admit a new integral transform, duplication/multiplication theorem, numerical evaluation, or a post-result auxiliary identity.",
      "rationale": "It gives a finite exact necessary obstruction to the specific standard factorwise route while retaining its residual lens label."
    },
    "decision_rule": {
      "kind": "expression",
      "value": "If the two product signatures differ for a square, then no identity obtained solely by pairing/reindexing individual Gamma_M factors through the admitted shifts and normalized reflections can prove that target binomial zero. If signatures agree, retain that square for a separate exact residual-prefactor audit; do not declare its binomial zero.",
      "rationale": "Signature equality is necessary but not sufficient, preventing a recurrence census from becoming a target identity claim."
    },
    "claim_boundary": {
      "kind": "expression",
      "value": "A mismatch rejects only the declared standard factorwise Gamma_M recurrence/reflection derivation for that target binomial. It does not certify the binomial nonzero at the fixed endpoint, exclude a multifactor equation-(66) transform, global pairing, duplication/multiplication identity, projective intertwiner, AFK, fusion, Stark, or TCC.",
      "rationale": "The experiment is a precise identity-basis audit, not an unsupported special-function inequality."
    }
  },
  "resource_caps": {
    "target_binomials": {"kind":"integer","value":25,"rationale":"Every elementary 5-by-5 C198 square."},
    "gamma_factors_per_product": {"kind":"integer","value":4,"rationale":"Two endpoint factors in each of the two product terms after the common scalar is retained separately."},
    "relation_generators": {"kind":"integer","value":3,"rationale":"T1, T2, and normalized reflection only."},
    "class_modulus": {"kind":"integer","value":72,"rationale":"Three times the exact rational invariant modulo the lens period 24."},
    "wall_seconds": {"kind":"integer","value":180,"rationale":"Exact rational label and signature ledger only."},
    "floating_point": {"kind":"not_applicable","justification":"The test is a finite exact recurrence-class invariant and cannot certify endpoint values numerically.","rationale":"No numerical recognition or endpoint approximation is admissible."}
  },
  "formula_families": [
    "Cycle-198 equation-(66) endpoint formula and characteristic ledger",
    "Cycle-206 elementary projective target-binomial ledger",
    "Cycle-190 standard Gamma_M T1/T2/helical/reflection lattice"
  ],
  "selection_rule": [
    "Generate all 25 target binomials from the C198 characteristic ledger before comparing a signature.",
    "Use the listed factorwise relation basis and no extra multiplication, duplication, integral, contour, numerical, or target-fitted identity.",
    "Record every matching and mismatching square; only a mismatch may close the declared factorwise route, while a match remains unresolved pending residual-prefactor proof."
  ],
  "failure_rule": [
    "A signature mismatch is a scoped factorwise-recurrence obstruction, not a proof that the target binomial is nonzero.",
    "A signature match cannot be promoted to binomial vanishing or projective equality without a separately proved residual prefactor identity.",
    "No affine denominator, source t/h, scalar normalization, alias, exponent, ray datum, AFK value, fusion, Stark, or TCC consequence may be introduced."
  ],
  "pre_execution": {
    "timestamp_utc": "2026-08-03T05:00:38Z",
    "git_head": "00afe864c5b9bac0f82ac5d859fc59e89bccfd53",
    "git_state": "DIRTY from concurrent repository-wide PROGRAM migration and unrelated projects/tools, plus this live C207 preregistration. This block freezes only the listed SIC--Stark mathematical inputs."
  },
  "input_paths": [
    "artifacts/cycle-206-b043-projective-line-interface-v1.json",
    "artifacts/cycle-205-b042-mellin-b-pairing-v1.json",
    "artifacts/cycle-198-b035-analytic-frequency-endpoint-v1.json",
    "proof/verify_cycle_206_projective_line_interface.py",
    "proof/verify_cycle_198_analytic_frequency_endpoint.py",
    "proof/verify_cycle_190_balanced_helical_reflection.py",
    "../../tools/preregistration_check.py"
  ]
}
-->
