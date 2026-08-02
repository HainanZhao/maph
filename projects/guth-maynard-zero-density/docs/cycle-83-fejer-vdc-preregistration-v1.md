# Cycle 83 preregistration: fixed-center Fejer--VdC band

## Claim boundary

This cycle tests only a fixed-center resonance estimate and its Fourier-band
consequence.  It will not claim `xi=37/75`, higher frequencies, packet
closure, density gain, or interval gain.

## Frozen inputs

- `D=X^(3/5+o(1))`, `Q=X^(1/3+o(1))`.
- Active input range `94/225<=xi<37/75`.
- Phase `f_j(d)=jkc0 exp(2pi d/D)` on a fixed smooth dyadic `d` support.
- Fejer bandwidth is exactly `H` comparable to `Q`; no post-result tuning.
- For a dyadic projector annulus of radius `L/Q`, use bandwidth `H~Q/L`
  and sum only after multiplying by a frozen Schwartz decay `L^-A`, with
  fixed `A>4`.
- The second-derivative estimate is used in the form
  `sum_(d~D)e(f_j(d)) << sqrt(jk)+D/sqrt(jk)` when
  `|f_j''|asymp jk/D^2` and has fixed sign.

## Frozen gates

The cycle passes only if:

1. the Fejer majorant yields
   `R_k<<D/Q+Q^-1 sum_(j<=Q)|E_j|`;
2. all second-derivative hypotheses hold uniformly for `j<=Q` on the stated
   range, including `jk/D^2<1`;
3. summation gives
   `R_k<<D/Q+sqrt(kQ)+D/sqrt(kQ)`;
4. `sqrt(kQ)` dominates on the full active range;
5. the dyadic annular projector sum has the same power exponent as the
   central resonance count;
6. the block exponent is `3xi/2+1/2`;
7. the strict cutoff is `37/75`, the new width is `17/225`, and the endpoint
   is recorded as a tie.

## Verification plan

- Pin every rational comparison in `conventions/fejer_vdc_resonance_v1.py`.
- Test the derivative range, three resonance terms, dominance, strict cutoff,
  and width independently.
- Seal against Cycles 81 and 82.  Record the local Guth--Maynard use of the
  classical first/second derivative bounds as the checked source context.
- Defer hostile audit until paper-stage promotion.
