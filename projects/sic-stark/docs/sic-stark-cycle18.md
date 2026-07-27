# SIC--Stark research cycle 18: the holomorphic-quartic gate

Date: 2026-07-27

## Outcome

Cycle 18 compares the cycle-17 fourth-moment target with the
holomorphic quartic of Bos and Waldron.  Their theorem is an exact
characterization of SIC overlaps on the unit torus, but its quartic
equation alone does not characterize the real-multiplication ghost.

The distinction is:

\[
\begin{array}{c|c}
\text{unit-torus SIC reconstruction}&
\text{RM ghost reconstruction}\\ \hline
A=A^\dagger&
G^\dagger=PGP\\
\operatorname{Tr}A^2=1&
\operatorname{Tr}G^2=1\\
\operatorname{Tr}A^4=1&
\operatorname{Tr}(PG)^4
 =(\operatorname{Tr}(PG)^2)^2
\end{array}
\]

For an ordinary Hermitian \(A\), the first two even moments force its
eigenvalue squares into the probability simplex, and the fourth
moment equals one only at a vertex.  For a parity-Hermitian ghost,
\(\operatorname{Tr}G^2\) is not the positive moment
\(\operatorname{Tr}G^\dagger G=\operatorname{Tr}(PG)^2\).
Replacing one by the other is invalid.

## 1. The published holomorphic quartic

Bos and Waldron reconstruct a matrix \(A=T(c)\) from overlap
coordinates \(c\).  On the overlap unit torus, the conjugation
condition makes \(A\) Hermitian and the fixed overlap magnitudes give

\[
\operatorname{Tr}A=\operatorname{Tr}A^2=1.
\]

Their Corollary 2.1 characterizes SIC overlaps by

\[
\operatorname{Tr}A^4=1.
\]

It is holomorphic after the unit-torus relations eliminate the
conjugate overlap variables.  This is closely related in shape to the
cycle-17 target, but the positivity is supplied by ordinary
Hermiticity on that specific locus.

The RM ghost is a different complex embedding of the overlap data.
Its real units obey reciprocal pairing rather than unit absolute
value, and its reconstructed matrix is parity-Hermitian rather than
ordinarily Hermitian.  The theorem's positivity argument therefore
does not automatically survive the embedding change.

## 2. Exact parity-Hermitian countermodel

There is a small exact model showing the gap.  In a parity eigenbasis
of dimension four, take

\[
P=\operatorname{diag}(1,1,1,-1)
\]

and

\[
G=
\begin{pmatrix}
1&0&0&0\\
0&1&0&0\\
0&0&-\frac12&\frac{\sqrt3}{2}\\
0&0&-\frac{\sqrt3}{2}&-\frac12
\end{pmatrix}.
\]

The lower block \(B\) satisfies

\[
B^\dagger
=\begin{pmatrix}1&0\\0&-1\end{pmatrix}
B
\begin{pmatrix}1&0\\0&-1\end{pmatrix},
\]

so \(G^\dagger=PGP\).  Its characteristic polynomial is

\[
(x-1)^2(x^2+x+1)=(x-1)(x^3-1),
\]

and its eigenvalues are

\[
1,\quad1,\quad\zeta_3,\quad\zeta_3^2.
\]

For every exponent not divisible by three, the three cube roots
contribute zero.  In particular,

\[
\boxed{
\operatorname{Tr}G
=\operatorname{Tr}G^2
=\operatorname{Tr}G^4
=1.
}
\]

Nevertheless

\[
\det G=1,\qquad \operatorname{rank}G=4.
\]

Thus parity-Hermiticity plus the first, second, and Bos--Waldron
fourth power traces does not imply rank one.  The third trace,
\(\operatorname{Tr}G^3=4\), visibly records the extra spectrum.

This model is not claimed to satisfy all RM characteristic identities.
Its purpose is narrower and exact: it proves that the
unit-torus/Hermitian hypothesis in the published quartic theorem
cannot be discarded merely because the ghost has parity-Hermiticity
and the same algebraic power traces.

## 3. Correct quartic for the ghost

Put \(J=PG\).  Then \(J=J^\dagger\), and multiplication by \(P\)
preserves rank.  The valid positive equation is

\[
\boxed{
\operatorname{Tr}J^4
=\bigl(\operatorname{Tr}J^2\bigr)^2,
\qquad J=PG.
}
\]

Equivalently,

\[
\frac12\left[
\bigl(\operatorname{Tr}(PG)^2\bigr)^2
-\operatorname{Tr}(PG)^4
\right]=0.
\]

The dimension-four countermodel has full rank, so this positive
quartic is strictly nonzero even though
\(\operatorname{Tr}G^4=1\).

There are therefore two genuinely different holomorphic-looking
expressions:

1. \(\operatorname{Tr}G^4-1\), transported algebraically from the
   unit-torus equation but insufficient on the larger
   parity-Hermitian locus;
2. \(\operatorname{Tr}(PG)^4-(\operatorname{Tr}(PG)^2)^2\), the
   positive rank certificate valid for the RM ghost.

Any proposed use of the published quartic must derive the second
identity or restore ordinary Hermiticity; the first identity alone
does not prove TCC.

## 4. Literature audit

The 2026 paper of Bengtsson and McConnell explains how products of
square roots of Stark units populate SIC overlaps and proves that
certain subfield contributions become \(\pm1\) in special dimension
families.  It supplies important arithmetic structure but does not
give a four-point convolution or fourth positive-moment identity.

The almost-flat SIC work studies additional overlap/component
relations in anti-unitary symmetric families.  Its authors explicitly
find that those relations do not determine the Stark units by
themselves.  These results are compatible with the gate above: special
line overlaps can simplify a pivot chart, but they do not evaluate the
global positive quartic.

No primary source located in this cycle proves

\[
\operatorname{Tr}(PG)^4
=\bigl(\operatorname{Tr}(PG)^2\bigr)^2
\]

for Shintani--Faddeev RM values.

## 5. Claim ledger

Proved in this cycle:

- the precise distinction between the Bos--Waldron quartic and the
  RM positive quartic;
- an exact dimension-four parity-Hermitian, full-rank countermodel
  with power traces \(1,1,1\) in degrees \(1,2,4\);
- necessity of retaining the unit-torus/ordinary-Hermitian hypothesis
  in the published theorem;
- failure of a direct holomorphic-quartic shortcut to TCC.

Still open:

- the positive RM fourth-moment identity;
- an RM-specific four-point cocycle theorem;
- TCC itself.

## Sources

- L. Bos and S. Waldron, *Equations for the overlaps of a SIC*,
  Corollary 2.1, [arXiv:2405.14123](https://arxiv.org/abs/2405.14123).
- I. Bengtsson and M. Grassl, *A Conjecture on Almost Flat
  SIC-POVMs*, [arXiv:2512.13201](https://arxiv.org/abs/2512.13201).
- I. Bengtsson and G. McConnell, *How Stark units enter SIC
  overlaps*, [arXiv:2606.23535](https://arxiv.org/abs/2606.23535).
- D. M. Appleby, S. T. Flammia, and G. S. Kopp,
  *A constructive approach to Zauner's conjecture via the Stark
  conjectures*, [arXiv:2501.03970](https://arxiv.org/abs/2501.03970).
