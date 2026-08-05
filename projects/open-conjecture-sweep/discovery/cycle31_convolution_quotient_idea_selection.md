# Cycle 31 idea selection: falsify convolution closure cheaply

## Candidate questions

1. **Targeted atom-pair closure.**  Reconstruct the sealed 1,390 atoms, test
   the two singleton translations, then ask whether pair-atom convolutions are
   constant on the two exceptional six-point atoms.  Only if those pass, test
   exceptional-by-pair profiles on every atom.  This directly seeks the
   smallest exact obstruction to an additive quotient.
2. **Theorem-first Schur ring.**  Guess that the negation pairs and two CRT
   zero-fiber atoms form a Schur ring and prove its structure from divisors of
   2786.  The shape is suggestive, but Cycle 30 proved only exceptional-atom by
   mask-union action; a hidden atom-pair split would make the theorem false.
3. **Ownership polynomial calculus.**  Build a Nullstellensatz refutation on
   the Cycle-29 rank-three blockers using the 1,390-state quotient.  This is a
   genuinely different future engine, but using a quotient before its
   algebraic action is proved can manufacture invalid polynomial identities.
4. **Full 1,390-squared table.**  Exhaust every atom pair immediately.  It is
   exact but asks a much larger question than needed to falsify closure.

## Questioning the questioning

Why can Cycle 30's 2,772 passing profiles be misleading?  Each transported
mask is a union of many atoms.  A convolution split from one constituent atom
can cancel against another constituent inside the mask, so mask-generator
action does not imply atom-pair closure.

Why test exceptional targets first?  Ordinary atoms are negation pairs.  The
only quotient identifications beyond the standard even-function quotient are
the two size-six atoms, so any genuinely new closure claim must first survive
there.  Pair atoms have only four ordered sums, making the test exact and
cheap.

What would make even this framing wrong?  A singleton translation that does
not permute atoms already kills the quotient before pair testing.  Conversely,
passing the targeted tests does not prove all atom-pair closure; it only earns
a separately frozen full-closure or theorem step.

## Choice and falsifier

Choose targeted atom-pair closure.  The main rejected alternative is the
theorem-first Schur-ring claim because the decisive closure premise is cheap
to falsify exactly.  The branch falsifier is atoms \(A,B,C\) and the least
two points \(x,x'\in C\) with unequal exact representation counts in
\(1_A*1_B\).  Stop at the lexicographically first witness and do not convert
it into a no-go for other convolution partitions or polynomial methods.
