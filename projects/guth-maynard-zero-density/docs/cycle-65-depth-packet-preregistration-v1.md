# Cycle 65 preregistration: depth-refined logarithmic packets

## Question

Refine Cycle 64 by retaining how many multiples of a primitive rational
packet are genuine hits. Determine the exact dyadic count target and whether
the low-denominator threshold matches an existing recurrence scale.

## Frozen setup

- `Delta=X^(3/5)` and `H=X^(11/25)`.
- `alpha_ell=exp(2pi ell/Delta)-1`.
- A primitive packet is `(ell,a/q)` with `(a,q)=1`, and its depth is
  `K=min(floor(H/q),floor(C/(X*|q alpha_ell-a|)))`, with the second term
  interpreted as infinity when the error is zero.
- A packet of depth `K` contributes
  `W=sum_(k<=K)(H-kq)` to the beta-free pair census.
- Dyadic scales are `q=X^(theta+o(1))`, `K=X^(kappa+o(1))`.
- The strict pair-census target is exponent below `17/25`.

## Outcomes

- `DEPTH_LEDGER`: derive the packet weight, the admissible region for
  `(theta,kappa)`, and the packet-count exponent sufficient on every dyadic
  scale. Identify exactly when one packet can meet or exceed the target.
- `NO_DEPTH_REFINEMENT`: depth does not improve the Cycle-64 harmonic-mass
  reduction or does not connect to a frozen recurrence threshold.

No packet discrepancy theorem, recurrence theorem, powered saving, density
gain, or interval gain is asserted by `DEPTH_LEDGER`.
