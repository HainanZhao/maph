# The standalone dimension-six boundary estimate

Date: 2026-07-29

This statement contains the remaining analysis without ray classes,
Stark units, SIC matrices, or TCC notation.

Put
\[
 \beta=\frac{5+\sqrt{21}}2,\qquad
 A=\begin{pmatrix}115&-24\\24&-5\end{pmatrix},
\]
and
\[
 \gamma(s)=
 \frac{\beta+\beta^{-1}s^2+i\sqrt{21}s}{1+s^2},
 \qquad s>0.
\]
Then
\[
 A\gamma(s)=\gamma(\beta^{-6}s).
\]
Set
\[
 t(\tau)=\tau+\tau^{-1}-5,\qquad
 \kappa(s)=2\pi|\Im(A\gamma(s)-\gamma(s))|.
\]
Exactly,
\[
 A\tau-\tau=-\frac{24\tau}{24\tau-5}t(\tau),
\]
and
\[
 t(\gamma(s))=i\frac{21}{\beta}s+O(s^2),\qquad
 \kappa(s)=
 2\pi\sqrt{21}(1-\beta^{-6})s+O(s^2).
\]

For \(\tau\in\mathbb H\), write
\[
 \omega=24\tau-5,\quad q=e^{2\pi i\tau},\quad
 \widetilde q=e^{2\pi iA\tau},\quad D=4\tau-1.
\]
For \(\mu\in\mathbb C\) and \(m\in\mathbb Z\), define
\[
 X(\mu,m)=e^{2\pi i(\mu+m)/24},
\]
\[
 \widetilde X(\mu,m)=
 \widetilde q\,
 e^{2\pi i(\mu+115m\omega)/(24\omega)},
\]
\[
 G_\tau(\mu,m)=
 \frac{(\widetilde X(\mu,m);\widetilde q)_\infty}
 {(X(\mu,m);q)_\infty}.
\]

For \(a,b\in\{0,\ldots,5\}\), put
\[
 \alpha_z=D\frac{4b-5a}{3}+2Dz,\qquad
 N_z=a+2-6z,
\]
\[
 K_{a,b}(z;\tau)=
 G_\tau(\alpha_z,N_z)
 G_\tau(-\alpha_z,4-N_z).
\]
For \(r=0,1,2\), the interior alias packet is
\[
 \mathscr S_{a,b,r}(s)
 =\sum_{k\in\mathbb Z}
 K_{a,b}(r+3k;\gamma(s)).
\]
It is absolutely convergent for \(s>0\). One alias period has the
universal boundary multiplier
\[
 -q=-e^{2\pi i\beta}.
\]
Thus the boundary oscillations have frequencies \(k\beta\) and the
additional antiperiodic factor \((-1)^k\). The active terms concentrate
where
\[
 |k|\asymp\kappa(s)^{-1}\asymp s^{-1}.
\]

The arithmetic small divisor is explicit:
\[
 \beta=[4;\overline{1,3}],
\]
\[
 (n\beta-m)(n\beta^{-1}-m)=m^2-5mn+n^2,
\]
so
\[
 \|n\beta\|\ge
 \frac1{\sqrt{21}n+\frac12},\qquad
 |1-e^{2\pi in\beta}|
 \ge\frac4{\sqrt{21}n+\frac12}.
\]

## BF\(_6(\eta)\): quantitative boundary fusion

For a boundary term, use the same \(24\)-factor continuation as in the
interior and define its Abel--Fresnel packet by
\[
 \mathscr S^{\rm fus}_{a,b,r}
 :=
 \lim_{\epsilon\downarrow0}
 \sum_{k\in\mathbb Z}
 e^{-\epsilon k^2}
 K_{a,b}(r+3k;\beta),
\]
with the inherited logarithm branch and level-\(24\) label.

> **Standalone estimate BF\(_6(\eta)\).** There exist
> \(\eta>0\), \(C>0\), and \(s_0>0\), independent of the thirty
> frequency pairs satisfying
> \[
> 4b-5a\not\equiv0\pmod6
> \]
> and of \(r=0,1,2\), such that
> \[
> \left|
> \mathscr S_{a,b,r}(s)
> -\mathscr S^{\rm fus}_{a,b,r}
> \right|
> \le C\,|t(\gamma(s))|^\eta
> \]
> for \(0<s<s_0\).

A Dini modulus tending to zero would suffice in place of the displayed
power. The Hölder form is stated because it is clean and falsifiable.
The six complementary frequency pairs are already handled by the
Fresnel/Abel prescription.

Since \(A\gamma(s)=\gamma(\beta^{-6}s)\), BF\(_6(\eta)\) makes the
boundary value invariant under the explicit hyperbolic return. Combined
with the already verified multiplier \(-1\), it implies the oriented
rank-one Stark identity over \(\mathbb Q(\sqrt{21})\); the existing
bridge theorem then implies both dimension-six TCC shifts.

## Conditioning measurement

At fixed Arb precision, divide the relative output radius by the
requested q-Pochhammer tolerance and call the result \(C_d(s)\). On the
pinned asymptotic windows:
\[
 \log_{10} C_6(s)
 =2.803972\,s^{-1}-14.9000,
 \qquad R^2=0.999996,
\]
\[
 \log_{10} C_4(s)
 =0.643602\,s^{-1}-17.0281,
 \qquad R^2=0.999933.
\]
Equivalently, against actual endpoint distance,
\[
 \log_{10}C_6
 \sim\frac{12.8721}{|\tau-\beta_6|},
\qquad
 \log_{10}C_4
 \sim\frac{1.43948}{|\tau-\beta_4|}.
\]

The slopes reproduce at a second precision. They show essential
exponential conditioning in \(1/s\) for this factorized-continuation
algorithm, not logarithmic or fixed-power widening. They are not
intrinsic exponents of BF\(_6\). The dimension-four answer is proved,
yet its raw continuation has the same pathology with a slope roughly
\(4.36\) times smaller. Numerical ill-conditioning therefore does not
imply failure of the boundary limit.

## Analytic versus arithmetic strata

The six Fresnel frequencies are
\[
 4b-5a\equiv0\pmod6.
\]
Under the exact frequency maps for both formal shifts, they coincide
with the six q-gamma singular-cancellation modes, including the zero
mode. This is an exact analytic coherence check.

They do **not** coincide with the conductor-lowered arithmetic stratum.
For either shift, the Fresnel set contains:
\[
 1\text{ denominator-1},\quad
 1\text{ denominator-2},\quad
 2\text{ denominator-3},\quad
 2\text{ denominator-6 characteristics}.
\]
The thirty growing modes contain two denominator-2, six denominator-3,
and twenty-two denominator-6 characteristics. Only one point of the
three-point proved modulus-three orbit is Fresnel. The analytic wall is
therefore a Fourier-direction phenomenon, not a conductor boundary.

Executable certificates:

- `scripts/dimension_six_conditioning_comparison.py`;
- `scripts/dimension_six_fresnel_stratum_audit.py`.
