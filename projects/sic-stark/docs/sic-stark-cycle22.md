# SIC--Stark research cycle 22: explicit modulus-four ray field

Date: 2026-07-27

## Outcome

The candidate class field in cycle 21 simplifies to

\[
\boxed{
K_{(4)\infty_2}=K(\sqrt\phi),
\qquad
K=\mathbb Q(\sqrt5),\quad
\phi=\frac{1+\sqrt5}{2}.
}
\]

Moreover, the target Stark unit is

\[
\boxed{x^2=\phi+\sqrt\phi.}
\]

This proves that the proposed algebraic value lies in the correct ray
field and has the correct Artin conjugate and norm.  It does not yet
prove that the analytic double-sine invariant equals that unit.

## 1. Radical collapse

The square proposed in cycle 21 was

\[
x^2=
\frac{1+\sqrt5+\sqrt{2+2\sqrt5}}2.
\]

Since

\[
1+\sqrt5=2\phi,\qquad
2+2\sqrt5=4\phi,
\]

this becomes

\[
x^2=\phi+\sqrt\phi.
\]

Its nontrivial conjugate over \(K\) is

\[
\phi-\sqrt\phi.
\]

Using \(\phi^2=\phi+1\),

\[
(\phi+\sqrt\phi)(\phi-\sqrt\phi)
=\phi^2-\phi=1.
\]

Thus the Artin conjugate is \(x^{-2}\), exactly as predicted.

## 2. Conductor and infinite place

Let \(L=K(\sqrt\phi)\).  The element \(\sqrt\phi\) is integral, and the
basis \(1,\sqrt\phi\) has discriminant

\[
4\phi.
\]

Because \(\phi\) is a unit, the corresponding discriminant ideal is

\[
\mathfrak d_{L/K}=(4).
\]

There is no integral half-basis reducing this discriminant: an element
\((a+b\sqrt\phi)/2\) with an odd numerator would have incompatible
trace or norm integrality at the dyadic prime.  Hence the displayed
relative discriminant is exact.

At the distinguished embedding,

\[
\phi>0,
\]

so \(L\) remains real.  At the conjugate embedding,

\[
\phi'=\frac{1-\sqrt5}{2}<0,
\]

so that real place becomes complex.  The complete conductor is
therefore

\[
(4)\infty_2.
\]

By the conductor--discriminant theorem, \(L/K\) is the quadratic
extension belonging to a character of this ray group.  Cycle 21
computed that the group itself has order two.  Consequently \(L\) is
the full ray class field for the stated modulus.

## 3. Exact Artin packet

Writing

\[
u=\phi+\sqrt\phi,
\]

the two ray conjugates are

\[
u,\quad u^{-1}=\phi-\sqrt\phi.
\]

They satisfy

\[
N_{L/K}(u)=1,\qquad
\operatorname{Tr}_{L/K}(u)=2\phi=1+\sqrt5,
\]

and hence

\[
u^2-(1+\sqrt5)u+1=0.
\]

The cocycle square roots give

\[
\pm\sqrt u,\qquad \pm\frac1{\sqrt u},
\]

with relative polynomial

\[
X^4-(1+\sqrt5)X^2+1.
\]

## 4. Remaining theorem

The arithmetic candidate is now completely identified.  The sole
dimension-four analytic target is

\[
\left(
\sqrt2\,
\frac{S_2(\beta/4)S_2(1/4)}
{S_2((\beta+1)/4)}
\right)^2
=\phi+\sqrt\phi.
\]

Kopp's theorem identifies the left side with an exponentiated partial
zeta derivative.  Proving the displayed equality requires evaluating
that derivative as the specific ray unit \(u\), not merely proving
that it is an algebraic unit in the same field.

This is the precise Stark step.  All ambiguity about the field,
conductor, Galois action, norm, and square-root degree has been removed.

## Sources

- G. Kopp, *The Shintani--Faddeev modular cocycle*,
  [arXiv:2411.06763](https://arxiv.org/abs/2411.06763).
- T. Shintani, *On certain ray class invariants of real quadratic
  fields*, [JMSJ 30 (1978), 139--167](https://doi.org/10.2969/jmsj/03010139).
