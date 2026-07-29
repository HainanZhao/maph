# SIC--Stark research cycle 154: Outcome B+

Date: 2026-07-29

## Conditioning slopes

For a complex Arb ball \(Z_d(s)\), define
\[
 C_d(s)=
 \frac{\operatorname{rad}Z_d(s)}{|\operatorname{mid}Z_d(s)|}
 \bigg/
 \text{requested q-Pochhammer tolerance}.
\]
This removes the chosen tail tolerance and measures decimal precision
lost by the factorized continuation.

The pinned asymptotic regressions give
\[
 \log_{10}C_6(s)
 =2.8039716\,s^{-1}-14.9000,
 \qquad R^2=0.9999955,
\]
\[
 \log_{10}C_4(s)
 =0.6436017\,s^{-1}-17.0281,
 \qquad R^2=0.9999328.
\]
The slopes reproduce at a second precision. Against the actual endpoint
distance the coefficients are
\[
 \frac{12.87212}{|\tau-\beta_6|},
 \qquad
 \frac{1.439477}{|\tau-\beta_4|}.
\]

Thus the observed widening is neither logarithmic nor a stable power
law. It is essential exponential in \(1/s\) for this implementation.
The dimension-six slope is \(4.35669\) times the dimension-four slope.
This is not promoted to an intrinsic exponent of the open estimate:
dimension four is proved and exhibits the same pathology.

## Fresnel versus arithmetic strata

The six Fresnel frequencies satisfy
\[
 4b-5a\equiv0\pmod6.
\]
Under the two exact TCC frequency maps they become, respectively,
\[
 \{(0,0),(4,1),(2,2),(0,3),(4,4),(2,5)\}
\]
and
\[
 \{(0,0),(5,5),(4,4),(3,3),(2,2),(1,1)\}.
\]
These are exactly the six q-gamma singular-cancellation patterns,
including zero. The analytic classification is therefore coherent.

They are not the conductor-lowered stratum. Each Fresnel set has
denominator counts
\[
 (1,1,2,2)\quad\text{for denominators }(1,2,3,6),
\]
whereas the thirty growing modes have
\[
 (0,2,6,22).
\]
Only one of the three proved modulus-three orbit points is Fresnel for
either shift. The analytic wall is organized by Fourier direction, not
by conductor.

## Outcome B+

The remaining estimate is now written without SIC, TCC, ray-class, or
Stark notation in
`docs/dimension-six-standalone-estimate.md`. It defines the two-base
q-Pochhammer kernel, its three alias sums, the universal \(-q\)
one-period multiplier, the \(n\beta_6\) oscillations, the
\(n\asymp s^{-1}\) concentration window, and the constants
\(\sqrt{21}\) and \(t(\tau)=\tau+\tau^{-1}-5\).

The quantitative form BF\(_6(\eta)\) is
\[
 |\mathscr S_{a,b,r}(s)-\mathscr S^{\rm fus}_{a,b,r}|
 \le C|t(\gamma(s))|^\eta
\]
uniformly over the thirty growing modes. A Dini modulus would suffice.
BF\(_6(\eta)\) implies MFC\(_6\), the analytic-to-Stark bridge, and both
dimension-six shifts.

Paper III now has the intended Outcome-B+ spine:

1. the two-base lens identification;
2. the complete \(d=4:-q\), \(d=5:+q\), zero-mode
   \(-4\sqrt7\) calibration;
3. the exact multiplier ledger;
4. the standalone boundary estimate; and
5. the analytic-to-Stark bridge.

Executable certificates:

- `scripts/dimension_six_conditioning_comparison.py`;
- `scripts/dimension_six_fresnel_stratum_audit.py`.
