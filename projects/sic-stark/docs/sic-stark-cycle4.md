# SIC--Stark research cycle 4: the primitive Fourier obstruction

Date: 2026-07-26

## Outcome

The first nonzero canonical TCC equation has been reduced to an explicit
finite Fourier coefficient of adjacent Shintani--Faddeev special-value
ratios. For

\[
u_d(\boldsymbol q)=
\mathfrak S^{\,\boldsymbol q/d}_{A_d}(\beta_d),
\qquad
\rho_{\boldsymbol p}(\boldsymbol q)
=\frac{u_d(\boldsymbol q)}{u_d(\boldsymbol q-\boldsymbol p)},
\]

the entire shift-one TCC is

\[
\boxed{
\widehat{\rho_{\boldsymbol p}}^{\,\mathrm{sp}}
   (Z^{-1}\boldsymbol p)
=d^2\delta_{\boldsymbol p,\boldsymbol0},
}
\]

where \(Z=I+L_d\) and the superscript denotes the finite symplectic
Fourier transform.

For the smallest nonzero output \(\boldsymbol p=(1,0)\), the special-value
ratio has also been expanded exactly into three universal \(S\)-kernels
and two explicit finite q-Pochhammer corrections.

The main negative result is equally useful: Zauner covariance, reciprocal
pairing, characteristic periodicity, and the resulting cyclic telescoping
products do **not** imply the primitive equation. An exact dimension-four
countermodel has residual

\[
\frac32(1-i)\ne0.
\]

Thus the missing theorem must be additive: a finite Fourier,
star--triangle, pentagon, or equivalent convolution identity for the
actual special values.

## 1. TCC is one distinguished Fourier coefficient

Use the symplectic Fourier convention

\[
\widehat f^{\,\mathrm{sp}}(\boldsymbol k)
=\sum_{\boldsymbol q\in(\mathbb Z/d\mathbb Z)^2}
\omega_d^{\langle\boldsymbol k,\boldsymbol q\rangle}
f(\boldsymbol q).
\]

For the canonical family,

\[
Z=I+L_d\equiv
\begin{pmatrix}0&-1\\1&1\end{pmatrix}\pmod d,
\qquad
Z^{-1}\equiv
\begin{pmatrix}1&1\\-1&0\end{pmatrix}\pmod d.
\]

The matrix \(Z\) has determinant one, so it is symplectic. Hence

\[
\langle\boldsymbol p,Z\boldsymbol q\rangle
=\langle Z^{-1}\boldsymbol p,\boldsymbol q\rangle.
\]

After using the inverse cocycle law on the second special-value factor,
the canonical TCC residual is therefore precisely

\[
R_d(\boldsymbol p)
=\widehat{\rho_{\boldsymbol p}}^{\,\mathrm{sp}}
   (Z^{-1}\boldsymbol p).
\]

This formulation is implemented and checked by
`canonical_tcc_fourier_frequency()`.

For \(\boldsymbol e_1=(1,0)\),

\[
Z^{-1}\boldsymbol e_1=(1,-1),
\qquad
\langle(1,-1),(q_1,q_2)\rangle=-(q_1+q_2).
\]

The first primitive equation is consequently

\[
\boxed{
\sum_{q_1,q_2\bmod d}
\omega_d^{-(q_1+q_2)}
\frac{u_d(q_1,q_2)}{u_d(q_1-1,q_2)}
=0.
}
\]

## 2. Exact three-kernel primitive quotient

Let

\[
\beta=\beta_d
=\frac{d-1+\sqrt{(d+1)(d-3)}}2,
\qquad
z_{\boldsymbol q}
=\left\langle\frac{\boldsymbol q}{d},\beta\right\rangle
=\frac{q_2\beta-q_1}{d}.
\]

Cycle 2 proved

\[
A_d=L_d^3=I+dB_d,\qquad
B_d=
\begin{pmatrix}
d^2-3d+1&2-d\\
d-2&-1
\end{pmatrix},
\]

and \(j_{A_d}(\beta)=\beta^3\). The finite correction index in the
definition of the modular cocycle is

\[
n(\boldsymbol q)
=((I-A_d)\boldsymbol q/d)_2
=q_2-(d-2)q_1.
\]

Combining the definition of the modular cocycle with the cycle-2
factorization of \(\sigma_{L_d^3}\) gives

\[
u_d(\boldsymbol q)
=
\frac{
\displaystyle\prod_{k=0}^{2}
\sigma_S(z_{\boldsymbol q}/\beta^k,\beta)}
{\operatorname{qp}_{n(\boldsymbol q)}
 (z_{\boldsymbol q}/\beta^3,\beta)}.
\]

For the adjacent characteristic,

\[
z_{\boldsymbol q-\boldsymbol e_1}
=z_{\boldsymbol q}+\frac1d,
\qquad
n(\boldsymbol q-\boldsymbol e_1)
=n(\boldsymbol q)+d-2.
\]

Therefore

