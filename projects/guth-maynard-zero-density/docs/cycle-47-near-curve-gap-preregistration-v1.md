# Cycle 47 preregistration: geometric correction and near-curve gap

## Question

Compare the Cycle 46 inverse-log count with source-checked lattice-point-near-
curve estimates, distinguishing graph derivatives from Euclidean curvature.

## Frozen scales and tests

- `Delta=X^(3/5)`, `h=X^(11/25)`, vertical tube
  `delta=X^(-21/25)`, and target count `X^(7/25+o(1))`.
- For `y(j)=(Delta/(2pi))log(1+(j+beta)/h)` on `j` intervals comparable
  with `h`, compute graph derivatives for every integer `3<=k<=20`.
- Evaluate every term of the Huxley--Sargos bound

  ```text
  R << N lambda_k^(2/(k(k+1)))
       + N delta^(2/(k(k-1)))
       + (delta/lambda_k)^(1/k) + 1.
  ```

- Record the minimizing derivative order and its exact gap from `7/25`.
- Separately compute Euclidean arclength, Euclidean curvature radius,
  Euclidean tube width, and affine-arclength exponents.

## Source boundary

Use the Huxley--Sargos theorem as displayed and proved in Zhao,
*Integral Points Close to Smooth Plane Curves*, arXiv:2407.01778, Theorem 2.1
and equation (29), and Howard--Trifonov, arXiv:2207.09532, only for the
geometric definitions and theorem shapes whose hypotheses are checked.
Huxley's `7/11` lattice discrepancy exponent is not imported merely because
its numeral matches the desired alias power.

## Outcomes

- `CLOSES`: a checked theorem yields exponent at most `7/25` uniformly.
- `PARTIAL`: a checked theorem improves the naive alias count but misses by a
  positive exact exponent; identify the term that must be improved.
- `NO_INPUT`: the hypotheses fail at the registered scales.

No `LCAM_s`, zero-density, or prime-interval gain is promoted in this cycle.
