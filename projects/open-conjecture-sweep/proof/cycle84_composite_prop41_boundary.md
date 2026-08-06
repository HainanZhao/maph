# C84 exact boundary: the direct composite analogue of Proposition 4.1

Let \(k=13\), so the modulus in the cited prime-field lemma would be
\(k+1=14\).  Let
\[
v=(0,7,0,0,\ldots,0)\in\mathbb Z_{14}^{13}.
\]
It is nonzero and has a zero coordinate.  The direct composite analogue would
assert the existence of units \(s,r\in\mathbb Z_{14}^{\times}\) such that
every coordinate of
\[
s v+r(1,2,\ldots,13)
\]
is in \(\{1,\ldots,12\}\).

`PROVED`: no such pair exists.  Every unit \(s\) is odd, hence
\(7s=7\bmod14\).  For each of the six values of \(r\), the independent
table checker gives a coordinate outside the target box:

| \(r\) | a forbidden coordinate |
| --- | --- |
| 1 | 13 |
| 3 | 2 |
| 5 | 11 |
| 9 | 3 |
| 11 | 5 |
| 13 | 1 |

Thus the field lemma from arXiv:2604.23906 cannot be extended verbatim by
replacing its prime modulus with \(14\).  The complete declared binary fiber
contains 4,824 failures among 8,191 nonzero vectors; this is independently
checked by exhaustive integer enumeration.

## Claim boundary

This is not a counterexample to the Lonely Runner Conjecture, an eventual
properness failure, or a proof that no CRT replacement exists.  It closes only
the direct target-box extension of the cited prime-field proposition.  A new
composite-modulus theorem would need a different target, a different witness
mechanism, or a proof that excludes this explicit zero-divisor case before it
could be used for \(LRC(13)\).
