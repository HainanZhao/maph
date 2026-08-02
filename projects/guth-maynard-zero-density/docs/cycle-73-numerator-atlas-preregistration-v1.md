# Cycle 73 preregistration: numerator-resolved packet atlas

## Question

Dyadically retain the positive numerator scale `a=X^(alpha+o(1))`. Determine
the resulting fraction-budget closure region, its relation to the curve-index
scale, and the cellwise factored-Hessian loss.

## Frozen setup

- `q=X^(theta+o(1))`, `K=X^(kappa+o(1))`,
  `a=X^(alpha+o(1))`, with `0<=alpha<=theta`.
- Packet accuracy and the small-proportion exponential curve give
  `a asymp q ell/Delta` on a fixed dyadic cell.
- The packet target is exponent strictly below `6/25-kappa`.
- The factored Hessian is `exp(4pi ell/Delta)-1`.

## Outcomes

- `NUMERATOR_ATLAS`: derive the cell count, strict closed region, exact
  `alpha`--`lambda` relation, and cellwise curvature loss.
- `NO_NUMERATOR_GAIN`: resolving `a` does not improve the coarse `Q^2`
  fraction budget or the `X^theta` curvature loss.

No boundary closure, two-variable sum, full packet theorem, recurrence
theorem, powered saving, density gain, or interval gain is asserted.
