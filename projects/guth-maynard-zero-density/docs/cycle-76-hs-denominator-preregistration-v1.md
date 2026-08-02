# Cycle 76 preregistration: Huxley--Sargos across denominators

## Question

Reverse Cycle 74: fix a numerator cell and apply the same checked order-three
near-integer theorem in the denominator variable. Determine the exact bound
after summing numerators and whether it closes any cell in the combined
Cycle-75 residual.

## Frozen setup

- `Y_a(q)=C log(1+a/q)` with `a=X^(alpha+o(1))` fixed and
  `q=X^(theta+o(1))` varying.
- On a dyadic block with `a<=q`, freeze
  `|Y_a'''(q)|asymp Delta*a/q^4`, of exponent
  `3/5+alpha-4theta`.
- The vertical tube exponent remains `-2/5-theta-kappa`.
- Use the Cycle-47 order-three theorem with denominator length `X^theta`,
  take the minimum with the trivial `X^theta` count, then sum
  `X^alpha` numerators.
- Compare against both Cycle 75's banked exponent
  `B=min(lambda,theta+w)` and the strict packet target `6/25-kappa`.

## Outcomes

- `HS_DENOMINATOR_WEDGE`: derive the exact piecewise exponent and exhibit a
  Cycle-75-live cell closed strictly by the denominator estimate.
- `NO_NEW_CELL`: the estimate never improves the combined banked bound on the
  registered atlas.

Any search is restricted to rational grids with denominators at most `300`
and is only `OBSERVED`; the promoted conclusion must follow from an exact
symbolic inequality and a rational witness.

No full denominator-average theorem, seed extraction, powered saving,
density gain, or interval gain is asserted by either outcome.
