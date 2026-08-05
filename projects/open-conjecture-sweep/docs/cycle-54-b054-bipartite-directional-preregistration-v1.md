# Cycle 54 / B054 preregistration: full bipartite directional theorem

## Decision question

Does C53's directional local-stability theorem extend from symmetric kernels
to every bounded nonzero zero-mean bipartite kernel, at every fixed
\(p\in(0,1)\)?

<!-- research-freeze-v1
{
  "schema":"research-preregistration-freeze-v1",
  "cycle":54,
  "parameters":{
    "target":{"kind":"expression","value":"Use the frozen 15-edge Möbius graph H. Let U:X times Y -> [−1,1] be measurable, nonzero in L2, and have integral zero, with left degree a(x)=integral_Y U(x,y)dy and right degree b(y)=integral_X U(x,y)dx. For fixed p in (0,1), W_epsilon=p+epsilon U is admissible for 0<epsilon<min(p,1-p).","rationale":"Fixes the bipartite kernel setting and graphon feasibility."},
    "formula":{"kind":"expression","value":"Prove or refute that the epsilon^2 coefficient is 15*p^13*(||a||_2^2+||b||_2^2). Conditional on a=b=0, prove the epsilon^3 coefficient is zero and the epsilon^4 coefficient is 5*p^11*tr((T_U T_U*)^2), positive for U nonzero, where T_U:L2(Y)->L2(X).","rationale":"Freezes the nonsymmetric analytic extension and all numerical graph coefficients."},
    "theorem_rule":{"kind":"expression","value":"If the identities hold, prove: for every fixed p in (0,1) and every eligible U, there exists delta(p,U)>0 such that t_H(p+epsilon U)>p^15 for 0<epsilon<min(delta(p,U),p,1-p). Do not claim uniformity over U or p, global Sidorenko, or a symmetric-graphon extremizer theorem.","rationale":"States the maximum justified directional conclusion."},
    "exact_checks":{"kind":"expression","value":"Reuse C53's independently sealed complete edge-subset classification only as frozen input. Independently derive the 15+15 incidence split and the two-sided leaf cancellation. Verify the rectangular four-cycle identity by a finite rational nonsymmetric matrix control and singular-value/trace algebra.","rationale":"Tests the new nonsymmetric bridge rather than relabeling C53."},
    "falsifier":{"kind":"expression","value":"An omitted two-sided degree term, surviving cubic leafless term, nonpositive rectangular C4 expression for nonzero U, invalid Hilbert-Schmidt/singular-value step, or failed rational matrix control is ERROR. A negative eligible direction is a counterexample candidate.","rationale":"Makes the extension falsifiable."},
    "claim_boundary":{"kind":"expression","value":"Success proves directional local positivity in the bipartite graphon setting at any fixed p, for the stated kernels. It supplies no uniform neighborhood, no global minimizer reduction, and no proof of Sidorenko.","rationale":"Maintains the local/global boundary."}
  },
  "resource_caps":{"worker_processes":{"kind":"integer","value":3,"rationale":"At most CPUs 0-2, reserve CPU 3."},"matrix_control_dimensions":{"kind":"integer","value":4,"rationale":"One frozen rectangular exact matrix control up to 4 by 4."},"aggregate_wall_seconds":{"kind":"integer","value":300,"rationale":"Analytic theorem audit only."},"aggregate_peak_memory_mib":{"kind":"integer","value":256,"rationale":"Small rational matrices."},"aggregate_temporary_disk_bytes":{"kind":"integer","value":1073741824,"rationale":"1 GiB under the prior free-space measurement and reserve."}},
  "formula_families":["bipartite edge-subset expansion","two-sided leaf cancellation","singular-value C4 positivity","exact rectangular matrix control"],
  "selection_rule":["Use the C53 subset census only for its stated graph combinatorics.","Prove only the frozen directional theorem.","Do not introduce a global optimizer or unregistered density extension."],
  "failure_rule":["Any analytic or control mismatch blocks promotion.","A valid negative direction is contained as a candidate.","A pass closes this local engine and requires a distinct nonlocal question."],
  "pre_execution":{"timestamp_utc":"2026-08-05T08:47:00Z","git_head":"29c098d7ee33e49049e4c4bea82c4155d190f6bf","git_state":"DIRTY with active project files untracked at repository level; C53 is sealed before this distinct bipartite extension.","filesystem_observation_bytes":{"size":206900281344,"used":45677531136,"available":161205972992,"reserved":5368709120,"maximum_temporary_cap":155837263872,"chosen_temporary_cap":1073741824,"mount":"/"}},
  "input_paths":["artifacts/cycle-53-b053-analytic-local-stability-v1.json","discovery/cycle54_bipartite_directional_idea_selection.md","../../tools/preregistration_check.py"]
}
-->

## Stop rule

Stop after the rectangular operator bridge and exact control prove the stated
theorem, yield a candidate, or fail. Do not convert C54 into a global search.
