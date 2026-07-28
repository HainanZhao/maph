# SIC--Stark research cycle 100: the Rankin--Eisenstein orientation gate

Date: 2026-07-28

## Question

Can the modular identification turn the missing value into a standard
Rankin--Selberg norm or a known modular-unit regulator?

## Exact orientation calculation

The coefficient field is

\[
 E=\mathbf Q(\zeta_6),\qquad \zeta_6^2-\zeta_6+1=0,
\]

and its nontrivial automorphism is

\[
 c(\zeta_6)=1-\zeta_6=\zeta_6^{-1}.
\]

In the basis \(1,\zeta_6\), this involution has matrix

\[
 \begin{pmatrix}1&1\\0&-1\end{pmatrix}.
\]

Both its fixed and anti-invariant subspaces are one-dimensional.  The
missing logarithmic resolvent has a nonzero anti-invariant component:
that component distinguishes \(\chi_1\) from \(\chi_5\).

A self Rankin--Selberg construction uses

\[
 \rho_f\otimes\rho_f^\vee
 =\mathbf 1\oplus\operatorname{Ad}^0(\rho_f).
\]

It is unchanged when \(f\) is replaced by \(f^c\).  It can therefore see
the norm/adjoint packet, but not the anti-invariant line that orients the
Stark unit.  This is the modular counterpart of the rational-character
obstruction in cycle 94.

The exact linear-algebra certificate is

```text
scripts/dimension_six_rankin_orientation_gate.py
```

## Modular-unit formulas do not automatically repair this

Known Siegel-unit regulator formulas evaluate regulators through
pairwise products of weight-one Eisenstein series or weight-two
modular-form values.  For example, Brunault's theorem gives regulators
of Siegel units in terms of such Eisenstein products
([arXiv:1504.08127](https://arxiv.org/abs/1504.08127)).
It does not identify the linear value \(L(1,\overline f)\) for this
cuspidal weight-one form.

A *linear* \(f\)-isotypic Eisenstein regulator could retain orientation,
but constructing and evaluating precisely that class is the new theorem
already isolated in cycle 96.  Merely taking \(f\overline f\), a
Petersson norm, an adjoint value, or a modular-unit norm cannot prove the
desired equality.

## Result

\[
\boxed{\text{standard norm/adjoint Rankin methods erase exactly the
missing orientation.}}
\]

The modular route remains viable only in a genuinely linear,
\(f\)-isotypic regulator construction.

