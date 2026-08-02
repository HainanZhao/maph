# Cycle 182 preregistration: common-intercept fibre-line rigidity

## Question

Inside one Cycle-181 common-intercept stable packet, can the retained physical
rows be upgraded from arbitrary pair choices to complete rational affine
fibres? The proposed engine combines rational separation of slopes with the
packet's common intercept and then uses the integral lattice of that line.
It is designed to expose a denominator-and-congruence capacity bound without
discarding labels, rows, residuals, or stable determinant/product data.

## Frozen state

- Fix one reduced Cycle-181 packet intercept `rho=p/v` with `gcd(p,v)=1`.
  Retain every participating label, all its actual rows, the full four-row
  rectangle state, the two pair residuals, slope determinant, and stable
  product shell. A label considered here has `N_ell>=2`.
- For an oriented pair at `ell`, write `d=h2-h1`, `a=j2-j1`, and reduce
  `a/d=A/U` with `gcd(A,U)=1`. Freeze `H=X^(11/25)` and the exact rational
  separation cutoff

  ```text
  4*C*H^2/X < 1.
  ```

  This follows from the already required Cycle-181 large-scale cutoff, but
  it is stated separately because it is the only threshold allowed in the
  slope-rigidity comparison.
- The actual fibre is the complete set of integer rows in `[H,2H]` satisfying
  `|j+beta-h alpha_ell|<=C/X`; no selected subset may replace it.

## Proposed engine

The engine tests these consequences in sequence.

1. Any two physical pairs in the same non-singleton fibre have the same
   reduced rational slope `A/U`: distinct reduced slopes of denominator at
   most `H` are separated by at least `1/H^2`, whereas their two strip
   estimates differ by at most `4C/X`.
2. Every actual row at that label lies on the unique affine rational line

   ```text
   j = (A/U) h + p/v.
   ```

   Its integral heights are one residue class modulo `U`; existence forces
   `v|U`. Between the extreme actual rows every lattice point of that class
   is actual by affine interpolation of the residual.
3. Hence the fibre is a consecutive arithmetic progression of step `U`,
   has `N_ell<=1+H/U`, and its extreme-pair approximation obeys

   ```text
   |A/U-alpha_ell| <= 2*C/((N_ell-1)*U*X).
   ```

## Advance and failure rules

Advance only if all three conclusions are proved with their exact hypotheses
and a replay keeps the complete fibre/packet fields. This promotes a
primitive-denominator and base-row congruence engine for a **fixed** packet;
it does not itself bound that packet, prove recurrence, improve density, or
improve prime intervals.

Failure is: two admissible pairs in one fibre with distinct reduced slopes;
an actual row off the asserted line; a missing integral lattice point between
two extreme actual rows; an integral line with `v` not dividing `U`; or a
lost packet field. Record any such event in this same live document set.

## Amendment log

- 2026-08-02: initial preregistration. The only new formula family is the
  primitive slope/intercept lattice line, and its cutoff, state, and failure
  rules are frozen before replay construction.
