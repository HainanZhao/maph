# SIC--Stark research cycle 5: the pentagon compatibility gate

Date: 2026-07-26

## Outcome

Cycle 4 proposed testing whether a published Fourier or pentagon identity
for the noncompact quantum dilogarithm descends to the primitive TCC
coefficient. The answer is:

\[
\boxed{\text{No known identity descends directly in the required
normalization and finite characteristic lattice.}}
\]

This is not a disproof of TCC, and it is not a proof that a new
quantum-dilogarithmic argument cannot work. It is a compatibility result:
the tempting direct applications fail for three independent, exact
reasons.

1. Faddeev's continuous Fourier identity evaluates the double sine on a
   vertical complex line. The TCC samples it on the real line.
2. The finite cyclic pentagon identity requires a root-of-unity
   deformation parameter. The canonical parameter \(\beta_d\) is
   irrational for every \(d\geq4\).
3. The general modular quantum dilogarithm attached to the actual matrix
   \(A_d=L_d^3\) has discrete modulus \(d(d-2)\), not \(d\), and its
   pentagon/beta identities retain a continuous integral.

The finite q-Pochhammer factors found in cycle 4 are essential to the
definition and periodicity of the Shintani--Faddeev values, but do not
alter any of these three structural facts.

The direct route should therefore stop here. A viable continuation would
need a new **real-multiplication localization theorem** that converts the
mixed sum--integral for the general modular quantum dilogarithm into the
finite \(d^2\)-term TCC transform.

## 1. Normalization dictionary

Put

\[
\beta=\beta_d,\qquad b=\sqrt{\beta},\qquad
c_0=\frac{1-\beta}{2}.
\]

In Kopp's normalization, Faddeev's quantum dilogarithm and the double-sine
kernel are related by

\[
\Phi_b(z)=\sigma_S(c_0-i b z,\beta).
\]

With the convention in Faddeev's 2012 pentagon paper,
\(\gamma(t)=\Phi_b(-t)\). Hence

\[
\boxed{
\gamma(t)=\sigma_S(c_0+i b t,\beta),\qquad
\sigma_S(s,\beta)=
\gamma\left(\frac{i(c_0-s)}{b}\right).
}
\]

This dictionary fixes the contour issue; it is not merely a difference
of notation.

Faddeev takes

\[
\omega=\frac{i}{2b},\qquad
\omega'=\frac{ib}{2},\qquad
\omega''=\omega+\omega'
 =\frac{i(b+b^{-1})}{2}.
\]

His Fourier duality is

\[
\int_{\mathbb R}
\gamma(t-\omega''+i0)e^{-2\pi ixt}\,dt
=\frac{c}{\gamma(x+\omega''-i0)}
\]

for an explicit constant \(c\). Under the dictionary above,

\[
\gamma(t-\omega'')
 =\sigma_S(1+i b t,\beta),
\qquad
\gamma(x+\omega'')
 =\sigma_S(-\beta+i b x,\beta).
\]

Thus the published transform runs along the vertical sigma lines

\[
1+i\sqrt{\beta}\,\mathbb R
\quad\text{and}\quad
-\beta+i\sqrt{\beta}\,\mathbb R.
\]

By contrast, cycle 4 showed that the primitive TCC quotient contains

\[
\sigma_S\left(\frac{z_{\boldsymbol q}}{\beta^k},\beta\right),
\qquad
\sigma_S\left(
\frac{z_{\boldsymbol q}+1/d}{\beta^k},\beta\right),
\quad k=0,1,2,
\]

where \(z_{\boldsymbol q}=(q_2\beta-q_1)/d\) is real. A contour rotation
from the published identity would cross poles and would require an
additional residue theorem. Replacing the continuous integral by a
finite discrete Fourier transform is therefore not a valid
specialization of that identity.

## 2. Exact cyclic-pentagon obstruction

