# Cycle 187 preregistration: separated weighted-packing limit

## Frozen question

Can Cycle 186's actual-curve local triple exclusion, combined only with
critical cross mass, full-fibre capacity, stable shells, and denominator-depth
windows, force a strict populated-box saving? Test this against a support
which is much more separated than the local exclusion requires.

<!-- research-freeze-v1
{
  "cycle": 187,
  "failure_rule": [
    "Seal LOCAL_PACKING_NO_GO if an explicit separated abstract occupancy has critical cross mass, complete fibres, stable shells, and at most one label in every window larger than the C186 local exclusion scale.",
    "Do not call that occupancy an actual-exponential family or an analytic counterexample.",
    "Do not promote a label-count or spacing calculation without the complete weighted cross-mass ledger."
  ],
  "formula_families": [
    "C185 critical full-fibre mass and stable-shell ledger",
    "C186 local actual-curve three-point exclusion scale Delta=T^15, X=T^25, S=T^2, U approximately T^9",
    "shifted ternary-digit AP-free support with a deterministic separation multiplier",
    "ordered cross-rectangle mass M*(M-1)*binom(S+1,2)^2"
  ],
  "input_paths": [
    "artifacts/cycle-185-three-label-curvature-convention-correction-v1.json",
    "artifacts/cycle-186-actual-curve-convexity-v1.json",
    "proof/cycle_seal_v1.py",
    "../../tools/preregistration_check.py"
  ],
  "parameters": {
    "power_ledger": {
      "kind": "expression",
      "rationale": "This aligns the C185 and C186 scales exactly.",
      "value": "T=3^(2k), X=T^25, H=T^11, Delta=T^15, S=T^2, U=T^9, M=T^(13/2)"
    },
    "separation": {
      "kind": "expression",
      "rationale": "T^2 separation is deliberately stronger than C186's local T-scale exclusion.",
      "value": "labels=1+T^2*cantor_encode(bits,24k), 0<=bits<M"
    },
    "advance_threshold": {
      "kind": "expression",
      "rationale": "Only an actual-exponential packing consequence could move E13.",
      "value": "strict critical-box saving, seeded recurrence, or a genuine actual-exponential separated saturator"
    }
  },
  "pre_execution": {
    "git_head": "194b51cb24af046c424b99c03b6d8ee553804aa9",
    "git_state": "clean worktree; C187 preregistration and one working ledger created before executable code",
    "timestamp_utc": "2026-08-02T14:29:14Z"
  },
  "resource_caps": {
    "candidate_engine_count": {
      "kind": "integer",
      "rationale": "Test one sharp separated-support falsifier of local packing.",
      "value": 1
    },
    "new_executable_code": {
      "kind": "not_applicable",
      "justification": "The initial task is a frozen exact scale ledger and construction specification; code follows only after preflight.",
      "rationale": "Preflight precedes executable construction and replay code."
    }
  },
  "schema": "research-preregistration-freeze-v1",
  "selection_rule": [
    "A no-go must retain the complete fibre and ordered-mass accounting, not merely a large separated set.",
    "An actual-exponential consequence is required for any density-facing claim."
  ]
}
-->

## Amendment log

- 2026-08-02: before executable work, corrected the Cantor digit budget from
  `12k` to `24k`: `2^(12k)` cannot contain `M=3^(13k)` labels. The larger
  budget still fits below `Delta` after the frozen `T^2` separation multiplier.
