# Cycle 229 / B066 preregistration: `F3^2` residual divisors

Cycle 228 leaves the two label-zero `F3^2` ordinary-gamma residual products
unreduced. This block decides whether either has an exact uncancelled divisor.

<!-- research-freeze-v1
{"schema":"research-preregistration-freeze-v1","cycle":229,
"parameters":{"blocks":{"kind":"expression","value":"Freeze the A and C m=0 F3^2 four-factor blocks from Cycle 228, in source order and with their exact argument and period triples.","rationale":"No other paths or labels are in scope."},"divisors":{"kind":"expression","value":"For gamma(z;alpha,beta), freeze poles z=-j*alpha-n*beta and zeros z=(j+1)*alpha+(n+1)*beta for j,n>=0. Pull each family back to the initial (mu,omega1,omega2) coordinates and compare complete families symbolically.","rationale":"An uncancelled lattice family proves non-scalarity without numerical sampling."},"acceptance":{"kind":"expression","value":"Accept only an exact family witness with its multiplicity and proof that no opposite divisor family cancels it. Complete cancellation must be displayed family-by-family. Do not infer a divisor result from finite enumeration.","rationale":"The result is an analytic invariant, not a search hit."}},
"resource_caps":{"blocks":{"kind":"integer","value":2,"rationale":"A,C only."},"factors":{"kind":"integer","value":8,"rationale":"Four per block."},"divisor_types":{"kind":"integer","value":2,"rationale":"Poles and zeros."},"family_comparisons":{"kind":"integer","value":64,"rationale":"Ordered factor/type comparisons."},"floating_point":{"kind":"not_applicable","justification":"Exact lattice algebra only.","rationale":"No numerical witness."},"wall_seconds":{"kind":"integer","value":300,"rationale":"Symbolic family analysis."}},
"formula_families":["ordinary hyperbolic-gamma product definition and divisor lattices","Cycle-228 exact residual factors"],
"selection_rule":["Compare all frozen divisor families, including within one block.","Record multiplicity and any cancellation map exactly."],
"failure_rule":["Do not truncate a lattice, use a numerical value, alter bases, or call a surviving divisor a signed extension.","Do not claim AFK covariance, fusion, Stark, or TCC."],
"pre_execution":{"timestamp_utc":"2026-08-03T10:45:00Z","git_head":"eb17af5e3047a560361ced31f55d0dea62b35b5d","git_state":"Dirty only from concurrent repository-wide PROGRAM migration and unrelated work."},
"input_paths":["artifacts/cycle-228-b065-f3-square-residual-block-v1.json","proof/verify_cycle_228_f3_square_residual_block.py","paper/sic-stark-dimension-six-boundary-fusion.tex","../../tools/preregistration_check.py"]}
-->
