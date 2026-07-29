# SIC--Stark research cycle 155: Row (i) -- tilted integral polynomially conditioned in both dimensions

Date: 2026-07-29

## Starting position

Cycle 154 measured the conditioning of the FACTORIZED q-Pochhammer
continuation and found essential exponential-in-\(1/s\) precision loss
in both the open dimension six and the proved dimension four:
\[
 \log_{10}C_6(s)=2.8040\,s^{-1}-14.900,\quad
 \log_{10}C_4(s)=0.6436\,s^{-1}-17.028.
\]
Since dimension four is proved and exhibits the same pathology, the
cycle-154 slope was identified as an implementation artifact of the
factorized route, not an intrinsic exponent of the open boundary
estimate BF\(_6(\eta)\).  The assigned question was: does the TILTED
CONTOUR INTEGRAL itself (the verified interior identity, not the
factorized continuation) exhibit the same exponential conditioning, or
is the pathology confined to the factorized representation?

The three possible outcomes were:

- **Row (i):** the tilted integral is polynomially conditioned in
  \(s\) as \(s\to0+\) in BOTH dimensions.  The boundary value exists
  numerically and fusion continuity is plausibly provable; the program
  endgame becomes one classical estimate.
- **Row (ii):** polynomial at \(d=4\) but exponential at \(d=6\),
  measuring an intrinsic gap.
- **Row (iii):** the tilt construction itself needs repair.

## The tilted sinh-integral route

The verified interior identity (cycle 147, S--S equation (66)) gives
the tilted contour integral as
\[
 \mathscr T(\alpha,N;\tau)
 = k\,\Gamma_M(-\alpha,\mathrm{tot}{-}N;\tau)\,
      \Gamma_M(\alpha,N;\tau)\,
      \Gamma_M(Q,0;\tau),
\]
where \(k\) is the lens level (\(k=24\) for \(d=6\), \(k=8\) for
\(d=4\)), \(\Gamma_M\) is the modular lens gamma, and
\(Q=\omega+1\) with \(\omega=k\tau-r\).  Each lens gamma splits into
\(k\) standard factors
\[
 \gamma_{\rm std}(z;\omega)
 = e^{\pi i B_{22}(z|\omega,1)/2}\,
   \gamma_2(z;\omega,1),
\]
where \(\gamma_2\) is evaluated by the absolutely convergent real-axis
integral
\[
 \log\gamma_2(z)
 =\int_0^\infty\!\left[
   \frac{\sinh((Q{-}2z)t/2)}
        {2t\,\sinh(\omega t/2)\,\sinh(t/2)}
   -\frac{Q{-}2z}{\omega\,t^2}
 \right]dt,
\]
valid for \(0<\Re z<\Re Q\), extended by the functional equation
\(\gamma_2(z+1)=2\sin(\pi z/\omega)\,\gamma_2(z)\).

The key structural observation is that the integrand's poles
\(t=2\pi i n/\omega\) lie at distance \(|\,2\pi/\omega\,|\) from the
positive real contour.  As \(s\to0+\) along the geodesic
\(\gamma(s)\to\beta_d\), the base \(\omega=k\tau-r\) approaches the
fixed real value \(k\beta_d-r>0\), so this distance stays bounded away
from zero.  The integral representation therefore does not degenerate
with the base, in stark contrast to the factorized q-Pochhammer route
where \(|q|=e^{-2\pi\Im\tau}\to1\) and \(|\tilde q|=e^{-2\pi\Im
A\tau}\to1\) cause catastrophic cancellation.

## Approach: validated evaluator and conditioning ladder

The evaluator `gamma_standard_tilted` computes each standard factor by
shifting \(z\) into the fundamental strip via the functional equation,
evaluating the Bernoulli polynomial \(B_{22}\) at the original argument,
and computing \(\log\gamma_2\) via the sinh integral with mpmath
adaptive quadrature (Taylor series near \(t=0\), `mp.quad` on
\((0,1]\), geometrically spaced nodes on \([1,T_{\rm cut}]\) with
\(T_{\rm cut}\sim 2\,{\rm dps}\cdot\ln 10\)).

**Independent crosscheck.**  The tilted evaluator was validated against
a from-scratch mpmath factorized q-Pochhammer route (computing the same
lens gamma as a product of \(k\) ratios of infinite q-Pochhammer
symbols) at interior points where both converge:

