# Cycle 85 preregistration: logarithmic crossing occupancy

## Claim boundary

This cycle tests whether the checked order-three near-integer theorem removes
the Cycle-84 crossing-discretization gap throughout
`43/75<=xi<16/25`.  It will not claim the endpoint, frequencies above
`16/25`, signed cancellation, packet closure, density gain, or interval gain.

## Frozen ranges and theorem specialization

- `D=X^(3/5+o(1))`, `Q=X^(1/3+o(1))`, `K=X^(xi+o(1))`.
- `43/75<=xi<16/25`, and dyadic Fejer frequency
  `j=X^(nu+o(1))`, `0<=nu<=1/3`.
- Crossing curve `g_j(r)=(D/(2pi))log(r/(j c0))`, `r~j`.
- Vertical tolerance `delta=D/(jK)`.
- Use exactly the Cycle-47 order-three Huxley--Sargos formula, with the
  trivial count minimum and no post-result derivative-order search.
- Projector annuli use the frozen Cycle-84 Fejer bandwidth and Schwartz power
  five.

## Frozen gates

The cycle passes only if:

1. occupied crossings imply `||g_j(r)||<<D/(jK)` with uniform constants;
2. the derivative, tube, ratio, and constant exponents are exactly those in
   the discovery candidate;
3. for every active `(xi,nu)`, the derivative term dominates the other
   Huxley--Sargos terms;
4. after the trivial minimum, the crossing exponent is
   `min(nu,1/10+nu/2)`;
5. `nu+crossing_exponent` is maximized at `nu=1/3` with value `3/5`;
6. annular losses are absorbed by the frozen Schwartz decay;
7. the strict cutoff is `16/25`, the added width is `1/15`, and equality is
   recorded as a tie;
8. the result is explicitly marked as the limit of unsigned incidence, not a
   bound for higher frequencies.

## Verification plan

- Encode the full two-parameter comparisons in
  `conventions/log_crossing_occupancy_v1.py`.
- Test all corners and symbolic dominance differences, not a sampled grid.
- Seal against Cycles 47 and 84 with deterministic hashes.
- Keep hostile audit deferred to paper stage.

