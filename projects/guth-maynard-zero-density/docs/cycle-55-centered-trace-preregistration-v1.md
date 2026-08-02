# Cycle 55 preregistration: can centering alone recover `3/50`?

## Question

After `s-1` candidate ordinary-coordinate contractions and the Cycle-48
powered saving, the selected `AMPR_s` class misses the off-diagonal trigger
by `3/50`. Determine whether replacing one-shot Halasz--Montgomery by an
arbitrary even centered Gram trace can cross this gap using only:

- equal row norm;
- one common coefficient vector large on every row;
- positivity of the Gram matrix;
- subtraction of the scalar diagonal.

## Frozen normalization

- Rows `x_1,...,x_R` have norm one.
- A unit vector `b` satisfies `|<b,x_t>|^2>=rho` for every row.
- The centered Gram matrix is `H=G-I_R`.
- At the Cycle-54 penultimate stage, `R rho` has exponent `-3/50`.
- Evaluate every even Schatten trace `tr(H^(2k))`, `k>=1`.

## Outcomes

- `CENTERING_CROSSES`: the frozen data force a positive centered trace at
  `R rho<=1`.
- `ABSTRACTLY_SHARP`: for every `0<=rho<=1/R`, construct rows satisfying the
  common-projection condition with `G=I_R`, hence all centered traces zero.

The second outcome is scoped to common-projection/PSD information. It does
not obstruct a trace that first uses actual prime coordinates, Cycle-51
partition subtraction, signed cumulants, or logarithmic recurrence.
