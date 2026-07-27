# Dimension-five unconditional-proof audit

Date: 27 July 2026

> **Later update on the same date.**  The obstruction recorded below has
> now been closed by combining Shintani's 1978 weak algebraicity theorem
> with an explicit exponent \(5760\), exact ray-field/Frobenius
> certificates, Arb interval evaluation, and Voutier height rigidity.
> See `docs/sic-stark-dimension-five-unconditional-closure.md`.  The
> historical audit below is retained because it explains why the direct
> quadratic-character shortcut fails.

## Result

The dimension-five calculation has reached a sharp boundary:

\[
\boxed{\text{the finite TCC packet is exact, but its analytic
identification is a published open rank-one Stark instance.}}
\]

No unconditional proof of the analytic identification is currently known.
This is not a failure of the minor computation. The missing equality is the
same \(\mathbb Q(\sqrt3)\), modulus-five example that Kopp published as a
conjectural Stark-unit recognition.

## What is unconditional

- \(\operatorname{Cl}_{(5)\infty_2}(\mathbb Q(\sqrt3))\cong C_8\), with
  sign class \(R=g^4\).
- Kopp's exponent is \(n=1\).
- All 24 positive characteristic lifts, ray logs, cocycle signs, and
  Kopp/AFK multiplier comparisons.
- The needed partial-zeta difference has character support
  \(k=1,3,5,7\), all of order eight.
- The unique quadratic character \(k=4\) has coefficient zero.
- The proposed degree-eight packet defines a field abstractly isomorphic to
  the required ray field.
- Rational Sturm intervals isolate the packet roots.
- Exact interval propagation certifies every `nfgaloisconj` label and
  uniquely selects factor four by the positive \(\sqrt5,\sqrt6\)
  embeddings.
- All 100 matrix minors vanish exactly for that labeled algebraic packet.
- The corrected Weyl calculation, including AFK's endpoint term
  \[
  \nu_0^{\rm aux}+(\nu_0^{\rm aux})^{-1}=-3\sqrt6,
  \]
  is equivalent to the canonical \(d=5,\lambda=1\) TCC identity.

The reconstruction entry \(T_{0,0}=\sqrt6\) is not
\(\nu_0^{\rm aux}\). It only packages the identity Weyl coefficient.

## Why the dimension-four shortcut cannot work

For \(\chi_k(g)=e^{2\pi i k/8}\), Fourier inversion gives the factor

\[
1-\chi_k(R)=1-(-1)^k.
\]

It kills every even \(k\), including the unique quadratic character, and
retains only the four faithful order-eight characters. Hence the required
value cannot factor through the unique quadratic subfield. Dedekind-zeta
quotients and ordinary regulator formulas do not isolate these four
additive character components.

## The exact open statement

Let

\[
U_k=\exp Z'_{(5)\infty_2}(0,g^k).
\]

The required input is

\[
(U_0,\ldots,U_7)
=(x^2,w^{-2},y^{-2},z^{-2},x^{-2},w^2,y^2,z^2),
\]

where the right side is selected by the certified rational intervals.
Already \(U_0=x^2\) is Kopp's published explicit example:

- G. S. Kopp, *Indefinite zeta functions*, §7, equation (7.21);
- G. S. Kopp, *A Kronecker limit formula for indefinite zeta functions*,
  Example 1.17, equation (3.12).

PARI's `bnrstark` reproduces the polynomial, but the
[PARI documentation](https://pari.math.u-bordeaux.fr/dochtml/html-stable/General_number_fields.html)
states that the Stark unit used by this routine is conjectural.
`bnfcertify=1` certifies the class group and units used by PARI; it does not
turn `bnrstark` into a proof of the Stark special-value equality.

## Direct-TCC bypass audit

A direct proof of the 24 double-sine convolution sums would avoid assuming
Stark algebraicity at the outset. The standard available routes do not
close it:

- the finite root-of-unity pentagon uses the wrong deformation parameter;
- the modular beta-integral specialization places all TCC samples strictly
  inside a pole-free strip, so residue localization cannot return them;
- ordinary reflection gives reciprocal products but not the required
  partial-Fourier exchange identities;
- ray-class character orthogonality acts on the whole residual packet and
  does not force an individual TCC coefficient to vanish;
- the 2026 Choie--Kumar real-quadratic limit formula concerns
  Zagier/narrow-class zeta values and natural arguments; it supplies no
  ray-class derivative-at-zero algebraicity or Artin law for this packet.

Thus a direct proof would require a genuinely new five-torsion identity
for the Shintani--Faddeev values, not a specialization of a currently
located transform identity.

## New local-isolation certificate

There is a useful new rigidity result. Take the four fan minors with row
pair \((0,1)\) and column pairs

\[
(0,1),\ (0,2),\ (0,3),\ (0,4).
\]

Their \(4\times4\) Jacobian with respect to \((x,y,z,w)\) has nonzero
determinant at the certified factor-four packet. This was checked by exact
number-field arithmetic, not numerically.

Consequently the rank-one packet is a reduced isolated point of these four
equations. Locally, the direct analytic TCC route is therefore not a soft
continuous identity: it pins the four values to algebraic coordinates.
This explains why proving TCC directly is capable of recovering the hard
algebraicity phenomenon rather than cheaply bypassing it.

Certificate:

- `scripts/dimension_five_local_isolation.gp`
- `certificates/dimension-five-local-isolation.txt`

## Honest next research target

The best remaining target is the smallest one:

\[
\boxed{\exp Z'_{(5)\infty_2}(0,I)=x^2.}
\]

A proof must introduce genuinely new input, for example:

1. an explicit rank-one Stark theorem for this \(C_8\) extension;
2. a new modular-unit/real-multiplication algebraicity theorem proving
   Kopp's example;
3. a new five-torsion Shintani--Faddeev identity proving the four isolated
   fan minors analytically.

Until one of these is supplied, “unconditional dimension-five proof” would
overstate the mathematics.
