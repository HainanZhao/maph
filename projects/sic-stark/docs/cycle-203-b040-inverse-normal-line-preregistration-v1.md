# Cycle 203 / B040 preregistration: inverse normal-line trivialization

Cycle 202 leaves open a geometrically twisted target. This block tests whether
the frozen `A_6` axis actually supplies an intrinsic inverse normal line that
cancels the Abel-rate weight, rather than merely an orientation or a
project-chosen coordinate.

<!-- research-freeze-v1
{
  "schema": "research-preregistration-freeze-v1",
  "cycle": 203,
  "parameters": {
    "axis_geometry": {
      "kind": "expression",
      "value": "Use the frozen attracting axis gamma(s)=(beta+beta^(-1)*s^2+i*sqrt(21)*s)/(1+s^2), beta=(5+sqrt(21))/2, with endpoint s=0 and A_6 contraction s->beta^(-6)*s. Define the normal cotangent line N^*=I/I^2 at s=0, where I is the endpoint ideal in the local axis coordinate.",
      "rationale": "The construction uses the actual source/geodesic geometry rather than a numerical Abel normalization."
    },
    "source_trivialization_test": {
      "kind": "expression",
      "value": "For every positive scalar c, compare the equally oriented local coordinate s_c=c*s. Verify that it has the same endpoint, A_6 contraction eigenvalue, pole-side orientation, and equation-(66) parameter family after reparametrization. A source-defined inverse normal density would be a nonzero element of N^(-1) invariant under every such admissible c-rescaling; a ray, orientation, ds/s, or a coordinate chosen by the project is not a trivialization.",
      "rationale": "It gives a falsifiable canonicity criterion: any genuine source normalization must distinguish c without importing target data."
    },
    "weight_cancellation_rule": {
      "kind": "expression",
      "value": "The Cycle-202 normal datum has Abel-rate weight one. Test whether an invariant source inverse normal density can produce a weight-zero tensor on all 36 rows. If no nonzero invariant inverse density exists, no canonical direct twist is available in this class; do not replace it by division by lambda, ds, or a chosen c.",
      "rationale": "A density line is useful only if its source normalization is fixed, not merely if a basis can be selected."
    },
    "claim_boundary": {
      "kind": "expression",
      "value": "A negative result rejects only an intrinsic trivialization derived from the declared A_6 axis, equation-(66) source family, and pole orientation. It does not exclude a new source theorem fixing a density, a covariant target line, nonlinear/higher-germ/non-Abel continuation, AFK, fusion, Stark, or TCC. A positive result would establish only the stated line trivialization and weight ledger.",
      "rationale": "The construction is tested as a named new engine without mistaking a coordinate choice for proof."
    }
  },
  "resource_caps": {
    "character_rows": {"kind":"integer","value":36,"rationale":"The complete normal-packet grid."},
    "axis_fixed_endpoints": {"kind":"integer","value":2,"rationale":"The two real A_6 fixed points."},
    "normal_line_dimension": {"kind":"integer","value":1,"rationale":"Local cotangent line at the attracting endpoint."},
    "scaling_family": {"kind":"expression","value":"c in R_{>0}","rationale":"All oriented local coordinate rescalings."},
    "wall_seconds": {"kind":"integer","value":180,"rationale":"Exact local-coordinate/covariance ledger."}
  },
  "formula_families": [
    "Cycle-196 frozen A_6 attracting-axis geometry",
    "Cycle-199 pole-side orientation",
    "Cycle-202 weight-one normal datum and weight-zero C198 targets"
  ],
  "selection_rule": [
    "Derive the A_6 local multiplier and test every statement under a symbolic positive c-rescaling, not at one chosen parameter value.",
    "Separate orientation, invariant logarithmic density, and a nonzero inverse-line trivialization in the ledger.",
    "If canonicity fails, record the exact free scalar and its incompatibility with all-row weight cancellation."
  ],
  "failure_rule": [
    "A project-written formula for gamma(s), a hyperbolic arc-length convention, or ds/s does not pass unless the frozen source formulas fix its nonzero normal-line scale under every c-rescaling.",
    "A target-dependent scalar or a division by the Abel rate is outside the declared class and cannot count as a density trivialization.",
    "Do not promote a line/density statement to a Zak map, AFK, fusion, Stark, or TCC claim."
  ],
  "pre_execution": {
    "timestamp_utc": "2026-08-03T06:55:00Z",
    "git_head": "a5ee30099022f26b6974da7606855d233b49318e",
    "git_state": "DIRTY from the concurrent repository-wide PROGRAM header migration and unrelated projects/tools, plus this live Cycle-203 preregistration. This block freezes only the listed SIC--Stark mathematical inputs."
  },
  "input_paths": [
    "artifacts/cycle-202-b039-normal-derivative-target-weight-v1.json",
    "artifacts/cycle-201-b038-two-scale-germ-covariance-v1.json",
    "artifacts/cycle-199-b036-full-phase-abel-boundary-v1.json",
    "artifacts/cycle-196-b033-endpoint-contour-geometry-v1.json",
    "proof/verify_cycle_202_normal_derivative_target_weight.py",
    "proof/verify_cycle_199_abel_pole_geometry.py",
    "proof/verify_cycle_196_endpoint_contour_geometry.py",
    "scripts/dimension_six_two_base_lens.py",
    "../../tools/preregistration_check.py"
  ]
}
-->
