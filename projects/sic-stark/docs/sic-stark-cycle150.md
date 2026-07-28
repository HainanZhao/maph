# SIC--Stark research cycle 150: adversarial sweep

Date: 2026-07-28

## Independent checks

An independent integer implementation rechecked \(1476\) helical records
and recovered both characteristic coordinates in every case. It also
reproduced the two analytic exclusions:

1. for the fused dimension-six bilateral series,
   \(cd/(ab)=q^2\) and \(z=-q\), so Slater's strict annulus is
   \[
   |q|^2<|q|<1;
   \]
   it collapses at the RM boundary \(|q|=1\);
2. at \(g=Q\), the two Bernoulli asymptotics cancel and the remaining
   linear exponential cannot decay at both ends of a vertical contour.

Thus neither a boundary Slater substitution nor a pointwise contour
exchange has been silently restored.

## Perturbation battery

Every requested corruption is visible:

- flipping the even-wrap sign changes the dimension-five \(+q\) closed
  locus to a distinct rational test value;
- replacing \(\tau\) by its lower-half-plane conjugate moves the
  \(q\)-base outside the convergence disk;
- shifting the lens label by one corrupts the recovered first frequency
  in all \(36\) cases;
- swapping the labeled infinite place replaces the proved
  dimension-five root \(>1\) by its reciprocal \(<1\);
- replacing the trace \(5\) by \(6\) separates the two notions of
  fusion.

The last perturbation is particularly useful. If
\(\rho^2-6\rho+1=0\), the standard pair still fuses because
\(\rho+\rho^{-1}=6\), but the \(A_6\) fixed-point numerator is

\[
 24(\rho^2-5\rho+1)=24\rho\ne0.
\]

Hence standard base equality is not a substitute for the arithmetic
\(A_6\)-fixed-point condition.

## Status

| Audit | Status |
|---|---|
| Independent frequency ledger | `VERIFIED` |
| Slater at boundary | `EXCLUDED` |
| Undeformed contour exchange | `EXCLUDED` |
| Five convention perturbations | all detected |
| Fusion-continuity lemma | `OPEN` |

## Four-item checkpoint log

The subsequently requested gates are recorded exactly by
`scripts/dimension_six_checkpoint_gates.py`.

1. **Pinch:** `UNPINCHED_BUT_NOT_ABSOLUTELY_CONVERGENT`.  The two pole
   cones remain separated by \(Q\); the failure is loss of decay at
   imaginary infinity, not a finite collision and not a residue jump.
2. **Dimension-four even wrap:** the pre-registered prediction is
   confirmed. Exact exponent reduction gives
   \[
   -q\frac{(1-x)(1-ix)}{(1+qx)(1+iqx)},
   \]
   so the third proved calibration point is also at argument \(-q\).
3. **Dimension-five level bit:** analytic lens level \(15\), two alias
   parity classes, sign bit \(0\), hence argument \(+q\).
4. **Residue versus RM auxiliary value:** subsequently closed in
   Cycle 153. The two-base tilted prescription and the zero-mode
   Fresnel/Abel limit give reciprocal roots
   \(-2\sqrt7\pm3\sqrt3\), hence trace \(-4\sqrt7\), matching the
   independent AFK endpoint enclosure. This is a normalization
   calibration and does not prove the nonzero oriented limit.

No gate is silent.
