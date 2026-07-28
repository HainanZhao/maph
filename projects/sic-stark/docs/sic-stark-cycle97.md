# SIC--Stark research cycle 97: derived-Hecke and harmonic-Maass coverage

Date: 2026-07-28

## Question

Does the exact level-\(756\) weight-one identification bring the missing
value under a proved modular Stark theorem?

## Derived Hecke for dihedral forms

Darmon--Harris--Rotger--Venkatesh prove the derived-Hecke/Stark-unit
statement for both imaginary- and real-dihedral weight-one forms.  The
real-dihedral part uses indefinite theta series, real quadratic closed
geodesics, and the Dedekind--Rademacher modular unit.

The theorem does not evaluate the \(L\)-function needed here.  Its Stark
unit belongs to

\[
 \left(\mathcal O^\times\otimes
       \operatorname{Ad}^{*}(\rho_f)\right)^{G_{\mathbf Q}},
\]

and the relevant real-quadratic \(L(1)\) term comes from the totally odd
character appearing in the adjoint quotient.

For the dimension-six form, the unresolved function is instead

\[
 L(s,f)=L_K(s,\chi_1),
\]

where \(\chi_1\) has mixed signature: it is odd at exactly one real place.
Passing to \(\operatorname{Ad}(\rho_f)\) replaces the selected
mixed-signature character by conjugation-invariant quotient data.  That
is the same loss of orientation already certified in cycle 94.

## Harmonic Maass forms

Duke--Li relate coefficients of weight-one harmonic Maass forms to Galois
representations and, in special dihedral cases, to derivatives predicted
by Stark.  Their proved explicit framework focuses on prime levels
\(p\equiv3\pmod4\); it does not give a composite-level \(756\)
mixed-signature unit formula.  In the general cases the relevant
coefficient identities are evidence for, or reductions to, Stark
conjectures rather than a proof of the required ray-unit equality.

## Exact mismatch

\[
\boxed{
\begin{array}{c|c|c}
\text{object}&\text{signature/representation}&\text{status}\\ \hline
\text{derived-Hecke unit}
 &\operatorname{Ad}(\rho_f),\ \text{totally odd quotient}
 &\text{proved}\\
\text{dimension-six unit}
 &\rho_f,\ \chi_1\text{ mixed signature}
 &\text{still open}
\end{array}}
\]

The modular literature supplies a useful blueprint—closed geodesics,
Dedekind--Rademacher cocycles, and higher Eisenstein classes—but applying
it here requires a new *mixed-signature, non-adjoint* regulator formula.

## Primary sources

- H. Darmon, M. Harris, V. Rotger, and A. Venkatesh,
  *The derived Hecke algebra for dihedral weight one forms*,
  <https://arxiv.org/abs/2207.01304>.
- W. Duke and Y. Li, *Harmonic Maass forms of weight one*,
  <https://www.math.ucla.edu/~wdduke/preprints/weight%20one.pdf>.

