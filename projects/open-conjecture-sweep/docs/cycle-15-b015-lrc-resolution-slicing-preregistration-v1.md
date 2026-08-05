# Cycle 15 / B015 preregistration: resolution-dependency slicing

## Decision question and idea selection

Can the selected Cycle-14 proof's exact LRAT dependency graph propose an
at-most-500-clause, color-discriminating input slice which receives a fresh
UNSAT certificate?

The primary proposed LRAT backward distance/frequency slices, resolution
dominators, and an exact CRT prototype.  Darwin independently proposed
resolution-graph backward/dominator slicing, with CRT as fallback.  We
questioned whether proof-graph centrality says anything about standalone
unsatisfiability; it does not.  The graph is therefore used only to freeze a
small candidate family.  Every accepted slice must be solved anew and receive
an independent DRAT check.  Repeating clause-by-clause deletion is rejected
because Cycle 14 exhausted that bounded engine without one certified deletion.

<!-- research-freeze-v1
{
  "schema":"research-preregistration-freeze-v1",
  "cycle":15,
  "parameters":{
    "idea_selection":{"kind":"text","value":"Primary: LRAT backward-distance/frequency slices, resolution dominators, or CRT. Companion: backward/dominator slicing, then CRT. Choose exact dependency slicing because it exploits the proof already paid for and candidates remain independently falsifiable by fresh SAT/DRAT checks.","rationale":"Both agents proposed graph slicing; centrality alone is explicitly denied proof status."},
    "source":{"kind":"expression","value":"Use only Cycle-14 base 7, noelimprobe solver, default core extraction: the frozen 2329-clause CNF and its fresh checked DRAT proof. Protect the same lexicographically smallest discriminating normalized coverage clause used in Cycle 14.","rationale":"No post-result proof or core reselection."},
    "dependency_trace":{"kind":"expression","value":"Run pinned drat-trim with ASCII LRAT output (-L) on the selected core/proof. Accept the dependency DAG only if every positive antecedent ID precedes its derived clause, the final active empty clause is identified, all reached input IDs map exactly to frozen input clauses, and drat-trim again reports VERIFIED.","rationale":"LRAT hints expose exact dependencies; malformed graphs cannot select candidates."},
    "candidate_families":{"kind":"expression","value":"Within the backward closure of the final empty clause, rank input clauses by exactly three frozen scores: minimum backward distance from the empty clause (ascending, then input ID); antecedent-reference frequency in the closure (descending, then input ID); and support size of each strict derived dominator on the empty-to-input-super-sink graph (ascending support size, then node ID). For distance and frequency take prefixes 128, 256, and 500. For dominators take at most the first six distinct supports of size at most 500. Add the protected clause to every candidate, dropping the last ranked nonprotected clause when needed. Deduplicate by clause-multiset SHA-256.","rationale":"A small deterministic portfolio tests local, frequent, and bottleneck proof structure."},
    "candidate_checks":{"kind":"expression","value":"For every distinct candidate, emit an exact input-clause subset CNF. Run pinned CaDiCaL with a 300-second limit. SAT requires an independently parsed model satisfying every candidate clause; UNSAT requires pinned drat-trim VERIFIED against the exact candidate and proof. Timeout or failed evidence is CAP/ERROR.","rationale":"Graph selection never replaces standalone certification."},
    "selection":{"kind":"expression","value":"Among certified UNSAT candidates select by fewer clauses, then more discriminating clauses, candidate-family order distance/frequency/dominator, parameter, and CNF SHA-256. If none certify, retain all rows and close only this slice family.","rationale":"Prevents result-driven slice selection."},
    "advance_condition":{"kind":"expression","value":"At least one freshly certified UNSAT candidate with at most 500 clauses and at least one discriminating coverage clause is a structural advance. A later target exclusion additionally requires exact typed mapped-clause containment; no target CNFs are inspected in this cycle.","rationale":"Separates source compression from transport."},
    "falsifier":{"kind":"expression","value":"Malformed or forward-pointing LRAT hints, input-ID mismatch, false dominator/support computation, candidate clause absent from source, failed DRAT check, or SAT model for a claimed UNSAT candidate invalidates the affected result.","rationale":"Defines exact contrary evidence."},
    "claim_boundary":{"kind":"expression","value":"Claims concern only the selected proof, frozen graph scores, and emitted source subsets. Centrality scores are OBSERVED selection devices. No statement about all cores, target embeddings, F_1 emptiness, J emptiness, or LRC(13) follows.","rationale":"A proof-specific slice is not a universal theorem."}
  },
  "resource_caps":{
    "worker_processes":{"kind":"integer","value":3,"rationale":"Use CPUs 0-2 and reserve CPU 3."},
    "source_cores":{"kind":"integer","value":1,"rationale":"Frozen Cycle-14 selected core only."},
    "prefix_candidates":{"kind":"integer","value":6,"rationale":"Three sizes for each of two rankings."},
    "dominator_candidates":{"kind":"integer","value":6,"rationale":"At most six distinct small dominator supports."},
    "candidate_clause_cap":{"kind":"integer","value":500,"rationale":"Frozen structural advance threshold."},
    "solver_seconds_per_candidate":{"kind":"integer","value":300,"rationale":"Timeout returns CAP."},
    "aggregate_wall_seconds":{"kind":"integer","value":3600,"rationale":"LRAT generation, parsing, candidate solving/checking, and audit combined."},
    "aggregate_peak_memory_mib":{"kind":"integer","value":16384,"rationale":"Three candidate solvers plus graph arrays."},
    "aggregate_temporary_disk_bytes":{"kind":"integer","value":21474836480,"rationale":"20 GiB, below current free space minus the mandatory 5 GiB reserve."},
    "rng_seed":{"kind":"not_applicable","justification":"Trace, graph ranks, ties, and solver configuration are deterministic.","rationale":"No randomized selection."}
  },
  "formula_families":["checked DRAT source proof","ASCII LRAT dependency DAG","backward input support","distance and frequency slices","strict dominator supports","fresh SAT/DRAT candidate certification"],
  "selection_rule":["Generate and validate one LRAT dependency graph from the frozen source.","Construct only the frozen distance, frequency, and dominator candidates.","Protect one discriminating clause in every candidate.","Check candidates on at most CPUs 0-2.","Select only from fresh certified UNSAT rows.","Do not inspect validation or external target CNFs."],
  "failure_rule":["Any trace/source mismatch halts candidate generation.","SAT with a checked model rejects only that candidate.","Timeout or proof failure retains the candidate as CAP/ERROR.","No certified slice closes only the frozen graph-slice family and does not imply core minimality."],
  "pre_execution":{"timestamp_utc":"2026-08-03T20:54:37Z","git_head":"29c098d7ee33e49049e4c4bea82c4155d190f6bf","git_state":"DIRTY with unrelated work; Cycle 14 is sealed before this distinct proof-graph engine.","filesystem_observation_bytes":{"size":206900281344,"used":38976307200,"available":167907196928,"reserved":5368709120,"maximum_temporary_cap":162538487808,"chosen_temporary_cap":21474836480,"mount":"/"}},
  "input_paths":["artifacts/cycle-14-b014-lrc-proof-diversification-v1.json","discovery/out/cycle14-proof-diversification/cores/007/noelimprobe/default.cnf","discovery/out/cycle14-proof-diversification/core-proofs/007/noelimprobe/default.drat","discovery/out/cycle8-p199-strata.txt","proof/cycle_11_sat_encoding_soundness.md","proof/cycle_13_semantic_instantiation_soundness.md","discovery/vendor/drat-trim-2e5e29cb0019d5cfd547d4208dca1b3ec290349f.tar.gz","../../tools/preregistration_check.py"]
}
-->

## Stop rule

Stop on a trace/source mismatch or aggregate cap.  After all frozen candidate
checks, obtain a material companion review before sealing, changing engines,
or declaring Problem 1 saturated.
