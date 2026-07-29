# Workstream-D human decision brief

Status: **CANCELLED_BY_USER.** No Workstream-D decision or experiment
is required.

The production directive requires an explicit choice before application
scoping.  No Workstream-D experiment may begin from this brief alone.

## Option 1 — public benchmark

Use a fully redistributable, version-pinned pricing/UQ integrand with a
documented smoothing or preintegration step.  Advantages:

- the complete pipeline, inputs, and randomized-shift transcript can
  ship with the engine;
- reviewers can replay the function-space and empirical boundaries;
- no proprietary model or data license enters the artifact; and
- the benchmark can become an example for the compact oracle and
  selected-entry verifier.

The limitation is external validity: a clean public integrand may not
represent the discontinuities, calibration choices, and operational
constraints of an internal pricing stack.

## Option 2 — internal pricing-stack integrand

Use a production-relevant internal payoff/risk aggregation family.
Advantages:

- direct evidence about integration cost and variance in the intended
  environment; and
- a realistic test of the smoothing and function-space claim boundary.

The limitations are reproducibility and scope.  The project would need
the precise transformation, model/discretization inputs, smoothing
code, license/confidentiality disposition, and a publishable surrogate
if the primary workload cannot ship.  Absence of any one item weakens
the public artifact and may leave only an internal report.

## Recommendation

Default to the public benchmark unless a concrete internal integrand
and its transformation/provenance package are already available.  This
recommendation does not authorize the choice; the human decision must
be recorded prospectively in `data/workstream-d-decision.json`.

Either path retains the same claim boundary:

- rule merit: exact or enclosed;
- RKHS inequality: stated separately;
- integrand membership and norm: proved, bounded, or explicitly
  empirical;
- smoothing/preintegration error: separately labeled;
- randomized-shift interval: statistical;
- model/discretization error: outside the rule-merit certificate; and
- no “certified price” wording without certification of every factor.
