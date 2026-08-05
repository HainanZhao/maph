# Cycle 51 / B051 preregistration: exact conjugacy averaging reconnaissance

## Decision question

Does the frozen exact finite-group corpus contain a nonnegative Cayley kernel
for which (K_{5,5}\setminus C_{10}) has smaller density than its conjugacy
class average?

<!-- research-freeze-v1
{
  "schema":"research-preregistration-freeze-v1",
  "cycle":51,
  "parameters":{
    "target_graph":{"kind":"expression","value":"Let left vertices L_i and right vertices R_j be indexed by Z/5Z. The deleted Hamilton cycle consists of L_iR_i and L_iR_{i-1}; H has all other L_iR_j, hence exactly 15 edges. For a finite group Gamma and a:Gamma to Q_{≥0}, t_Cay(H;Gamma,a)=E_{x_i,y_j} product_{L_iR_j in E(H)} a(x_i^{-1}y_j). The class average is a^cl(g)=E_h a(h^{-1}gh).","rationale":"Pins the 15-edge convention, normalization, and the paper's exact comparator."},
    "corpus":{"kind":"expression","value":"Enumerate every indicator function of S3, D8, and Q8. Separately enumerate every distinct product-set T1T2 with T1,T2 subgroups of S3 or S4, using its indicator. No other groups, weights, random samples, or outcome-selected functions are included.","rationale":"Separates a complete small nonabelian test from the specific symmetric-group/subgroup-product reduction family."},
    "evaluator":{"kind":"expression","value":"Use left-translation invariance to fix x0=e, sum exactly over the four remaining left variables, and for each right vertex count the intersection of its required translated connection sets. All counts are integers and each density is stored as numerator divided by |Gamma|^9. Compute a^cl exactly by conjugacy-class counts. A direct all-ten-variable enumerator is required only as a control on Gamma=S3.","rationale":"Provides a fast exact formula and an independent small control."},
    "comparison":{"kind":"expression","value":"For every frozen function, compare t_Cay(H;Gamma,a) and t_Cay(H;Gamma,a^cl) by integer cross multiplication. A strict negative difference is COMPARISON_COUNTERMODEL. Equality or positive difference is PASS_ROW. Preserve every row and the lexicographically first countermodel if any.","rationale":"The comparison direction is exactly that in Zhao Theorem 1.3."},
    "interpretation":{"kind":"expression","value":"A countermodel on any group refutes the universal all-finite-group comparison hypothesis of Zhao Theorem 1.3, but does not disprove Sidorenko. A countermodel among S_n subgroup-product rows also refutes the comparison on that frozen reduction subclass, but not every possible reduction host. A full finite pass proves only the frozen corpus result, not the universal comparison or Sidorenko.","rationale":"Prevents finite evidence from becoming a conjecture claim."},
    "controls":{"kind":"expression","value":"Verify H has 15 edges and D10 automorphism action preserves its adjacency. Check constant empty/full functions, conjugacy-invariant inputs, and three frozen S3 controls (empty, full, and lexicographically least non-class indicator) against the direct ten-variable enumerator. Independently rebuild group multiplication, conjugacy classes, subgroup products, and reverse-order comparison rows without importing the principal evaluator.","rationale":"Separates graph convention, algebra, optimization identity, and corpus enumeration without turning a control into an avoidably huge repeated replay."},
    "method_collapse_guard":{"kind":"expression","value":"No floating arithmetic, optimizer, graphon discretization, SOS solver, norming test, or adaptive group/function enlargement may determine the C51 outcome. The output is only the frozen exact comparison census.","rationale":"Maintains the proposed route's sharp falsifier."},
    "advance_condition":{"kind":"expression","value":"A COMPARISON_COUNTERMODEL is a durable route falsifier. A full PASS corpus is a finite theorem only; then classify its equality/nontrivial-gap signatures before choosing one distinct next engine. An implementation or coverage mismatch is ERROR, not evidence.","rationale":"States the permitted outcomes without overclaim."},
    "falsifier":{"kind":"expression","value":"Any evaluator/control disagreement, nonintegral class average, wrong edge count, row-coverage mismatch, or independent replay mismatch is ERROR. Mathematically, one exact negative comparison is the route falsifier.","rationale":"Gives exact mathematical and implementation failure criteria."},
    "claim_boundary":{"kind":"expression","value":"This cycle cannot prove or disprove Sidorenko unless it somehow produces a direct graphon counterexample, which is not expected from this comparator. It tests only Zhao's proposed sufficient comparison on a finite frozen corpus.","rationale":"Keeps the local finite result correctly scoped."}
  },
  "resource_caps":{
    "worker_processes":{"kind":"integer","value":3,"rationale":"Use at most CPUs 0-2 and reserve CPU 3."},
    "groups":{"kind":"integer","value":5,"rationale":"S3,D8,Q8 plus S3,S4 subgroup-product families."},
    "indicator_functions":{"kind":"integer","value":1024,"rationale":"All subsets of S3,D8,Q8: 64+256+256; distinct S3/S4 product sets are capped separately."},
    "subgroup_product_sets":{"kind":"integer","value":4096,"rationale":"Absolute cap for all distinct T1T2 products over the frozen S3,S4 subgroup pairs."},
    "normalized_left_assignments":{"kind":"integer","value":100000000,"rationale":"Aggregate |Gamma|^4 exact evaluations over all rows and controls."},
    "aggregate_wall_seconds":{"kind":"integer","value":7200,"rationale":"Principal exact census, direct S3 controls, independent replay, and audit."},
    "aggregate_peak_memory_mib":{"kind":"integer","value":4096,"rationale":"Bitset/intersection tables plus three workers."},
    "aggregate_temporary_disk_bytes":{"kind":"integer","value":1073741824,"rationale":"1 GiB under 161206743040 measured available bytes, retaining the required reserve."}
  },
  "formula_families":["Cayley homomorphism density","conjugacy-class averaging","Szegedy symmetric-group reduction interface","exact translated-set intersections"],
  "selection_rule":["Enumerate the frozen corpus exhaustively and retain every comparison row.","Use no adaptively selected groups or functions.","Require direct S3 controls and a separate reverse-order reconstruction."],
  "failure_rule":["Any exact negative comparison is a scoped route falsifier, not a Sidorenko counterexample.","No full finite pass may be promoted to Zhao's universal hypothesis or Sidorenko.","Coverage, convention, or replay mismatches halt the branch as ERROR."],
  "pre_execution":{"timestamp_utc":"2026-08-05T07:52:33Z","git_head":"29c098d7ee33e49049e4c4bea82c4155d190f6bf","git_state":"DIRTY with the active project untracked at repository level; Problem 1 is paused at sealed C50 and Problem 2 is provisionally eligible.","filesystem_observation_bytes":{"size":206900281344,"used":45676761088,"available":161206743040,"reserved":5368709120,"maximum_temporary_cap":155838033920,"chosen_temporary_cap":1073741824,"mount":"/"}},
  "input_paths":["discovery/problem2_eligibility_audit.md","discovery/cycle51_conjugacy_averaging_idea_selection.md","artifacts/cycle-50-b050-lrc-deletion-aware-packet-v1.json","../../tools/preregistration_check.py"]
}
-->

## Stop rule

Stop after the complete frozen corpus is independently reconstructed, on its
first exact comparator countermodel, or on error/cap.  Do not enlarge the
group/function family inside this cycle.
