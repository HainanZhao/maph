# Stage 2 brainstorm: from data to an infinite family

## Current bottleneck

For primes \(p<q<r\), we know

\[
f(pqr)>\sqrt{pqr}
\quad\Longleftrightarrow\quad
r<pq\ \text{and}\ f(pqr)=pq.
\]

The remaining task is therefore not to estimate a large binomial coefficient.
It is to prevent every admissible \(k\) from producing one of the smaller
gcds \(p,q,r\).

Proposition 8 says that a single-prime gcd can occur only at

\[
k=tqr,\qquad k=tpr,\qquad k=tpq,
\]

respectively. Lucas's theorem tests each possibility digit by digit.

## Why begin with \(p=2\)

The eligible triples become

\[
n=2qr,\qquad q<r<2q.
\]

This has three advantages:

1. the interval for \(r\) is short;
2. Lucas's criterion modulo \(2\) is the bitwise condition
   \[
   \binom nk\equiv1\pmod2
   \quad\Longleftrightarrow\quad
   k\mathbin{\&}\mathord{\sim}n=0;
   \]
3. the candidate for gcd \(2\) is only \(k=qr=n/2\), and it can be analyzed
   completely.

The first goal is an exact criterion for
\[
f(2qr)=2q
\]
in terms of a short list of digit conditions.

## Ranked approaches

### A. Explicit witness exclusion for \(2qr\) — primary

For each non-hit, record:

- which smaller prime \(q\) or \(r\) occurs as the gcd;
- the multiplier \(t\);
- the base-\(2\), base-\(q\), and base-\(r\) digits responsible.

Then search for a parameterized condition that makes every such witness
impossible. Candidate conditions may involve:

- the binary support of \(q\), \(r\), and \(qr\);
- a fixed relationship \(r=q+d\) or \(r=2q-d\);
- intervals between powers of two;
- congruence restrictions on \(q\) and \(r\).

### B. Fixed small \(p>2\) — secondary

Repeat the same analysis for \(p=3,5,\ldots\). This provides more flexibility
in choosing \(q,r\), but introduces more candidate multipliers and loses the
simple bitwise parity test.

### C. Higher prime exponents — reserve

The general data contains strict hits such as \(84=2^2\cdot3\cdot7\).
Prime powers may ultimately give easier infinite families, but their gcds
have several possible valuations instead of only squarefree divisors. We
postpone this until the squarefree witness mechanism is understood.

### D. Probabilistic/density argument — speculative

The scan through primes \(200\) found many hits, suggesting one might prove
that the union of all bad digit conditions cannot cover every eligible prime
triple. This would require genuine distribution results for primes under
digit restrictions, so it is less elementary and should follow—not precede—
the structural analysis.

## Falsification rules

- A relation observed for small consecutive primes is not a conjecture until
  tested well beyond the discovery range.
- A proposed family must survive targeted searches for the Lucas witnesses,
  not merely a table of \(f(n)\).
- Dependence on an unproved assertion such as infinitely many twin primes
  must be stated explicitly; a conditional family is not an unconditional
  solution.

## Immediate deliverables

1. [Complete] A triple analyzer returning explicit single-prime witnesses.
2. [Complete] A proof that gcd \(2\) cannot occur when \(q<r<2q\).
3. [Complete] Simplified ranges for the remaining gcd-\(q\) and gcd-\(r\)
   witnesses.
4. [Complete] A dataset grouped by witness type and multiplier.

## First construction found

Proposition 10 first proves that if
\[
q=2^m-1,\qquad r=2^{m+1}-3
\]
are both prime, then \(f(2qr)=2q>\sqrt{2qr}\). The proof uses the final
\(m\) binary digits to exclude every remaining witness.

Proposition 11 strengthens this substantially: only \(r=2^{m+1}-3\) needs
to be prime; \(q=2^m-1\) may be composite. Thus the binomial-gcd part of the
construction is now completely controlled, and the remaining obstruction is
the unknown infinitude of primes of the form \(2^a-3\).

This is a useful structural success but not the final objective: infinitude
of simultaneous primes of these two forms is not known. It suggests two next
directions:

1. abstract the binary block argument to intervals containing primes whose
   existence follows from established prime-distribution theorems.
2. seek a construction in which \(r\) may also be composite without creating
   a small gcd from one of its proper factors.
