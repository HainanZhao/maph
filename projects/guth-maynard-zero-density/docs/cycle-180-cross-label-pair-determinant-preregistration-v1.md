# Cycle 180 preregistration: nonzero cross-label pair determinant

## Question

Can the Cycle-179 affine-area census be sharpened by retaining a second
same-label pair rather than discarding it?  The target is a coefficient- and
orientation-preserving four-row rectangle whose determinant is forced
nonzero for distinct exponential labels.  This is intended to expose a
Farey-like spacing obstruction for the remaining approximate cross-label
geometry.

## Amendment log

- 2026-08-02: before computation, freeze the low-product/stable-product
  split below. It is an exact counting reduction inside the same rectangle
  state, not a new cycle or a scalar replacement.

## Frozen state

- At label `ell`, take an ordered actual pair with `h2>h1`,

  ```text
  d=h2-h1,  a=j2-j1,  |a-d alpha_ell|<=2C/X.
  ```

  At a distinct label `m`, retain `(e,b)` analogously. Freeze the complete
  state `(ell,m,h1,h2,j1,j2,s1,s2,k1,k2,d,e,a,b)`; no projected scalar may
  replace it in the census.
- Freeze the integer cross determinant and its phase:

  ```text
  D=e*a-d*b,
  Psi=d*e*(alpha_ell-alpha_m).
  ```

  Work only under `z-1>4C/X`, where `z=exp(2 pi/Delta)`; this is the frozen
  large-scale distinct-label separation condition.  Also freeze the
  Cycle-178 light threshold `R=ceil(X^(6/25))` and `X>=2^38` for the explicit
  critical-population constants.
- Let `p_ell=binom(N_ell,2)` be the number of unordered within-label row
  pairs and `W_cross=sum_(ell!=m)p_ell p_m` the ordered distinct-label
  rectangle count.  The initial engine is exact determinant forcing plus
  light-fibre population algebra; any later bound must retain the complete
  rectangle labels, gap signs, determinant value, and both pair errors.
- For `r=|ell-m|`, freeze

  ```text
  K0=(4C/pi)*H*Delta/X,
  low: r*d*e<K0,
  stable: r*d*e>=K0.
  ```

  The low-product count may use only `p_ell(d)<=N_ell<=2R`, the admitted
  label count `L<=Delta`, and the elementary three-divisor sum. The stable
  branch must retain `D` and prove a two-sided comparison with `r*d*e/Delta`.

## Advance and failure rules

Advance if all listed conclusions are proved.

1. Every retained cross-label rectangle satisfies
   `|D-Psi|<=4CH/X` and `D!=0`.  The `D=0` exclusion must use the common
   rational slope of the two pairs, not only the weaker product estimate.
2. If `T>=X^(16/25)` and all fibres are light, then
   `W_cross>=T^2/32>=X^(32/25)/32` under the frozen large-`X` cutoff.
3. The result must state the remaining analytic census in the full rectangle
   state and identify a falsifiable next bound or a nonrational saturator.
4. `PROVED`: the low product range contains at most
   `O(R^2 Delta K0 log^2 K0)=X^(28/25+o(1))` rectangles. Hence a critical
   light census leaves `>>X^(32/25)` stable rectangles, and each has
   `|D|asymp r*d*e/Delta` with frozen constants.

This is a reduction, not a claimed determinant-count upper bound, density
gain, recurrence theorem, or interval theorem.

## Falsifiers

- A legitimate pair-pair rectangle has `D=0` despite distinct labels and
  `z-1>4C/X`.
- The pair error or the light rectangle mass inequality fails with its stated
  ordered normalization.
- The low-product sum reaches the critical exponent, or a stable rectangle
  violates the determinant/product comparison.
- A derivation loses either source pair, label, orientation, determinant
  value, or individual approximation error.
