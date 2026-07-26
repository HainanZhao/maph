# Lagrangian certificates and baseline counterexamples

## Separable upper bound

For a multiplier \(\lambda\geq0\), relaxing the fixed-input equality gives

\[
B(\lambda)=\lambda Q+
\sum_i\max\left\{0,\sup_{x\geq0}
   [f_i(x)-\lambda x]-q_i\right\}.
\tag{1}
\]

Every feasible route has net output at most \(B(\lambda)\).  For a
constant-product pool,

\[
\sup_{x\geq0}[f_i(x)-\lambda x]
=
\left(\sqrt{b_i}-
\sqrt{\frac{\lambda a_i}{\gamma_i}}\right)^2
\]

when \(0<\lambda<b_i\gamma_i/a_i\), and the supremum is zero above that
range.  After charging the fixed cost, pool \(i\) contributes strictly to
(1) exactly when

\[
\lambda<
\tau_i:=
\frac{\gamma_i}{a_i}
\left(\sqrt{b_i}-\sqrt{q_i}\right)^2,
\qquad q_i<b_i.
\tag{2}
\]

Between consecutive activation thresholds, the active dual terms are fixed
and

\[
B'(\lambda)
=Q+\sum_{i\in A}\frac{a_i}{\gamma_i}
-\frac{1}{\sqrt{\lambda}}
\sum_{i\in A}\sqrt{\frac{a_ib_i}{\gamma_i}}.
\]

Thus every possible minimizer is either a threshold or the single
stationary point in one threshold interval.  The implementation enumerates
those \(O(m)\) candidates after sorting the thresholds, then reports the
smallest bound and its gap above a supplied feasible route.

The floating-point result includes an explicit roundoff cushion, but it is
not an interval-arithmetic proof for adversarial machine inputs.

## Why the certificate is not a rounding algorithm

Dual activation describes the optimizer of a relaxation.  It does not
identify a primal active set in general, and even a zero duality gap does
not make a deterministic tie-breaking rule safe.

Take \(Q=4\) and two pools

\[
(a_i,b_i,\gamma_i,q_i)=(2,2,1,1/4),\quad(2,2,1,1/2).
\]

The optimum uses both pools, sends two units to each, and returns net output
\(5/4\).  The minimized dual bound is also \(5/4\), at
\(\lambda=1/4\).  The second pool is tied at zero reduced benefit.  A rule
that drops tied pools sends all input to the first pool and obtains only
\(13/12\).  The bound remains valid; the rounding rule is what failed.

## Why standalone profitability overactivates

Take \(Q=1\) and two identical pools

\[
(a_i,b_i,\gamma_i,q_i)=(1,2,1,1/2).
\]

Each pool would return one unit if it alone received the full trade, so a
standalone test declares both profitable.  Water filling then sends
\(1/2\) to each.  The resulting net output is \(1/3\), whereas using just
one pool returns \(1/2\).  Gross-output water filling and standalone
thresholding therefore make the same wrong activation decision here.

## Why initial marginal price is not a route ranking

For \(Q=100\), compare zero-cost pools \((a,b)=(1,2)\) and
\((a,b)=(100,190)\).  The first pool has the better initial marginal output,
\(2>1.9\), but it has almost no depth.  Sending the entire finite trade to
that initially better pool returns less than \(2\), while the exact
water-filled route returns more than \(80\).

Initial marginal price is a local derivative.  It can screen inactive pools
inside a correctly solved continuous subproblem, but it cannot rank entire
finite-size routes.
