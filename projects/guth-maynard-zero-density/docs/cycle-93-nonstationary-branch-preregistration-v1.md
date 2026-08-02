# Cycle 93 preregistration: sub-alias nonstationary closure

## Claim boundary

This cycle may prove that the strict sub-alias branch of the Cycle-87 signed
second moment is power-negligible under fixed smooth cutoffs. It may not
include the transition `|Delta h|~K/D`, the stationary integer-alias branch,
the unresolved equal-height analytic branch, a full moment theorem, or a
density/interval gain.

## Frozen conventions and branch

- `e(x)=exp(2pi i x)`, `t=D Delta h/(2pi)`.
- `k~K`, with a fixed `C_c^infinity((0,infinity))` weight supported in
  `c_0<=k/K<=c_1`.
- `Delta h` is a nonzero integer and
  `0<|Delta h|<=c_* K/D`, where the fixed constant is chosen so that
  `|t|/(Kc_0)<=1/4`.
- Poisson integer is `m`, and after `k=Kx` the phase is
  `t log(Kx)-mKx`.

## Frozen gates

1. For `m=0`, verify derivative `t/x` and lower bound `>>D` from
   `|Delta h|>=1`.
2. For `m!=0`, verify derivative `t/x-mK` and lower bound
   `>>(1+|m|)K` after separating `|m|=1` from the tail.
3. Repeated integration by parts must give, for every fixed `A`, a total
   smoothed `k` kernel `O_A(KD^-A)` uniformly in the branch.
4. Charge the complete polynomial number of `(h,h',r,r')` support cells and
   verify that choosing `A` after the frozen support exponents makes the full
   branch `O_B(X^-B)` for every fixed `B`.
5. Keep the transition region and all stationary aliases explicitly open.

## Failure rule

A derivative lower bound depending on an unregistered endpoint buffer, a
nonzero stationary Poisson integer, or a remainder that cannot absorb the
full support count halts the cycle.

