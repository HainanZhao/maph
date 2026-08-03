# Cycle 230 / B067 preregistration: `F3^2` divisor coboundary

Cycle 229 proves an order-four residual pole at `mu=0`. This block tests
whether a permitted argument-dependent divisor cochain can absorb it.

<!-- research-freeze-v1
{"schema":"research-preregistration-freeze-v1","cycle":230,
"parameters":{"action":{"kind":"expression","value":"Freeze the positive m=0 F3^2 action (mu,omega1,omega2)->(576*mu,576*omega1,576*omega2) at raw starts A,C, and its fixed divisor mu=0.","rationale":"C227 supplies the only source-defined product-node return."},"module":{"kind":"expression","value":"Use the free integer divisor module on the exact residual pole/zero lattice families. Admit a cochain only as a meromorphic divisor D with finite valuation at mu=0; its coboundary is D(action(x))-D(x).","rationale":"This tests the necessary divisor condition before any infinite product."},"acceptance":{"kind":"expression","value":"Accept only an exact solution or fixed-point valuation obstruction for the residual divisor. Do not construct a function from a divisor solution, use a negative-k path, or claim a signed extension.","rationale":"Divisor solvability is necessary, not sufficient."}},
"resource_caps":{"starts":{"kind":"integer","value":2,"rationale":"A,C."},"fixed_point_valuations":{"kind":"integer","value":2,"rationale":"One per block."},"divisor_coefficients":{"kind":"integer","value":1,"rationale":"Residual order four."},"floating_point":{"kind":"not_applicable","justification":"Exact valuations only.","rationale":"No numerical products."},"wall_seconds":{"kind":"integer","value":180,"rationale":"Finite valuation obstruction."}},
"formula_families":["Cycle-227 F3^2 positive scaling","Cycle-229 residual divisor","divisor coboundary equation"],
"selection_rule":["Test both starts at the fixed divisor first.","Keep solution and function-realization claims separate."],
"failure_rule":["Do not bypass fixed-point valuation with an infinite product or a fitted singular cochain.","Do not claim AFK covariance, fusion, Stark, or TCC."],
"pre_execution":{"timestamp_utc":"2026-08-03T11:10:00Z","git_head":"e994ad32163256c711d20ac264206b97e2f47a97","git_state":"Dirty only from concurrent repository-wide PROGRAM migration and unrelated work."},
"input_paths":["artifacts/cycle-229-b066-f3-square-divisor-v1.json","proof/verify_cycle_229_f3_square_divisor.py","artifacts/cycle-227-b064-augmented-transport-normal-forms-v1.json","../../tools/preregistration_check.py"]}
-->
