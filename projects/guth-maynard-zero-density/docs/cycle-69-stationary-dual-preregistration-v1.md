# Cycle 69 preregistration: stationary dual of the folded transport phase

## Question

Apply Poisson summation in the curve index to the folded phase
`m(exp(2pi ell/Delta)-1)`. Compute the stationary Legendre phase, its
curvature, stationary-index range, and the exact relation to the critical
`21/25` skeleton scale.

## Frozen setup

- Smooth the fixed-proportion `ell` interval at constant cost and put
  `x=ell/Delta`.
- The folded frequency satisfies `1<=m<=X^(36/25+o(1))`.
- Fourier convention is `e(x)=exp(2pi i x)`.
- No stationary-phase remainder estimate or cancellation theorem is asserted
  unless derived explicitly.

## Outcomes

- `STATIONARY_DUAL`: derive the stationary point and phase, compute its full
  Hessian determinant, and derive the maximum dual-index exponent.
- `NO_STATIONARY_RANGE`: the proposed Poisson dual has no stationary regime
  on the registered scales.

No bound for the primitive Poisson form, packet theorem, recurrence theorem,
powered saving, density gain, or interval gain is asserted by
`STATIONARY_DUAL`.
