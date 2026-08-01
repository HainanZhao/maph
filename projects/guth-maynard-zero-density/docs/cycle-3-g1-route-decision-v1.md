# Cycle 3 G1 route decision v1

## Claim boundary

`OBSERVED`: literal application of the frozen G1 clauses to the sealed exact,
certified finite-energy, and two-fresh-run empirical evidence gives
`NO_SELECTION`. This is a bounded program decision. It is not a theorem,
asymptotic obstruction, saturation result, density improvement, or refutation
of P2A, P2B, or P2C.

## Decision

- P2A is not selected: no retained row isolates a trace feature absent from
  the cubic terms.
- P2B is not selected: no retained row establishes a consistent energy/affine
  obstruction. The `CERTIFIED_NUMERICAL` finite energy result is not an
  asymptotic classification.
- P2C is not selected: the `PROVED` exact transfer map names LV3 as the
  zero-residual term, but no retained local candidate exists to propagate.
- No combination is selected because no constituent route has separate
  affirmative evidence.

`OBSERVED`: the empirical record accounts for all 588 rows: 429 completed and
159 failed (154 infeasible-cardinality and five nonpositive-value failures),
with zero retained and zero validation rows. Separately,
`CERTIFIED_NUMERICAL`: all 434 feasible finite energy rows fail the energy half
of retention by a positive exact margin. These are different predicates and
their counts must not be conflated.

Rejected means “not selected from this frozen atlas,” not “refuted.” A new
`PLAN.md`-authorized preregistration is required before replacement screening
or any P2 theorem search.

## Replay

```sh
cd /root/projects/maph/projects/guth-maynard-zero-density
python3 proof/adjudicate_g1_route_selection_v1.py \
  --check artifacts/cycle-3-g1-route-decision-v1.json
python3 -m unittest tests/test_g1_route_selection_v1.py -v
```
