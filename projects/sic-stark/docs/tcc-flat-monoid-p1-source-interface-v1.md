# AFK flat-monoid pilot P1 — source interface audit

**Status:** PROVED source-scope finding; no monoid enumeration or
partial-zeta evaluation has been performed.
**Date:** 2026-08-01 UTC
**Preregistration:** data/tcc-flat-monoid-p1-preregistration-v1.json

## Outcome

The proposed d=7, f=2 pilot cannot safely start from the finite residue
ring O/(7O), even though that ring supplies useful local data. Kopp's
flat-imprimitive monoid construction defines classes by an equivalence
relation on semilocally integral invertible ideals. Its resolution
proposition gives a surjective monoid sequence

    (O/m, multiplication) times {plus,minus}^S -> Clt_(m,S)(O) -> Cl(O) -> 1.

The paper explicitly defines exactness for commutative monoids so that a
fiber is a coset of an image; this is weaker than a presentation by an
injective left map. Therefore neither the residue ring itself nor a
guessed quotient by global-unit residue orbits has been shown equal to
the AFK monoid.

This is a scope containment, not an obstruction to the successor theorem.
It prevents a false finite-algebra certificate from being built on an
unproved multiplication table.

## Checked source facts

- Kopp, arXiv:2411.06763, Section 3.2, defines the flat imprimitive ray
  class monoid as semilocally integral O-invertible ideals modulo its
  stated common-factor equivalence.
- The same section defines its noncancellative notion of an exact
  monoid sequence before Proposition exmonoid.
- Proposition exmonoid gives the displayed residue/sign-to-monoid-to-class
  sequence but does not assert that its residue/sign map is injective.
- AFK's theorem nupnumpeq1 indexes its squared overlap by precisely this
  type of monoid class for O_f.

## Consequence for the P1 adapter

The next implementation task is to enumerate semilocally integral
O_f-invertible ideal classes and test their equivalence directly, with
the common-factor witnesses retained. A residue computation may be used
only as an independently checked quotient or invariant. No radical,
character, Euler-factor, packet, or TCC statement is authorized until
that multiplication table and the AFK label map pass G1.

## Falsification condition

This containment is refuted only by a source theorem or a direct proof
that computes the kernel of the residue/sign map for the frozen d=7,
f=2 level and identifies it with the proposed model. A finite match of
cardinalities alone is insufficient.

## Pilot-specific refinement — class-number-one quotient lemma

**PROVED for the two frozen class-number-one controls.** The preceding
containment forbids an unproved *general* residue presentation. It does
not forbid a direct derivation in a class-number-one case.

Let O have trivial ordinary ideal class group. For a fixed modulus m and
sign set S, the flat O-invertible monoid is the quotient of

    (O/m, multiplication) times {plus,minus}^S

by the action of the global unit group, where a unit multiplies the
residue and changes each sign by its sign at that real place.

Here is the direct proof needed by the pilot. Kopp--Lagarias Definition
A.8 uses a common factor c that is coprime to m. Triviality of Cl(O)
makes c principal, say c=delta O; coprimality makes delta a unit modulo
m. If alpha O and beta O are equivalent, their two displayed principal
generators differ after multiplication by delta by global units u and v.
The congruence and sign conditions then reduce, after cancelling delta
modulo m, to

    u alpha = v beta modulo m,
    sign(u alpha) = sign(v beta).

Thus their residue/sign pairs differ by the action of the global unit
v inverse u. The converse follows directly by taking the common factor
to be O. A semilocally integral fractional generator is first cleared by
a denominator coprime to m, which is invertible modulo m, so the same
argument supplies a residue/sign representative.

The ordinary class numbers used here are one:

- O_1 in Q(sqrt(5)) has class number one;
- O_2=Z[2 sqrt(2)] has discriminant 32 and class number one. The order
  class-number formula gives h(32)=h(8)*2/[O_K^x:O_2^x]=1, since the
  fundamental unit 1+sqrt(2) has square 3+2 sqrt(2) as the first unit
  lying in O_2.

The same direct lemma applies to the separately preregistered d=12,f=3
overlap pilot after its own class-number check: its order has discriminant
117 and

    h(117)=h(13)*3*(1-1/3)/2=1.

The denominator is again two because
epsilon=(3+sqrt(13))/2 is not in O_3 whereas epsilon squared is the first
positive generator in O_3. This supplies a pilot-specific quotient
presentation only. It does not turn the monoid-resolution sequence into
an injective presentation for a general AFK order.
