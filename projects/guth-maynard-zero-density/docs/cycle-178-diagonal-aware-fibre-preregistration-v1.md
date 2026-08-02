# Cycle 178 preregistration: diagonal-aware fixed-beta fibre extraction

## Question

For the fixed-beta Cycle-63 transport strips

```text
|j + beta - h alpha_ell| <= C/X,
h in [H,2H] cap Z,  H=X^(11/25),
alpha_ell=exp(2 pi ell/Delta)-1,
```

can a large **actual** fibre at one label be converted, with its seed and
approximation error retained, into the seeded recurrence object required by
Cycle 67?  After that conversion, can failure of the direct target be written
as an explicitly cross-label population problem rather than being hidden in
the diagonal pair mass saturated by Cycle 177?

## Frozen regime and objects

- Fix positive `X,H,C`, a real `alpha`, and a real `beta`; take distinct
  integer rows `(h,j)` satisfying the displayed strip, with `h in [H,2H]`.
  Freeze the integer-forcing cutoff `4*C*H/X < 1` and fibre size `N>=3`.
- At a fixed label, order its `N` retained `h` values.  Let `d0` be the
  smallest adjacent gap and let `a0` be the corresponding `j` difference.  Reduce
  `(d0,a0)` by `g=gcd(d0,a0)` to `(q,a)`; `a=0,q=1` is retained as a legal
  primitive zero-numerator branch rather than discarded.
- Set `K=floor((N-1)/2)`.  The proposed exact output is a retained seed,
  `(a,q)=1`, `qK<=H`, and `|q alpha-a|<=C/(KX)`, followed by a one-sided
  progression of at least `K+1` rows in the enlarged `2C/X` strip.
- For the full census put `N_ell` for the fibre counts and
  `T=sum_ell N_ell`.  Freeze `R=ceil(X^(6/25))`, heavy as
  `N_ell>=2R+1`, and the ordered distinct-label mass
  `U_cross=sum_(ell!=ell') N_ell N_ell'`.
- No numerical parameter selection, literature theorem, terminal-web
  classifier, raw beta-free pair bound, or scalar gcd statistic may count as
  the engine.  The only proposed engine is exact determinant forcing on
  **actual fixed-beta rows**, followed by the elementary diagonal extraction.

## Advance and failure rules

Advance if all of the following are proved with exact floor handling.

1. Every frozen heavy fibre supplies the Cycle-67-type seeded packet above,
   at depth at least `R`, with no loss of the label, beta seed, numerator, or
   approximation error.
2. If no heavy fibre occurs then
   `U_cross >= T*(T-2R)`; consequently, whenever `T>=4R`, at least half of
   the ordered pair mass is genuinely cross-label.
3. The direct critical failure `T>=X^(16/25)` therefore has exactly two
   retained alternatives: a critical seeded recurrence packet or a
   cross-label population of size `U_cross >> X^(32/25)` (for the frozen
   large-`X` range).  This is a reduction, not a cross-label bound.

The next authorized engine after a successful extraction is a
coefficient-preserving cross-label determinant, bilinear-spacing, or an
actual cross-label saturator.  A complete cross-label bound or saturator is
not required to seal this cycle; it is required before any E13 advance or
density promotion.

## Falsifiers

- A valid fixed-beta fibre violates the claimed integer determinant forcing
  under `4CH/X<1`.
- Reduction fails to retain a primitive numerator/denominator, seed,
  approximation error, or in-range progression.
- A heavy fibre has `K<R`, or the light-fibre diagonal inequality fails.
- The argument silently replaces actual fixed-beta rows by beta-free pairs,
  assumes `a!=0`, or claims a cross-label analytic estimate from the
  combinatorial dichotomy alone.
