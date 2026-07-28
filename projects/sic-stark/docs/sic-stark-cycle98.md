# SIC--Stark research cycle 98: exact functional-equation normalization

Date: 2026-07-28

## Result

For the primitive character \(\chi_1\), PARI's exact Hecke
\(L\)-function data gives:

\[
 N=756,\qquad
 (\mu_1,\mu_2)=(0,1),\qquad
 W(\chi_1)=i.
\]

With

\[
 \Gamma_{\mathbf R}(s)=\pi^{-s/2}\Gamma(s/2),
\]

the completed function is

\[
 \Lambda(s,\chi_1)
 =
 756^{s/2}
 \Gamma_{\mathbf R}(s)
 \Gamma_{\mathbf R}(s+1)
 L(s,\chi_1).
\]

Since
\(\Gamma_{\mathbf R}(s)\sim2/s\) at zero and
\(\Gamma_{\mathbf R}(2)=1/\pi\), the functional equation gives the
oriented identity

\[
\boxed{
 2L'(0,\chi_1)
 =
 \frac{i\sqrt{756}}{\pi}
 L(1,\overline{\chi_1}).
}
\]

The root number \(i\) is decisive: no unspecified sign or cyclotomic
phase remains in the passage from \(s=0\) to \(s=1\).

## Certificate

The script

```text
scripts/dimension_six_weight_one_functional_equation.gp
```

checks the exact conductor, gamma shifts, and root number, then verifies
the displayed formula numerically to more than \(100\) decimal places.

## New closure target

If

\[
 R_{\mathrm{alg}}
 =
 r_0+\zeta_6r_1+\zeta_6^2r_2
\]

is the certified logarithmic resolvent, then dimension six is now
equivalent to

\[
\boxed{
 L(1,\overline f)
 =
 \frac{2\pi}{i\sqrt{756}}R_{\mathrm{alg}},
}
\]

for the unique modular form \(f\) isolated in cycle 95.

This is a cleaner modular-period statement than the original derivative
formula.  It remains a mixed-signature Stark regulator identity, but all
analytic normalization constants and the orientation phase are now exact.

