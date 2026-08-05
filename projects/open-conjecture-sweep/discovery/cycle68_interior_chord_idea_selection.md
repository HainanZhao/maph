# C68 creative idea selection: interior fiber control

## Candidate mechanisms

1. **Piecewise rational `u`-chord remainder.**  Put
   `r2=6*t^2*z^2`, so the upper endpoint is `u+=2*t^3*z^3`.  The lower
   endpoint is `-u+` for `0<=z<=1/2` and `t^3*(3*z^2-1)` for
   `1/2<=z<=1`.  On each polynomial chart, subtract the chord between the
   two endpoint values and divide exactly by `lambda*(1-lambda)`.  Global
   `u`-concavity (`P_uu<=0`) is a cheaper sufficient subtest, not an
   assumption.
2. **Exact resultant/Sturm exclusion.**  Isolate every feasible solution of
   `P_u=P_s2=0` uniformly over the outer domain, then certify its value.  This
   is decisive but begins with the full degree-26 branch geometry.
3. **Invariant SOS around the C67 zero curves.**  Search for a global Gram or
   quadratic-module identity suggested by the repeated squared equality
   factors.  This may explain C67 structurally but has no pinned finite ansatz.
4. **Two-coordinate minimum principle.**  Seek separate concavity or a
   maximum-principle operator in both `u` and `s2`.  This is stronger than
   necessary and the degree-seven `s2` direction is the less favorable first
   coordinate.

## Questioning the questions

Why ask about a chord now?  C67 proves every fiber edge, while C64 fixes a
rectangle in `(u,s2)` and gives `deg_u(P)=5`; a chord in `u` uses the new edge
theorem directly and reduces the interior question to one explicit remainder.
Why not ask only for concavity?  Concavity may fail although the chord
remainder stays nonnegative, so a negative `P_uu` sign is an advance but a
positive `P_uu` point rejects only the shortcut.  Why not eliminate critical
points immediately?  The resultant is uniform but leaves a three-dimensional
outer sign problem and has much higher cost.  What framing could be wrong?
Endpoint positivity does not control an interior minimum without the chord
inequality; convexity would point in the wrong direction.  The fiber is
two-dimensional, so the chord must be asserted at every fixed `s2`, not only
on a selected slice.

## Selection

Select the piecewise rational `u`-chord remainder.  The main rejected
alternative is immediate resultant/Sturm exclusion because its cost is high
before testing the exact degree-five leverage.  The engine falsifier is one
exact feasible point with negative chord remainder.  The target falsifier is
one exact feasible interior point with `P<0`; it would refute the fixed-`S3`
comparison.  A negative chord remainder with nonnegative `P` rejects only this
engine and authorizes the resultant fallback.
