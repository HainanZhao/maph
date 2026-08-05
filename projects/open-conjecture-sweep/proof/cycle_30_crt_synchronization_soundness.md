# Cycle 30: gcd-stratified transport algebra

## Claim boundary

The transport theorem below is `PROVED` in general.  The algebra dimensions,
atom descriptions, and exceptional-atom convolution action are `PROVED`
finite results for the complete H11 corpus and p199 base 4 / leaf 78.  The
convolution test does not prove closure for all atom pairs.  No p199 leaf is
excluded, no other survivor is classified, and LRC(13) is not proved.

## Unit-associate transport theorem

Fix a modulus \(q\), a bad residue set \(B\subseteq\mathbb Z/q\mathbb Z\),
and

\[
M_a=\{t:at\in B\}.
\]

If \(u\) is a unit modulo \(q\), then `PROVED`

\[
M_{ua}=u^{-1}M_a.
\]

Indeed, \(t\in M_{ua}\) iff \(uat\in B\), iff \(ut\in M_a\).  Also
`PROVED`: two residues modulo \(q\) are associates under the unit group iff
they have the same gcd with \(q\).  One implication follows because units do
not change that gcd.  For the converse, write both residues as the common gcd
times residues coprime to the complementary modulus, solve for a relative
unit there, and lift it to avoid every prime dividing the common gcd by the
Chinese remainder theorem.  The executable replay additionally constructs
the least multiplier and checks every named mask bit-for-bit.

## Exact pointwise algebra

For every represented gcd stratum, choose its least allowed speed, generate
the subgroup of relative unit multipliers, and transport the canonical mask
through that subgroup.  A unital algebra of zero-one functions under
pointwise addition and multiplication consists exactly of functions constant
on the common membership atoms of its generators.  This is `PROVED`: products
of generators and complements give each nonempty membership atom's indicator,
while every algebra expression is constant on points with the same generator
membership vector.

Consequently every allowed mask and every finite union, intersection, or full
uncovered product is constant on these atoms.  Direct full-cover testing on
one representative per atom is therefore exact, not a relaxation.

## Finite results and the apparent factor two

`PROVED` by two independent exhaustive implementations: for H11, 20 distinct
transported masks generate 23 atoms—two singletons and 21 pairs.  The quotient
reproduces all 64,000 lifted assignments, all 720 raw full covers, the 32,000
gcd-admissible assignments in four equal parity classes, and zero retained
improper bases.

For p199 base 4 / leaf 78, `PROVED` as a finite exact result: the 159 allowed
speeds occupy gcd strata 1, 2, 7, and 14; every generated relative subgroup is
the full 1,188-element unit group; and 1,386 distinct transported masks
generate 1,390 atoms.  Their sizes are two singletons, 1,386 pairs, and two
six-point atoms.  All 147 frozen baseline/single-coordinate-substitution
controls agree with direct raw masks.

Every bad mask is invariant under \(t\mapsto-t\), so time reversal alone has
1,394 orbits.  The independent replay proves that the only further mergers
are

\[
\{199,597,995,1791,2189,2587\},\qquad
\{398,796,1194,1592,1990,2388\}.
\]

These are the nonzero \(199\)-multiples split into the two remaining
modulo-14 gcd types; \(0\) and \(1393\) are the fixed singleton atoms.
Therefore the frozen factor-two threshold passes by three atoms, but the
algebra saves only four atoms beyond the standard negation quotient.  The
finite compression is exact yet strategically almost entirely explained by
old symmetry and the CRT zero fiber.

## Exceptional-atom convolution action

For functions on \(\mathbb Z/2786\mathbb Z\), write

\[
(f*g)(x)=\sum_y f(y)g(x-y).
\]

`PROVED` as a complete finite result by two independent exact routes: for each
of the two size-six atoms \(E\) and each of the 1,386 transported mask
generators \(M\), the profile \(1_E*1_M\) is constant on all 1,390 pointwise
atoms.  The primary route evaluated 46,336,752 incidences pointwise; the
independent route accumulated 6,623,100 translated-support incidences.  Both
checked all 2,772 profiles, and the latter found 2,079 distinct compressed
profiles.

Thus the exceptional CRT mergers are compatible with this entire named
additive action family; they are not merely an accidental pointwise
identification.  This statement is deliberately narrower than closure of the
1,390-dimensional atom algebra under every atom-pair convolution, and it is
not a polynomial or leaf-exclusion certificate.

## Falsifiers

Any unit-transport, subgroup, direct-mask, generator, atom, quotient-cover,
H11 count, p199 target, atom-size, or exceptional-atom mismatch invalidates
the affected finite claim.  A new atom merger outside the two displayed
six-point classes would refute the complete p199 atom description.  Any one
of the 2,772 convolution profiles splitting a pointwise atom would refute the
exceptional-action result; failure of an untested atom-pair convolution would
not.
