# Cycle 3 G1 route decision v2 correction

## Claim boundary

`OBSERVED`: the corrected adjudicator closes only the sealed zero-retained
branch and records `NO_SELECTION`. It is not a theorem, asymptotic
obstruction, saturation result, density improvement, or refutation of P2A,
P2B, or P2C.

## Correction

The preserved v1 artifact reached the correct result for the actual
zero-retained evidence, but its counterfactual affirmative predicates were
incomplete: any retained row would have acted as a proxy for route-specific
trace, energy/affine, and propagation evidence. V1 also failed to bind the
adjudicator executable in its output artifact. The hostile audit therefore
records `FAIL_ROUTE_PREDICATE_COMPLETENESS`, and v1 is not an authority for
promotion.

V2 is intentionally no-selection-only. It requires exactly zero retained and
zero validation rows, sets every route selection to false, records its own
path and SHA-256, and fails closed if a positive row appears. A future
affirmative route decision needs separately sealed, labeled evidence for the
exact frozen feature predicate; this package cannot make one.

## Evidence and decision

- `PROVED`: the exact atlas has 7,744 local rows and 560 transfer rows, and
  LV3 is the zero-residual critical transfer term, conditional on the checked
  published formulas.
- `OBSERVED`: both fresh empirical runs reconcile byte-for-byte on 588 rows:
  429 completed, 159 failed, zero retained, and zero validated.
- `CERTIFIED_NUMERICAL`: 434 feasible finite energy rows have zero
  energy-retention-eligible rows at the frozen finite scale. This is not an
  asymptotic obstruction.
- `OBSERVED`: P2A, P2B, P2C, and their combination are `NOT_SELECTED`, not
  refuted. G1 closes as `NO_SELECTION`.

## Replay

```sh
cd /root/projects/maph/projects/guth-maynard-zero-density
python3 proof/adjudicate_g1_route_selection_v2.py \
  --check artifacts/cycle-3-g1-route-decision-v2.json
python3 -m unittest tests/test_g1_route_selection_v2.py -v
```
