# Cycle 70 preregistration: curvature after unfurling `m=rq'`

## Question

Test whether the stationary Hessian degeneracy of Cycle 69 is caused by
collapsing the product frequency. Compute the Hessian in the factored
variables `(r,q')`, isolate its degenerate endpoint, and compare that endpoint
with the packet-count target.

## Frozen setup

- `m=rq'` in the Cycle-66 primitive Poisson form.
- The stationary phase is `Psi(m,k)=u-m-u log(u/m)`,
  `u=kDelta/(2pi)`, with stationary ratio `u/m=exp(2pi x)` and
  `x=ell/Delta`.
- On a dyadic `ell` block `L=X^(lambda+o(1))`, uniqueness gives at most `L`
  primitive packets.
- The packet-count target is exponent strictly below `6/25-kappa`.

## Outcomes

- `UNFURLED_CURVATURE`: compute `det Hess_(r,q') Psi(rq',k)` exactly,
  identify the automatically subcritical small-`ell` range, and quantify the
  weakest curvature on the remaining range.
- `DEGENERACY_PERSISTS`: the factored Hessian remains identically zero.

No exponential-sum estimate, packet theorem beyond the registered trivial
small-block bound, recurrence theorem, powered saving, density gain, or
interval gain is asserted by `UNFURLED_CURVATURE`.
