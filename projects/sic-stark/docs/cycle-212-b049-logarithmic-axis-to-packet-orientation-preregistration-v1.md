# Cycle 212 / B049 preregistration: logarithmic axis-to-packet orientation

Cycle 211 left two packet cusps. This block tests the natural source-only
logarithmic lifts from the oriented attracting `A6` axis to the packet
coordinate, including both possible signs, and audits whether the pinned
Frobenius/embedding data breaks that sign symmetry.

<!-- research-freeze-v1
{
  "schema": "research-preregistration-freeze-v1",
  "cycle": 212,
  "parameters": {
    "axis_and_packet_coordinates": {
      "kind": "expression",
      "value": "Use the frozen upper-half-plane axis coordinate s>0 with A6:s->beta^(-6)*s, beta=(5+sqrt(21))/2>1, and the packet coordinate t=exp(-pi*D*Lambda/(36*omega)), D=9+2*sqrt(21), omega=55+12*sqrt(21). Consider exactly the two logarithmic lift orientations Lambda_epsilon(s)=epsilon*(36*omega/(pi*D))*log(s), epsilon in {+1,-1}; hence t_epsilon(s)=s^(-epsilon).",
      "rationale": "These are the two source-coordinate logarithmic lifts producing the two Cycle-211 packet cusps as s downarrow 0."
    },
    "orientation_inputs": {
      "kind": "expression",
      "value": "Freeze: s>0 is the upper-half-plane attracting orientation; the selected real embedding is beta'=(5-sqrt(21))/2; g=Frob_(4 beta+1) has norm 37 and ray log 1; A6 fixes all characteristic labels modulo 6. Do not add an unrecorded action of g on s, Lambda, t, or epsilon.",
      "rationale": "This distinguishes established arithmetic labels from an assumed analytic action."
    },
    "equivariance_test": {
      "kind": "expression",
      "value": "Audit both epsilon lifts under A6: t_epsilon(beta^(-6)*s)=beta^(6*epsilon)*t_epsilon(s), so epsilon=+1 tends to the t->infinity cusp [e_(0,5)] and epsilon=-1 tends to the t->0^+ cusp [e_(5,0)]. Verify that the frozen real embedding and arithmetic Frobenius label do not contain a declared map to epsilon, and that A6 itself preserves rather than swaps the two signs.",
      "rationale": "A valid orientation theorem must do more than restate the pre-existing sign choice."
    },
    "claim_boundary": {
      "kind": "expression",
      "value": "A symmetric result proves only that the declared axis, embedding, Frobenius, and A6 data do not select between the two specified logarithmic lifts. It does not rule out a new theorem defining an analytic Frobenius action, a source density, a non-logarithmic link, C198 comparison, AFK identity, fusion, Stark, or TCC statement.",
      "rationale": "The test is a concrete new lift, not a universal orientation no-go."
    }
  },
  "resource_caps": {
    "lift_signs": {"kind":"integer","value":2,"rationale":"Both and only the frozen logarithmic orientations."},
    "characteristic_labels": {"kind":"integer","value":36,"rationale":"A6 label action remains all-row."},
    "arithmetic_orientation_primes": {"kind":"integer","value":1,"rationale":"Only the pinned norm-37 Frobenius prime is used."},
    "wall_seconds": {"kind":"integer","value":180,"rationale":"Exact symbolic orientation audit."},
    "floating_point": {"kind":"not_applicable","justification":"All comparisons are exact signs, algebraic inequalities, and symbolic powers.","rationale":"No target value is evaluated."}
  },
  "formula_families": [
    "Cycle-203 A6 attracting axis and rescaling symmetry",
    "Cycle-200 packet coordinate and complete exponent family",
    "Cycle-211 source cusp sections",
    "Cycle-173 norm-37 arithmetic Frobenius orientation"
  ],
  "selection_rule": [
    "Retain both epsilon signs and identify their cusp limits before testing any selector.",
    "Use the exact frozen source/embedding/Frobenius statements only; never invent an action of g on analytic coordinates.",
    "Accept a selector only if a displayed frozen theorem maps one sign to a distinguished arithmetic or geometric datum and excludes the other."
  ],
  "failure_rule": [
    "Do not treat the chosen upper-half-plane s orientation as a choice of epsilon without an exact axis-to-packet theorem.",
    "Do not convert the arithmetic ray label g into an analytic t action by convention or endpoint fitting.",
    "If either lift law, cusp correspondence, A6 action, embedding convention, or source-provenance audit fails, withhold the symmetry/no-selector conclusion."
  ],
  "pre_execution": {
    "timestamp_utc": "2026-08-03T05:44:38Z",
    "git_head": "0c792da711e3c8a93ed2984fc1a781f4b421f200",
    "git_state": "Dirty only from concurrent repository-wide PROGRAM migration outside this new cycle; Cycle 212 freezes the listed SIC--Stark mathematical inputs."
  },
  "input_paths": [
    "artifacts/cycle-211-b048-cusp-asymptotic-flat-sections-v1.json",
    "artifacts/cycle-163-spectral-ray-interface-v1.json",
    "artifacts/cycle-203-b040-inverse-normal-line-v1.json",
    "artifacts/cycle-200-b037-regular-residue-jet-v1.json",
    "artifacts/cycle-173-local-artin-action-v2.json",
    "proof/verify_cycle_203_inverse_normal_line.py",
    "proof/verify_cycle_163_fixed_full_ray_selector.py",
    "proof/verify_cycle_200_regular_residue_jet.py",
    "proof/verify_cycle_173_local_artin_action.py",
    "../../tools/preregistration_check.py"
  ]
}
-->
