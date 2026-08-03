# Cycle 209 / B046 preregistration: fixed diagonal projective interface

This block tests a genuinely source-derived covariance engine before trying to
construct coefficients: can one fixed label-preserving diagonal map send the
complete unselected Cycle-206 projective source family to the fixed C198
projective target? It does not evaluate a target minor or fit a coefficient.

<!-- research-freeze-v1
{
  "schema": "research-preregistration-freeze-v1",
  "cycle": 209,
  "parameters": {
    "source_family": {
      "kind": "expression",
      "value": "Use the Cycle-206 denominator-free projective coordinates P_(a,b;h)(t)=zeta_6^(5*h*a)*t^(4*b-5*a), with a,b,h in Z/6Z and t>0, t!=1 (the frozen real source locus has Lambda!=0); the common nonzero factor is removed projectively. Keep every h and every admissible t unselected.",
      "rationale": "This is the complete source family, not one fitted source point."
    },
    "target_family": {
      "kind": "expression",
      "value": "Use the ordered C198 point [L_(a,b)] in P^35, whose 36 coordinates are proved finite and nonzero. Treat each L_(a,b) as a fixed nonzero coordinate; do not evaluate its ratios or minors.",
      "rationale": "Only target nonvanishing and label order are needed for the covariance test."
    },
    "map_family": {
      "kind": "expression",
      "value": "Freeze fixed label-preserving diagonal maps J_c(e_(a,b))=c_(a,b)*chi_(a,b), with 36 nonzero complex constants c_(a,b) independent of h and t. The candidate projective interface condition is [c_(a,b)P_(a,b;h)(t)]_(a,b)=[L_(a,b)] for every h in Z/6Z and every t>0.",
      "rationale": "Nonzero c is necessary because every target coordinate is nonzero; fixedness is the testable naturality requirement."
    },
    "covariance_engine": {
      "kind": "expression",
      "value": "Compare labels (0,0) and (0,1). The frozen source ratio is P_(0,1;h)(t)/P_(0,0;h)(t)=t^4. A fixed diagonal projective equality would force the nonzero constant (L_(0,1)c_(0,0))/(L_(0,0)c_(0,1)) to equal t^4 for every admissible t. Test the exact witnesses t=2 and t=3.",
      "rationale": "This preserves the full unselected source family and uses no target endpoint evaluation."
    },
    "claim_boundary": {
      "kind": "expression",
      "value": "A failure proves only that no fixed nonzero label-preserving diagonal map realizes the stated all-h, all-t projective equality. It does not reject a parameter-dependent, non-diagonal, nonlinear, selected-source-point, or otherwise new source-authorized interface; it proves no target minor identity, AFK, fusion, Stark, or TCC statement.",
      "rationale": "The proposed covariance engine must remain sharply scoped."
    }
  },
  "resource_caps": {
    "source_labels": {"kind":"integer","value":36,"rationale":"The complete labelled P^35 source grid."},
    "source_channels": {"kind":"integer","value":6,"rationale":"All unselected h channels are retained."},
    "test_t_values": {"kind":"integer","value":2,"rationale":"The exact admissible witnesses t=2 and t=3 suffice for the frozen t^4 contradiction."},
    "map_coefficients": {"kind":"integer","value":36,"rationale":"No coefficient is chosen or fitted."},
    "wall_seconds": {"kind":"integer","value":180,"rationale":"Exact finite covariance audit."},
    "floating_point": {"kind":"not_applicable","justification":"All source ratios and witnesses are exact symbolic or rational values.","rationale":"No numerical endpoint calculation is permitted."}
  },
  "formula_families": [
    "Cycle-206 denominator-free projective normal packet",
    "Cycle-198 ordered nonzero endpoint character point",
    "Cycle-208 full diagonal coordinate-ring family"
  ],
  "selection_rule": [
    "Keep h and t unselected; use only the fixed admissible t=2,3 covariance witnesses.",
    "Use only nonzero fixed diagonal coefficients and never infer or fit their values from L.",
    "Accept a no-go only if both projective equality consequences and the exact t^4 witness contradiction are recorded."
  ],
  "failure_rule": [
    "Do not turn the scoped fixed-diagonal failure into a no-go for any broader interface family.",
    "Do not evaluate a C198 target minor, target ratio, raw contour, AFK value, ray datum, fusion condition, Stark value, or TCC expression.",
    "If the source ratio, target nonvanishing premise, fixedness premise, admissible t-domain, or t=2,3 contradiction does not hold exactly, withhold the no-go."
  ],
  "pre_execution": {
    "timestamp_utc": "2026-08-03T05:27:22Z",
    "git_head": "14b88f17cb77335527aad52a97eee66373a4be2e",
    "git_state": "Dirty only from concurrent repository-wide PROGRAM migration outside this new cycle; Cycle 209 freezes the listed SIC--Stark mathematical inputs."
  },
  "input_paths": [
    "artifacts/cycle-208-b045-polarized-minor-pairing-v1.json",
    "artifacts/cycle-206-b043-projective-line-interface-v1.json",
    "artifacts/cycle-198-b035-analytic-frequency-endpoint-v1.json",
    "proof/verify_cycle_208_polarized_minor_pairing.py",
    "proof/verify_cycle_206_projective_line_interface.py",
    "proof/verify_cycle_198_analytic_frequency_endpoint.py",
    "../../tools/preregistration_check.py"
  ]
}
-->

## Amendment log

- 2026-08-03 — `OBSERVED` — The Cycle-206 frozen real source locus excludes
  `Lambda=0`, hence excludes `t=1`. The initial C209 witnesses `t=1,2` were
  therefore not both admissible. Before any seal, they are replaced by the
  admissible exact witnesses `t=2,3`, where `t^4` is respectively `16,81`.
  No target value or coefficient was selected; fresh preflight and replay are
  required.
