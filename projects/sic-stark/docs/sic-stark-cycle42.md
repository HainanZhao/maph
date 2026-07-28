# SIC--Stark research cycle 42: the orientation sign is unconditional

Date: 2026-07-27

## Outcome

The analytic orientation has been certified rigorously:

\[
 \boxed{\operatorname{Im}L'_S(0,\chi_1)>0.}
\]

This removes the sign task from the remaining dimension-six theorem.

## Exact reduction

Let

\[
 D_j=\zeta'(0,g^j)-\zeta'(0,g^{j+3}),
 \qquad 0\leq j<3,
\]

and choose \(\chi_1(g)=\zeta_6\).  Fourier transformation gives

\[
 \Lambda=D_0+\zeta_6D_1+\zeta_6^2D_2
\]

and therefore

\[
 \operatorname{Im}\Lambda
 =\frac{\sqrt3}{2}(D_1+D_2).
\]

The exact characteristic-to-ray certificate gives

\[
 (3,5)\longmapsto g,\qquad
 (3,4)\longmapsto g^2.
\]

Kopp's convention-matched formula identifies each \(D_j\) with twice
the logarithm of the corresponding absolute principal overlap.

## Arb certificate

Certified double-sine integration gives

\[
\begin{aligned}
D_1&\in[2.046482\pm5.05\cdot10^{-7}],\\
D_2&\in[2.182996\pm7.34\cdot10^{-7}],\\
\operatorname{Im}\Lambda
&\in[3.662836\pm8.16\cdot10^{-7}].
\end{aligned}
\]

All three intervals are strictly positive.  The integration uses
interval fourth-derivative bounds for adaptive Simpson quadrature and an
explicit exponential tail majorant.

The algebraic candidate has the same orientation independently:
the exact root intervals give \(0<z,w<1\), so

\[
 \operatorname{Im}R
 =\frac{\sqrt3}{2}\bigl(\log z^{-2}+\log w^{-2}\bigr)>0.
\]

## Reproducibility

- `scripts/certify_dimension_six_orientation.py`
- `scripts/certify_dimension_five_double_sine.py`
- `scripts/dimension_six_ray_recon.gp`
- `scripts/dimension_six_scalar_closure.py`

The generalized interval integrator was regression-tested against all
four dimension-five certificates; its height-gap certificate still
passes.

