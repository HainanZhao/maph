# C84 source audit: LRC(13) polynomial eventual properness

## Source and exact interface

`OBSERVED` from the primary preprint Sungkawichai--Trakulthongchai,
*Eleven, twelve, and thirteen lonely runners*,
[arXiv:2604.23906v1](https://arxiv.org/abs/2604.23906): Theorem 1.3 proves
\(LRC(k)\) through \(k=12\).  Thus it does not resolve \(LRC(13)\).

`PROVED` as a quoted theorem from that source, Proposition 1.4 (proved in its
Section 4 as Proposition 4.4): if \(k+1\) and \(p>k^2+k\) are odd primes,
then a primitive speed tuple congruent to \((1,\ldots,k)\bmod p\) has the LR
property.  The route uses Proposition 4.1: for every nonzero
\(v\in\mathbb Z_{k+1}^{k}\) with a zero coordinate, there are units \(s,r\)
such that
\[
 s v+r(1,2,\ldots,k)\in\{1,\ldots,k-1\}^{k}.
\]
Its proof explicitly works in the field \(\mathbb Z_{k+1}\).

For \(k=13\), \(k+1=14\) is composite.  The source theorem does not apply.
The C84 gate asks only whether the displayed proposition already fails on the
declared finite binary fiber \(v\in\{0,7\}^{13}\setminus\{0\}\) with at
least one zero coordinate.  This isolates the new zero divisor before any
large sieve or LRC claim.

## Literature boundary

`OBSERVED`: the abstract and Theorem 1.3 of the cited v1 source establish
\(k\le12\), not \(k=13\).  The bounded search in this selection found no
primary source resolving \(LRC(13)\); this is not a universal novelty or
openness claim.  The source's prime condition is a stated structural limit,
not evidence that no composite-modulus replacement exists.
