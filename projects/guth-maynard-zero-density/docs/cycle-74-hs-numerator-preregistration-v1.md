# Cycle 74 preregistration: Huxley--Sargos on numerator cells

## Question

Apply the checked order-three Huxley--Sargos near-integer theorem to the
numerator variable on each Cycle-73 cell. Determine its exact piecewise count
and whether it closes cells not already closed by the raw numerator budget.

## Frozen setup

- `y_q(a)=(Delta/(2pi))log(1+a/q)` on `a=X^(alpha+o(1))`,
  `q=X^(theta+o(1))`.
- `|y_q^(3)(a)|asymp Delta/q^3` on every fixed-ratio dyadic cell.
- The vertical tube has exponent `-2/5-theta-kappa`.
- Sum the fixed-`q` result over `X^(theta+o(1))` denominators.
- Compare with packet target `6/25-kappa` and retain strict inequalities.

## Outcomes

- `HS_NUMERATOR_WEDGE`: derive the piecewise exponent and exhibit at least
  one cell which ties or fails the raw fraction budget but closes strictly.
- `NO_NEW_CELL`: the checked theorem gives no closure beyond Cycle 73.

No full residual-atlas theorem, recurrence theorem, powered saving, density
gain, or interval gain is asserted by `HS_NUMERATOR_WEDGE`.
