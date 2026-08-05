# Cycle 16 / B016 preregistration: exact gcd-witness decision tree

## Decision question and idea selection

Can the first-lift contradiction be decomposed into a compact, independently
certified tree over canonical mod-2/mod-7 gcd witnesses, with small leaf cores
that transfer to held-out bases?

The primary proposed canonical gcd-witness leaves, an exact CRT bridge, and
resolution-community unions.  Darwin independently proposed a gcd-conditioned
learned-certificate tree, with CRT and checked community optimization as
fallbacks.  We questioned whether “learned” meant an unverifiable classifier;
it does not here.  The selected state space exactly partitions every
gcd-admissible assignment, and every closed leaf requires a replayable DRAT
certificate.  Tree statistics and proof-size predictions are only `OBSERVED`.

<!-- research-freeze-v1
{
  "schema":"research-preregistration-freeze-v1",
  "cycle":16,
  "parameters":{
    "idea_selection":{"kind":"text","value":"Primary: canonical gcd-witness leaves, CRT, or resolution-community unions. Companion: gcd-conditioned learned certificates, then CRT or checked community optimization. Choose canonical witnesses because they exactly partition admissible lifts and make every leaf independently certifiable.","rationale":"Both agents propose engines; statistical classification is explicitly excluded."},
    "canonical_state":{"kind":"expression","value":"For a selected lift, let (i,j), i<j, be the first two coordinates whose lifted residues are not divisible by 2, and (u,v), u<v, the first two not divisible by 7. A leaf fixes these canonical events: coordinates before i are divisible by 2, i is not; coordinates i+1..j-1 are divisible by 2, j is not; later coordinates unrestricted, and analogously for 7. The 78^2=6084 leaves are disjoint and cover exactly all assignments satisfying N2<=11 and N7<=11.","rationale":"Transforms the gcd cardinality condition into an exact finite decision tree."},
    "residual_cnf":{"kind":"expression","value":"Start from the exact Cycle-11 base CNF and add one negative unit for every x choice forbidden by a leaf's canonical 2/7 conditions. Deduplicate units. A leaf is UNSAT only after pinned CaDiCaL plus pinned drat-trim VERIFIED; SAT requires a preserved model checked against the full residual and direct improper-lift predicate.","rationale":"Each leaf certificate is standalone and maps back to Definition 2.1."},
    "training":{"kind":"expression","value":"Use only frozen sample base index 7 for the complete 6084-leaf tree. Process leaves lexicographically by (i,j,u,v), in three deterministic contiguous shards. Preserve every residual CNF and accepted proof/model until the decision boundary.","rationale":"A complete single-base tree is the smallest falsifiable prototype."},
    "leaf_core_selection":{"kind":"expression","value":"If all 6084 leaves are certified UNSAT, order leaves by proof bytes then ordinal and extract input cores for the first floor(6084/10)=608 leaves. Accept only source-subset cores with fresh checked proofs. Select the smallest core retaining a discriminating coverage clause, tied by leaf tuple then SHA-256.","rationale":"Searches for reusable leaf structure only after exact tree closure; the floor convention resolves the preregistered decile rounding ambiguity before core extraction."},
    "validation":{"kind":"expression","value":"Map the selected leaf core, if it has at most 500 clauses, to held-out frozen bases 4 and 3 under the Cycle-13 typed substitution family and the corresponding canonical leaf units. Accept only full literal clause-multiset containment. Do not inspect other bases.","rationale":"Tests exact transfer without training-target leakage."},
    "template_census_continuation":{"kind":"expression","value":"The selected 27-clause direct cover-deficit core matched both held-out leaves. Continue in the same cycle over all 6084 canonical leaves of all 100 frozen Cycle-8 sample bases. For each base/leaf, accept at most the first target coverage clause in source-CNF order whose divisor-color coordinate signature admits a typed bijection and whose every literal is forbidden by the canonical leaf units. Reconstruct the full typed map and require exact mapped-clause multiset containment. Store base index, leaf ordinal, and target clause index as the deterministic replay certificate; do not invoke SAT or inspect the 4,748,938-base census.","rationale":"Companion-reviewed continuation measures exact transfer breadth for the same learned-certificate question."},
    "advance_condition":{"kind":"expression","value":"A complete 6084-leaf checked tree is an independent exact certificate of the named base-7 first-lift exclusion. A selected at-most-500-clause discriminating leaf core or exact held-out embedding is the reusable structural advance. Partial closure, caps, and proof-size patterns make no universal claim.","rationale":"Separates exact named closure from reusable mechanism."},
    "falsifier":{"kind":"expression","value":"A gcd-admissible assignment outside the leaf partition or in two leaves, an emitted unit inconsistent with its canonical state, failed model/direct check, rejected proof, false core subset, or false mapped containment invalidates the affected result.","rationale":"Defines exact contrary evidence."},
    "claim_boundary":{"kind":"expression","value":"Even a complete tree reproves only base 7's first-lift exclusion. It proves no other base, full F_1 emptiness, J emptiness, or LRC(13) without exact transferred certificates.","rationale":"Prevents one-base decomposition overclaim."}
  },
  "resource_caps":{
    "worker_processes":{"kind":"integer","value":3,"rationale":"Use CPUs 0-2 and reserve CPU 3."},
    "canonical_leaves":{"kind":"integer","value":6084,"rationale":"All ordered pairs of two-element coordinate subsets."},
    "training_bases":{"kind":"integer","value":1,"rationale":"Frozen base index 7."},
    "validation_bases":{"kind":"integer","value":2,"rationale":"Frozen held-out indices 4 and 3."},
    "template_census_bases":{"kind":"integer","value":100,"rationale":"Exactly the frozen Cycle-8 sample, including training and held-out controls."},
    "template_census_leaf_tests":{"kind":"integer","value":608400,"rationale":"Every canonical leaf for every frozen sample base."},
    "solver_seconds_per_leaf":{"kind":"integer","value":60,"rationale":"Residual leaves should be easier; timeout returns CAP."},
    "core_extraction_decile_percent":{"kind":"integer","value":10,"rationale":"Only the frozen smallest proof-size decile after complete closure."},
    "candidate_clause_cap":{"kind":"integer","value":500,"rationale":"Reusable leaf-core threshold."},
    "aggregate_wall_seconds":{"kind":"integer","value":3600,"rationale":"Complete tree, checks, selected extraction, validation, and audit."},
    "aggregate_peak_memory_mib":{"kind":"integer","value":16384,"rationale":"Three solver/checker workers."},
    "aggregate_temporary_disk_bytes":{"kind":"integer","value":21474836480,"rationale":"20 GiB, below current free space minus the mandatory 5 GiB reserve."},
    "rng_seed":{"kind":"not_applicable","justification":"Leaf order, sharding, solver, ties, and validation are deterministic.","rationale":"No randomized selection."}
  },
  "formula_families":["canonical first-two nondivisibility witnesses","exact residual first-lift CNF","leaf DRAT certificates","checked leaf input cores","typed held-out containment"],
  "selection_rule":["Prove the canonical leaf partition before execution.","Process all 6084 base-7 leaves lexicographically on CPUs 0-2.","Accept only direct SAT models or checked UNSAT proofs.","Extract cores only after complete closure and only from the frozen proof-size decile.","Validate first on frozen bases 4 and 3.","After both exact matches, census every frozen sample base/leaf in deterministic order and store only the first exact mapped target clause."],
  "failure_rule":["Any partition or residual-encoding control failure halts leaf execution.","CAP or failed evidence retains the leaf and blocks complete-tree closure.","Partial tree statistics do not support a mathematical claim.","No full-census or other-base solve is authorized."],
  "pre_execution":{"timestamp_utc":"2026-08-03T21:05:05Z","git_head":"29c098d7ee33e49049e4c4bea82c4155d190f6bf","git_state":"DIRTY with unrelated work; Cycle 15 is sealed before this distinct exact gcd-witness tree.","filesystem_observation_bytes":{"size":206900281344,"used":39112994816,"available":167770509312,"reserved":5368709120,"maximum_temporary_cap":162401800192,"chosen_temporary_cap":21474836480,"mount":"/"}},
  "input_paths":["artifacts/cycle-15-b015-lrc-resolution-slicing-v1.json","artifacts/cycle-14-b014-lrc-proof-diversification-v1.json","discovery/out/cycle11-certified-sat/p199/007.cnf","discovery/out/cycle11-certified-sat/p199/004.cnf","discovery/out/cycle11-certified-sat/p199/003.cnf","discovery/out/cycle8-p199-strata.txt","proof/cycle_11_sat_encoding_soundness.md","proof/cycle_16_gcd_witness_tree_soundness.md","discovery/vendor/cadical-f13d74439a5b5c963ac5b02d05ce93a8098018b8.tar.gz","discovery/vendor/drat-trim-2e5e29cb0019d5cfd547d4208dca1b3ec290349f.tar.gz","../../tools/preregistration_check.py"]
}
-->

## Stop rule

Stop on a partition/encoding failure or aggregate cap.  After the complete tree
or partial capped outcome, obtain a material companion review before sealing,
changing engines, or declaring Problem 1 saturated.
