# Hostile proof audit

Audit date: 2026-08-07 UTC.

## Claim boundary

- `PROVED`: the sufficient direction of CIMSY Conjecture 5.4.
- `PROVED`: the hybrid multi-spacer allocation criterion.
- No necessity or exact-characterization claim.

## Failure modes checked

1. The source statement uses the weak inequality and an `OR`; the manuscript
   matches it exactly.
2. The recursion has the correction length `a+r(b+1)`, confirmed both
   algebraically and by the complementary exponent-pair partition.
3. The induction never sums arbitrary unimodal polynomials: every pair of
   summands has common center `(E+2r_j)/2`.
4. Residual allocation rows remain valid in correction terms because all
   current ordinary lengths are at least their base values and the selected
   correction length is larger.
5. A divisibility absorption consumes each ordinary index at most once. The
   resulting pair factors and residual matrix factor are disjoint, so product
   closure applies factor by factor.
6. Multiplication by `[r_j]_q` after substituting `z=q^{r_j}` repeats each
   coefficient in a consecutive block; it does not leave internal gaps.
7. The statement permits `r_j=1`, and neither the identity nor induction
   assumes a larger step.
8. The symmetric non-unimodal product `[2]_(q^2)[2]_(q^3)` is outside the
   matrix hypothesis. The unimodal `a=5` near-miss is also outside it, so the
   manuscript does not suggest necessity.

## Regression evidence

The combined exact runner retains 1,680 two-route identity rows and 15,163
one-spacer induction rows, checks 400 allocated products with up to four
spacers and 43,002 nested recursion steps, tests 6,833 small hybrid-certified
products, and reproduces all adversarial thresholds and width-five coverage
counts. A separately written direct-product corpus adds 20 identity rows, 20
matrix instances, and 10 absorption instances.

Audit outcome: no surviving mathematical defect in the combined theorem.
