# Cycle 49 preregistration: row-Fourier exceptional-set engine

## Question

Use only separation and the exact Fourier transform of the row set to bound
the measure of frequencies on which the `s=4` pointwise saving fails.

## Frozen data

- `C` has `R<=X^(21/25)` points separated by `Delta=X^(3/5)`.
- Frequency window is `[-B,B]`, `B=X^(3/10)`.
- `R_C(xi)=sum_(t in C)exp(-it xi)`.
- Thresholds are `R X^(-tau)` for
  `tau in {7/50,4/25,17/50}`.

## Tasks

1. Prove an explicit continuous mean-square bound using the ordered-row
   harmonic sum; retain diagonal and off-diagonal terms separately.
2. Apply Chebyshev to compute the exact exceptional-measure exponent at each
   registered threshold.
3. State the precise sampling/discrepancy theorem for the prime-monomial
   log-ratio measure that would convert the continuous estimate into the
   localized-comb bound.

## Claim boundary

This cycle may prove a theorem for arbitrary separated row sets and define a
prime-ratio sampling gate. It may not infer that a discrete arithmetic
frequency measure obeys Lebesgue measure, nor promote `LCAM_s`, density, or
interval conclusions without that theorem.
