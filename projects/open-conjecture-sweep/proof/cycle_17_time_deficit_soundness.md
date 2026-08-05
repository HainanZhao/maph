# Cycle 17: exact weighted time-deficit certificates

Fix a base and one canonical gcd-witness leaf.  Let (A_i) be the lift
digits still allowed at coordinate (i).  For every denominator time (t),
let (b_{i,d,t}) be one exactly when the positive choice literal (x(i,d))
occurs in the frozen time-coverage clause for (t).

For any finitely supported nonnegative integer weights (w_t), put

\[
  W=\sum_t w_t,
  \qquad
  U=\sum_i\max_{d\in A_i}\sum_t w_t b_{i,d,t}.
\]

If a selection (d_i\in A_i) covers every time, then each time clause has at
least one selected literal.  Counting with weights gives

\[
  W\le \sum_i\sum_t w_t b_{i,d_i,t}\le U.
\]

Consequently (U<W) is an exact contradiction and certifies the leaf as
UNSAT using only its canonical units, its exactly-one coordinate choices, and
the named time clauses.  Overlap can only increase the middle sum, so the
argument does not assume that a time is covered uniquely.  A singleton with
(U=0<W=1) is the direct cover-deficit certificate found in Cycle 16.

The converse is not claimed: failure to find a frozen bounded-support weight
vector does not imply that the leaf is satisfiable or that no analytic
certificate exists.  A full base exclusion follows only when independently
checked certificates cover all 6,084 canonical leaves.
