# Cycle 184 preregistration: ray-box determinant-orbit engine

## Frozen question

Within one Cycle-183 populated primitive-ray box, determine whether the exact
relation

```text
w*A - u*B = F != 0
```

at its inherited stable size, together with both retained near-orbit widths,
forces either a coefficient-preserving in-box census bound or a seeded
recurrence. In parallel, seek the smallest actual nonrational exponential
prototype that would falsify either conclusion.

<!-- research-freeze-v1
{
  "cycle": 184,
  "failure_rule": [
    "Seal NO_GO_OR_UNRESOLVED if the exact determinant and both orbit inequalities admit a coefficient-preserving legal family with no forced seeded recurrence and no bound.",
    "Do not promote a scalar determinant count, a dyadic partition, a rational beta-zero tower, a low-product family, or an unlabelled rational approximation as an advance."
  ],
  "formula_families": [
    "C180 stable physical determinant comparison after C183 primitive clearing",
    "integer Bezout and divisibility identities for w*A-u*B=F",
    "two-sided C183 near-orbit inequalities for U*alpha_ell and V*alpha_m",
    "actual positive-exponential phase relation with common rational intercept"
  ],
  "input_paths": [
    "artifacts/cycle-180-cross-label-pair-determinant-v1.json",
    "artifacts/cycle-181-common-intercept-packet-v1.json",
    "artifacts/cycle-182-fibre-line-rigidity-v1.json",
    "artifacts/cycle-183-intercept-cleared-ray-box-v1.json",
    "conventions/intercept_cleared_ray_box_v1.py",
    "proof/cycle_seal_v1.py",
    "../../tools/preregistration_check.py"
  ],
  "parameters": {
    "box_fields": {
      "kind": "symbolic",
      "rationale": "The candidate class must retain coefficient-sensitive depth, denominator, multiplier, and label-gap scales.",
      "value": "(N_ell,N_m,U,V,k,q,r)"
    },
    "determinant_relation": {
      "kind": "expression",
      "rationale": "C183's exact primitive determinant is the proposed new engine's integer state equation.",
      "value": "F=w*A-u*B; D=k*q*v*F; F!=0"
    },
    "orbit_widths": {
      "kind": "expression",
      "rationale": "Both sides must retain the depth-sensitive actual exponential information.",
      "value": "||U*alpha_ell||<=2C/((N_ell-1)X), ||V*alpha_m||<=2C/((N_m-1)X)"
    },
    "stable_factor_window": {
      "kind": "expression",
      "rationale": "The primitive determinant must remain at the inherited stable physical scale, not be replaced by a scalar surrogate.",
      "value": "pi*r*U*V/(v*Delta)<=|F|<=(2*pi*exp(2*pi*c)+pi)*r*U*V/(v*Delta), 0<c<1"
    }
  },
  "pre_execution": {
    "git_head": "1b491682b77a2c5d86c6167b2fd584557774e7fe",
    "git_state": "CLEAN",
    "timestamp_utc": "2026-08-02T13:42:30Z"
  },
  "resource_caps": {
    "actual_prototype_dimension": {
      "kind": "integer",
      "rationale": "Small countermodels must expose both rays and one physical rectangle before any larger search is justified.",
      "value": 2
    },
    "candidate_engine_count": {
      "kind": "integer",
      "rationale": "Test the Bezout/orbit compression and an actual nonrational prototype; do not proliferate interfaces.",
      "value": 2
    },
    "new_executable_code": {
      "kind": "not_applicable",
      "justification": "The initial block is symbolic derivation and a hand-checkable countermodel specification; executable code is authorized only after this freeze validates.",
      "rationale": "Preflight must precede any executable discovery, proof, test, or replay code."
    }
  },
  "schema": "research-preregistration-freeze-v1",
  "selection_rule": [
    "Retain a derivation only if it uses the exact labelled ray state, both near-orbit inequalities, the physical multipliers, and the stable factor window.",
    "A positive result must yield either an explicit in-box upper bound with a strict triple-census margin, a quantified seeded-recurrence forcing statement, or a genuine nonrational actual exponential saturator."
  ]
}
-->

## Advance condition

`PROVED` advancement requires one of: an explicit coefficient-preserving
in-box bound with a strict direct triple-census margin; a quantified forcing
of a seeded recurrence; or a genuine nonrational actual exponential
saturator for this whole frozen class. All other outcomes remain containment
or `NO_PROMOTION`.
