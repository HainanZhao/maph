# Phase-0 preregistration

Date frozen: 2026-07-29 UTC

Status: `PREPARED_NOT_ACTIVATED`

## Sequencing gate

The sweep does not begin until all of the following are recorded:

1. Paper I has an arXiv identifier and immutable artifact DOI.
2. Paper II has an arXiv identifier and immutable artifact DOI.
3. The author has reviewed and sent the Kopp correspondence.

The sibling project currently records both deposits as blocked on
external credentials and the correspondence as drafted but unsent.
Creating schemas and replay wrappers does not count as launching the
census.

## Frozen range

- radicands: all 121 squarefree integers \(2\le D\le200\);
- fields: \(K=\mathbb Q(\sqrt D)\), one per radicand;
- finite moduli: every nonzero integral ideal of norm at most 100;
- archimedean part: exactly one real place;
- Galois-conjugate pairs
  \((\mathfrak f,\infty_i)\) and
  \((\overline{\mathfrak f},\infty_{3-i})\) are one census case;
- full-identification ray-group exponent cap: 24;
- certified identification degree cap: 32;
- wall-clock cap: one node-hour per case.

The machine-readable freeze is `data/range-v1.json`.  Ideal
representatives will be canonicalized by lexicographically comparing
the two conjugate normalized HNF records.  This avoids making the
paper-specific label `infinity_2` part of the mathematical identity of
a census row.  Each anchor records its historical place label
separately.

## Verdicts and decision order

A final record is either `PROVED` or `FRONTIER`.  A proved record has
exactly one `proof_engine` in `{A,B,C}`.  Engine precedence is:

1. A, if the exact support has order at most two;
2. C, if the nonquadratic support has order four and every C predicate
   passes;
3. B, for every remaining case for which every B predicate passes.

If a C candidate fails, B is still tested before a frontier verdict.
Thus an order-three character is not automatically
`SUPPORT_ORDER_3`: Engine B may prove the whole invariant.

A frontier record carries one deciding obstruction:
`EXPONENT_CAP`, `WILD_RAMIFICATION`, `SUPPORT_ORDER_k`,
`PROJECTIVE_ORDER_GE_3`, `INDEX_GT_2`,
`UNIT_CONGRUENCE_FAIL`, `DEGREE_CAP`, `TIME_CAP`, or
`IDENTIFICATION_FAIL`.  The obstruction is the predicate that
eliminates the last otherwise eligible engine.  `SUPPORT_ORDER_k` is
used only when support eliminates A and C and no Engine-B theorem is
applicable; it is not inferred merely from \(k\ge3\).  The evidence
field states exactly which tests were run, including earlier failed
engine candidates.

## Engine boundary

- Engine A applies only when every character in the Fourier support has
  order at most two and every regulator/index assertion is exact.
- Engine B applies only when the operational predicates extracted from
  the working Paper-I/II scripts all pass, the two independent
  imaginary-base routes agree, every divisor exponent is printed, and
  the Arb-to-height margin is at least 100.
- Engine C applies only to the order-four support isolated by genuine
  linear CM reinduction, with the projective \(V_4\) quotient, exact
  local factors, \(|S|\ge3\), certified roots of unity, and exact
  orientation.

No case may combine engines in one `PROVED` verdict.  When a historical
TCC proof combined a lower Engine-B packet with a primitive Engine-C
packet, those are separate census pairs or support components and are
separate anchor bundles.

## Seven-anchor gate

The number seven refers to proof bundles:

1. dimension 4, discriminant 5, Engine A;
2. dimension 5, discriminant 12, Engine B;
3. dimension 7, discriminant 8, Engine B;
4. dimension 7, discriminant 32, Engine B;
5. dimension 8, conductor-three lower ray-12 packet, Engine B;
6. dimension 8, conductor-three primitive ray-24 packet, Engine C;
7. dimension 8, conductor-one quadratic packet, Engine A.

Bundles 6 and 7 each contain two character packets.  Thus “7/7
anchors” is not the same count as either census rows or individual
characters.

Any command failure, missing expected marker, source-tree mismatch, or
disagreement with the frozen values halts Phase 0.  A failure transcript
is preserved before any amendment.

## Yield gate

After W1, count `PROVED`-eligible census pairs excluding all anchor
pairs.  At least 15 continues the census-paper framing.  Fewer than 15
forces the pre-registered rescope to a frontier-map paper.  The
threshold decides genre only; it never changes a mathematical verdict.
