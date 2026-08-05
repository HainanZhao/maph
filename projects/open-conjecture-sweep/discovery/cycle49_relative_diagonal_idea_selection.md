# Cycle 49 idea selection: coupled diagonal fibers, not isolated defects

## Evidence that fixes the question

- `PROVED` Cycle 48: the Möbius tensor has the prescribed three pair
  marginals; alternating cubes are the complete local zero-marginal move
  family used there; every frozen start repairs deterministically.
- `PROVED` Cycle 48 finite no-go: all 314 nontrivial frozen starts have a
  literal nonjoinable reached diamond.  Uniqueness of normal form is not the
  needed theorem.
- `PROVED` pre-execution correction: a single cube cannot isolate a defect on,
  say, the 01 diagonal, because its vertex obtained by changing only coordinate
  2 retains the same forbidden 01 pair.
- `CONJECTURED`: the successful targeted reductions are shadows of a
  contraction on whole diagonal fibers, forced by the zero deleted-pair
  marginals, rather than accidents of lexicographic order.

## Serious candidates and their decision questions

### A. Relative diagonal-stratum contraction

Filter forbidden cells by the 01, 02, and 12 deleted-pair diagonals and their
triple intersections.  A deleted 01 fiber has total coefficient
`P01(w,w)=0`; cube packets act as differences along that fiber.  Ask whether
one can freeze support/buffer hypotheses under which explicit packet moves
contract successive pair strata and leave a zero terminal triple-intersection
group.

- Preserves: all three pair marginals, allowed support outside the active
  stratum, and a stated filtration.
- Falsifier: an exact surviving terminal relative cycle/dual cochain, or a
  full-domain p199 interface that violates the sufficient buffer hypothesis.
- Cost/information: moderate; a symbolic theorem or a named relative-homology
  obstruction directly resolves whether the local algebraic gate is real.

### B. Gauge-invariant next-lift obstruction

Accept nonconfluence as affine gauge freedom and ask for the next degree-four
or CRT obstruction directly on the quotient by allowed zero-marginal tensors.

- Preserves: equivalence of valid face sections.
- Falsifier: the proposed lift depends on the section representative, or no
  necessary lift map can be defined from the current interface.
- Cost/information: potentially high, but premature while the lift map and its
  necessity for a direct-cover object remain unproved.

### C. Quotient confluence

Prove all rewrite outputs equal modulo the allowed cube kernel.

- Falsifier: two outputs differ outside that kernel.
- Cost/information: low, but likely tautological because every valid output
  with the same pair marginals already differs by a zero-marginal tensor.  It
  does not construct the missing universal section.

### D. Abstract homology census

Compute relative groups for more sampled face patterns and infer a
classification.

- Falsifier: an unseen positive group.
- Cost/information: low-to-moderate, but another census violates the current
  gate and cannot distinguish a theorem from sampling luck.

## Question the questioning

Why continue asking a local face question after C47 already produced a dense
global section?  Because the next lift needs a rule that is justified beyond
one patch; however, “canonical” and “confluent” were inherited conveniences,
not necessities.  The true invariant is existence modulo the zero-marginal
gauge.

Why should zero fiber totals suffice?  They need not.  Contracting one pair
stratum can spill into either other pair stratum or terminate at an unavailable
cell.  Therefore the buffer hypothesis and terminal intersection group must be
declared before any positive examples are inspected.  Inferring them from the
512 repaired rows would be circular.

Why is A not merely Cycle 46's Čech coordinate reformulation again?  It counts
as an advance only if it proves a symbolic exactness/contraction theorem from
explicit support hypotheses, or produces a surviving relative class.  A
per-face boundary solve, renamed filtration, or sampled vanishing table is
`METHOD_COLLAPSE`.

The simpler defect-isolation question was rejected because it is formally
impossible on pair-diagonal defects.  The more ambitious gauge-lift question
was rejected for now because its target map is not yet defined.  The most
discriminating current question is whether coupled fiber packets close at the
triple-intersection stratum.

## Choice and final clarity rule

Choose A.  Freeze the abstract state space, filtration, packet formula family,
sufficient buffer hypothesis, terminal group, and small positive/negative
controls before executable work.  Check the declared hypothesis on the full
frozen p199 type-interface domain, not a repaired-face holdout.

Cycle 49 is the final clarity gate for Problem 1.  A symbolic contraction
theorem with checked p199 hypotheses is clear positive direction.  An exact
surviving terminal class or full-domain hypothesis failure is a clear scoped
obstruction.  If neither emerges within the frozen block, pause LRC(13), make
one concise handoff, and do not open Cycle 50.
