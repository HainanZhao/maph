# Dimension-six state notes v3

Date: 2026-07-28

## Current theorem boundary

Dimension six is not yet proved unconditionally. The complete statement
is conditional on one named analytic lemma:

> **MFC\(_6\).** The primitive order-six logarithmic spectral resolvent,
> defined by any admissible tilted contour in the pole-free strip and
> with its branch continued from the two-base chamber, has a finite
> limit along the attracting \(A_6\)-axis, and spectral periodization
> commutes in that component with trace-five base fusion, preserving
> the norm-\(37\) Frobenius/lens label.

Only scalar geodesic convergence is assumed. Uniform convergence,
Hölder regularity, and two-sided continuity are not required.
Existence makes the limit \(A_6\)-invariant because the stabilizer
translates the same axis toward \(\beta_6\). This matches Kopp's
Definitions 4.7 and 4.9 and the upper-half-plane limiting realization
in Proposition 7.20.

Everything after this lemma is exact and verified.

## Promoted facts

- `VERIFIED`: \(A_6\beta_6=\beta_6\) and
  \(\beta_6+\beta_6^{-1}=5\).
- `ENCLOSED`: the direct two-base general modular gamma agrees with its
  24-factor Faddeev continuation at three interior points.
- `ENCLOSED`: all nine dimension-six bibasic alias classes at those
  points.
- `VERIFIED`: formal fusion gives the earlier dimension-six
  \({}_2\psi_2\) at argument \(-q\).
- `VERIFIED`: the dimension-five control fuses at \(+q\), the closed
  locus, and recovers its independently proved algebraic packet.
- `VERIFIED`: the specialized Sarkissian--Spiridonov meromorphic Fourier
  evaluation and its parameter map.
- `VERIFIED`: the interior identity as a meromorphic spectral identity.
- `VERIFIED`: \(A_6\equiv I\pmod6\),
  \(\psi^2(A_6)=-1\), and all 36 Kopp/AFK multiplier comparisons.
- `VERIFIED`: the conditional implication from fusion-continuity to both
  formal TCC shifts and form transport.
- `ENCLOSED`: the double-sine candidate and all 225 minor balls.
- `VERIFIED`: the exceptional endpoint \(-4\sqrt7\).
- `VERIFIED`: no finite pole pinch occurs at \(g=Q\); the endpoint
  failure is loss of decay at imaginary infinity.
- `VERIFIED`: the dimension-four fused packet is at \(-q\).
- `VERIFIED`: the dimension-five transcript has lens level \(15\),
  alias sign bit \(0\), and fused argument \(+q\).
- `VERIFIED`: admissible tilted contours give the same interior value
  by Cauchy's theorem in the pole-free strip.
- `VERIFIED`: the component split is six purely oscillatory/Fresnel
  modes and thirty one-sided-growing modes.
- `VERIFIED`: \(A_6\tau-\tau=
  -24\tau(\tau+\tau^{-1}-5)/(24\tau-5)\).
- `VERIFIED`: \(\beta_6=[4;\overline{1,3}]\) and
  \(\|n\beta_6\|\ge(\sqrt{21}n+\tfrac12)^{-1}\).
- `VERIFIED`: the zero-mode tilted/Fresnel normalization has reciprocal
  roots \(-2\sqrt7\pm3\sqrt3\) and trace \(-4\sqrt7\).
- `MEASURED`: for the factorized-continuation implementation,
  \(\log_{10}C_6(s)=2.8039716/s-14.9000\) and
  \(\log_{10}C_4(s)=0.6436017/s-17.0281\), with the slopes reproduced
  at a second precision.  These are implementation-conditioning slopes,
  not intrinsic exponents of the open boundary estimate.
- `VERIFIED`: under both exact TCC frequency maps, the six Fresnel modes
  are exactly the six q-gamma singular-cancellation modes.
- `EXCLUDED`: identifying those six modes with the conductor-lowered
  arithmetic stratum.  Only one point of the proved three-point
  modulus-three orbit is Fresnel; the analytic split is organized by
  Fourier direction rather than conductor.

## Excluded shortcuts

- `RETIRED`: equal-base \({}_2\psi_2\) as an interior representation.
- `EXCLUDED`: Slater's strict bilateral annulus at the RM boundary.
- `EXCLUDED`: absolute convergence of the undeformed vertical endpoint
  contour at \(g=Q\).
- `NOT APPLICABLE`: Garoufalidis--Kashaev Theorem 1.1 to the
  general-\(A_6\), \(\mathbb Z/24\)-labeled kernel.
- `NOT APPLICABLE`: rational-root Nahm-sum boundary theorems at the
  quadratic irrational endpoint.
- `EXCLUDED`: treating equality of the standard modular bases as a
  substitute for the \(A_6\) arithmetic fixed point.
- `OPEN`: enclosure-grade convergence of the nonzero tilted packet to
  the oriented boundary packet. The numerical rehearsal exposes
  rapidly worsening conditioning and is not promoted to a proof.

## Grade-2 conservation and Grade-3 gain

The S--S evaluation is a new integral-transform identity, but its
double-sine reduction leaves the oriented product

\[
 \Gamma_M(-\alpha,4-N)\Gamma_M(\alpha,N).
\]

It supplies no new finite multiplicative relation. At the rigid endpoint,
fusion is Grade-2 reduction-equivalent to the older oriented regulator
equality

\[
 L'_S(0,\chi_1)
 =r_0+\zeta_6r_1+\zeta_6^2r_2,
\]

using only the proved quadratic component, reciprocity, exact
\(C_6\) Fourier inversion, shift/reflection/duplication, conductor
lowering, and the multiplier ledger. No TCC equation or minor is used in
either endpoint reduction.

The full MFC\(_6\) statement remains strictly stronger: its limit
existence and fusion interchange do not follow from the rigid equality
through that basis. Thus the endpoint value is Grade-2 equivalent, but
the converse for MFC\(_6\) is open. This Grade-3 formulation supports
differentiation, contour
motion, lens-label variation, geodesic iteration, and
badly-approximable-point estimates. The exact tripwire is
`scripts/dimension_six_grade2_equivalence.py`.

## Next proof attack

Do not return to the retired equal-base interior series. The live
analysis should target one of:

1. a distributional boundary theorem for the meromorphic S--S Fourier
   transform at a hyperbolic fixed point;
2. a quantum-modular radial theorem at quadratic irrational points that
   retains the lens labels;
3. a direct comparison of the spectral continuation with Kopp's RM
   boundary cocycle, including the correction term forced by the
   trace-integrality locus.

Any proposed theorem must reproduce the dimension-five \(+q\) control
and the exact all-36 multiplier ledger.

## Parallel-screen conclusions

- Dimension seven, discriminant \(32\): complete and rerun.
- Dimension sixteen: Shintani index \(16\), so condition (0-9) fails.
- Paper I and Paper II release archives: deterministic and ready for
  authenticated Zenodo upload.
