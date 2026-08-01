# Cycle 135 — corrected direct-source transport batch

Recorded: 2026-08-01 UTC, after the integral-basis geometry correction
and before extracting quotient-prime ray logs or writing formulas.

## Frozen targets

The batch is exactly the ten corrected geometrically eligible targets:

| closure | sealed source | targets |
|---|---|---|
| B5-021 | RQ-002057 | RQ-002079 |
| B5-033 | RQ-002955 | RQ-002964, RQ-002983 |
| B5-086 | RQ-001107 | RQ-001115, RQ-001125, RQ-001132, RQ-001133, RQ-001149, RQ-001164, RQ-001172 |

The source data, certified-Arb transcript, and source program must
match their frozen hashes. This is sealed-source reuse, not a fresh
analytic replay.

## Acceptance gates

For every target, retain the corrected integral-basis geometry record,
then independently compute the quotient's distinct prime factors and
their source ray logs.  Require the recorded target-to-source ray-map
matrix, identity, and sign map.  The promoted formula is the exact
subset Euler-deletion identity

\[
 X_{\mathfrak m_t}(a)=
 \prod_{J}X_{\mathfrak m_s}
 \left(ca-\sum_{j\in J}\ell_j\right)^{(-1)^{|J|},
\]

where \(c\) is the generator coefficient and the \(\ell_j\) are the
source ray logs of the distinct quotient primes.  Rank-one parity
vanishing supplies the differentiated identity. Positivity of the
sealed source packet supplies orientation of each product/quotient.

Any source hash, factorization, map, or orientation failure leaves the
target unpromoted. No direct Arb run, numerical recognition, or new
packet polynomial is in scope.
