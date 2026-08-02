# Cycle 179 preregistration: cross-label geometric rational-base tower

## Question

Cycle 178 leaves only ordered distinct-label mass as the unstructured
critical obstruction.  Can the most natural simultaneous rational-root
construction on the actual positive exponential—a geometric rational-base
tower—already saturate that mass?  If it cannot, what exact cross-label state
must a new determinant or spacing engine preserve beyond independent
same-label packets?

## Amendment log

- 2026-08-02: before computation, freeze the beta-eliminated oriented
  three-row area state below. This is the promised coefficient-preserving
  determinant engine, not a new cycle or document.
- 2026-08-02: before computation, enlarge the special base `(r+1)/r` to the
  gcd-compressed rational-base class `u/v>1`. The proposed proof engine is
  exact Bézout recovery of `exp(2 pi g/Delta)` from all exact rational labels;
  this tests the full exact-rational class, not just one prototype.

## Frozen construction

- Fix `0<c<1`, an integer `r>=2`, and a positive integer `L`.  Put

  ```text
  Delta=2 pi L/log(1+1/r),
  X=Delta^(5/3), H=Delta^(11/15), beta=0.
  ```

- Retain exactly the labels `ell=mL` with
  `1<=m<=M=floor(2 pi c/log(1+1/r))`; they lie in the Cycle-63 chart.  At
  such a label,

  ```text
  alpha_m=(1+1/r)^m-1=((r+1)^m-r^m)/r^m.
  ```

- Count only the exact rows `h=k r^m`, `j=k((r+1)^m-r^m)` in `[H,2H]`.
  Their denominators are to be proved primitive, not assumed.
- More generally, freeze a finite set of labels with exact rational values
  `1+alpha_ell`. If `g` is their gcd and `ell=gm`, Bézout recovery is to show
  `exp(2 pi g/Delta)=u/v` is rational in lowest terms. Every retained label
  is then a member of the single tower

  ```text
  alpha_(gm)=(u^m-v^m)/v^m.
  ```

  At beta zero, its **exact zero-residual** rows have denominator `v^m` and
  are multiples of it. This exact-row statement, including the integral-base
  case `v=1`, is frozen as part of the test. It is not a claim about arbitrary
  `C/X`-strip hits at large denominator.
- Freeze the ordered cross-label mass `U_tower=sum_(m!=n)N_mN_n`.  The
  target to test is the Cycle-178 light-branch scale `X^(32/25)`.
- Freeze the oriented actual triangle with two distinct rows
  `(h1,j1),(h2,j2)` at label `ell` and one row `(h3,j3)` at `m!=ell`:

  ```text
  A=(h2-h3)j1+(h3-h1)j2+(h1-h2)j3,
  Phi=h3(h2-h1)(alpha_ell-alpha_m).
  ```

  The frozen triangle target retains label order, all three row fields, and
  beta residuals; `A` is the asserted integer. Set
  `Q_tri=sum_ell N_ell(N_ell-1)(T-N_ell)` and, only for the explicit
  critical-population consequence, freeze `X>=2^25`.
- The first proposed engine is exact geometric-denominator summation,
  including the regime where `r` may vary with the scale.  After it, the only
  admissible new engine is a coefficient-preserving cross-label determinant,
  bilinear spacing form, or another actual cross-label prototype.  A
  collection of independent same-label packet statements is non-progress.

## Advance and failure rules

Advance on either result.

1. `PROVED`: uniformly in `r>=2`, the whole chart-admissible geometric tower
   has `U_tower=O(H^2)=X^(22/25)` (up to the frozen logarithmic boundary), so
   it misses the critical cross-label obstruction by a fixed `2/5` exponent.
   This banks a real multi-label countermodel constraint, not a cross-label
   estimate for arbitrary labels.
2. `PROVED`: a genuine tower or another explicitly frozen construction has
   cross mass at the critical `X^(32/25-o(1))` scale, with every label and row
   verified in the actual chart.  That is a scoped cross-label saturator.
3. `PROVED`: every frozen actual triangle obeys
   `|A-Phi|<=2CH/X`; in the light branch, a direct-target failure forces
   `Q_tri>=X^(32/25)/4`. This is a new exact triangle-transport reduction,
   not its needed analytic upper bound.
4. `PROVED`: the entire exact-rational label class gcd-compresses to one
   rational-base tower and, at beta zero with exact rows, has ordered
   cross-label mass `O(H^2)`. This rules out an exact-rational exact-row
   cross-label saturator but does not bound approximate rational roots,
   arbitrary fixed-beta strip hits, or the new area-resonance census.

If the tower is subcritical, the cycle must still formulate a smallest
coefficient-preserving pair state and an exact determinant/spacing identity
whose failure could distinguish arbitrary cross-label mass from this tower.
No density, interval, or E7/E9 promotion is authorized.

## Falsifiers

- A retained `mL` lies outside the chart, its displayed alpha is not the
  reduced rational with denominator `r^m`, or its exact row count is wrong.
- The denominator sum admits cross-label mass at `X^(32/25-o(1))`.
- The area identity fails to cancel beta, has a non-integer `A`, or the
  light-population count fails at its explicitly frozen normalization.
- A finite exact-rational label set fails Bézout base recovery, or the
  resulting beta-zero exact-row denominator/multiple bound is false.
- The proposed next pair state drops label order, beta, numerator, or the
  signed approximation error.
