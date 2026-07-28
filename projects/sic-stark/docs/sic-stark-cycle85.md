# SIC--Stark research cycle 85: unconditional quadratic units

The supported quadratic characters cut out the fields
\[
L_0=\mathbb Q(h),\quad h^4-h^2-1=0,
\]
and
\[
L_1=\mathbb Q(r),\quad r^4-2r^2-4=0.
\]
Both have signature \((2,1)\), class number one, and successful
`bnfcertify`.

Writing \(\phi=(1+\sqrt5)/2\), the oriented relative units are
\[
u_0=\phi+h,\qquad
u_1=\frac{r+\phi}{r-\phi}.
\]
The analytic class-number formula gives unconditionally
\[
L'(0,\chi_0)=\log u_0,\qquad
L'(0,\chi_1)=\log u_1.
\]
Numerically,
\[
u_0=2.890053638\ldots,\qquad
u_1=18.891337596\ldots.
\]

The class fields, conductors, units, regulators, and analytic
identities are certified in
`scripts/dimension_eight_maximal_quadratic_units.gp`.

