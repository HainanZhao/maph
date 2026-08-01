# Semisimple descent criterion for a finite commutative ray monoid

**Status:** `PROVED` algebra lemma; AFK application `OPEN`
**Date:** 2026-08-01 UTC
**Claim boundary:** This supplies an exact finite-algebra criterion for
when a monoid-indexed packet has an ordinary-character expansion. It does
not prove that AFK's differenced-zeta packet meets the criterion, and hence
does not reopen the TCC sweep.

## Lemma

Let \(M\) be a finite commutative monoid, \(A=\mathbb C[M]\), and
\(J=\operatorname{Jac}(A)\). For a packet \(F:M\to\mathbb C\), write
\(\ell_F\in A^*\) for its linear extension. Then
\[
 \ell_F\in\operatorname{span}_{\mathbb C}\operatorname{Hom}_{\rm mon}
 (M,\mathbb C)
 \quad\Longleftrightarrow\quad \ell_F(J)=0.
\]

**Proof.** A monoid character extends uniquely to a unital algebra map
\(A\to\mathbb C\), and every such map vanishes on \(J\), proving the
forward implication. Conversely, \(\ell_F(J)=0\) means that \(\ell_F\)
is a functional on \(A/J\). This is a finite-dimensional commutative
semisimple complex algebra, hence
\(A/J\cong\mathbb C^r\). Its coordinate maps are precisely its algebra
maps to \(\mathbb C\), and their linear span is \((A/J)^*\). Pulling
back gives the desired character expansion. \(\square\)

The expansion is unique after equal characters are identified, because the
coordinate maps of \(\mathbb C^r\) are linearly independent.

## Consequence for the sweep

The lemma converts the missing all-order interface into four explicit
claims. For each AFK \((\mathcal O_f,d\mathcal O_f,\infty_2)\), one would
need to prove:

1. **Radical annihilation:** the relevant differenced-zeta functional
   \(\ell_Z\) vanishes on \(J\subset\mathbb C[\operatorname{Clt}]\);
2. **spectral identification:** determine the resulting character
   coefficients and all deleted Euler factors;
3. **quadratic criterion:** prove that the nonzero coefficients occur
   only on a precisely specified quadratic subset of the characters of
   \(A/J\); and
4. **arithmetic closure:** connect those coefficients to a Tate-compatible
   group/ray-class regulator theorem with preserved AFK labels.

If (1) fails, ordinary characters are mathematically incomplete by the
lemma. The local calculation in
`tcc-sweep-flat-monoid-zeta-obstruction-v1.md` gives an exact model where
it does fail. If (1) holds for a restricted AFK family, this criterion
would define a legitimate successor scan—but only after (2)--(4) are
proved as well.

This is a `PROVED` algebraic reduction of the theorem obligation, not a
claim that AFK satisfies radical annihilation.
