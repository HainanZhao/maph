# SIC--Stark research cycle 31: final dimension-six bridge audit

Date: 2026-07-27

## Outcome

The dimension-six analytic bridge has been re-audited after discovering
the order/maximal-order zeta mismatch in dimension eight.  No analogous
problem occurs here:

\[
 K=\mathbb Q(\sqrt{21}),\qquad
 \mathcal O_K=\mathbb Z[\beta],\qquad
 \beta=\frac{5+\sqrt{21}}2.
\]

The discriminant is the fundamental discriminant \(21\), so the
multiplier order is already maximal.  The modulus in Kopp's theorem and
the modulus used by PARI are both
\[
 (6)\infty_2.
\]

Every one of the eighteen characteristics for which
\[
 \gcd(a^2-5ab+b^2,6)=1
\]
was checked separately.  After choosing the representative
\(\widetilde a\equiv a\pmod6\) satisfying
\[
 b\beta'-\widetilde a>0,
\]
the principal ideal
\[
 (b\beta-\widetilde a)
\]
was mapped to its exact logarithm in
\[
 \operatorname{Cl}_{(6)\infty_2}(K)
 =\langle g\rangle\simeq C_6.
\]
For all eighteen characteristics,
\[
 2\log|\widetilde\nu_{a,b}|
 =
 Z'_{(6)\infty_2}(0,g^{\,\ell(a,b)}).
\]
The maximum numerical residual is
\[
 1.9\times10^{-9},
\]
which is at the accuracy of the elementary double-sine quadrature.

This simultaneously verifies:

- the labeling of the infinite place;
- the positive representative used in Kopp's correspondence;
- the ray generator and its direction;
- Kopp's exponent \(n=1\);
- the full-modulus Euler factors;
- the AFK phase after squaring; and
- the absence of a conductor-lowering correction in the primitive
  packet.

## The exact remaining statement

Let
\[
 \mathfrak p=(4\beta+1),\qquad N\mathfrak p=37,
\]
and let \(\sigma=\operatorname{Frob}_{\mathfrak p}\).  The exact ray
calculation gives \([\mathfrak p]=g\).  For the certified algebraic
candidate
\[
 \varepsilon=x^2
\]
write
\[
 r_j=\log|\sigma^j(\varepsilon)|.
\]
The quadratic component is unconditional:
\[
 L_S'(0,\chi_3)=r_0-r_1+r_2=2\log Y.
\]
The complete dimension-six theorem is therefore equivalent to the
single oriented identity
\[
\boxed{
 L_S'(0,\chi_1)
 =
 r_0+\zeta_6r_1+\zeta_6^2r_2,
 \qquad \chi_1(g)=\zeta_6.
}
\]
Its conjugate supplies \(\chi_5\), and Fourier inversion then gives the
complete primitive ray packet.

## Why the remaining identity is not a finite ambiguity

The algebraic Artin direction is fixed exactly by the norm-\(37\) prime.
Reversing \(g\) exchanges \(\chi_1\) and \(\chi_5\), so rational
subfield data, norms, class-number formulas, and reciprocal polynomials
cannot choose the imaginary part of the complex regulator.

Shintani's 1978 algebraicity theorem does not apply: the relevant ray
field is degree six over \(K\), rather than quadratic over its maximal
absolutely abelian subfield.  Roblot's sextic theorem excludes the wild
prime above \(3\), and in any event concludes only equality up to
absolute values.  The proved Brumer--Stark theorem concerns CM
extensions and does not cover this mixed-signature field.

In fact, merely extending Roblot's absolute-value theorem across the
wild prime would still be insufficient.  If
\[
 \Lambda_1=\rho e^{i\theta},\qquad
 q=L_S'(0,\chi_3),
\]
then Fourier inversion gives the real one-parameter family
\[
 D_j(\theta)
 =
 \frac{2\rho\cos(\theta-j\pi/3)+(-1)^jq}{3},
 \qquad 0\leq j<6.
\]
For every real \(\theta\),
\[
 D_{j+3}(\theta)=-D_j(\theta),
\]
and the exponentials are positive reciprocal pairs.  Hence the
quadratic identity, the primitive absolute value, positivity, and
Kopp's \(R\)-reciprocity leave an entire circle of possible packets.
They do not reduce the problem to the six Artin orientations of the
algebraic unit.

Consequently, a finite computation cannot promote the observed
agreement to a proof.  One must establish the displayed oriented
rank-one Stark identity, either directly from its period-one Shintani
cone or through a new wild cyclic-sextic theorem that proves the
oriented equality itself, not just its absolute value.

## Reproducibility

- `scripts/verify_dimension_six_ray_bridge.py`
- `scripts/dimension_six_ray_recon.gp`
- `scripts/dimension_six_primitive_fourier_audit.gp`
- `scripts/dimension_six_artin_orientation.gp`
- `scripts/dimension_six_shintani_cycle.py`
- `scripts/verify_dimension_six_conjugates.gp`
- `scripts/analyze_dimension_six_orientation_obstruction.py`

## Recommendation

Dimension six is fully reduced but not presently unconditional.  It
remains the smallest and cleanest target for a genuinely new analytic
result: one convention-fixed complex equality, with every finite and
class-field-theoretic label already certified.
