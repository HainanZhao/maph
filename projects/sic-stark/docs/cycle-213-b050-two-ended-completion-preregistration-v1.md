# Cycle 213 / B050 preregistration: two-ended completion

Cycles 211--212 leave two equally admissible source cusps.  This block builds
the smallest formal completion containing both ends, with an involution that
exchanges them, and tests exactly whether its multiplier action permits a
sign-independent scalar pairing or only a character-valued one.

<!-- research-freeze-v1
{
  "schema": "research-preregistration-freeze-v1",
  "cycle": 213,
  "parameters": {
    "two_ended_state_space": {
      "kind": "expression",
      "value": "Use exactly W=C*u_infinity direct_sum C*u_zero, where u_infinity represents the Cycle-211 line [e_(0,5)] and u_zero represents [e_(5,0)].  Define only the formal exchange iota(u_infinity)=u_zero, iota(u_zero)=u_infinity; do not assert that iota is induced by an analytic, arithmetic, or AFK operation.",
      "rationale": "This is the smallest sign-independent completion of the two frozen cusp lines."
    },
    "multiplier_action": {
      "kind": "expression",
      "value": "Freeze the Cycle-211 common A6 multiplier exponent 8 modulo 48.  With chi=zeta_48^8, A6 acts on both basis lines by chi, and the coefficient line M has A6 action chi^2=zeta_48^16.  Check chi^2 != 1 exactly modulo 48.",
      "rationale": "Both cusp labels are fixed by A6 and have the same frozen multiplier, so any claimed pairing must account for its weight."
    },
    "pairing_family": {
      "kind": "expression",
      "value": "Examine all C-bilinear pairings W x W -> C for strict A6 invariance.  Separately examine the exchange-symmetric cross pairing B:W x W -> M with B(u_infinity,u_zero)=B(u_zero,u_infinity)=q, B(u_infinity,u_infinity)=B(u_zero,u_zero)=0, for formal nonzero q in M.  Test its restriction to W^iota=span(u_infinity+u_zero).",
      "rationale": "The cross pairing is the minimal candidate that uses both ends without selecting either one."
    },
    "claim_boundary": {
      "kind": "expression",
      "value": "A successful construction establishes only a formal two-ended completion and the exact scalar-versus-character-valued pairing distinction under the declared multiplier action.  It neither glues actual analytic ends nor supplies a source density, quotient descent, C198 comparison, AFK identity, fusion-continuity theorem, Stark relation, or TCC proof.",
      "rationale": "A formal invariant line is not an operational bridge or fusion theorem."
    }
  },
  "resource_caps": {
    "cusp_basis_dimension": {"kind":"integer","value":2,"rationale":"The completion contains exactly the two C211 cusp lines."},
    "a6_multiplier_rows": {"kind":"integer","value":2,"rationale":"Audit exactly the two frozen cusp labels."},
    "pairing_matrix_entries": {"kind":"integer","value":4,"rationale":"Exhaust the full bilinear pairing matrix on W."},
    "wall_seconds": {"kind":"integer","value":180,"rationale":"Finite exact character and matrix calculation."},
    "floating_point": {"kind":"not_applicable","justification":"The calculation is over formal roots of unity and symbolic bilinear matrices.","rationale":"No analytic packet value is evaluated."}
  },
  "formula_families": [
    "Cycle-211 exact cusp lines and A6 multiplier ledger",
    "Cycle-212 two equally covariant logarithmic orientations",
    "Formal two-dimensional representation with exchange involution",
    "Bilinear equivariance to a multiplier-character coefficient line"
  ],
  "selection_rule": [
    "Retain both cusp basis vectors and require all proposed structures to commute with iota.",
    "Accept a scalar pairing only if it is nonzero and strictly A6-invariant, not merely projectively or character-valuedly equivariant.",
    "Record a character-valued cross pairing only if its A6 weight and exchange symmetry are shown exactly, then keep it separate from scalar fusion."
  ],
  "failure_rule": [
    "Do not identify the formal iota with a proved source, analytic, or arithmetic symmetry.",
    "Do not call a pairing on W^iota quotient descent: no quotient relation is frozen in this block.",
    "Do not convert the multiplier line M into C by a chosen trivialization, and do not fit any construction to C198.",
    "If either cusp multiplier is not 8 modulo 48, A6 does not fix the labels, chi^2 equals 1, or the cross pairing lacks stated exchange/equivariance properties, withhold the claimed distinction."
  ],
  "pre_execution": {
    "timestamp_utc": "2026-08-03T05:52:31Z",
    "git_head": "a090a73bc553086ef1b9132cf2f846873d9a8afa",
    "git_state": "Dirty only from concurrent repository-wide workflow migration and unrelated project work; this cycle freezes the listed SIC--Stark mathematical inputs."
  },
  "input_paths": [
    "artifacts/cycle-211-b048-cusp-asymptotic-flat-sections-v1.json",
    "artifacts/cycle-212-b049-logarithmic-axis-to-packet-orientation-v1.json",
    "proof/verify_cycle_211_cusp_asymptotic_flat_sections.py",
    "scripts/dimension_six_stabilizer_ledger.py",
    "../../tools/preregistration_check.py"
  ]
}
-->
