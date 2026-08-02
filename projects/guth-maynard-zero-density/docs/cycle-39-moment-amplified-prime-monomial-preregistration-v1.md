# Cycle 39 moment-amplified prime-monomial preregistration v1

## Claim boundary

This cycle may prove coefficient-multiplicity bounds and exact exponent
ledgers for

```text
F_(m,s)(t)=K(t)^s K(mt).
```

It may state a sufficient hollow separated restriction theorem, but may not
promote that theorem, a kernel-count gain, a density gain, or an interval
gain without proving the new analytic estimate with strict margin.

## Frozen scale

```text
H=X^(12/5), Delta=X^(3/5), V=X^(7/10),
A=X^(3/10), M=X^(1+o(1)), target count=X^(21/25).
```

The row set is hollow and separated:

```text
C subset {t: Delta<=|t|<=H},    |t-t'|>=Delta.
```

The two registered harmonic-energy decays are `e=3/5` and `e=6/5`:

```text
sum_(2<=m<=A)|K(mt)/M|^2 >= X^(-e).
```

## Registered tasks

1. Expand `F_(m,s)` and bound, uniformly in `m>=2`, the multiplicity of the
   labels `(product_i p_i)q^m`. No ambient-length substitution is allowed.
2. Compute its coefficient-square norm at exponent level for fixed `s`.
3. Freeze the candidate cardinality-scale vector restriction bound

   ```text
   sum_(t in C) sum_(2<=m<=A)|F_(m,s)(t)|^2
      <= X^(s+31/10+o(1)).
   ```

   This bound is only a target unless analytically proved.
4. Derive the resulting row-count exponent for general fixed `s` and each
   registered `e`. Identify the least integer `s` that beats `21/25` and its
   exact margin.
5. Compare `s=1` with Cycle 38 to decide whether an unamplified second-moment
   route can close either branch.
6. Keep the hollow condition and the dependence on fixed `s` visible in the
   theorem statement. Record that uniformity in the growing harmonic order
   `m<=A` is part of the analytic gate.

## Outcomes

- `MOMENT_AMPLIFIED_REDUCTION` if fixed moments close the exponent ledger
  conditional on one explicit sparse restriction estimate.
- `MOMENT_AMPLIFIED_GAIN` only if that estimate is proved for the actual
  prime kernel.
- `AMPLIFICATION_SATURATION` if an actual-prime separated family disproves
  every closing fixed moment at the target scale.

Hostile audit remains deferred to paper stage.
