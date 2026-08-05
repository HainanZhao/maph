# Cycle 32: degree-zero GF(2) uncovered tensors

## Claim boundary

`PROVED`: p199 base 4 / leaf 78 has no degree-zero GF(2) identity among the
1,394 negation-deduplicated uncovered-time predicates.  This does not exclude
the leaf and says nothing about positive degree, another field, rational
coefficients, ownership-blocker calculus, other leaves, or LRC(13).

## Algebraic certificate criterion

For a digit tuple \(d=(d_i)\), let \(F_t(d)=1\) exactly when every selected
coordinate option misses time \(t\).  Coordinatewise,

\[
F_t(d)=\prod_i b_{t,i}(d_i),
\]

so these are rank-one tensors.  If coefficients \(\lambda_t\in\mathbb F_2\)
satisfy

\[
\sum_t\lambda_tF_t(d)=1
\]

for every digit tuple, then `PROVED` no full cover exists: a full cover makes
every \(F_t\) zero, contradicting the identity.

Conversely, restrict a claimed identity to any finite set of digit tuples and
write the resulting evaluation matrix as \(E\).  If the system
\(E\lambda=\mathbf1\) is inconsistent, then `PROVED` no global degree-zero
identity exists, because any global identity would solve every restriction.

All direct masks are invariant under \(t\mapsto-t\).  Deduplicating each such
pair therefore preserves the evaluation columns exactly, giving 23 H11 and
1,394 p199 predicate columns.  No Cycle-30 six-point merger is used.

## Exact controls and p199 obstruction

The lexicographically first H11 base with no raw full lift is \((1,1,1)\).
`PROVED` by complete enumeration of its 64 lifts: time 12 is uncovered by
every tuple, so the weight-one identity \(F_{12}=1\) is an exact degree-zero
refutation.  This is a deliberately simple positive control.

For p199 base 4 / leaf 78, the first frozen system contains 4,243 exact digit
tuples and 1,394 predicate columns.  Primary least-pivot elimination found a
577-row subsystem whose left sides XOR to zero while the 577 right sides XOR
to one.  Hence `PROVED` the evaluation system is inconsistent and no
degree-zero GF(2) identity exists.  An independent implementation rebuilt all
masks and rows as sets, rechecked the same 577-row XOR exactly, and independently
reached inconsistency using reversed row order and highest pivots.

This is a structural negative result for the smallest algebraic layer, not a
failure of polynomial methods generally.

## Falsifiers

A mask/negation mismatch, an H11 lift covering time 12, a contradiction row
outside the frozen tuple set, a nonzero XOR coefficient column, an even RHS
parity, or a consistent independent elimination invalidates the affected
claim.
