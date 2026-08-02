# Cycle 72 preregistration: primitive positive-numerator cutoff

## Question

Use the reduced numerator label, not only packet injectivity, to sharpen the
small-`ell` endpoint and the Cycle-70 Hessian loss.

## Frozen setup

- `alpha_ell=exp(2pi ell/Delta)-1>0`.
- A primitive packet satisfies `(a,q)=1`, `q>1`, and
  `|q alpha_ell-a|<=C/(KX)=o(1)`.
- On the fixed small-proportion curve range,
  `alpha_ell asymp ell/Delta`.
- At stationarity,
  `det Hess_(r,q')=exp(4pi ell/Delta)-1`.

## Outcomes

- `POSITIVE_NUMERATOR_CUTOFF`: prove `a>=1`, derive
  `ell>>Delta/q`, and sharpen the determinant-loss exponent.
- `ZERO_NUMERATOR_SURVIVES`: a primitive packet with `q>1` may have `a=0`.

The exceptional denominator `q=1` is retained separately. No two-variable
sum, full packet, recurrence, powered, density, or interval gain is asserted.
