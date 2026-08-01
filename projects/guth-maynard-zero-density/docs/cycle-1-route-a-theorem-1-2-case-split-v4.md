# Cycle 1, Route A v4: Theorem 1.2 case-split audit

## Claim boundary

`PROVED` below means exact rational arithmetic conditional on the analytic
inputs used in Guth--Maynard's proof of Theorem 1.2: the zero-detection
lemma, Theorem 1.1, and the mean-value theorem.  This is not an independent
proof of any of those inputs and does not establish a new density estimate.

This document implements the frozen *Theorem 1.2 case-split amendment* in
[`cycle-1-g0-preregistration.md`](cycle-1-g0-preregistration.md).  It is a
new v4 Route A certificate; Route A v1--v3 artifacts are retained unchanged.

## Source and frozen conventions

`PROVED`: Guth--Maynard, arXiv:2405.20552v2, source lines 2307--2399,
proves Theorem 1.2 by splitting Type I/II zeros and then choosing an integer
power \(k\).  The frozen source tarball and TeX SHA-256 values are recorded
in the v4 artifact.  The relevant source statements are:

- Type II zeros contribute at most \(T^{2-2s}(\log T)^{O(1)}\).
- For Type I zeros, \(1/100<n\le1/2+o(1)\), where
  \(n=\log N/\log T\).
- The chosen power has \(q=\log(N^k)/\log T\), and the proof requires the
  displayed lower/upper power window only up to the stated \(o(1)\) slack
  in the large-\(n\) regime.

Freeze, for \(7/10\le s\le4/5\),

\[
l(s)=\frac {10}{6+10s},\quad u(s)=\frac {15}{6+10s},\quad
B(s)=\frac {15(1-s)}{3+5s},\quad
d(s)=\frac {18}{5}-4s,\quad \alpha(s)=\frac{B(s)}{d(s)}.
\]

All denominators used below are positive on the frozen interval.  The replay
certifies this by endpoints and monotonicity: \(d(s)\ge2/5\),
\(9-10s\ge1\), \(u(s)\ge15/14>1\), and the remaining linear denominators
are plainly positive.

## Exact branch audit

### Type II

`PROVED`:

\[
B(s)-2(1-s)=\frac{(1-s)(9-10s)}{3+5s}\ge0
\]

for \(s\le9/10\), hence on the frozen interval.  This contains the Type II
exponent \(2(1-s)\) in the target \(B(s)\).

### Integer choice

For \(n\le l(s)/2=5/(6+10s)\), take \(k=\lceil l(s)/n\rceil\).  Then

\[
l(s)\le q=kn<l(s)+n\le\frac32l(s)=u(s).
\]

The lower power-scale bound \(n>1/100\) and \(l(s)\le10/13\) give
\(k\le77\), so this is a bounded-power choice.

For \(n>l(s)/2\), take \(k=2\).  Then \(q=2n>l(s)\).  The source gives
only \(q\le1+o(1)\), not a literal finite-\(T\) upper bound.  Since
\(u(s)\ge15/14=1+1/14\), that slack is uniformly contained:
\(q\le u(s)+o(1)\), and indeed \(q<u(s)\) for sufficiently large \(T\).
The replay deliberately does **not** replace this with an unqualified
finite-\(T\) claim \(q\le u(s)\).

### Theorem 1.1 branch: \(q\le\alpha(s)\)

`PROVED`: all three exponent comparisons are obtained at their monotone
boundary values:

\[
2u(s)(1-s)=B(s),\qquad d(s)\alpha(s)=B(s),\qquad
1+(12/5-4s)l(s)=B(s).
\]

The first expression increases with \(q\); it gives \(B(s)\) exactly in
the small-\(n\) regime and \(B(s)+o(1)\) in the large-\(n\) regime.  The
second increases because \(d(s)>0\).  The third decreases because
\(12/5-4s<0\).  Consequently the three Theorem 1.1 terms are bounded by
\(B(s)+o(1)\), \(B(s)\), and \(B(s)\), respectively.

### Mean-value branch: \(q>\alpha(s)\)

The first mean-value term is the same \(2q(1-s)\) expression and therefore
has the same contained \(B(s)+o(1)\) bound.  The second has negative
coefficient \(1-2s\), so \(q>\alpha(s)\) gives a strict inequality.  The
exact source margin is

\[
B(s)-[1+(1-2s)\alpha(s)]
=\frac{250(s-3/4)^2+3/8}{2(3+5s)(9-10s)}>0.
\]

The v4 replay evaluates direct rational substitutions at \(7/10,3/4,4/5\)
and records the exact margins \(1/26,1/54,1/14\); positivity on the full
interval follows from the displayed positive numerator and denominator, not
from sampling.

### Contained construction correction

`OBSERVED`: before the first v4 artifact was written, an exact assertion
rejected a hand-entered value \(3/52\) for the midpoint margin.  Direct
substitution into the frozen source formula gives \(1/54\), which is the
value used in the certificate and tests.  No certified record was overwritten.

## Replay

```sh
python3 projects/guth-maynard-zero-density/proof/replay_theorem_1_2_case_split_route_a_v4.py
python3 -m unittest projects/guth-maynard-zero-density/tests/test_theorem_1_2_case_split_route_a_v4.py -v
```

The first command writes the hash-recorded artifact
`artifacts/theorem-1-2-case-split-route-a-v4.json`.  The script uses Python
standard-library `fractions.Fraction` for every mathematical quantity and
records its own SHA-256, tool version, and integer-nanosecond wall time.