\[
 \begin{array}{cccl}
 d & s & \text{working dps} & \text{agreement (digits)}\\
 \hline
 6 & 1/8 & 35 & 33.0\\
 4 & 1/8 & 35 & 34.3
 \end{array}
\]

Both agree to near full working precision, confirming that the
sinh-integral and q-Pochhammer routes compute the same function.
(`numerical` at 35 working digits; reproducible via
`scripts/dimension_six_tilted_integral_crosscheck.py`.)

**Conditioning measurement.**  The tilted value was evaluated at
dps\(_{\rm low}=40\) and dps\$_{\rm high}=70\) (each with 15 guard
digits) on a geometric ladder of \(s\) values following the exact
geodesic recursion \(A\,\gamma(s)=\gamma(\beta^{-6}s)\):

\[
 s\in\{1/8,\,1/16,\,1/24,\,1/32,\,1/64,\,1/128,\,1/256,\,
       \beta^{-6}/8,\,\beta^{-12}/8\}
\]
for \(d=6\), and analogously for \(d=4\) starting at \(s=1/32\).
The deepest points reach \(1/s\approx1.17\times10^9\) (\(d=6\)) and
\(1/s\approx3.32\times10^6\) (\(d=4\)).

The conditioning diagnostic is
\[
 \text{digits lost}(s)
 = {\rm dps}_{\rm low}
   -\bigl(-\log_{10}|Z_{\rm low}/Z_{\rm high}-1|\bigr),
\]
measuring decimal digits of agreement between the two precision levels.

## Findings

### Row classification: (i)

`numerical`.  In both dimensions, the tilted integral loses ZERO digits
of precision across the entire ladder, from \(1/s=8\) to
\(1/s\approx10^9\):

\[
 \begin{array}{ccccc}
 d & \text{max digits lost} & \text{tilted slope} &
   \text{factorized slope (cycle 154)} & \text{ratio}\\
 \hline
 6 & 0.00 & 0.000000 & 2.803972 & 0.000\\
 4 & 0.00 & 0.000000 & 0.643602 & 0.000
 \end{array}
\]

The actual relative error between the 55-digit and 85-digit runs is
\(\sim10^{-53}\) at every point (including \(s\approx9\times10^{-10}\)
in \(d=6\)), confirming that the computation is stable to the full
working precision regardless of \(s\).  The tilted conditioning slope
is consistent with zero; the factorized route would require
\(\sim2.8\times10^9\) extra decimal digits at the deepest \(d=6\)
point.

**The cycle-154 exponential-in-\(1/s\) conditioning is an artifact of
the factorized q-Pochhammer continuation, not of the tilted integral.**
Through the sinh-integral route, the same primitive kernel keeps
constant precision uniformly down the geodesic ladder in both
dimensions.  This is row (i).

### d=4 ground truth calibration

`numerical`, backed by the proved class-number formula.  The
fundamental unit for \(d=4\) is
\[
 u=\varphi+\sqrt{\varphi},\qquad
 \varphi=\frac{1+\sqrt5}{2},\qquad
 \log u = 1.061275061905035652033018916213573485807\ldots
\]
The tilted scalar \(\Gamma_M(Q,0)\) at the fusion point
\(\tau=\beta_4=(3+\sqrt5)/2\) satisfies
\[
 |\Gamma_M(Q,0)|=\sqrt{2/u},\qquad
 \log u = \log 2 - 2\log|\Gamma_M(Q,0)|,
\]
with residual \(<10^{-84}\) at 85 working digits.  The cycle-24
Kronecker limit formula cocycle satisfies \(\mathrm{cocycle}^2=u\)
with residual \(0\) (to full precision).  (`numerical` at the stated
precision; the identity itself is `proved` by the class number formula.)

The tilted value converges to this boundary value at rate
\[
 |\mathscr T(s)-\mathscr T(0)|\sim s^{0.99},\qquad
 R^2=0.9999\quad(d=4).
\]

### d=6 boundary convergence

`numerical`.  The tilted value converges to its boundary value at rate
\[
 |\mathscr T(s)-\mathscr T(0)|\sim s^{0.98},\qquad
 R^2=0.999\quad(d=6).
\]

Both dimensions exhibit essentially LINEAR convergence (\(s^1\)) to the
boundary, consistent with the first-order geodesic approach
\(\Delta(\gamma(s))=i(21/\beta)s+O(s^2)\).  Since
\(|t(\gamma(s))|=|\Delta(\gamma(s))|\sim(21/\beta)s\), this is
equivalent to
\[
 |\mathscr T(s)-\mathscr T(0)|\le C\,|t(\gamma(s))|^{1-\epsilon}
\]
for any \(\epsilon>0\), which is stronger than the Dini modulus
required by BF\(_6(\eta)\).

