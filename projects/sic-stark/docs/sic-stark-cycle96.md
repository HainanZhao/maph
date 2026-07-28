# SIC--Stark research cycle 96: the modular route's exact boundary

Date: 2026-07-28

## What modularity adds

Cycle 95 identifies the missing primitive \(L\)-function with a single
weight-one newform \(f\) of level \(756\), nebentypus \(-7\), and
projective type \(D_{12}\).  The functional equation therefore converts
the missing derivative at zero into an explicitly normalized critical
value at one:

\[
 L'_K(0,\chi)
 \longleftrightarrow
 L(1,\overline f).
\]

The root number, gamma factor, conductor, and coefficient-field
orientation are now finite and computable.

## What modularity does not add

The form is real-dihedral, not imaginary-dihedral CM:

- the exact quadratic-base audit gives quadratic subfields of
  discriminants \(21,-3,-7\);
- only the original real base \(\mathbf Q(\sqrt{21})\) makes the
  relevant relative extension abelian; and
- neither imaginary quadratic subfield gives an elliptic-unit induction.

Thus the standard CM evaluation of \(L(1,f)\) by elliptic or Siegel units
is unavailable.

The normalized form also cannot be a single integral eta quotient.
Its exact Fourier coefficient at \(q^5\) is a nonrational multiple of
\(\sqrt{-3}\), whereas a normalized eta quotient with integral exponents
has integral Fourier coefficients.  Linear combinations of eta quotients
are not excluded, but an identity of that kind would still need a
period/regulator evaluation retaining the coefficient-field orientation.

## Sharpened next lemma

The most specific modular closure target is now:

> Construct an explicit modular unit or Eisenstein regulator class at
> level \(756\) whose \(f\)-isotypic regulator equals
> \(L(1,\overline f)\), and prove that its real-multiplication evaluation
> is the logarithmic resolvent of the certified ray unit
> \(x_{\mathrm{alg}}^2\), with the norm-\(37\) Frobenius orientation.

Such a lemma would prove

\[
 L'_S(0,\chi_1)
 =
 r_0+\zeta_6r_1+\zeta_6^2r_2
\]

and hence complete dimension-six TCC.

## Status after four distinct cycles

\[
\boxed{
\begin{array}{l}
\text{existing CM sextic theorem: excluded by signature;}\\
\text{Tangedal/Shintani level-three formula: already used, no level-six lift;}\\
\text{rational Artin induction: sees only the inversion-even packet;}\\
\text{weight-one modular form: identified exactly, unit evaluation still open.}
\end{array}}
\]

The modular identification is the cycle's durable advance.  The remaining
problem is no longer an unstructured search over special functions; it is
one oriented regulator identity for a uniquely specified modular form.

