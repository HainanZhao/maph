# Cycle 181 preregistration: common-intercept packet engine

## Question

Can the common fixed strip translate `beta`, retained in the complete
Cycle-180 four-row state, impose an exact compatibility stronger than the
nonzero slope determinant? The proposed engine assigns a rational intercept
to each physical same-label pair and tests whether every cross-label
rectangle must use the *same* intercept at both labels. This is a new
four-row invariant, not a scalar determinant-shell count.

## Frozen state and scale

- Retain every Cycle-180 stable rectangle in its complete state
  `(ell,m,h1,h2,j1,j2,s1,s2,k1,k2,d,e,a,b,D)` and its two row-pair
  residuals. Thus `d=h2-h1>0`, `a=j2-j1`, and similarly `(e,b)` at `m`.
- For the first row of each oriented pair freeze the integer intercept

  ```text
  q=d*j1-a*h1,       q'=e*k1-b*s1.
  ```

  No rational intercept packet may discard its source label, physical pair,
  gap, numerator gap, residuals, determinant value, or stable product shell.
- Keep `H=X^(11/25)`, `Delta=X^(15/25)`, `d,e<=H`, and the Cycle-180 stable
  product condition. In addition freeze the exactification cutoff

  ```text
  10*C*H^2/X < 1,      5*C*H/X < 1/2.
  ```

  All asymptotic packet constants are permitted to depend only on the frozen
  strip and chart constants `C,c`; no search-selected cutoff is permitted.

## Proposed invariant

Let `delta=a-d*alpha_ell` and `epsilon=b-e*alpha_m`. The engine tests the
integer

```text
I=e*q-d*q'.
```

The intended proof uses the two independent pair residual identities to show
`|I|<=10*C*H^2/X`, hence `I=0` at the frozen cutoff. It must then derive a
shared reduced intercept `rho=p/v=q/d=q'/e`, with `v|d,e` and

```text
|rho+beta| <= 5*C*H/(min(d,e)*X),
|p+v*beta| <= 5*C*H/X.
```

## Advance and failure rules

Advance only if every item below is proved with the complete rectangle state
retained.

1. `I=0` follows from the row-specific residual bounds; it is not assumed
   from the slope determinant and does not use an unproved Diophantine fact
   about `beta` or the exponential.
2. All surviving stable rectangles partition by a common reduced rational
   intercept. There are at most `H` eligible intercepts for a fixed `beta`.
3. Combining Cycle 180's stable population with that partition yields one
   labelled common-intercept stable packet of at least
   `X^(21/25-o(1))` ordered distinct-label rectangles whenever the direct
   critical light census occurs. The proof must state the threshold and keep
   all product/determinant/orientation/residual data.
4. The resulting record must make clear that this is not yet a recurrence,
   density, interval, or stable-shell upper bound. Its next target must be a
   coefficient-preserving bound or a nonrational actual saturator *inside*
   one common-intercept packet.

Failure is a legitimate stable rectangle with `I!=0`, an intercept packet
count requiring more than `H` reduced denominators, a lost physical field,
or a critical stable population that cannot yield the stated packet. Any such
failure is recorded in this same live document set and halts promotion.

## Amendment log

- 2026-08-02: initial preregistration. Formula family, cutoffs, packet
  indexing, and failure rule frozen before exact replay construction.
- 2026-08-02: corrected the first-row height factor before computation:
  `h1,s1<=2H` makes the valid constants `5` and `10`, replacing the
  initially proposed `3` and `6`. The asymptotic exponent and packet
  criterion are unchanged.