\[
\boxed{
\frac{u_d(\boldsymbol q)}
     {u_d(\boldsymbol q-\boldsymbol e_1)}
=
\frac{
\operatorname{qp}_{n(\boldsymbol q)+d-2}
 ((z_{\boldsymbol q}+1/d)/\beta^3,\beta)}
{\operatorname{qp}_{n(\boldsymbol q)}
 (z_{\boldsymbol q}/\beta^3,\beta)}
\prod_{k=0}^{2}
\frac{\sigma_S(z_{\boldsymbol q}/\beta^k,\beta)}
{\sigma_S((z_{\boldsymbol q}+1/d)/\beta^k,\beta)}.
}
\]

At integral characteristics, this is interpreted with the limiting
convention in the source definition. The correction-index relation is
checked by `canonical_primitive_correction_indices()`.

## 3. Why the elementary telescope stops here

For each fixed \(q_2\), set

\[
\rho_{q_2}(q_1)
=\frac{u_d(q_1,q_2)}{u_d(q_1-1,q_2)}.
\]

Characteristic periodicity gives the exact cyclic identity

\[
\prod_{q_1\bmod d}\rho_{q_2}(q_1)=1.
\]

The wrap in the \(q_2=0\) row is valid too: the only special zero value
cancels between adjacent terms, and periodicity is applied to the
nonintegral characteristics \((-1/d,0)\) and \(((d-1)/d,0)\).

This multiplicative identity does not determine the additive Fourier
coefficient

\[
\sum_{q_1}\omega_d^{-q_1}\rho_{q_2}(q_1),
\]

much less the subsequent weighted sum over \(q_2\).

The known elementary special-function shifts do not close this gap.
The finite q-Pochhammer recursion changes an integer product index, while
the double sine has quasiperiods \(1\) and \(\beta\). The adjacent TCC
ratio instead shifts \(z\) by \(1/d\), and shifts the three \(S\)-kernel
inputs by \(1/(d\beta^k)\). A multiplication formula may control the
product over all fractional shifts, but TCC is a weighted sum of their
quotients.

## 4. Exact countermodel

Dimension four has six Zauner-orbit representatives:

\[
(0,0),(0,1),(0,2),(0,3),(1,1),(2,3).
\]

Assign the orbit-constant values

\[
1,\ 2,\ 1,\ \frac12,\ 1,\ 1,
\]

respectively. This abstract array satisfies

\[
u(L_4\boldsymbol q)=u(\boldsymbol q),
\qquad
u(-\boldsymbol q)=u(\boldsymbol q)^{-1}.
\]

Its adjacent ratios telescope to \(1\) in every \(q_2\)-row. Grouping
the primitive sum by its phase exponent \(e=0,1,2,3\) gives exact rational
totals

\[
(C_0,C_1,C_2,C_3)
=\left(6,\frac92,\frac92,6\right).
\]

Since \(\omega_4=i\), its residual is

\[
C_0+iC_1-C_2-iC_3
=\frac32-\frac32i.
\]

This is not proposed as an array of Shintani--Faddeev values. It is a
logical counterexample showing that the symmetries and multiplicative
functional equations isolated so far cannot, by themselves, prove TCC.
`canonical_dimension_four_countermodel()` and
`canonical_tcc_orbit_model_phase_totals()` make the witness executable.

## 5. Best next question

The next cycle should not seek another orbit symmetry. It should ask:

> Does the Fourier transform or pentagon identity of the noncompact
> quantum dilogarithm descend, after the three-kernel factorization and
> finite q-Pochhammer corrections, to the finite Zak-transform identity
> \(\widehat{\rho_{\boldsymbol p}}^{\,\mathrm{sp}}
> (Z^{-1}\boldsymbol p)=0\)?

This route has the right algebraic shape. The \(S\)-kernel is a
noncompact quantum dilogarithm, whose operator pentagon identity has
finite-dimensional and star--triangle variants. Unlike quasiperiodicity,
those are additive or convolutional identities and could in principle
force a Fourier coefficient to vanish.

Concrete next steps:

1. write the known Fourier transform of the \(S\)-kernel in the present
   normalization;
2. compute the finite Zak transform over the characteristic lattice
   \((1/d)\mathbb Z^2/\mathbb Z^2\);
3. track the \(n(\boldsymbol q)\) finite corrections through that
   transform;
4. test whether the three factors associated to \(L_d^3\) compose by a
   pentagon/star--triangle move;
5. if they do not, use the exact formula above to identify the residual
   multiplier rather than adding more symmetry hypotheses.

## Primary-source anchors

- Appleby--Flammia--Kopp, arXiv:2501.03970:
  definitions `dfn:variantqPochhammer`, `df:shinfadjacocycle`,
  `def:shin`; equations `eq:sfjcocyclerelInt`, `eq:shindf`, and
  `eq:tcc`; lemmas `lm:shinperiodicity` and `lm:shinatzero`.
- Kopp, arXiv:2411.06763:
  double-sine quasiperiodicity and the Shintani--Faddeev cocycle laws.
- Faddeev--Kashaev, arXiv:hep-th/9310070:
  the quantum-dilogarithm pentagon identity, its finite-dimensional
  realization, and relation to a restricted star--triangle relation.
- Faddeev, arXiv:1201.6464:
  a Hilbert-space form of the modular quantum-dilogarithm pentagon.
