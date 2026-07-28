# SIC--Stark research cycle 111: exhaustive induction bases

Date: 2026-07-28

## Question

Could the two-dimensional target be induced from a one-dimensional
character over some base field not covered by the previous CM audit?

## Dimension argument

If

\[
 \rho\simeq\operatorname{Ind}_{G_F}^{G_{\mathbf Q}}\psi
\]

with \(\psi\) one-dimensional and \(\dim\rho=2\), then
\([G_{\mathbf Q}:G_F]=2\).  Thus \(F\) must be quadratic.  There are no
higher-degree induction bases to search.

The faithful projective quotient has exactly three quadratic subfields:

\[
 \mathbf Q(\sqrt{21}),\qquad
 \mathbf Q(\sqrt{-3}),\qquad
 \mathbf Q(\sqrt{-7}).
\]

The first is the original real induction base.  For each imaginary base,
the index-two projective subgroup is nonabelian.  If the restriction of
\(\rho\) split into one-dimensional characters, its projective image
would be simultaneously diagonalizable and hence abelian.  Therefore
the restrictions over the two imaginary bases are irreducible and
cannot induce \(\rho\).

The subgroup enumeration and abelianness tests are exact in

```text
scripts/dimension_six_quadratic_induction_audit.gp
```

## Result

\[
\boxed{\mathbf Q(\sqrt{21})\text{ is the unique one-dimensional
induction base for the target.}}
\]

Together with cycles 109--110, this exhausts both genuine induction and
projective-CM-plus-twist descent.

