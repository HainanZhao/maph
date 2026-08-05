# Cycle 9: weighted first-lift dual

Fix a base tuple `v` in `I(k,p,1)`, a multiplier `c`, and `q=cp`. For every
coordinate `i` and digit `d`, let `D_{i,d}` be the denominator-`q` bad-time
mask of `v_i+p d`. Suppose nonnegative integer weights `n_a` satisfy

\[
  \sum_{i=1}^k\max_{0\le d<c}\sum_{a\in D_{i,d}}n_a
  < \sum_{a\in\mathbb Z_q}n_a. \tag{*}
\]

If a digit selection `d_1,...,d_k` had no denominator-`q` witness, its
selected masks would cover every time. Nonnegativity would give

\[
 \sum_a n_a\le\sum_i\sum_{a\in D_{i,d_i}}n_a
 \le\sum_i\max_d\sum_{a\in D_{i,d}}n_a,
\]

contradicting `(*)`. Therefore every digit selection has a witness. In
particular there is no `(k,p,c)`-improper lift in the parent fiber, so the
base tuple is absent from `F_1(k,p,c)`.

This criterion is sufficient only. Its failure does not construct an
improper lift and does not invalidate the first-lift retained-path argument.
The verifier works entirely with the integer weights and masks, so a discovery
LP may use floating point only to propose a candidate; it cannot support a
certificate without the exact strict check above.

Conversely, if a concrete digit selection has selected masks covering every
time (regardless of whether the Definition-2.1 gcd clause later makes that
lift proper), then for every nonnegative `n` the two inequalities in the
display above reverse the desired strict conclusion:

\[
 \sum_i\max_d\sum_{a\in D_{i,d}}n_a\ge\sum_a n_a.
\]

Thus one exact mask-cover selection is a structural falsifier for this entire
nonnegative weighted-dual family on that base tuple, not merely a failure of a
particular LP search.