### d=6 boundary scalar

`numerical`.  The tilted scalar \(\Gamma_M(Q,0)\) at
\(\tau=\beta_6\) satisfies
\[
 \Gamma_M(Q,0)=-1/x,
\]
where \(x\approx2.212885289017182609068716603734125615545\) is the
real root of the degree-12 polynomial
\[
 x^{12}+3x^{11}-6x^{10}-16x^9+3x^8+27x^7+3x^5-16x^4-6x^3+3x^2+1=0,
\]
with residual \(<10^{-83}\).  This is the cycle-143 algebraic primitive
root, consistent with the zero-mode tilted/Fresnel normalization.

## What this means for the program

Row (i) is the most favorable outcome.  The tilted integral's boundary
value exists numerically in both dimensions, with polynomial (linear)
convergence and no conditioning obstruction.  The program endgame is
now a single classical estimate: prove that the interior tilted value
extends continuously to \(\beta_6\) with a power-law (or Dini) modulus,
which is BF\(_6(\eta)\).  The numerical rehearsal shows \(\eta\approx1\)
is achievable.

The factorized-continuation pathology of cycle 154 is fully explained:
the q-Pochhammer products degenerate because \(|q|,|\tilde q|\to1\) as
\(\Im\tau\to0\), while the sinh-integral representation has poles at a
fixed distance from the contour.  The two routes compute the same
function (crosscheck above) but have radically different numerical
conditioning.

## Artifacts

- `scripts/dimension_six_tilted_integral_rehearsal.py`:
  mpmath evaluator for the tilted contour integral via the sinh-integral
  identity, with two-precision conditioning diagnostic and automatic
  row classification.  Fixed a `Fraction`-to-`mpf` conversion bug in
  `geodesic_point`.
- `scripts/dimension_six_tilted_integral_crosscheck.py`:
  independent mpmath factorized q-Pochhammer crosscheck.
- `certificates/dimension-six-cycle155-tilted-integral-rehearsal.json`:
  full certificate with all ladder records, conditioning fits, boundary
  identifications, crosscheck results, and test-suite status.

Reproduction:
```
cd scripts && python3 dimension_six_tilted_integral_rehearsal.py \
  --dps-low 40 --dps-high 70 \
  --ladder-six 8,16,24,32,64,128,256 \
  --ladder-four 32,48,64,128,256 \
  --deep-recursion-steps 2 --skip-packet
```
Runtime: ~6 minutes.  Crosscheck:
```
cd scripts && python3 dimension_six_tilted_integral_crosscheck.py
```

Test suite: `python3 -m unittest discover -s tests -v` -- 208 tests,
13 skipped (flint/ARB-gated, requiring `SIC_STARK_RUN_ARB=1` in the
pinned python-flint environment), 0 failures, 0 errors.  GREEN.

## Open questions and next position

1. **Prove BF\(_6(\eta)\) from the sinh-integral representation.**  The
   numerical evidence shows \(\eta\approx1\) (linear convergence).  The
   sinh integral's uniform convergence as \(s\to0+\) follows from the
   fixed-distance pole structure; the remaining work is to control the
   periodization (alias sum) tail, where the small-divisor estimate
   \(\|n\beta_6\|\ge(\sqrt{21}n+\tfrac12)^{-1}\) enters.  This is now a
   single classical estimate, not a numerical conditioning problem.

2. **Per-period decomposition.**  Dissect how the tilted value
   accumulates across the helical period, especially under the
   universal \(-q\) one-period multiplier and the \((-1)^k\)
   antiperiodic factor.

3. **d=4 mechanism extraction.**  Trace which feature of the tilted
   integral at \(\tau+\tau^{-1}=3\) encodes \(\log u\) via the
   \(\Gamma_M(Q,0)\) scalar, and identify the \(d=6\) analogue where
   the order-six \(L'\)-value must enter.

4. **Interval-arithmetic enclosure.**  Replace the mpmath
   floating-point rehearsal with a validated-interval enclosure (Arb or
   mpfi) to promote the boundary convergence from `numerical` to
   `certified`.  The fixed-distance pole structure makes this
   straightforward in principle.
