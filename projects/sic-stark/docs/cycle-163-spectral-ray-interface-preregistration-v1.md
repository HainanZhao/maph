# Cycle 163 / B001 preregistration: spectral-to-ray interface prototype

Date: 2026-08-02 UTC  
Status: `PREREGISTERED_NOT_EXECUTED`

## Question and claim boundary

Can the existing, ordinary-Fourier-gauged 36-coefficient family be given a
canonical finite-characteristic descent to the three primitive
norm-37-oriented ray-log slots, before any boundary or fusion-limit claim is
made?

`CONJECTURED`: the candidate below could be the finite selector layer of an
operational interface.  It is **not** a definition of a ray logarithm, a
proof of a finite part, an AFK-cocycle identification, a Stark identity, or
a dimension-six TCC identity.  Cycle 157 remains the frozen statement that
those analytic layers are currently absent.

## Operational reading

The embedded manifest below is the sole authoritative specification of the
candidate, conventions, resources, selection, and failure conditions.  In
plain language it tests whether a direct fixed-\((6)\infty_2\) assignment
is even defined on the full 36-characteristic source before any logarithm,
finite part, AFK-cocycle identification, or boundary limit is attempted.

The sole allowed advance is its exact prototype passing.  A failure rejects
only that fixed-full-ray selector and requires the separately named,
orientation-preserving characteristic-dependent ray-monoid engine; it is
not an interface or TCC no-go.

<!-- research-freeze-v1
{
  "schema": "research-preregistration-freeze-v1",
  "cycle": 163,
  "parameters": {
    "dimension": {"kind": "integer", "value": 6, "rationale": "The candidate is only the dimension-six finite characteristic grid."},
    "field": {"kind": "symbolic", "value": "Q(sqrt(21)); beta^2-5*beta+1=0; beta'=(5-sqrt(21))/2", "rationale": "Pins the two embeddings used by the positive lift and norm."},
    "full_modulus": {"kind": "symbolic", "value": "(6)infinity_2", "rationale": "The candidate class is explicitly a fixed full-ray construction."},
    "characteristic_grid": {"kind": "expression", "value": "(Z/6Z)^2, enumerated lexicographically (a,b) with 0<=a,b<6", "rationale": "Fixes all 36 inputs and their order."},
    "positive_lift": {"kind": "expression", "value": "p*=a-6k is the unique congruent integer with b*beta'-p*>0 and p*+6 failing it", "rationale": "Pins the finite representative without floating point."},
    "shintani_action": {"kind": "expression", "value": "T(a,b)=(5a+b,-a) mod 6", "rationale": "Fixes the orbit-covariance test."},
    "orientation": {"kind": "text", "value": "g=[(4beta+1)], arithmetic Frobenius; anchors (3,5)->g^1 and (3,4)->g^2", "rationale": "Prevents a reversal or geometric-Frobenius convention from passing."}
  },
  "resource_caps": {
    "rows": {"kind": "integer", "value": 36, "rationale": "The prototype may inspect exactly the full finite grid and no adaptive rows."},
    "exact_integer_operations": {"kind": "integer", "value": 20000, "rationale": "The bounded enumeration needs no unbounded search."},
    "external_programs": {"kind": "not_applicable", "rationale": "The frozen prototype must isolate the finite-domain question from all external algebra and analytic engines.", "justification": "The prototype is pure Python rational/integer arithmetic; PARI, Arb, and packet evaluation are excluded."},
    "floating_point": {"kind": "not_applicable", "rationale": "Eligibility and multiplicity are exact finite predicates.", "justification": "No numerical value can determine the fixed-ray domain or label multiplicity."}
  },
  "formula_families": [
    "ordinary-Fourier-gauged additive coefficient C_(a,b)(tau) from Cycle 157, referenced but not evaluated",
    "positive-lift principal ideal gamma_(a,b)=b*beta-p*",
    "norm N(gamma)=p*^2-5*p*b+b^2",
    "fixed-full-ray eligibility gcd(N(gamma),6)=1",
    "three-step Shintani action T(a,b)=(5a+b,-a) mod 6"
  ],
  "selection_rule": [
    "Enumerate every characteristic in the frozen lexicographic grid.",
    "Use no target-derived row selection; provisional primitive slots are g^0,g^1,g^2 only after totality is established.",
    "Check the two orientation anchors only as independently frozen convention checks."
  ],
  "failure_rule": [
    "Any noneligible row exactly falsifies the fixed-full-ray direct-selector class.",
    "Any non-three-to-one multiplicity or nonconstant Shintani orbit exactly falsifies that class.",
    "A failure starts the characteristic-dependent conductor-lowering/ray-monoid engine; it cannot be promoted to an interface or TCC no-go."
  ],
  "pre_execution": {
    "timestamp_utc": "2026-08-02T00:00:00Z",
    "git_head": "eed84535c53465f4345c558aaf5ec25960ae87ca",
    "git_state": "M ../../AGENTS.md; M AGENTS.md; ?? discovery/cycle-163-spectral-ray-interface-working.md; ?? docs/cycle-163-spectral-ray-interface-preregistration-v1.md; ?? proof/verify_cycle_163_fixed_full_ray_selector.py"
  },
  "input_paths": [
    "../../AGENTS.md",
    "AGENTS.md",
    "docs/sic-stark-cycle157.md",
    "certificates/dimension-six-cycle157-fourier-normalization-audit.json",
    "scripts/dimension_six_cycle157_fourier_normalization_audit.py",
    "scripts/dimension_six_ray_recon.gp",
    "scripts/dimension_six_stabilizer_ledger.py",
    "scripts/dimension_six_shintani_cycle.py",
    "scripts/certify_dimension_six_orientation.py",
    "docs/dimension-six-analytic-to-stark-theorem.md",
    "docs/effective-stark-sweep-context-v1.md",
    "proof/cycle_seal_v1.py",
    "../../tools/preregistration_check.py",
    "../../tools/research_records.py"
  ]
}
-->

## Amendment log

- 2026-08-02 UTC: initial freeze; no executable discovery has occurred.
