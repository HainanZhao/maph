# Cycle 52 / B052 preregistration: exact local step-graphon variation

## Decision question

Does a frozen primitive symmetric zero-mean 2- or 3-step perturbation of the
constant (p=1/2) graphon give an exact negative local direction for
(K_{5,5}\setminus C_{10})?

<!-- research-freeze-v1
{
  "schema":"research-preregistration-freeze-v1",
  "cycle":52,
  "parameters":{
    "target":{"kind":"expression","value":"Use H with left L_i and right R_j indexed by Z/5Z, edges L_iR_j exactly when j-i is not 0 or -1 modulo 5. Thus e(H)=15. For a symmetric q-step graphon W, t_H(W) is the exact sum over all maps of the ten vertices to q blocks, weighted by equal block measures q^-10.","rationale":"Pins the graph, 15-edge convention, graphon normalization, and finite evaluator."},
    "direction_family":{"kind":"expression","value":"For q in {2,3}, enumerate every symmetric integer q by q matrix B with entries in {-2,-1,0,1,2}, weighted entry sum zero, nonzero, and primitive gcd of nonzero entries one. Identify B and -B only by retaining the lexicographically smaller flattened sign representative. Set U=B/2, so |U|<=1 and p+epsilon U lies in [0,1] for every epsilon in [0,1/2]. Do not impose D10 symmetry on B.","rationale":"Freezes a finite asymmetric step-direction family while avoiding scale and global-sign duplicates."},
    "coefficient_rule":{"kind":"expression","value":"Expand exactly P_B(epsilon)=t_H(1/2+epsilon U)-(1/2)^15 as a degree-at-most-15 polynomial over Q. The first nonzero coefficient is the least k>=1 with nonzero coefficient; its sign is LOCAL_NEGATIVE, LOCAL_POSITIVE, or IDENTICALLY_ZERO. Compute by exact multiplication of the 15 edge factors over all q^10 block assignments, not floating differences.","rationale":"Defines the local invariant without numerical cancellation."},
    "realization_rule":{"kind":"expression","value":"For every LOCAL_NEGATIVE B, test epsilon=2^-m for m=2,...,512 in increasing m until P_B(epsilon)<0. Store the first such rational epsilon and all q^2 graphon values. A missing realization within this frozen range is ERROR, not a counterexample. LOCAL_POSITIVE and IDENTICALLY_ZERO rows are finite local classifications only.","rationale":"Requires an explicit bounded rational graphon rather than a formal infinitesimal claim."},
    "controls":{"kind":"expression","value":"Verify the 15 edges and D10 graph automorphisms. Check the direct 2-step hand expansion for B=((1,-1),(-1,1)); verify P_B(0)=0, mean(U)=0, and W in [0,1] for every recorded epsilon. Independently rebuild the direction list in reverse order and evaluate each polynomial by a separately implemented reverse-edge recurrence (the coefficient recurrence equivalent to the edge-subset expansion); use literal subset-of-edges expansion on the frozen 2-step hand control.","rationale":"Separates conventions, expansion algebra, graphon feasibility, and full family coverage without converting the independent control into an avoidably super-cap exhaustive subset traversal."},
    "interpretation":{"kind":"expression","value":"One realized negative row is COUNTEREXAMPLE_CANDIDATE and blocks all positive Sidorenko promotion pending independent replay. A full finite nonnegative census proves only local stability on this frozen 2/3-step family; it does not prove local Sidorenko for arbitrary graphons or Sidorenko.","rationale":"Prevents a finite local test from becoming a global theorem."},
    "method_collapse_guard":{"kind":"expression","value":"No optimizer, floating point, adaptive partition, SOS, norming argument, or post-result direction extension is permitted. The only positive result is the fixed exact direction census.","rationale":"Keeps a counterexample search from becoming an unbounded numerical hunt."},
    "advance_condition":{"kind":"expression","value":"A realized negative row is a durable candidate requiring a separate exact audit. If all rows are nonnegative, seal the finite local boundary and select a distinct nonlocal extremizer engine; do not enlarge q or the entry alphabet in this cycle.","rationale":"Makes both outcomes strategic rather than a census treadmill."},
    "falsifier":{"kind":"expression","value":"Any wrong edge/automorphism count, nonzero mean, out-of-range W, coefficient mismatch, duplicate/corpus mismatch, independent replay mismatch, or negative row lacking a frozen rational realization is ERROR. A realized negative row is the mathematical candidate.","rationale":"States algebraic, coverage, and graphon-realization checks."},
    "claim_boundary":{"kind":"expression","value":"A pass proves only the frozen local 2/3-step direction result. A negative row is a concrete graphon counterexample candidate, not a published proof until its independent exact replay and all conventions are audited.","rationale":"Correctly limits both possible claims."}
  },
  "resource_caps":{
    "worker_processes":{"kind":"integer","value":3,"rationale":"Use CPUs 0-2 at most and reserve CPU 3."},
    "directions":{"kind":"integer","value":20000,"rationale":"All primitive sign-canonical symmetric 2/3-step matrices under the frozen alphabet."},
    "block_assignments":{"kind":"integer","value":1200000000,"rationale":"Aggregate q^10 exact assignment evaluations across principal/replay and controls."},
    "polynomial_degree":{"kind":"integer","value":15,"rationale":"One factor per frozen H edge."},
    "dyadic_realization_exponents":{"kind":"integer","value":512,"rationale":"Fixed realization search for any negative leading row."},
    "aggregate_wall_seconds":{"kind":"integer","value":7200,"rationale":"Exact principal census, independent replay, and audit."},
    "aggregate_peak_memory_mib":{"kind":"integer","value":4096,"rationale":"Compact coefficient counts and streamed rows."},
    "aggregate_temporary_disk_bytes":{"kind":"integer","value":1073741824,"rationale":"1 GiB under 161205972992 measured available bytes, retaining the reserve."}
  },
  "formula_families":["exact step-graphon homomorphism polynomial","fixed-density zero-mean perturbation","dyadic rational graphon realization","D10 convention control"],
  "selection_rule":["Enumerate the full frozen 2/3-step matrix family once, retaining every row.","Use exact coefficient arithmetic and no adaptive direction selection.","Independently reconstruct every matrix and polynomial in reverse order."],
  "failure_rule":["A realized negative polynomial row is a counterexample candidate requiring containment and independent audit.","A full positive census is finite local evidence only.","Any convention, feasibility, coefficient, coverage, or replay mismatch halts as ERROR."],
  "pre_execution":{"timestamp_utc":"2026-08-05T08:01:59Z","git_head":"29c098d7ee33e49049e4c4bea82c4155d190f6bf","git_state":"DIRTY with the active project untracked at repository level; Cycle 51 is sealed before this distinct local graphon engine.","filesystem_observation_bytes":{"size":206900281344,"used":45677531136,"available":161205972992,"reserved":5368709120,"maximum_temporary_cap":155837263872,"chosen_temporary_cap":1073741824,"mount":"/"}},
  "input_paths":["artifacts/cycle-51-b051-sidorenko-conjugacy-averaging-v1.json","discovery/problem2_eligibility_audit.md","discovery/cycle52_local_variation_idea_selection.md","../../tools/preregistration_check.py"]
}
-->

## Stop rule

Stop on a fully replayed realized negative row, after complete nonnegative
coverage of the frozen family, or on error/cap. Do not enlarge the local family
inside C52.