Faddeev--Kashaev's finite-dimensional quantum dilogarithm is built at a
primitive root of unity. In the modular double-sine normalization, the
corresponding deformation parameter is an exponential of \(\beta\), such
as \(e^{i\pi\beta}\) depending on convention. Such an exponential is a
root of unity only if \(\beta\) is rational.

For the canonical family,

\[
\beta=\frac{d-1+\sqrt{\Delta_d}}2,
\qquad
\Delta_d=(d+1)(d-3)=(d-1)^2-4.
\]

Suppose \(\Delta_d=m^2\). Then

\[
(d-1-m)(d-1+m)=4.
\]

Both factors have the same parity. The only positive same-parity
factorization of \(4\) is \(2\cdot2\), which gives \(d=3\) and \(m=0\).
Therefore

\[
\boxed{\beta_d\notin\mathbb Q\quad\text{for every }d\geq4.}
\]

The finite cyclic pentagon is consequently an identity for a different
special function, not a finite evaluation of the modular
Shintani--Faddeev values in TCC.

The exact predicate `canonical_beta_is_rational()` checks this
discriminant condition.

## 3. The primitive shifts are not quasiperiods

The three adjacent sigma ratios shift their first arguments by

\[
\delta_k=\frac1{d\beta^k},\qquad k=0,1,2.
\]

Using

\[
\beta^2-(d-1)\beta+1=0,
\qquad
\beta^{-1}=d-1-\beta,
\]

their coordinates in the basis \((1,\beta)\) are

\[
\begin{aligned}
\delta_0&=\frac1d,\\
\delta_1&=\frac{d-1}{d}-\frac1d\beta,\\
\delta_2&=(d-2)-\frac{d-1}{d}\beta.
\end{aligned}
\]

None lies in the quasiperiod lattice
\(\mathbb Z+\beta\mathbb Z\) for \(d\geq4\). Therefore the ordinary
double-sine shift laws cannot turn an individual primitive quotient into
a finite product.

`canonical_primitive_sigma_shift_coordinates()` records the exact
rational coordinates, and
`canonical_primitive_sigma_shifts_are_quasiperiods()` checks the lattice
test.

## 4. Why the rarefied/general modular identity does not close the gap

The rarefied hyperbolic gamma function is the most relevant published
generalization because it includes a discrete variable. Its
star--triangle and pentagon identities are nevertheless mixed
sum--integrals:

\[
\sum_{m\bmod r}\int_{\mathcal C}
  \prod_j\Lambda(\text{continuous argument},
                  \text{discrete argument})\,dy
=\text{finite product}.
\]

The general modular quantum dilogarithm sharpens this comparison. For

\[
M=\begin{pmatrix}a&b\\c&d\end{pmatrix},
\]

its discrete variable is taken modulo \(|c|\). The matrix occurring in
the canonical SIC--Stark construction is

\[
A_d=L_d^3=I+dB_d,\qquad
B_d=
\begin{pmatrix}
d^2-3d+1&2-d\\
d-2&-1
\end{pmatrix}.
\]

Its lower-left entry is

\[
c=d(d-2).
\]

Consequently the native discrete modulus of the published general
modular identity is

\[
\boxed{k=d(d-2),}
\]

whereas the TCC characteristic grid is
\((\mathbb Z/d\mathbb Z)^2\). These moduli never agree for \(d\geq4\).
Moreover, the general modular beta and pentagon formulas still integrate
over a continuous contour.

In the decisive test case \(d=4\),

\[
\beta=\frac{3+\sqrt5}{2},\qquad
A_4=\begin{pmatrix}21&-8\\8&-3\end{pmatrix}.
\]

The published modular quantum dilogarithm therefore has discrete modulus
\(8\), while the primitive TCC residual is a \(16\)-term transform on
\((\mathbb Z/4\mathbb Z)^2\). The three primitive shifts have coordinates

\[
\left(\frac14,0\right),\qquad
\left(\frac34,-\frac14\right),\qquad
\left(2,-\frac34\right),
\]

