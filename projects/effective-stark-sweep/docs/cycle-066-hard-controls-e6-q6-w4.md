# Cycle 066 — hard controls, first \(e=6\) tranche, and W4 discoveries

**Claim tags:** `VERIFIED` for the closed packets;
`VERIFIED_EXACT_CENSUS_STATISTICS` for the inventories;
`CONJECTURAL_ENGINE_DESIGN` for Engine D.

## Normalization and hard-control reproduction

With \(\ell_g=\log|g\varepsilon|_{\rm ord}\), the formulas used by
the generic pipeline are
\[
\zeta'_S(0,g)=-\frac2e\ell_g,\qquad
\ell_g=-\frac e2\zeta'_S(0,g),
\]
and, for the frozen quartic convention,
\[
L'_S(0,\psi)=-\frac4e(\ell_1-i\ell_\sigma),\qquad
\ell_1-i\ell_\sigma=-\frac e4L'_S(0,\psi).
\]
The forward coefficients are \(2/e\) and \(4/e\); the other two are
inverse recovery factors. An \(e=2\) replay cannot distinguish
\(2/e\) from the unsigned magnitude \(e/2\). The nontrivial
normalization control is RQ-000458 at \(e=4\); the
\(\mathbb Q(\sqrt{35})\) two-base computation validates the generic
direct-\(L'\), unit-orbit, and exact-bridge implementation.

RQ-000458 is the packet over \(\mathbb Q(\sqrt{14})\) with finite
modulus HNF `[[12,0],[0,6]]`, norm 72, one-place ray group
\(C_4\times C_2\), and supported ray characters \([1,1]\) and
\([3,1]\), both of order four.

The generic exact pipeline was run twice on both RQ-000458
imaginary-base routes and both algebraic halves of the
\(\mathbb Q(\sqrt6)\) case. The record JSON and raw transcripts were
byte-identical between executions. Three failed gate attempts are
preserved: a ray-basis label comparison, the misleading
`rnfisabelian` false negative, and an unnormalized polynomial-string
comparison. The corrected abelianity gate is the exact
`rnfconductor` to `bnrclassfield` round trip.

## Four real roots

For the \(\mathbb Q(\sqrt{35})\) packet, exact normal-closure
arithmetic proves that all four Artin norm classes are fixed by the
chosen conjugation. Arb orbit isolation matches them bijectively to
the four real roots. The other four roots are two nonreal conjugate
pairs, so the signature is \([4,2]\). This is the first
non-totally-real packet produced by the generic Engine-C tranche, not
the first in the full corpus.

## First elevated \(e=6\) tranche

The first three inventory fields with \(e=6\) are now `VERIFIED`:

| canonical case | two imaginary bases | occurrences |
|---|---|---:|
| RQ-001569 | \(\mathbb Q(\sqrt{-7})\), \(\mathbb Q(\sqrt{-6})\) | 6 |
| RQ-007519 | \(\mathbb Q(\sqrt{-6})\), \(\mathbb Q(\sqrt{-31})\) | 7 |
| RQ-001894 | \(\mathbb Q(\sqrt{-15})\), \(\mathbb Q(\sqrt{-85})\) | 1 |

All six character fields have \(e=6\), \(|S|\ge3\), exact selected
characters, overlapping independent Arb \(L'(0)\) balls, isolated
integral \(C_4\) unit orbits, identical two-route packet
polynomials, and exact conjugation-fixed Artin classes matching the
four real roots. The separator-prime bridge permits multiple prime
ideals only when they select one identical Frobenius automorphism.

## \(\mathbb Q(\sqrt6)\): auxiliary-prime closure

The former \(|S|=2\) halt is discharged by two independent auxiliary
rational primes. Exact Euler factors agree on the real source and
both CM routes:
\[
P_3(1)=1+i,\qquad P_5(1)=2.
\]
Neither multiplier vanishes, so analytic rank remains one.
After enlarging \(S\), the secondary route has \(|S|=3\), and
Stark's global-unit clause applies. Dividing the two enlarged Arb
targets by their exact multipliers recovers one common primitive
\(L'(0)\) ball.

On both routes, \(q=3\) gives the exact \((I\pm A)\) transform of the
natural coordinate orbit, while \(q=5\) gives twice that orbit.
The \(q=5\) theorem therefore identifies the square of each positive
packet norm. Positivity supplies the unique square root, recovering
the natural packet; the existing exact identity
\(q_8^3=q_{12}^2\) aligns the two bases. RQ-000129 is now
`VERIFIED`.

## Odd indices and Engine D

The 88 odd-index FRONTIER rows split as \(75+6+7\) at indices
\(3,5,9\). In 85 rows the index equals the normal-closure commutator
size; the three exceptions have index 3 and commutator size 6.
Support shares an odd prime with the index in 86 rows. A
3-primary support component occurs in \(80/88=10/11\), compared with
\(298/721\) among even-index controls carrying the same historical
obstruction label.

The index-one audit answers the Engine-D question affirmatively.
There are 3,521 index-one occurrences whose ray fields are abelian
over \(\mathbb Q\). After removing cases already handled by Engine A
and empty-support rows, 276 substantive FRONTIER occurrences across
85 fields remain. Frozen examples are RQ-000018
(\(\mathbb Q(\sqrt2)\), norm 41, support order 8), RQ-000032
(\(\mathbb Q(\sqrt2)\), norm 79, orders 2 and 6), and RQ-000274
(\(\mathbb Q(\sqrt{10})\), norm 36, order 4).

This is a candidate fourth engine, not yet a theorem. Its next gate is
a uniform reduction of the absolute abelian ray characters to
Dirichlet \(L'\)-values and cyclotomic/ACNF units, replayed on the
three frozen examples before any bulk use.
