# Cycle 29 / B029 preregistration: ownership-blocker semantic primal lift

## Decision question and idea selection

Does labeled time ownership with coordinate-local minimal blocker hyperedges give
an exact bidirectional feasibility interface for the direct cover problem, pass
complete synthetic and H11 controls, and retain raw-time distinctions between
same-divisor-color digits on frozen p199 base 4 / leaf 78? If so, does the
complete blocker antichain on that target expose a bounded-rank structure worth
pursuing as a new completion invariant?

The adversarial comparison is in
`discovery/cycle29_semantic_primal_idea_selection.md`. The main rejected
alternative is exact rational reconstruction for one Cycle-28 LP: it has a
strong verifier but low expected leaf-closing information and remains inside
the thread-sensitive fixed-geometry family. The ownership-blocker engine is
chosen because it changes the state space and admits an exact equivalence
theorem before any survivor search.

For finite times (T), coordinates (i), allowed digits (A_i), and bad-time
masks (M_{i,d}\subseteq T), a labeled ownership state is a partition
(T=O_1\sqcup\cdots\sqcup O_k) such that each (O_i\) is contained in at least
one (M_{i,d}). A coordinate blocker is an inclusion-minimal set
(E\subseteq T) contained in no (M_{i,d}). The intended theorem is that a
direct full cover exists exactly when a legal ownership state exists, and
local legality is exactly avoidance of every coordinate blocker.

For implementation, quotient raw times at each coordinate by the exact
digit-support signature (D_t=\{d\in A_i:t\in M_{i,d}\}). A local cell is
legal exactly when the intersection of its signatures is nonempty. A minimal
blocker contains at most one time from each signature class and corresponds
exactly to a minimal family of present signatures with empty intersection;
the number of concrete blockers represented by a signature pattern is the
product of its class sizes. The census must retain every signature class,
pattern, rank, and exact multiplicity.

The branch falsifier is any direct cover without a legal canonical ownership
state, legal ownership state whose canonical local witnesses do not reconstruct
a direct cover, blocker/local-legality mismatch, H11 interface mismatch, or
loss of the frozen same-color raw-mask distinction. Equivalence with only an
unstructured full blocker family is containment, not progress.

