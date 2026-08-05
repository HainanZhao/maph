# Cycle 33: degree-zero odd-characteristic uncovered tensors

## Claim boundary

`PROVED`: p199 base 4 / leaf 78 has no degree-zero identity over either
\(\mathbb F_3\) or \(\mathbb F_5\) among the 1,394 negation-deduplicated
uncovered-time predicates. This does not exclude the leaf and says nothing
about rational coefficients, another characteristic, positive degree,
ownership-blocker calculus, other leaves, or LRC(13).

## Algebraic certificate criterion

For a digit tuple \(d=(d_i)\), let \(F_t(d)=1\) exactly when every selected
coordinate option misses time \(t\). Coordinatewise,

\[
F_t(d)=\prod_i b_{t,i}(d_i).
\]

Over a field \(K\), a degree-zero identity would be coefficients
\(\lambda_t\in K\) satisfying \(\sum_t\lambda_tF_t(d)=1\) for every digit
tuple. Restricting to finitely many tuples gives \(E\lambda=\mathbf1\).
Thus a vector \(y\) with

\[
y^{\mathsf T}E=0,\qquad y^{\mathsf T}\mathbf1=1
\]

proves that the restricted system, and therefore any full-domain identity,
is impossible in that field.

## Exact controls and p199 obstructions

The H11 base \((1,1,1)\) is the frozen positive control. `PROVED` by complete
enumeration of its 64 lifts: time 12 is always uncovered, so \(F_{12}=1\)
over both fields.

For p199 base 4 / leaf 78, both routes independently rebuilt the same 4,243
assignment rows (SHA256
`de06f7bea5bf1673f5a31d2febcac3e130fd67f5bf1ed6112e237b76a0cf5f84`)
and 1,394 predicate columns. Least-pivot elimination produced normalized
left-null certificates of size 802 over \(\mathbb F_3\) and 985 over
\(\mathbb F_5\). Exact recombination gives zero in every predicate column and
RHS one in the corresponding field. An independently written set-based
replay verified both certificates and independently found inconsistency using
reversed row order and highest pivots.

Consequently, `PROVED` no degree-zero identity exists over either tested odd
field on the full interface. The result is field-specific: finitely many
modular obstructions do not imply a rational obstruction, because a rational
solution may have denominators divisible by the tested primes.

## Falsifiers

An assignment-hash or mask mismatch, an H11 lift covering time 12, a
certificate coefficient outside its field, any nonzero recombined predicate
column, an RHS sum other than one, or a consistent independent elimination
invalidates the affected claim.
