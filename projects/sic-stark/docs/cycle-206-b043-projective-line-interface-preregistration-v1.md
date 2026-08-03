# Cycle 206 / B043 preregistration: projective normal-line interface

Cycle 205 proved that the local Mellin residue retains a common regulator
weight.  This block tests the distinct construction suggested by that fact:
pass the complete normal packet through its common weight-one line and retain
only denominator-free projective data.  It may establish a covariant source
projective object; it may not call a label correspondence an amplitude map.

<!-- research-freeze-v1
{
  "schema": "research-preregistration-freeze-v1",
  "cycle": 206,
  "parameters": {
    "source_normal_packet": {
      "kind": "expression",
      "value": "For exactly (a,b,h) in (Z/6Z)^3, retain the Cycle-200 first regular packet P_(a,b;h)(t)=zeta_6^(5*h*a)*t^(4*b-5*a)*(1+t^6+t^12), t=exp(-pi*D*Lambda/(36*omega)), on real Lambda!=0. The rank-36 normal vector is R=lambda*P and lambda is its sole regulator line coordinate.",
      "rationale": "This is the complete frozen all-character source packet, not a chosen row, channel, alias, or endpoint value."
    },
    "projective_quotient": {
      "kind": "expression",
      "value": "Quotient R by only its common nonzero lambda scaling. Represent its projective data by every elementary 2-by-2 homogeneous binomial P_(a,b;h)P_(a+1,b+1;h)-P_(a+1,b;h)P_(a,b+1;h) for 0<=a,b<5 and every h in Z/6Z, together with the ordered label ledger. No affine chart, component denominator, t value, h value, scalar, or normalization may be selected.",
      "rationale": "The elementary binomials give a finite denominator-free test of the source toric projective line without converting it into an amplitude."
    },
    "target_comparison": {
      "kind": "expression",
      "value": "Use exactly the 36 finite nonzero C198 endpoint values L_(a,b) with their frozen (sigma,N mod 24) labels. Test only: label preservation, all-row nonzeroness, and whether a source theorem supplies equality of the frozen source homogeneous binomials with the corresponding target homogeneous binomials. Absence of such a theorem is a contained missing interface, not a numerical or symbolic inequality claim.",
      "rationale": "C198 defines a linear endpoint functional, while a projective equality would require a new multiplicative source law."
    },
    "a6_covariance": {
      "kind": "expression",
      "value": "Use the exact A6 axis action s->beta^(-6)*s, the common normal weight one, A6 mod 6=identity on all 36 characteristics, and psi^2(A6)=-1. Verify that source projective data are invariant under the common normal rescaling and that the C198 label ledger is fixed projectively; do not infer numerical amplitude equality from covariance.",
      "rationale": "This separates the exact common-line covariance that projectivization can remove from the still-missing bridge."
    },
    "claim_boundary": {
      "kind": "expression",
      "value": "A positive source result proves only a denominator-free all-row projective normal packet and its A6 covariance. A negative/contained result rejects only the claim that the listed inputs already define a source-selected projective equality to C198. It does not exclude an equation-(66) multiplicative theorem, global Mellin pairing, nonlinear/higher-germ/non-Abel continuation, AFK, fusion, Stark, or TCC.",
      "rationale": "The block cannot elevate a common scaling quotient into the missing amplitude theorem."
    }
  },
  "resource_caps": {
    "character_rows": {"kind":"integer","value":36,"rationale":"The entire characteristic grid is mandatory."},
    "residue_channels": {"kind":"integer","value":6,"rationale":"All h channels are retained; none is selected."},
    "elementary_binomials": {"kind":"integer","value":150,"rationale":"25 grid squares times six h channels, each denominator-free."},
    "dilation_probes": {"kind":"integer","value":3,"rationale":"q in {2,3,5} tests common-line invariance."},
    "wall_seconds": {"kind":"integer","value":180,"rationale":"Exact finite label and binomial ledger only."}
  },
  "formula_families": [
    "Cycle-200 full three-residue regular packet",
    "Cycle-201/202 common regulator-weight-one normal line",
    "Cycle-198 analytic-frequency endpoint character ledger",
    "dimension-six A6 stabilizer and multiplier ledger"
  ],
  "selection_rule": [
    "Enumerate every 36 source label, all six h channels, and every elementary grid binomial before examining target formulas.",
    "Use no quotient coordinate with a selected denominator; homogeneous products and their exact vanishing are the sole allowed source projective coordinates.",
    "Mark C198 comparison as established only if an imported frozen source theorem explicitly equates the relevant homogeneous target and source expressions with matching labels."
  ],
  "failure_rule": [
    "A common lambda weight cancelling in projective source data is not an all-row C198 amplitude equality.",
    "If the frozen inputs provide no multiplicative equation-(66) or other source theorem for C198 homogeneous binomials, classify the C198 projective equality as an open interface rather than fitting ratios or declaring inequality.",
    "No selected t, h, affine chart, scalar normalization, alias, exponent, ray datum, AFK value, fusion, Stark, or TCC consequence is admissible."
  ],
  "pre_execution": {
    "timestamp_utc": "2026-08-03T04:51:57Z",
    "git_head": "4ff54f0c970549abc22d331da1319973a7fe8ef9",
    "git_state": "DIRTY from concurrent repository-wide PROGRAM migration and unrelated projects/tools, plus this live C206 preregistration. This block freezes only the listed SIC--Stark mathematical inputs."
  },
  "input_paths": [
    "artifacts/cycle-205-b042-mellin-b-pairing-v1.json",
    "artifacts/cycle-204-b041-log-normal-bundle-v1.json",
    "artifacts/cycle-202-b039-normal-derivative-target-weight-v1.json",
    "artifacts/cycle-200-b037-regular-residue-jet-v1.json",
    "artifacts/cycle-198-b035-analytic-frequency-endpoint-v1.json",
    "proof/verify_cycle_205_mellin_b_pairing.py",
    "proof/verify_cycle_202_normal_derivative_target_weight.py",
    "proof/verify_cycle_200_regular_residue_jet.py",
    "proof/verify_cycle_198_analytic_frequency_endpoint.py",
    "scripts/dimension_six_stabilizer_ledger.py",
    "../../tools/preregistration_check.py"
  ]
}
-->