<!-- research-freeze-v1
{"schema":"research-preregistration-freeze-v1","cycle":29,
"parameters":{"theorem":{"kind":"expression","value":"Prove for every finite direct-cover interface that union_i M_(i,d_i)=T for some allowed digits iff T has a labeled disjoint ownership partition O_i with O_i subset M_(i,d_i) for some local witness digit. The forward map assigns each time to the least-index covering coordinate; the reverse map chooses the least allowed digit covering each ownership cell. Prove additionally that O_i is locally legal iff it contains no inclusion-minimal set missed by every allowed digit. For digit-support signatures D_t={d:t in M_(i,d)}, prove that minimal blockers are exactly concrete lifts of minimal families of present signatures with empty intersection and never repeat a signature.","rationale":"Exact bidirectional feasibility, blocker characterization, and signature quotient before computation."},"synthetic_controls":{"kind":"expression","value":"Exhaust every 2-coordinate, 2-digit, 4-time Boolean mask interface (2^16 interfaces), and every 3-coordinate, 2-digit, 3-time Boolean mask interface (2^18 interfaces). For each, compare direct assignment feasibility with exhaustive ownership labelings, verify both canonical maps when feasible, enumerate minimal blockers, and compare blocker avoidance with direct local legality for every ownership cell.","rationale":"Complete small controls exercise feasible and infeasible directions without relying on LRC structure."},"h11_control":{"kind":"expression","value":"For k=3,p=11,c=4, exactly reproduce the raw 64,000 lifted assignments over all base tuples in {1,...,10}^3 using the frozen Cycle-8 bad-mask and omission-gcd conventions. Decompose gcd-admissible assignments into the four exact parity signatures (no even speed or exactly one named even coordinate), map every direct full cover forward and back, and require zero retained improper bases as in Cycle 8.","rationale":"Actual complete LRC interface control with labels and gcd-channel decomposition."},"p199_target":{"kind":"expression","value":"Exactly Cycle-25 target base_index=4, leaf_ordinal=78, using the frozen base, allowed-digit, and raw-time coverage conventions. Find the lexicographically first coordinate and pair of allowed digits with the same (2-divides-speed,7-divides-speed) color but distinct masks, and the least distinguishing raw time. For every coordinate, partition all 2786 raw times by exact allowed-digit support signature, enumerate every minimal empty-intersection signature pattern, and record its rank and exact concrete multiplicity as the product of class sizes.","rationale":"Smallest frozen survivor control, exact blocker quotient, and explicit escape from Cycle-13 color collapse."},"advance_condition":{"kind":"expression","value":"A proved general equivalence, all complete synthetic and H11 controls passing, one exact same-color/distinct-mask p199 witness, and a complete p199 blocker census within cap that exposes at least one proper blocker and its verified rank distribution.","rationale":"Establish an exact non-color-collapsed semantic engine with a falsifiable structural prototype."},"falsifier":{"kind":"expression","value":"Any forward/reverse map, label, feasibility, blocker-minimality, blocker-completeness, signature-class, pattern-multiplicity, H11 retained-count, p199 target, allowed-digit, color, mask, or distinguishing-time mismatch halts the affected branch. A complete but noncompressible blocker family is CONTAINED, not a no-go for other semantic lifts.","rationale":"Concrete contrary evidence and scoped containment."},"claim_boundary":{"kind":"expression","value":"The equivalence theorem concerns finite direct-cover feasibility for frozen allowed sets. Synthetic and H11 controls validate the implementation; one p199 blocker census concerns only base 4 / leaf 78. No result by itself excludes a new p199 leaf, closes all 60 survivors, or proves LRC(13).","rationale":"No promotion from interface equivalence to conjecture closure."}},
"resource_caps":{"worker_processes":{"kind":"integer","value":3,"rationale":"Use CPUs 0-2 and reserve CPU 3."},"synthetic_interfaces":{"kind":"integer","value":327680,"rationale":"Exactly 2^16 plus 2^18 complete interfaces."},"h11_lifted_assignments":{"kind":"integer","value":64000,"rationale":"Frozen complete raw Cycle-8 control."},"p199_targets":{"kind":"integer","value":1,"rationale":"One named semantic prototype before any survivor campaign."},"p199_coordinates":{"kind":"integer","value":13,"rationale":"All labeled coordinates of the named target."},"signature_patterns_total":{"kind":"integer","value":2000000,"rationale":"Aggregate minimal empty-intersection signature-pattern cap; no silent truncation."},"transversal_nodes":{"kind":"integer","value":20000000,"rationale":"Aggregate exact signature-pattern search cap."},"blocker_rank":{"kind":"integer","value":14,"rationale":"No minimal empty-intersection signature family needs more witnesses than the at-most-14 allowed digits; exceeding this signals a defect."},"aggregate_wall_seconds":{"kind":"integer","value":1800,"rationale":"Theorem audit, complete controls, one p199 census, independent replay, and tests."},"aggregate_peak_memory_mib":{"kind":"integer","value":4096,"rationale":"Three bounded exact workers, below host capacity."},"aggregate_temporary_disk_bytes":{"kind":"integer","value":5368709120,"rationale":"5 GiB, below measured free space minus the required 5 GiB reserve."},"rng_seed":{"kind":"not_applicable","justification":"All interfaces, assignments, ownership labelings, targets, signature patterns, ties, and witnesses are exhaustive and lexicographic.","rationale":"No randomness."}},
"formula_families":["direct bad-time masks","labeled ownership partitions","digit-support signature quotient","coordinate-local minimal empty-intersection families","asymmetric blocker hypergraph coloring","exact gcd parity signatures"],"selection_rule":["Prove and audit the finite equivalence first.","Run both complete synthetic corpora in lexicographic mask order.","Replay the complete H11 interface and four exact parity signatures.","Use only frozen p199 base 4 / leaf 78.","Select the first same-color distinct-mask witness lexicographically.","Partition all raw times by exact local digit-support signature and enumerate every minimal empty-intersection signature pattern with exact concrete multiplicity.","Do not search any other survivor until all controls pass."],"failure_rule":["A theorem-interface or complete-control mismatch halts the branch.","A p199 target or same-color witness mismatch is ERROR.","A node, signature-pattern, wall, memory, or disk cap is CAP and no completeness claim is made.","A complete census with no proper or no compressible blocker structure is CONTAINED.","No failed coordinate or interface is dropped."],"pre_execution":{"timestamp_utc":"2026-08-04T13:35:40Z","git_head":"29c098d7ee33e49049e4c4bea82c4155d190f6bf","git_state":"DIRTY with unrelated root work and the active open-conjecture-sweep project untracked at repository level; C28 containment sealed before this distinct state-space question.","filesystem_observation_bytes":{"size":206900281344,"used":45288189952,"available":161595314176,"reserved":5368709120,"maximum_temporary_cap":156226605056,"chosen_temporary_cap":5368709120,"mount":"/"}},"input_paths":["artifacts/cycle-8-b008-lrc-fused-lift-v1.json","artifacts/cycle-13-b013-lrc-semantic-collapse-v1.json","artifacts/cycle-28-b028-lrc-portfolio-cyclic-width-five-v1.json","proof/check_cycle_8_fused_lift.py","discovery/out/cycle11-certified-sat/p199/004.cnf","discovery/out/cycle25-quadratic-crt/results.tsv","discovery/lrc_pair_choice.py","discovery/lrc_coupled_incidence.py","discovery/lrc_width_four_stage_a.py","discovery/cycle29_semantic_primal_idea_selection.md","../../tools/preregistration_check.py"]}
-->

## Stop rule

Stop at the first theorem/control mismatch, missing same-color distinction,
complete p199 blocker census, or aggregate cap. A complete exact equivalence
without a bounded-rank/compressible p199 structure is a contained semantic
interface, not authorization to relabel the same mechanism and continue.
