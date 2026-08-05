# Cycle 21 / B021 preregistration: coupled CRT incidence and width-three deficits

## Decision question and idea selection

Can the two CRT diagonals be lifted to an exact globally coupled row-fiber
incidence model, and can a deterministic width-three block deficiency search
use that model to close at least one of the 76 surviving p199 leaves?

The primary proposed a coupled row-fiber model followed by width-three block
deficits, a Fourier/character bound on unions of the two relations, and a
finite-state transfer over the 14 beta fibers.  Darwin independently proposed
proving a coupled incidence formulation first, then seeking Hall or matching
deficiency, with Fourier as a higher-risk follow-on and transfer as an
implementation fallback.  We questioned the phrase “permutation graph”:
nonunit selected residues can have zero or multiple beta solutions, so any
independent-edge or permutation relaxation is unsound.  We selected exact
solution sets plus width-three blocks because this preserves the shared speed
choice across every alpha row and strictly extends the successful pair-block
theorem.  The main rejected alternative is an independently selectable-edge
matching model, falsified by any leaf whose relaxed outcome differs from its
direct CNF.

<!-- research-freeze-v1
{
  "schema":"research-preregistration-freeze-v1",
  "cycle":21,
  "parameters":{
    "idea_selection":{"kind":"text","value":"Primary: exact coupled row fibers plus width-three deficits, Fourier/character bounds, or finite-state beta transfer. Companion: exact coupled incidence first, then Hall/matching deficiency; Fourier and transfer as follow-ons. Choose coupled incidence plus width-three deficits; reject independently selectable permutation edges because nonunit residues and the shared speed choice make that relaxation unsound.","rationale":"Smallest exact extension with a strict new certificate family."},
    "incidence":{"kind":"expression","value":"For speed s, alpha in Z_p, beta in Z_c, xp=(alpha*(s mod p)) mod p canonically and w=s mod c. The coupled row mask contains beta iff w*beta=xp mod c, or xp!=0 and w*beta=xp-p mod c. Retain all solutions for nonunit w and use the same w in every alpha row.","rationale":"Cycle-20 theorem rewritten without reconstructing a modulo pc."},
    "interface_controls":{"kind":"expression","value":"Reconstruct the complete Cycle-11 formula twice, once with its frozen direct predicate and once with coupled CRT incidence, for all 240 deterministic H11 bases, all 53 frozen p47 bases, and p199 frozen base indices 3 and 4. Require clause-tuple equality, direct formula SHA-256 agreement with the frozen Cycle-11 result table, and exact equality of gcd/divisibility clauses. This performs 1,873,178 coordinate-choice-time predicate comparisons.","rationale":"Tests global cover and gcd interfaces without treating finite agreement as the general proof."},
    "target_rows":{"kind":"expression","value":"Exactly the 76 Cycle-18 rows with status UNRESOLVED, ordered by base 4 then base 3 and leaf ordinal. Verify exact equality with the frozen Cycle-18 table and with the Cycle-17 boundary before search.","rationale":"No target reselection."},
    "allowed_digits":{"kind":"expression","value":"Reconstruct each canonical mod-2/mod-7 witness leaf by the frozen Cycle-16/Cycle-18 ordinal convention. A block option is the Cartesian product of exactly those allowed digit sets; no gcd condition is dropped or added.","rationale":"Retains the certified canonical leaf cover."},
    "partition_family":{"kind":"expression","value":"Canonical blocks have size 1,2,or3. Include 13 cyclic partitions: for shift h=0..12 order coordinates h,h+1,... modulo 13, split the first 12 into four consecutive triples and leave the last singleton. For each of the leaf witness pairs P2,P7 and each r outside that pair, force the triple P union {r}, then split remaining coordinates in increasing order into consecutive triples and one final block of size 1 or 2. Add one combined partition: force the union if |P2 union P7|<=3; if the pairs are disjoint force both pairs; then complete the increasing remainder in triples and a final size-1-or-2 block. Canonicalize coordinates within blocks and blocks lexicographically; deduplicate while retaining first-generation order. At most 36 partitions per leaf.","rationale":"Deterministic witness-aware triples plus unbiased cyclic controls."},
    "certificate_search":{"kind":"expression","value":"For every frozen partition, solve the Cycle-18 nonnegative time-weight LP with block-option vectors equal to exact within-block unions, now allowing blocks of size three. Preserve distinct time clauses by earliest Cycle-11 clause representative after deduplicating identical positive choice-literal sets. Test integerization denominators 4096,65536,1048576,16777216 in order; retain only positive support at most 256 and promote only exact integer U<W after enumerating every allowed option in every block.","rationale":"Strictly extends pair-choice certificates while keeping exact replay small."},
    "transfer_continuation":{"kind":"expression","value":"After the frozen first pass produced 15 exact certificates and 61 unresolved leaves, directly test each of those 15 integer time-weight vectors against each of the 61 target leaves under cyclic coordinate shifts h=0..12 of the source partition. Interpret source clause number 1197+t as raw time t; rotate every coordinate label i to i+h mod 13, canonicalize the blocks, and enumerate every target-leaf block option from the original direct CNF. Test sources in results-table order and shifts 0..12; retain the first strict U<W per target. Similarity or inferred isomorphism is never a certificate.","rationale":"Same width-three question; exact target replay is cheaper and stronger than a guessed orbit rule."},
    "selection":{"kind":"expression","value":"Process every one of the 76 targets on CPUs 0-2. Within a leaf use frozen partition and denominator order and stop that leaf at its first exact deficit. Retain every leaf status and exact certificate. A cap leaves the current and unstarted targets unresolved.","rationale":"No favorable post-result partition or leaf selection."},
    "advance_condition":{"kind":"expression","value":"All interface controls must pass, and at least one exact width-three deficit must close a previously unresolved p199 leaf. Interface agreement alone is a proved representation but does not satisfy the research advance gate. A directly checked full-cover assignment is a headline falsifier.","rationale":"Requires mathematical discrimination beyond another encoding."},
    "falsifier":{"kind":"expression","value":"Any direct/CRT predicate mismatch, formula or frozen-hash mismatch, nonunit-solution loss, strict-boundary error, allowed-digit mismatch, omitted block option, or exact replay with U>=W invalidates the affected claim. A direct CNF model surviving a claimed deficit invalidates that leaf certificate.","rationale":"Defines exact contrary evidence."},
    "claim_boundary":{"kind":"expression","value":"Incidence equivalence concerns the frozen formulas and the general local theorem. Each deficit concerns one named canonical leaf. Partial closure does not close a base, F_1, J, or LRC(13); a cap or LP optimum at least one is not a no-go for triples, Fourier bounds, or other coupled engines.","rationale":"No promotion beyond checked interfaces and named leaves."}
  },
  "resource_caps":{
    "worker_processes":{"kind":"integer","value":3,"rationale":"Use CPUs 0-2 and reserve CPU 3."},
    "interface_instances":{"kind":"integer","value":295,"rationale":"240 H11, 53 p47, and two named p199 bases."},
    "interface_predicate_comparisons":{"kind":"integer","value":1873178,"rationale":"Complete coordinate-choice-time comparison count."},
    "target_rows":{"kind":"integer","value":76,"rationale":"Exact Cycle-18 unresolved boundary."},
    "partitions_per_leaf":{"kind":"integer","value":36,"rationale":"Hard cap implied by the frozen deterministic family."},
    "maximum_block_size":{"kind":"integer","value":3,"rationale":"First strict extension of the pair-block family."},
    "integer_certificate_support":{"kind":"integer","value":256,"rationale":"Exact replayable support cap inherited from Cycle 18."},
    "transfer_trials":{"kind":"integer","value":11895,"rationale":"At most 15 sources times 61 targets times 13 cyclic coordinate shifts."},
    "aggregate_wall_seconds":{"kind":"integer","value":3600,"rationale":"Controls, all target LPs reached before the deadline, exact replays, audit, and tests."},
    "aggregate_peak_memory_mib":{"kind":"integer","value":16384,"rationale":"Three sparse LP workers with explicit option matrices."},
    "aggregate_temporary_disk_bytes":{"kind":"integer","value":21474836480,"rationale":"20 GiB, below current free space minus the mandatory 5 GiB reserve."},
    "rng_seed":{"kind":"not_applicable","justification":"Bases, leaves, partitions, LP method, denominators, options, and ties are deterministic.","rationale":"No randomized selection."}
  },
  "formula_families":["coupled CRT row-fiber solution sets","Cycle-11 exact formula","canonical gcd-witness leaves","width-three block union masks","nonnegative weighted coverage deficits","direct cyclic certificate transfer"],
  "selection_rule":["Pass all direct-versus-CRT formula controls.","Verify the exact 76-row boundary and allowed digits.","Enumerate the frozen witness-aware and cyclic partitions.","Search the frozen LP and integerization family in order.","Apply all 15 exact weights to unresolved leaves under shifts 0..12 in frozen order.","Promote only exact target-specific U<W witnesses independently replayed from direct CNFs."],
  "failure_rule":["Any interface mismatch halts the search branch.","Any target or allowed-digit mismatch halts execution.","An LP, wall, memory, or disk cap retains affected targets as CAP.","A failed integerization or transfer remains unresolved.","A mapped target replay with U>=W makes no claim.","A direct full-cover candidate is retained and checked before classification."],
  "pre_execution":{"timestamp_utc":"2026-08-03T23:41:54Z","git_head":"29c098d7ee33e49049e4c4bea82c4155d190f6bf","git_state":"DIRTY with unrelated work; Cycle 20 is sealed before this distinct global coupled-incidence engine.","filesystem_observation_bytes":{"size":206900281344,"used":41260470272,"available":165623033856,"reserved":5368709120,"maximum_temporary_cap":160254324736,"chosen_temporary_cap":21474836480,"mount":"/"}},
  "transfer_pre_execution":{"timestamp_utc":"2026-08-04T00:25:21Z","git_head":"29c098d7ee33e49049e4c4bea82c4155d190f6bf","prior_stage":"The frozen width-three pass and independent direct-CNF audit completed before this same-cycle continuation; its result table is now a frozen executable input.","remaining_aggregate_wall_seconds":1369},
  "input_paths":["artifacts/cycle-20-b020-lrc-crt-diagonal-v1.json","artifacts/cycle-18-b018-lrc-pair-choice-v1.json","artifacts/cycle-16-b016-lrc-gcd-witness-tree-v1.json","discovery/lrc_certified_sat.py","discovery/out/cycle11-certified-sat/controls.tsv","discovery/out/cycle11-certified-sat/p199.tsv","discovery/out/partitioned-k6.txt","discovery/out/cycle8-p199-strata.txt","discovery/out/cycle11-certified-sat/p199/004.cnf","discovery/out/cycle11-certified-sat/p199/003.cnf","discovery/out/cycle18-pair-choice/results.tsv","discovery/out/cycle17-time-deficit/lp-results.tsv","discovery/out/cycle21-coupled-incidence/results.tsv","proof/cycle_11_sat_encoding_soundness.md","proof/cycle_18_pair_choice_soundness.md","proof/cycle_21_coupled_incidence_soundness.md","../../tools/preregistration_check.py"]
}
-->

## Stop rule

Stop on an interface, target, or exact-replay failure, or at the aggregate
resource cap.  After the complete frozen run, ask Darwin to review the
evidence, independently propose the next engine, and advise whether Cycle 21
continues, seals, or yields to a genuinely different question.