so none is a quasiperiod.

These checks are implemented by
`canonical_general_modular_modulus()` and
`canonical_pentagon_compatibility_record()`.

## 5. Assessment of the finite q-Pochhammer corrections

The cycle-4 formula is

\[
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
\]

The correction index \(n(\boldsymbol q)\) is integral and changes by
\(d-2\). These factors:

- restore the characteristic-periodicity convention in the modular
  cocycle;
- contribute genuine zeros, poles, and phases that must be retained;
- can alter the value of the final finite Fourier coefficient.

But they do not:

- rotate Faddeev's continuous Fourier contour to the real sigma line;
- make the irrational deformation parameter a root of unity;
- change the lower-left entry of \(A_d\) from \(d(d-2)\) to \(d\);
- remove the continuous integral from the general modular identity.

Thus there is no unidentified scalar multiplier to cancel. The mismatch
occurs before an equality with the TCC sum can be written down.

## 6. The new research question

The pentagon idea remains viable only in the following stronger form.

> **Real-multiplication localization problem.** At the quadratic fixed
> point \(\beta_d\) and matrix \(A_d=L_d^3\), can a contour identity for
> the general modular quantum dilogarithm be localized to the
> characteristic lattice so that its continuous residues and
> \(d(d-2)\)-valued discrete index combine into
> \((q_1,q_2)\in(\mathbb Z/d\mathbb Z)^2\), with exactly the finite
> q-Pochhammer corrections and phase
> \(\omega_d^{-(q_1+q_2)}\) of primitive TCC?

A useful theorem must supply all of the following, not just a formal
pentagon relation:

1. a justified contour deformation with a finite residue set;
2. an explicit map from the modular discrete index and residues to the
   \(d^2\) characteristics;
3. exact recovery of the q-Pochhammer correction indices;
4. exact recovery of the symplectic Fourier phase;
5. cancellation of the remaining boundary or contour terms.

This is a precise new theorem, not a routine specialization. It may be
worth investigating because it would directly produce the missing
additive identity. It should first be tested at \(d=4\); failure of any
one of the five conditions would end the route cheaply.

## Recommendation

Do not continue trying to apply the standard continuous or cyclic
pentagon identity directly. That avenue is now closed by exact
compatibility checks.

Proceed only with a narrowly scoped localization cycle:

1. write the general modular sum--integral for \(A_4\);
2. list its poles in the normalization above;
3. test whether any natural contour deformation produces exactly the
   \(16\) TCC characteristics and their q-Pochhammer weights;
4. stop immediately if the residue count or phases disagree.

This minimizes further effort while preserving the only
quantum-dilogarithmic mechanism that could still have the correct
additive shape.

## Primary-source anchors

- Kopp, [arXiv:2411.06763](https://arxiv.org/abs/2411.06763):
  the relation between \(\Phi_b\) and \(\sigma_S\), and the
  Shintani--Faddeev cocycle.
- Faddeev,
  [arXiv:1201.6464](https://arxiv.org/abs/1201.6464):
  the continuous Fourier duality and Hilbert-space pentagon.
- Faddeev--Kashaev,
  [arXiv:hep-th/9310070](https://arxiv.org/abs/hep-th/9310070):
  the root-of-unity finite quantum dilogarithm and finite pentagon.
- Sarkissian--Spiridonov,
  [arXiv:1809.00493](https://arxiv.org/abs/1809.00493):
  rarefied hyperbolic gamma sum--integral identities.
- Sarkissian--Spiridonov,
  [arXiv:1910.11747](https://arxiv.org/abs/1910.11747):
  the general modular quantum dilogarithm, its discrete modulus, and
  general modular beta/pentagon sum--integrals.
- Appleby--Flammia--Kopp,
  [arXiv:2501.03970](https://arxiv.org/abs/2501.03970):
  the canonical SIC--Stark construction, q-Pochhammer corrections, and
  TCC.
