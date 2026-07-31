# One-Place Stark Census paper — execution plan v1

Date frozen: 2026-07-30 UTC

Working title: *A Certified Census of One-Place Stark Invariants over
Real Quadratic Fields: Taxonomy, Exact Quadratic Stratum, and the
Higher-Order Frontier*.

## Claim boundary

The paper proves a finite-range structural trichotomy and solves the
quadratic-support stratum exhaustively by the uniform exact formula.
It classifies, but does not re-prove, higher-order packets. All
frequencies are exact statements about the frozen universe, not
asymptotic density claims.

The trichotomy is defined by the exact differenced Fourier support:

- `T`: empty support;
- `Q`: nonempty support consisting only of characters of order at most
  two;
- `H`: nonempty support containing a character of order greater than
  two.

This definition is deliberately independent of the evaluated value.
In particular, a Q-row whose imprimitive Euler products all vanish
remains in Q even though the exact formula gives \(X_A=1\).

## Frozen universe

The paper uses the existing maximal-order range:

- squarefree radicands \(2\le D\le200\), so
  \(K=\mathbb Q(\sqrt D)\);
- all nonzero integral ideals \(\mathfrak f\subseteq\mathcal O_K\)
  with \(N\mathfrak f\le100\);
- one infinite place, modulo
  \((\mathfrak f,\infty_1)\sim
  (\overline{\mathfrak f},\infty_2)\);
- 121 fields, 13,939 raw ideals, and 8,200 conjugacy
  representatives.

The parameter \(D\) is a squarefree radicand, not a fundamental
discriminant. Nonmaximal form-order moduli from the TCC companions are
not silently added to this 8,200-row theorem universe; they are
external reconciliation anchors.

The RQ registry is stable: sort by
\((D,N\mathfrak f,\operatorname{HNF}(\mathfrak f))\) after replacing
an ideal by the lexicographically smaller of it and its conjugate,
then number consecutively from `RQ-000001`.

## First reconciliation result

A clean PARI enumeration reproduced the banked mathematical payload.
The paper-level support trichotomy is

| stratum | rows |
|---|---:|
| T: empty support | 3,936 |
| Q: nonempty quadratic support | 1,560 |
| H: nonempty higher-order support | 2,704 |
| total | 8,200 |

This corrects—not erases—a routing issue in census v5. That artifact
reported 3,899 `PROVED_TRIVIAL` and 1,628 `FRONTIER` rows. Thirty-seven
empty-support rows had W1 engine `NONE` and were assigned
`EXPONENT_CAP` before the empty-support theorem was applied. For the
structural census these rows belong to T, leaving 1,591 unresolved
higher-order frontier rows. Census v5 remains preserved as the
historical routing declaration; the paper uses the corrected
support-first partition.

The Q reconciliation is unchanged: 1,560 rows, 2,232 supported
quadratic-character occurrences, and 912 distinct quartic fields.
There are 672 zero imprimitive Euler products affecting 603 rows; all
supported terms vanish in 346 rows. These 346 rows remain Q and form
the exact-value-one degeneracy sub-stratum.

## Main theorem plan

1. **Structural trichotomy.** State the support-first partition and
   the empty-support/sign-class equivalence, with the exact
   3,936/1,560/2,704 counts and manifest hash.
2. **Quadratic stratum.** Apply the uniform Engine-A theorem to every
   Q-row. Emit exact per-character exponents, certified quartic unit
   data, orientation, and Artin labels.  Synthesize denominator-cleared
   packet-power orbits over \(K\) by the compositum-free trace
   recurrence in the versioned amendment.  When the common exponent
   denominator is \(q>1\), factor \(P(X^q)\) exactly and require the
   separate positivity/Artin lift before calling a factor the packet
   polynomial.  When the Artin sign image is smaller than the formal
   sign cube—as for the four supported characters over \(C_2^3\)—an
   exact Artin-coset factor gate is required even when \(q=1\).
   Exact irreducibility and orbit-cardinality gates precede the word
   “minimal.”
3. **Parity audit.** Restate the proved parity lemma and report its
   independent replay on all 446 odd-index rows, all in T.
4. **Higher-order taxonomy.** For every H-row, record support orders,
   Engine-B predicates, complete Engine-C geometry, Roblot coverage,
   resolved-elsewhere pointers, and the remaining obstruction.
5. **Frontier.** Give the smallest unresolved row at every observed
   support order and the smallest row failing every known mechanism,
   led by the \(\mathbb Q(\sqrt{21})\) wall.

## Gates and execution order

1. `BANKED`: range and audit preregistration in
   `data/census-paper-preregistration-v1.json`.
2. `BANKED`: clean enumeration and Layer-0 reconciliation in
   `artifacts/census-paper-layer0-reconciliation-v1.json`.
3. `BANKED`: the worked imprimitive \(E_\chi=2\) row RQ-000013.
4. `BANKED`: prove and replay trace-descent
   synthesis plus the dimension-eight denominator-two lift.
5. `BANKED`: close the proper-Artin-image factor gate on corrected
   four-effective-character anchor RQ-000245.  RQ-000089 remains the
   preserved failed anchor selection because one Euler term vanishes.
6. `BANKED`: the full height-only calibration observed a maximum
   89-digit predictor and mechanically froze the 256-digit cap.
7. `BANKED`: all 1,560 exact Q-row packet polynomials pass the
   hash-chain audit; the maximum exact coordinate height is 62 digits.
8. `BANKED`: the deterministic 50-row independent Arb regulator audit
   passes at 384 bits after preserving the 192-bit radius failure.
9. `ACTIVE`: construct H eligibility columns and the frontier table.
10. `READY`: write finite-range distributions and quarantined
   conjectures.
11. `BLOCKED` on 7–10: freeze corpus, mint DOI, and compile the journal
   manuscript.

No manuscript count may be copied from v5 without passing the
support-first reconciliation. Any independent-audit failure halts the
affected table and remains preserved.
