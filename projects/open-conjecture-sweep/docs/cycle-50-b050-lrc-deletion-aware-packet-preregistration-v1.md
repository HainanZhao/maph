# Cycle 50 / B050 preregistration: deletion-aware relative cube packets

## Decision question

Does one lexicographic deletion-aware triple-packet rule close every
full-domain p199 residual of structural support pattern `(2,2,2)` or
`(2,2,4)`, with no forbidden spill and no new residual class?

<!-- research-freeze-v1
{
  "schema":"research-preregistration-freeze-v1",
  "cycle":50,
  "parameters":{
    "state":{"kind":"expression","value":"Use exactly the Cycle 49 p199 type reconstruction, Möbius source tensor, pair transports, and pair/triple deletion masks. A cell is allowed precisely when it passes Cycle 49 cell_allowed. The pair-fiber stage is unchanged from Cycle 49.","rationale":"Freezes the inherited semantic interface and prevents a new local-complex convention."},
    "packet_rule":{"kind":"expression","value":"At each forbidden triple pivot (w,w,w), enumerate alternative triples (a0,a1,a2) in lexicographic order with ai in Si minus {w}; equality across distinct ai is permitted. For each normalized alternating cube, use its unique pivot-killing scale and inspect every cube vertex against the actual masks. Select the first cube for which every forbidden cube vertex has zero post-packet coefficient; allowed cube vertices are unrestricted. Thus a packet may discharge a coupled forbidden star but may leave neither a residual nor a new forbidden coefficient. If none exists, return NO_ADMISSIBLE_PACKET. Do not inspect a later outcome to choose another rule.","rationale":"Replaces exactly the pairwise-distinct surrogate by one actual-mask-defined coupled-discharge selector."},
    "packet_invariant":{"kind":"expression","value":"Prove symbolically that every selected cube has zero three pair marginals, kills its pivot, and leaves zero coefficient on every actual-mask-forbidden cube vertex. Therefore each packet boundary preserves pair marginals and creates no forbidden spill. The unchanged Cycle 49 pair-fiber theorem applies only after the triple stage leaves no forbidden triple coefficient.","rationale":"Separates a formula theorem from a local elimination solve."},
    "domain":{"kind":"expression","value":"Reconstruct every raw-multiplicity-valid unordered p199 type triple using Cycle 49 exact conventions. Select before evaluation every interface whose ordered support-size multiset is either (2,2,2) or (2,2,4). Run the frozen deletion-aware triple selector followed by the unchanged pair-fiber stage. Record exact raw multiplicity, type labels, masks, packet alternatives, and terminal status for every selected interface.","rationale":"Tests all instances of the two structural patterns, not only the five known labels."},
    "classification":{"kind":"expression","value":"THEOREM_PASS requires every selected interface to finish allowed, no packet spill, unchanged pair marginals, and no residual pattern outside the selected structural patterns in a full residual census rebuilt independently. THEOREM_FAIL is the lexicographically first NO_ADMISSIBLE_PACKET, forbidden spill, pair-marginal mismatch, or nonzero forbidden terminal. No solver fallback, second packet family, or per-interface exception is permitted.","rationale":"Makes the pattern theorem and its decisive falsifier exact."},
    "controls":{"kind":"expression","value":"Before the full run, exhaust all owner assignments on universes five and six for the selector's cube-marginal and mask-support claims; retain a repeated-alternative positive control reproducing Cycle 49 (4,4,5), and a negative control with no admissible cube. Independently reconstruct selected raw terms and classifications in reverse type order without importing the principal selector.","rationale":"Tests algebra, actual-mask admissibility, negative semantics, and full-domain coverage separately."},
    "method_collapse_guard":{"kind":"expression","value":"The positive route may enumerate only candidate cubes of the frozen selector. It may not call Gaussian elimination, rank, sparse_solve, a basis search, or outcome-dependent cube choice. The independent route may use separate direct enumeration only to verify the same frozen rule.","rationale":"Prevents a local solver from being relabeled a packet theorem."},
    "advance_condition":{"kind":"expression","value":"If THEOREM_PASS holds, seal the deletion-aware pattern theorem and stop local face work; reassess whether a nonlocal lift object can be defined. If THEOREM_FAIL holds, seal the falsifier, pause Problem 1, and create one handoff. In either case do not open Cycle 51 on local exception repair.","rationale":"This is the single closure block authorized after Cycle 49 clarity."},
    "falsifier":{"kind":"expression","value":"Any selected cube with a nonzero forbidden post-packet vertex, pair-marginal change, incomplete selected-domain coverage, independent mismatch, or terminal forbidden coefficient is an ERROR or THEOREM_FAIL. Any residual support pattern not in the two frozen patterns is a full-domain classification failure.","rationale":"States both mathematical and implementation failure modes."},
    "claim_boundary":{"kind":"expression","value":"A pass proves only the specified deletion-aware triple-packet theorem for the frozen p199 type interface plus the inherited pair-fiber stage. It does not prove an arbitrary relative contraction, construct a global lift, prove every quadruple fills, or prove LRC(13).","rationale":"Prevents local closure from being promoted to the conjecture."}
  },
  "resource_caps":{
    "worker_processes":{"kind":"integer","value":3,"rationale":"Use CPUs 0-2 at most; reserve CPU 3."},
    "raw_type_triples":{"kind":"integer","value":400000000,"rationale":"Full raw-valid p199 unordered triple ceiling inherited from C49."},
    "selected_type_triples":{"kind":"integer","value":50000000,"rationale":"Ceiling for all full-domain (2,2,2)/(2,2,4) support-pattern interfaces."},
    "candidate_cubes":{"kind":"integer","value":200000000,"rationale":"Aggregate selector enumeration across controls, principal, and independent replay."},
    "fraction_height_bits":{"kind":"integer","value":131072,"rationale":"Exact tensor and packet coefficient cap."},
    "aggregate_wall_seconds":{"kind":"integer","value":3600,"rationale":"Controls, full principal pattern census, independent reconstruction, and audit."},
    "aggregate_peak_memory_mib":{"kind":"integer","value":8192,"rationale":"Three processes with compact streamed classification."},
    "aggregate_temporary_disk_bytes":{"kind":"integer","value":1073741824,"rationale":"1 GiB under 161177346048 measured available bytes, retaining the required 5 GiB reserve."}
  },
  "formula_families":["deletion-aware alternating 2x2x2 triple packet","Cycle 49 pair-fiber contraction","actual diagonal-mask admissibility","full-domain support-pattern census"],
  "selection_rule":["Use the first lexicographically admissible actual-mask cube only.","Evaluate every full-domain selected support pattern, never just the five labels.","Require an independently reconstructed raw-term and residual census."],
  "failure_rule":["A forbidden spill, no admissible packet, nonzero forbidden terminal, marginal mismatch, coverage error, or independent mismatch fails the theorem.","Do not add a second packet family or per-interface repair after failure; pause and hand off Problem 1."],
  "pre_execution":{"timestamp_utc":"2026-08-05T07:35:40Z","git_head":"29c098d7ee33e49049e4c4bea82c4155d190f6bf","git_state":"DIRTY with the active project untracked at repository level; Cycle 49 is sealed before this distinct deletion-aware packet theorem.","filesystem_observation_bytes":{"size":206900281344,"used":45706158080,"available":161177346048,"reserved":5368709120,"maximum_temporary_cap":155808636928,"chosen_temporary_cap":1073741824,"mount":"/"}},
  "input_paths":["artifacts/cycle-49-b049-lrc-relative-diagonal-contraction-v1.json","discovery/lrc_relative_diagonal.py","discovery/lrc_relative_diagonal_full_audit.py","discovery/lrc_relative_diagonal_inventory.py","discovery/lrc_cube_rewrite.py","discovery/cycle50_deletion_aware_packet_idea_selection.md","../../tools/preregistration_check.py"]
}
-->

## Stop rule

Stop on the first theorem pass, the first theorem falsifier, an error/cap, or
an independent mismatch.  Do not extend the local packet family after this
block: seal and either reassess the nonlocal lift boundary (pass) or hand off
Problem 1 (failure).
