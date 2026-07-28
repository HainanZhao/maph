# SIC--Stark research cycle 149: stabilizer and multiplier ledger

Date: 2026-07-28

## Exact ledger

The canonical matrix is

\[
 A_6=\begin{pmatrix}115&-24\\24&-5\end{pmatrix}
 \equiv I\pmod6.
\]

It therefore fixes all \(36\) level-six characteristics. Its Rademacher
invariant is \(6\), and hence

\[
 \boxed{\psi^2(A_6)=-1.}
\]

For \(\boldsymbol r=(a/6,b/6)\), direct substitution in Kopp's theta
character gives an exponent \(\theta_{a,b}\). Exact rational arithmetic
checks in every case that

\[
 (\psi^{-2}\chi_{\boldsymbol r}^{-1})(A_6)
 =
 \Phi_{a,b}^{\,2}.
\]

The executable ledger is
`scripts/dimension_six_stabilizer_ledger.py`.

## Conditional closing theorem

Assume the arithmetic fusion-continuity lemma from Cycle \(148'\).
Then the two-base spectral packet and the convention-matched AFK/Kopp
packet have the same boundary value with the same labels and multiplier.
Combining this with the two exact frequency bijections, the \(225\)
minor reductions, trace normalization, and the exceptional endpoint
\(-4\sqrt7\) proves that \(0\) and \(1\) are shifts for the canonical
dimension-six tuple. The already verified
\(\mathrm{GL}_2(\mathbb Z)\)-covariance transports this to every
admissible dimension-six tuple.

This theorem remains `CONDITIONAL`: the multiplier ledger does not prove
fusion-continuity.

## Three-grade equivalence tripwire

The earlier obstruction was the oriented identity

\[
 L'_S(0,\chi_1)
 =r_0+\zeta_6r_1+\zeta_6^2r_2.
\]

Grade 1 is deliberately not used: observing that both closure targets
imply TCC would say nothing.

At Grade 2, the **pointwise endpoint identity** is reduction-equivalent
to the displayed regulator identity. Fusion implies it by primitive
Fourier projection. Conversely, the regulator identity and its conjugate,
the proved quadratic component, and exact \(C_6\) Fourier inversion give
\[
 D_0=\frac{Q+2A+B}{3},\quad
 D_1=\frac{-Q+A+2B}{3},\quad
 D_2=\frac{Q-A+B}{3},
\]
where \(\Lambda_1=A+\zeta_6B\) and \(Q=D_0-D_1+D_2\).
Reciprocity supplies \(D_{j+3}=-D_j\);
shift/reflection/duplication and conductor lowering supply the remaining
characteristics; the multiplier ledger supplies all phases. No TCC
identity or minor is consumed. Conservation therefore holds for the
rigid endpoint value.

The literal flow-invariant continuity statement is not derived from the
regulator identity by this standard basis: existence and regularity of
the two-base boundary limit remain analytic inputs.

At Grade 3 the family formulation is materially different even though
its endpoint value is the same obstruction. It permits differentiation
in \(\tau\), contour motion, pinch/residue analysis, variation of the
lens label, iteration by the \(A_6\) return map, and
badly-approximable-point estimates. These operations do not exist on
the rigid regulator equality.

The exact audit is
`scripts/dimension_six_grade2_equivalence.py`; the standalone
analytic-to-Stark theorem is
`docs/dimension-six-analytic-to-stark-theorem.md`.

## Status

| Statement | Status |
|---|---|
| \(A_6\) fixes all 36 characteristics | `VERIFIED` |
| \(\psi^2(A_6)=-1\) | `VERIFIED` |
| Kopp/AFK multiplier match, all 36 cases | `VERIFIED` |
| Conditional TCC implication | `VERIFIED` as an implication |
| Grade-2 endpoint reduction | `EQUIVALENT` |
| Grade-3 family attack surface | `STRICTLY RICHER` |
| Arithmetic fusion-continuity | `OPEN` |
