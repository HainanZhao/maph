# Width-four q-Fibonomial factorization split

Claim boundary: this is a `PROVED` algebraic reduction of the width-four
q-Fibonomial target.  It does not prove unimodality.  The target itself is
now proved by the coefficient-difference argument in
`proof/qfib_width4_unimodality_proof.md`; retain this note only as a separate
factorization observation.

Put

```text
W_m(q) = [F_(m+1)]_q [F_(m+2)]_q [F_(m+3)]_q [F_(m+4)]_q / ([2]_q[3]_q).
```

The Fibonacci divisibility facts used below are exact: `2 | F_n` iff
`3 | n`, and `3 | F_n` iff `4 | n`.

## Split by `m mod 12`

In every window `m+1,...,m+4`, a multiple of three supplies `[2]_q` and a
multiple of four supplies `[3]_q`.

- If `m mod 12` is in `{0,1,2,3,4,5,6,7}`, these indices are distinct.
  If their Fibonacci values are `E` and `T`, exact factorization gives

  ```text
  W_m(q) = [u]_q[v]_q [E/2]_(q^2)[T/3]_(q^3),
  ```

  where `u,v` are the other two Fibonacci values.  Every displayed factor
  has nonnegative coefficients.

- If `m mod 12` is in `{8,9,10,11}`, the same Fibonacci value is divisible
  by both two and three.  The local quotient is

  ```text
  [6c]_q / ([2]_q[3]_q) = [c]_(q^6) (q^2-q+1),
  ```

  so it is not a coefficientwise-positive factorization by itself.  This is
  the precise four residue classes where the direct denominator split fails.

Thus a width-four proof separates into an all-positive two-step/three-step
product in eight congruence classes and a cyclotomic-correction problem in
the remaining four.  A proof must still establish unimodality in both forms;
the reduction merely prevents treating them as one undifferentiated obstacle.
