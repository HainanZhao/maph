# C80 / B080 preregistration: quaternary Legendre length-42 compression gate

<!-- research-freeze-v1
{
  "schema": "research-preregistration-freeze-v1",
  "cycle": 80,
  "parameters": {
    "decision_question": {
      "kind": "expression",
      "value": "Do exact 6- and 7-compression identities and finite Gaussian-integer signature spaces yield a proof-producing reduction for quaternary Legendre pairs at length 42 before any sequence lift search?",
      "rationale": "Oracle-selected compression-first gate; brute force is excluded."
    },
    "target": {
      "kind": "expression",
      "value": "A,B in {1,-1,i,-i}^42 have periodic PAF_A(s)+PAF_B(s)=-2 for 1<=s<=21, normalized by sum A=0 and sum B=1+i.",
      "rationale": "Pins the exact selected open case and conventions."
    },
    "compression": {
      "kind": "expression",
      "value": "For d in {6,7}, m=42/d, C^(d)_r=sum_{t=0}^{d-1} C_{r+t*m}. Then pair PAF after compression is 86-2d at zero and -2d at every nonzero shift modulo m.",
      "rationale": "The zero row is original 84 plus d-1 nonzero rows of -2."
    },
    "signature_domain": {
      "kind": "expression",
      "value": "Each compressed coordinate is x+iy with |x|+|y|<=d and x+y congruent to d modulo 2.",
      "rationale": "Finite exact coordinate domain, with no floating spectral filter."
    },
    "final_signature_gate": {
      "kind": "expression",
      "value": "Run one bounded exact necessary-condition witness search only for d=6,m=7: seven coordinates for each sequence from the 49-value d=6 domain; impose sum A=0, sum B=1+i, and combined compressed PAF (74,-12,-12,-12,-12,-12,-12). Do not enumerate or lift length-42 coordinate fibers.",
      "rationale": "Oracle's single final engine before pivot. The 74,-12 row is d=6,m=7, correcting the verbal d=7 indexing slip."
    },
    "control_lengths": {
      "kind": "expression",
      "value": "Enumerate all quaternary pairs at lengths 2 and 6 under the identical periodic PAF convention and check all divisor compressions.",
      "rationale": "Prevents a length-42 convention error becoming a search claim."
    },
    "advance_condition": {
      "kind": "expression",
      "value": "A complete exact signature census plus a checked join map with a proof-producing lift partition and measured strict reduction, an explicit length-42 pair, or a complete proof-logged unrestricted UNSAT lift.",
      "rationale": "Separates a useful compression theorem from raw candidate counts."
    },
    "claim_boundary": {
      "kind": "expression",
      "value": "A compressed-signature witness proves only necessary-condition feasibility. It never establishes a length-42 pair, nonexistence, or a valid unrestricted lift.",
      "rationale": "Controls finite-gate scope."
    }
  },
  "resource_caps": {
    "worker_processes": {
      "kind": "integer",
      "value": 3,
      "rationale": "Three deterministic witness seeds; reserve one of four CPUs."
    },
    "length_42": {
      "kind": "integer",
      "value": 42,
      "rationale": "Selected smallest unresolved length."
    },
    "compression_factors": {
      "kind": "integer",
      "value": 2,
      "rationale": "Exactly d=6 and d=7."
    },
    "control_lengths": {
      "kind": "integer",
      "value": 2,
      "rationale": "Exactly lengths 2 and 6."
    },
    "canonical_compressed_witnesses": {
      "kind": "integer",
      "value": 1000000,
      "rationale": "Prevents feasibility enumeration from replacing a proof-producing reduction."
    },
    "aggregate_wall_seconds": {
      "kind": "integer",
      "value": 3600,
      "rationale": "Aggregate C80 control, census, and final gate budget."
    },
    "aggregate_peak_memory_mib": {
      "kind": "integer",
      "value": 2048,
      "rationale": "Bounded exact state and candidate storage across workers."
    },
    "aggregate_temporary_disk_bytes": {
      "kind": "integer",
      "value": 1073741824,
      "rationale": "Within the measured free-space reserve."
    },
    "rng_seed": {
      "kind": "text",
      "value": "71237,71239,71243",
      "rationale": "Frozen deterministic witness seeds; every reported witness is exactly checked."
    }
  },
  "formula_families": [
    "periodic quaternary autocorrelation",
    "Gaussian-integer d-compression",
    "compressed PAF identity",
    "exact balance constraints",
    "Parseval/PSD signature filters",
    "exact integer compressed-signature residual"
  ],
  "selection_rule": [
    "Derive the compression identity before signature enumeration.",
    "Run both frozen control lengths under the same convention.",
    "Run only the final d=6,m=7 necessary-condition gate; never launch a length-42 lift without a checked proof-producing partition."
  ],
  "failure_rule": [
    "A control mismatch blocks all length-42 work.",
    "Restricted UNSAT is only an engine no-go unless an unrestricted lift partition is proved.",
    "A compressed signature is only a necessary-condition witness.",
    "On the million-witness cap, aggregate wall cap, or a witness family without a new forced invariant, pivot immediately to LEM 4-cycle."
  ],
  "pre_execution": {
    "timestamp_utc": "2026-08-05T19:20:39Z",
    "git_head": "29c098d7ee33e49049e4c4bea82c4155d190f6bf",
    "git_state": "DIRTY repository; unrelated changes preserved. The initial live zero-row factor 84-2d was corrected to 86-2d before valid execution. The final bounded signature gate is an in-place C80 amendment after Oracle review.",
    "filesystem_observation_bytes": {
      "size": 206900281344,
      "used": 47074586624,
      "available": 159808917504,
      "reserved": 5368709120,
      "maximum_temporary_cap": 154440208384,
      "chosen_temporary_cap": 1073741824,
      "mount": "/"
    }
  },
  "input_paths": [
    "discovery/cycle80_next_target_primary_analysis.md",
    "discovery/cycle80_oracle_selection.md",
    "../../tools/preregistration_check.py"
  ]
}
-->

## Claim boundary

C80 is an exact compression-interface gate only. It forbids an unrestricted
length-42 brute-force search in this research block.

## Live amendment before valid C80 execution

The first live manifest wrote the compressed shift-zero row as \(84-2d\).
Direct expansion gives \(84-2(d-1)=86-2d\): one folded row is the original
zero row and the other \(d-1\) rows equal \(-2\). A temporary balance/norm
census therefore returned zero against an impossible target. It is discarded,
creates no claim, and no length-42 sequence or lift was inspected. Valid
controls now use the corrected rows \(74\) for \(d=6\) and \(72\) for \(d=7\).

After the corrected census, Oracle advised one final bounded
necessary-condition gate. Its earlier verbal \(d=7\) label was an indexing
slip; the specified \((74,-12,\ldots,-12)\) system is \(d=6,m=7\). A
compressed witness remains only a necessary condition.
