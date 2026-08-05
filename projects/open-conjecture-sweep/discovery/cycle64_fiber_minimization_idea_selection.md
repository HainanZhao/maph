# C64 idea selection: minimize the exact shape fiber, not a stronger surrogate

## Serious candidates

1. **Exact fiberwise invariant minimization (chosen).** Fix
   `(e,t,c,r2)`.  C63 makes the remaining feasible set
   `0<=s2<=c^2` and
   `max(t*r2/2-t^3,-sqrt(r2^3/54)) <= u <= sqrt(r2^3/54)`.
   The deficit has degrees at most five in `u` and seven in `s2`.
   Derive all boundary restrictions and the interior equations
   `P_u=P_s2=0`, then use exact gcd/subresultant/Sturm tools to decide
   whether fiber minima reduce to explicit boundary strata or finitely
   certifiable branches.
2. **Separate Schur-convexity.** Prove both exchange factors nonnegative, so
   successive class averaging reaches the central point.  This is retained as
   a falsifiable diagnostic but rejected as the primary target: it is stronger
   than `P>=0`, and C62's mixed quotients provide no structural reason it must
   hold.
3. **Saturated full stationary Groebner basis.** Add inverse variables for all
   generic-stratum factors and rerun the six-variable ideal.  Rejected as the
   first move because C63 spent its 300-second tranche on degree growth before
   producing a basis; the two-variable fiber structure should be exploited
   first.
4. **Adaptive Bernstein subdivision or another dense census.** Rejected at
   this gate.  Without first locating the exact fiber critical branches, it
   risks becoming another certificate ladder that cannot distinguish a narrow
   algebraic minimum from a boundary zero.

## Questioning the question

Why should fixing four variables help?  It is useful only because the two
remaining inequalities decouple: the cycle coordinate is an interval and the
transposition cubic invariant has two explicit algebraic endpoints.  This
makes every fiber minimum either a named endpoint or a common zero of two
low-degree derivatives.  The outer variables remain difficult, so merely
showing a generic fiber is finite is not closure; exceptional outer loci and
the signs of every feasible branch must remain visible.

Why not prove monotonicity in `s2`, given 300,000 positive exchange probes?
Those probes are `OBSERVED`, and monotonicity is stronger than the target.
Assuming it would reproduce the framing error that C63 was designed to avoid.
The exact derivative is tested, but interior critical branches receive equal
standing.

Why now?  C63 has already paid for the full orbit conversion and showed that
orientation coupling disappears.  A full Groebner calculation ignored the
resulting fibration and hit its wall cap.  The rejected alternative most likely
to obscure the problem is another global cone search.

## Chosen question, falsifiers, and stop rule

Can every feasible `(u,s2)` fiber minimum be reduced exactly to the
discriminant, root-zero, cycle-equality, or cycle-support boundaries, or to a
finite set of certified interior algebraic branches whose deficit signs can be
decided uniformly in the outer variables?

- An exact feasible invariant tuple with negative deficit, reconstructed as a
  nonnegative S3 function, falsifies S3 Zhao comparison.
- An exact feasible interior fiber minimum below every named boundary
  falsifies the boundary-only engine even when its deficit is nonnegative.
- A strict exchange reversal falsifies only the stronger Schur route.
- If one bounded fiber-minimization cycle yields no reusable reduction, pause
  this S3 route instead of opening another cone, census, or exception ladder.
