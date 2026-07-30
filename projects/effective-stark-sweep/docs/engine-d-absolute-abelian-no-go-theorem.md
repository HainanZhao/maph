# Engine D gate: absolute-abelian parity is a no-go theorem

**Date:** 2026-07-30  
**Status:** `VERIFIED_THEOREM`; promoted to a displayed paper lemma
**Scope:** one-place ray invariants over real quadratic fields

## The missing predicate

Let \(K/\mathbb Q\) be real quadratic, let
\(\mathfrak f\) be a finite modulus, and let \(N\) be the ray field for
\(\mathfrak f\infty_1\infty_2\). Put
\[
 A=\operatorname{Gal}(N/K),\qquad
 C=(\iota-1)A,
\]
where \(\iota\) is the non-trivial automorphism of \(K/\mathbb Q\).
Let \(B\) be the kernel of the map which forgets \(\infty_1\), so the
one-place field is \(H=N^B\).

The familiar formula
\[
 [H:H\cap\mathbb Q^{\rm ab}]
   =\frac{|CB|}{|B|}
   =\frac{|C|}{|B\cap C|}                         \tag{D.1}
\]
requires \(\iota(\mathfrak f)=\mathfrak f\). Only then does \(\iota\)
act on the *same* two-place ray group and only then is \(C\) the
commutator subgroup of a single normal closure over \(\mathbb Q\).
For a split prime ideal \(\mathfrak p\), conjugation instead maps the
ray problem modulo \(\mathfrak p\) to the different ray problem modulo
\(\bar{\mathfrak p}\). Expressing conjugated ideals in the original
ray coordinates does not define the action used in (D.1).

The W1 screen omitted this stability predicate. Its recorded
`shintani_index` and `commutator_size` remain exact outputs of that
coordinate calculation, but they have no maximal-absolute-abelian
interpretation when \(\iota(\mathfrak f)\ne\mathfrak f\).

## The corrected theorem

**Theorem D (absolute-abelian parity obstruction).** Let
\(\mathfrak f\) be conjugation-stable. If the right side of (D.1) is
one, then \(H/\mathbb Q\) is abelian. Every one-dimensional absolute
character restricts to the same archimedean parity at the two real
places of \(K\): either \((0,0)\) or \((1,1)\). Consequently no
character with one-place parity \((0,1)\) or \((1,0)\) is the
restriction of a Dirichlet character. In particular, an
absolute-abelian reduction cannot prove a substantive odd-on-\(R\)
one-place packet of order \(>2\).

**Proof.** Under modulus stability, \(N/\mathbb Q\) is Galois and
\[
 \operatorname{Gal}(N/\mathbb Q)
   =A\rtimes\langle\iota\rangle,\qquad
 [\operatorname{Gal}(N/\mathbb Q),
   \operatorname{Gal}(N/\mathbb Q)]=C.
\]
Equation (D.1) equal to one says \(C\subseteq B\). Hence the quotient
\(\operatorname{Gal}(N/\mathbb Q)/B=\operatorname{Gal}(H/\mathbb Q)\)
is abelian.

A Dirichlet character has a single parity, its value on complex
conjugation. On restriction to \(K\), the two real places are
conjugate over \(\mathbb Q\), so their parities agree. This gives only
\((0,0)\) and \((1,1)\). The differenced one-place invariant is
supported on characters non-trivial on the sign class \(R\), namely
characters of asymmetric parity. Such a character therefore cannot
come from the absolute Dirichlet group. This proves the obstruction.
\(\square\)

The parity step is independently present in the dimension-six
program's Cycle 101: a Dirichlet character changes both real parities
simultaneously and cannot move a \((0,1)\) character into the
totally-even or totally-odd sector.

## Complete census consequence

The corrected exact screen gives:

- former `index=1, commutator=1` proxy: 3,521 occurrences;
- conjugation-stable finite moduli within that proxy: 1,042;
- substantive new Engine-D occurrences among the stable rows: **0**;
- former proposed substantive Engine-D rows with unstable modulus:
  **276**.

The 3,521 proxy rows partition, without double counting, as
\[
  2552\ \text{empty-support}
  +693\ \text{substantive Engine A}
  +276\ \text{unstable-modulus false Engine-D candidates}.
\]
Thus the proposed census split
\[
 \texttt{FRONTIER}:1818\to1542,\qquad
 \text{substantive}:2483\to2759
\]
is rejected. The verified split remains unchanged pending a broader
repair of all conjugation-dependent B predicates.

## What the failed anchor gate taught us

The proposed controls RQ-000018, RQ-000032, and RQ-000274 all have
non-stable finite moduli. The first two one-place fields have mixed
signatures \((8,4)\) and \((6,3)\). A finite abelian extension of
\(\mathbb Q\) is Galois, hence is either totally real or totally
imaginary; a mixed signature is an immediate exact contradiction to
the proposed absolute-abelian interpretation.

Paper I's identification
\(M\simeq\mathbb Q(\zeta_{60})^+\) remains adjacent machinery, but it
illustrates the correct index-two situation: \(M\) is the maximal
absolutely abelian *subfield* of a mixed-signature non-Galois field
\(H\), not an identification of \(H\) itself with an absolute abelian
field.

## Tags and bulk disposition

- theorem and stability audit: `VERIFIED`;
- old 3,521 “abelian over \(\mathbb Q\)” wording:
  `RETRACTED_FALSE_INTERPRETATION`;
- 276-case D bulk: `CANCELLED_EMPTY_CORRECTED_POPULATION`;
- no analytic values, Arb recognitions, or theorem tags were promoted
  before this gate fired.
