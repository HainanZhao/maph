# Cycle 34: exact rational degree-zero obstruction

## Claim boundary

`PROVED`: for p199 base 4 / leaf 78, the constant function is not in the
degree-zero \(\mathbb Q\)-span of the 1,394 negation-deduplicated direct
uncovered-time predicates. This does not exclude the leaf and says nothing
about positive degree, ownership auxiliaries, other leaves, or LRC(13).

## Exact criterion

Let \(E\in\{0,1\}^{4243\times1394}\) evaluate the direct uncovered predicates
on the frozen assignment rows. A degree-zero rational identity on the full
digit domain would give \(E\lambda=\mathbf1\) after restriction. Cycle 34
constructs an integer vector \(y\) such that

\[
y^{\mathsf T}E=0,\qquad y^{\mathsf T}\mathbf1\ne0.
\]

Multiplying a hypothetical restricted solution by \(y^{\mathsf T}\) would
give \(0=y^{\mathsf T}\mathbf1\), a contradiction. Thus the finite integer
certificate proves rational inconsistency without any denominator assumption.

## Construction and heightened checks

The Cycle 33 GF(5) echelon selected 1,228 original rows and pivot columns; its
first contradictory row is row 1,228. This modular stage selects a nonsingular
square skeleton but is not itself the rational conclusion. Exact PARI/GMP
solving of the skeleton transpose expressed the target on the pivot columns.
The same relation then agreed exactly on all 1,394 predicate columns. Clearing
denominators and primitive normalization produced 1,229 nonzero integer terms
with maximum coefficient height 2,807 bits and nonzero coefficient sum.

`PROVED`: the primary arbitrary-precision replay recombines every predicate
column to zero and the RHS to a nonzero integer. Because the favorable result
shared the primary predicate representation, an independently written route
rebuilt the base, allowed digits, assignment stream, negation representatives,
and evaluation rows as Python sets. It reproduced the frozen assignment hash,
found zero in all 1,394 integer column sums, the identical nonzero RHS,
primitive gcd one, and the prescribed sign. A supplementary audit-prime replay
also agrees, but the integer replay—not the modular check—is the proof.

## Falsifiers

A different assignment hash, predicate-membership mismatch, repeated or
out-of-range certificate row, nonprimitive normalization, any nonzero integer
predicate sum, or zero/mismatched integer RHS invalidates the claim. A
rational solution on only the frozen rows would falsify this obstruction; a
restricted-row solution alone would not prove a full-domain identity.
