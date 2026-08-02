# Cycle 80 preregistration: phase occupancy and clustered large sieve

## Question

Bound a nontrivial high-frequency portion of the Cycle-79 Fourier contract
directly in the primal variables, without using an unproved stationary
remainder expansion.

## Frozen setup

- On `k=X^(xi+o(1))`, use points
  `x_d=k c_0 exp(2pi d/Delta) mod 1`, `d~Delta`.
- Define `A_k` as the maximum number of `x_d` in any circular interval of
  length `O(1/Q)`.
- Apply the checked Cycle-47 order-three theorem uniformly in the interval
  center; the third derivative has exponent `xi-9/5` and the tube exponent
  is `-1/3`.
- Use a clustered large-sieve/Schur bound with local occupancy `A_k`, then
  Cauchy over `q~Q`.
- Compare each dyadic `k` block with the raw Fourier target `31/25`.

## Outcomes

- `PHASE_OCCUPANCY_BAND`: prove a uniform occupancy exponent and close a
  strict band beyond the Cycle-79 trivial cutoff `4/15`.
- `NO_NEW_BAND`: the checked occupancy and large-sieve exponents do not beat
  `31/25` beyond `4/15`.

No full high-frequency bound, ACSI, packet closure, powered saving, density
gain, or interval gain is asserted by a regional band.
