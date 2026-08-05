# Cycle 53 / B053 preregistration: analytic directional local stability

## Decision question

For the Möbius graph \(H=K_{5,5}\setminus C_{10}\), can the exact expansion
at the constant graphon \(W\equiv1/2\) prove directional local positivity for
every nonzero bounded symmetric zero-mean kernel, rather than merely the C52
step directions?

<!-- research-freeze-v1
{
  "schema":"research-preregistration-freeze-v1",
  "cycle":53,
  "parameters":{
    "target":{"kind":"expression","value":"Use left L_i and right R_j indexed by Z/5Z, with edge L_iR_j iff j-i is not 0 or -1 modulo 5; e(H)=15. Let U:[0,1]^2->[−1,1] be measurable, symmetric, and have integral zero. Put d_U(x)=integral U(x,y)dy and W_epsilon=1/2+epsilon U for 0<epsilon<=1/2.","rationale":"Fixes the graph, kernel class, density, and graphon feasibility convention."},
    "formula":{"kind":"expression","value":"Expand t_H(W_epsilon)-2^-15 by edge subsets. Prove or refute: its epsilon^2 coefficient equals 30*(1/2)^13*integral d_U(x)^2 dx. Conditional on d_U=0, its epsilon^3 coefficient vanishes and its epsilon^4 coefficient equals c4*(1/2)^11*trace(T_U^4), where c4 is the exactly enumerated number of 4-cycles in H and (T_U f)(x)=integral U(x,y)f(y)dy.","rationale":"Freezes the proposed analytic identity and exact coefficients, so an attractive but wrong local argument fails cleanly."},
    "theorem_rule":{"kind":"expression","value":"If the identities hold with c4>0, prove the directional statement: for every eligible nonzero U there exists delta(U)>0 such that t_H(1/2+epsilon U)>2^-15 for every 0<epsilon<min(delta(U),1/2). If d_U is nonzero use the positive quadratic leading coefficient; if d_U=0 use the positive quartic leading coefficient and the spectral fact trace(T_U^4)>0 for nonzero symmetric Hilbert-Schmidt U. Do not claim a uniform L-infinity neighborhood or Sidorenko.","rationale":"Uses only first-nonzero-coefficient positivity and correctly limits the scope."},
    "exact_checks":{"kind":"expression","value":"Independently enumerate every subset of the 15 frozen edges, its degree sequence, connected components, and cycle type. Verify pair counts, the absence of a minimum-degree-two 3-edge subset, and the 4-cycle count. Independently derive the pair coefficient by vertex incidence counting. Check the operator trace identity first for finite step kernels by exact index expansion, then state the Hilbert-Schmidt extension with hypotheses.","rationale":"Separates graph combinatorics from functional analysis and blocks a hidden coefficient or orientation error."},
    "falsifier":{"kind":"expression","value":"Any edge-subset count incompatible with the stated quadratic/kernel formulas, c4=0, a surviving cubic kernel term, a negative kernel quartic term, or an ineligible operator extension is ERROR. An explicit eligible U with negative first surviving coefficient is a counterexample candidate.","rationale":"Makes every critical bridge testable."},
    "claim_boundary":{"kind":"expression","value":"A successful result is a directional local-stability theorem at the single constant graphon p=1/2 for the stated symmetric zero-mean bounded kernels. It neither handles nonzero-mean directions, uniform neighborhoods, other densities, nor proves Sidorenko.","rationale":"Prevents local analysis from being promoted to the global conjecture."}
  },
  "resource_caps":{
    "worker_processes":{"kind":"integer","value":3,"rationale":"At most CPUs 0-2, reserving CPU 3."},
    "edge_subsets":{"kind":"integer","value":32768,"rationale":"Complete 2^15 exact graph-subset classification in each independent route."},
    "step_control_assignments":{"kind":"integer","value":59049,"rationale":"One q=3 exact trace-expansion control."},
    "aggregate_wall_seconds":{"kind":"integer","value":600,"rationale":"Small exact combinatorial proof audit."},
    "aggregate_peak_memory_mib":{"kind":"integer","value":512,"rationale":"Subset rows and exact controls."},
    "aggregate_temporary_disk_bytes":{"kind":"integer","value":1073741824,"rationale":"1 GiB under the pre-C52 measured available space, retaining the system reserve."}
  },
  "formula_families":["edge-subset homomorphism expansion","zero-degree kernel cancellation","Hilbert-Schmidt trace positivity","exact finite step-kernel trace control"],
  "selection_rule":["Classify every frozen edge subset; no sampled subgraphs.","Prove only the stated directional theorem if all checks pass.","Use no optimizer, numerical positivity, or unregistered extension to other densities."],
  "failure_rule":["Any mismatch is ERROR and blocks theorem promotion.","A valid negative kernel direction is contained as a counterexample candidate.","A pass closes this local mechanism and sends global search to a distinct engine."],
  "pre_execution":{"timestamp_utc":"2026-08-05T08:36:00Z","git_head":"29c098d7ee33e49049e4c4bea82c4155d190f6bf","git_state":"DIRTY with active project files untracked at repository level; C52 is sealed before this distinct analytic engine.","filesystem_observation_bytes":{"size":206900281344,"used":45677531136,"available":161205972992,"reserved":5368709120,"maximum_temporary_cap":155837263872,"chosen_temporary_cap":1073741824,"mount":"/"}},
  "input_paths":["artifacts/cycle-52-b052-sidorenko-local-variation-v1.json","discovery/cycle53_analytic_local_stability_idea_selection.md","../../tools/preregistration_check.py"]
}
-->

## Stop rule

Stop after the full edge-subset and operator checks establish the directional
theorem, produce a candidate, or reveal an error.  Do not turn this cycle into
a global extremizer search.
