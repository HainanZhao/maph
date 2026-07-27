# SIC--Stark research cycle 2: conjugation and the three-kernel normal form

Date: 2026-07-26

> **Cycle-3 update:** the special-value covariance posed below was proved by
> specializing the source's \(GL_2(\mathbb Z)\)-transformation theorem.
> The zero-output orbit is also automatic. Thus the unresolved equation
> count is one less than the orbit count displayed here; see
> `docs/sic-stark-cycle3.md`.

## Outcome

This cycle closes one question from sprint 1 and makes the main analytic
target substantially more explicit.

1. The two rank-one shifts \(0\) and \(1\) are equivalent under complex
   conjugation. It is enough to prove either one.
2. Every canonical \(L_d^3\) Jacobi-cocycle value is a product of three
   evaluations of the single \(S\)-kernel at geometrically scaled
   arguments.
3. The finite phase kernel is exactly invariant under simultaneous Zauner
   action. This reduces the \(d^2\) output equations to about \(d^2/3\)
   once the matching covariance of the special-value array is proved.

These are reductions, not a proof of the Twisted Convolution Conjecture.

## 1. Shift zero and shift one occur together

Section `sbsc:ProofMainTheoremsFurtherRemarks` of
Appleby--Flammia--Kopp proves that complex conjugation sends every valid
shift \(\lambda\) to another valid shift

\[
\bar\lambda=-(\lambda+d_j-1)\pmod d.
\]

In the rank-one family, \(m=1\) and \(d_j=d\). Therefore

\[
\boxed{\bar\lambda=1-\lambda\pmod d.}
\]

In particular, \(\bar0=1\) and \(\bar1=0\). Thus

\[
0\in\mathcal Z_t\quad\Longleftrightarrow\quad1\in\mathcal Z_t.
\]

This answers sprint-1 Question 2 without a new change-of-variable
calculation. It does **not** establish that either shift is valid; it proves
that a proof for one automatically supplies the other. The identity is
implemented as `canonical_shift_partner()`.

## 2. Exact lift of the level stabilizer

Let

\[
L=L_d=
\begin{pmatrix}d-1&-1\\1&0\end{pmatrix}.
\]

Direct multiplication gives

\[
L^3=I+dB_d,\qquad
B_d=
\begin{pmatrix}
d^2-3d+1&2-d\\
d-2&-1
\end{pmatrix}.
\]

Consequently \(L^3\) fixes every characteristic modulo \(d\). For
\(\boldsymbol r=\boldsymbol q/d\),

\[
(I-L^3)\boldsymbol r=-B_d\boldsymbol q\in\mathbb Z^2.
\]

The finite q-Pochhammer correction in the modular-to-Jacobi conversion has
integer index equal to the second component of this vector:

\[
n_d(\boldsymbol q)=q_2-(d-2)q_1.
\]

Both formulas are now executable as `canonical_level_quotient()` and
`canonical_characteristic_correction_index()`.

## 3. Three copies of one universal Jacobi kernel

Write \(\sigma_M(z,\tau)\) for the Shintani--Faddeev Jacobi cocycle with
zero translation characteristic. The canonical quadratic point satisfies

\[
\beta=\beta_d=d-1-\frac1\beta,\qquad L\cdot\beta=\beta,
\qquad j_L(\beta)=\beta.
\]

The canonical matrix has the period-one word

\[
L=T^{d-1}S,\qquad
S=\begin{pmatrix}0&-1\\1&0\end{pmatrix}.
\]

Apply the Jacobi cocycle law to \(A=L^3\):

\[
\sigma_{L^3}(z,\tau)=
\sigma_L\!\left(\frac{z}{j_{L^2}(\tau)},L^2\!\cdot\tau\right)
\,\sigma_L\!\left(\frac{z}{j_L(\tau)},L\!\cdot\tau\right)
\sigma_L(z,\tau).
\]

Here juxtaposition denotes multiplication. At \(\tau=\beta\),
\(j_{L^k}(\beta)=\beta^k\), and the functional equation
\(\sigma_{T^aS}=\sigma_S\) gives the uniform normal form

\[
\boxed{
\sigma_{L^3}(z,\beta)=
\sigma_S(z/\beta^2,\beta)\,
\sigma_S(z/\beta,\beta)\,
\sigma_S(z,\beta).
}
\]

The modular cocycle value
\(\mathfrak S^{\boldsymbol r}_{L^3}(\beta)\) differs from this expression
only by the explicit finite q-Pochhammer correction indexed by
\((I-L^3)\boldsymbol r\). The restricted TCC contains this \(L^3\) value
and an \(L^{-3}\) value; the latter is the reciprocal of its corresponding
\(L^3\) value by the modular cocycle law because \(\beta\) is fixed.

This completes the useful part of sprint-1 Question 1: the growing matrix
\(A_d\) no longer requires a dimension-dependent continued-fraction
expansion. The remaining analytic object is always the same \(S\)-kernel
(equivalently, the double sine/noncompact quantum dilogarithm), evaluated
three times.

Boundary-value qualification: the displayed identity follows first on the
common meromorphic domain and then at nonsingular real-multiplication
values by continuation. The singular characteristics still require the
representative convention used in the source TCC.

## 4. Exact Zauner covariance of the finite kernel

Set

\[
Z=I+L.
\]

The characteristic equation gives

\[
I+L+L^2\equiv0\pmod d,
\qquad Z\equiv-L^2\pmod d.
\]

Because \(Z\) is a polynomial in \(L\), it commutes with \(L\). Also
\(\det L=1\), so \(L\) preserves the symplectic form. Hence

\[
\boxed{
\langle L\boldsymbol p,ZL\boldsymbol q\rangle
=\langle\boldsymbol p,Z\boldsymbol q\rangle\pmod d.
}
\]

Moreover,

\[
\boldsymbol p+L\boldsymbol p+L^2\boldsymbol p=0\pmod d.
\]

Thus the finite phase in TCC is constant under simultaneous Zauner action.
If the special-value array \(u(\boldsymbol q)\) can be shown to obey
\(u(L\boldsymbol q)=u(\boldsymbol q)\), then changing variables
\(\boldsymbol q\mapsto L\boldsymbol q\) proves that the TCC residual is
constant on every Zauner orbit of \(\boldsymbol p\).

The number of potentially independent equations would then be

\[
N_d=
\begin{cases}
(d^2+2)/3,&3\nmid d,\\
d^2/3+2,&3\mid d.
\end{cases}
\]

At the end of this cycle the word “if” still mattered: only covariance of
the algebraic kernel had been proved. Cycle 3 closes this gap using the
source's transformation theorem.

## 5. New smallest target

Insert the three-\(S\)-kernel normal form and its finite correction into the
shift-\(1\) canonical TCC, then prove the missing characteristic covariance
or determine its exact phase defect:

\[
u(L\boldsymbol q)=\zeta_d(\boldsymbol q)\,u(\boldsymbol q).
\]

If \(\zeta_d=1\), the output equations reduce immediately to Zauner-orbit
representatives. If it is a nontrivial root of unity, the next task is to
test whether it cancels between the two special-value factors in the
convolution. This is now the highest-leverage unresolved calculation.

## Primary-source anchors

- Appleby--Flammia--Kopp, arXiv:2501.03970:
  Definition `dfn:shift`, equation `eq:tcc`, Lemma
  `lem:shiftslambdabar`, subsection
  `ssc:CalculatingShinFunction`, and equation `eq:sfjldecom`.
- Kopp, arXiv:2411.06763:
  Definitions `defn:sfjacobimaster`, `defn:sfmodular`, Proposition
  `prop:goose`, and the cocycle law.
