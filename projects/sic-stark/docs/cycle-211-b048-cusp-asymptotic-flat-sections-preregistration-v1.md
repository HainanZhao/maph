# Cycle 211 / B048 preregistration: cusp asymptotic flat sections

This block tests whether the source packet itself supplies the missing base
data for Cycle 210. It derives both oriented cusp limits of the flat packet
bundle and asks whether the frozen source data select one of them.

<!-- research-freeze-v1
{
  "schema": "research-preregistration-freeze-v1",
  "cycle": 211,
  "parameters": {
    "source_packet_and_connection": {
      "kind": "expression",
      "value": "Use the 36 source exponents E_(a,b)=4*b-5*a and the Cycle-210 flat packet P_(a,b;h)(t)=zeta_6^(5*h*a)*t^E_(a,b), projectively. On t->infinity normalize by t^(-20); on t->0^+ normalize by t^(25). Retain every h channel.",
      "rationale": "The two normalizations are determined by the unique maximum 20 and minimum -25 exponents."
    },
    "cusp_sections": {
      "kind": "expression",
      "value": "Derive the all-h projective cusp lines: t->infinity gives [e_(0,5)] and t->0^+ gives [e_(5,0)]. Audit both as horizontal asymptotic sections of nabla=d-diag(E)*dlog(t), and do not choose either as a base section.",
      "rationale": "Both oriented ends are intrinsic source asymptotics; neither is C198 data."
    },
    "symmetry_audit": {
      "kind": "expression",
      "value": "Audit that A6 fixes both labels modulo 6 and acts diagonally through the frozen multiplier ledger. This may establish projective invariance of each cusp line but cannot choose between them.",
      "rationale": "A label-fixed diagonal symmetry cannot identify two distinct coordinate lines."
    },
    "selection_and_failure": {
      "kind": "expression",
      "value": "Accept a source-only canonical base section only if an exact frozen source rule distinguishes one cusp without a target value, selected finite t, or orientation added after results. If the two cusp lines are distinct and all frozen source/A6/multiplier data preserve both, record only the two-cusp nonselection obstruction.",
      "rationale": "The design question is canonical selection, not existence of a convenient cusp limit."
    },
    "claim_boundary": {
      "kind": "expression",
      "value": "This block may prove two exact source cusp sections and their nonselection under the listed data. It does not rule out an additional source theorem choosing an orientation, a non-diagonal boundary theory, a C198 comparison, AFK identity, fusion, Stark, or TCC statement.",
      "rationale": "An absent selector in this finite source package is not a universal no-go."
    }
  },
  "resource_caps": {
    "label_count": {"kind":"integer","value":36,"rationale":"Complete characteristic grid."},
    "source_channel_count": {"kind":"integer","value":6,"rationale":"All h channels are retained in both limits."},
    "cusp_count": {"kind":"integer","value":2,"rationale":"The two oriented source ends t->0^+ and t->infinity."},
    "wall_seconds": {"kind":"integer","value":180,"rationale":"Exact exponent-order and symmetry audit."},
    "floating_point": {"kind":"not_applicable","justification":"Only integer exponent ordering and finite multiplier labels are used.","rationale":"No target or numerical limit is evaluated."}
  },
  "formula_families": [
    "Cycle-206 denominator-free projective normal packet",
    "Cycle-210 logarithmic projective connection",
    "dimension-six A6 stabilizer and multiplier ledger"
  ],
  "selection_rule": [
    "Enumerate all 36 exponents before identifying either extremum.",
    "Keep both cusp lines and all six h channels; do not select an orientation or finite basepoint.",
    "Use no C198 coordinate, ratio, minor, AFK value, ray datum, or target fit."
  ],
  "failure_rule": [
    "Do not call the existence of a cusp line a canonical base-section construction.",
    "Do not infer an orientation selector from A6/multiplier covariance when both lines are preserved.",
    "If extremum uniqueness, asymptotic normalization, h-independence, label action, or line distinction fails, withhold the associated claim."
  ],
  "pre_execution": {
    "timestamp_utc": "2026-08-03T05:38:47Z",
    "git_head": "1294bcf733da7ce3fa5bf5f63db7f06c58666408",
    "git_state": "Dirty only from concurrent repository-wide PROGRAM migration outside this new cycle; Cycle 211 freezes the listed SIC--Stark mathematical inputs."
  },
  "input_paths": [
    "artifacts/cycle-210-b047-logarithmic-projective-connection-v1.json",
    "artifacts/cycle-206-b043-projective-line-interface-v1.json",
    "proof/verify_cycle_210_logarithmic_projective_connection.py",
    "proof/verify_cycle_206_projective_line_interface.py",
    "scripts/dimension_six_stabilizer_ledger.py",
    "../../tools/preregistration_check.py"
  ]
}
-->
