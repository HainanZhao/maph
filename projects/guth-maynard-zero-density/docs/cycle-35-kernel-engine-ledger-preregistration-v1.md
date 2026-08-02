# Cycle 35 kernel-engine ledger preregistration v1

## Claim boundary

This cycle may prove exact algebraic/exponent reductions for the unweighted
prime kernel from Cycle 34 and elementary finite-measure lemmas. It may not
claim the required prime-kernel count, a zero-density gain, or an interval
improvement unless a strict analytic margin is independently proved.

## Frozen scale

```text
M=X^(1+o(1)),       H=X^(12/5),
Delta=X^(3/5),      V=X^(7/10),
R_target=X^(21/25), delta=V/M=X^(-3/10).
```

Remove the single point `h=0` before any hollow estimate. All remaining
sets are `Delta`-separated and lie in `Delta<=|h|<=H`.

## Registered engines

1. **Hollow fractional restriction.** Compute the exact exponent in

   ```text
   sum_(h in C)|K(h)|^(24/5) <= X^(B+o(1))
   ```

   needed to imply `|C|<=R_target`, and compare it with the frozen global
   moment exponent from Cycle 14. Record the coherent `h=0` obstruction.

2. **Sieve-curvature differencing.** Apply the finite van der Corput
   inequality to the prime indicator and define the shifted-prime
   correlation

   ```text
   C_q(t)=sum_n 1_P(n)1_P(n+q)
                 exp(-it log(n/(n+q))).
   ```

   Compute a sufficient aggregate correlation estimate for pointwise
   exclusion when `|t|>=X^(3/5+eta)`, and separately prove the analogous
   first-derivative estimate for the unrestricted integer correlation.
   The integer estimate may motivate, but may not be transferred to primes.

3. **Multiscale phase entropy.** Partition the circle into `L` equal arcs,
   approximate the first Fourier coefficient by arc centres, and use
   Pinsker's inequality to lower-bound the histogram relative entropy of
   every large kernel value. State the separate accumulation theorem that
   would still be required.

## Frozen outcomes

- `ENGINE_SELECTED` only if one engine proves a fixed-power kernel-count
  saving under checked prime hypotheses.
- `REDUCTION` if exact sufficient targets and at least one unconditional
  structural lemma are proved but no prime saving follows.
- `CORRECTION` if an advertised engine is algebraically incapable of the
  target at the frozen exponents.

## Falsifiers

- An exponent recomputation shows the proposed hollow bound does not imply
  `21/25`.
- The van der Corput normalization loses an unregistered factor of `X` or
  the claimed low-time consequence does not beat `V`.
- The phase-histogram approximation or Pinsker constant fails for the frozen
  arc count.

## Review policy

Use exact algebra, lightweight proof checks, and constructive boundary
examples. Hostile audit remains deferred to paper stage.
