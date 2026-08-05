# Cycle 35: rank-one coordinate-local signed measure

## Claim boundary

`PROVED`: for p199 base 4 / leaf 78, the 1,394 direct uncovered predicates
admit a rank-one full-grid signed measure of mass one that annihilates every
predicate. Consequently, the constant function is not in their degree-zero
rational span. This is a structural no-go for that certificate calculus, not
a leaf exclusion, a positive-degree result, or a proof of LRC(13).

## Local-to-global certificate

Write each direct predicate as

\[
F_t(d)=\prod_{i=0}^{12} b_{t,i}(d_i),
\]

where \(b_{t,i}\) is the binary vector recording which allowed options at
coordinate \(i\) miss time \(t\). Cycle 35 constructs integer local vectors
\(u_i\), aligned with the frozen allowed-option order, such that

\[
\sum_{d_i}u_i(d_i)=1
\]

for every coordinate, and for every one of the 1,394 predicates there is at
least one coordinate with \(\langle u_i,b_{t,i}\rangle=0\).

Define \(y(d)=\prod_i u_i(d_i)\) on the complete digit Cartesian product.
Exact finite distributivity gives

\[
\sum_d y(d)=\prod_i\sum_{d_i}u_i(d_i)=1,
\qquad
\sum_d y(d)F_t(d)=\prod_i\langle u_i,b_{t,i}\rangle=0.
\]

Applying this functional to a hypothetical identity
\(\sum_t\lambda_tF_t=1\) yields \(0=1\). Hence `PROVED` no degree-zero
rational identity exists on the full grid. The local coefficients have
maximum absolute value five; some are negative, so this is a signed functional
and not a probability or entropy measure.

## Search boundary and checks

The first exact representation enumerated all lower local flats and stopped at
its frozen one-million-state cap; it made no p199 claim. The same live cycle
reformulated the identical hyperplane-cover question as an on-demand exact
matroid CSP. H11 stops at time 12: its local pattern is all ones at every
coordinate, so no nonzero-mass normal can kill it. On p199 the optimized route
found the product measure in 26 states.

The primary route verified all local masses and every local dot product. A
separate replay rebuilt the base, allowed digits, direct masks, negation
representatives, and patterns without importing the primary mask code. It
verified all 1,394 predicates independently: each has between one and thirteen
killing coordinates, all local masses are one, and the global mass is one.
Exactly 181 predicates have a single killing coordinate; these are the sharp
boundary for lifting this functional against one-coordinate multipliers.

During heightened checking, a reported per-coordinate count disagreed. The
cause was contained before sealing: the field counted only labels forced by
the search span, while the chosen free-zero normal killed additional patterns.
The final record distinguishes the span-guaranteed count from the normal's
actual exact kill count; the independent replay agrees with the latter.

## Falsifiers

A changed allowed-option order, direct-mask or negation mismatch, any local
mass other than one, or any predicate whose local dot products are all
nonzero invalidates the product certificate. Negative coefficients also
falsify any interpretation of this functional as a probability measure.
