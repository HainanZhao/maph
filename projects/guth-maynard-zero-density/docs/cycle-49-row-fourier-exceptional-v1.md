# Cycle 49: exceptional row frequencies are tiny, but absolute pairing is fatal

## Claim boundary

`PROVED`: for a target-sized separated row set, frequencies where its Fourier
sum fails the `s=4` pointwise saving occupy Lebesgue measure at most
`X^(-13/50+o(1))`. This is a strong scalar nonlattice statement.

`PROVED` scoped boundary: pairing that pointwise statement with the absolute
prime-monomial autocorrelation still exceeds the `LCAM_4` target by
`X^(39/10)`. The missing theorem must couple row-Fourier oscillation to
coefficient-pair cancellation; small exceptional measure alone is not the
bridge.

No `LCAM_s`, density, or interval gain is proved.

## 1. Continuous row-Fourier budget

Order `C={t_1<...<t_R}` with gaps at least `Delta`. Direct integration gives

```text
integral_(-B)^B |R_C(xi)|^2 dxi
 =2BR + sum_(i!=j) 2sin(B(t_i-t_j))/(t_i-t_j).        (1)
```

Since `|t_i-t_j|>=Delta|i-j|`, the absolute off-diagonal in (1) is
`O(R log R/Delta)`. At

```text
R=X^(21/25), Delta=X^(3/5), B=X^(3/10),
```

the diagonal and off-diagonal exponents are respectively `57/50` and
`6/25`; the latter is smaller by `9/10`.

Chebyshev therefore gives

```text
meas{xi in [-B,B]: |R_C(xi)|>R X^(-tau)}
 << B X^(2tau)/R.                                    (2)
```

The measure exponents for `tau=7/50,4/25,17/50` are
`-13/50,-11/50,7/50`.

## 2. Why this does not yet prove the localized comb

For fixed `m`, the positive total variation of the prime-monomial pair
measure is the square of the coefficient sum, of exponent `2s+2`; its
diagonal energy has exponent only `s+1`. Bounding every nonexceptional
frequency by `R X^(-tau)` and taking absolute values therefore gives, after
the harmonic range, exponent

```text
2s+2 + 21/25 + 3/10 - tau.
```

Against the `LCAM_s` target `s+31/10`, the excess is

```text
s+1/25-tau.
```

It equals `39/10` for `(s,tau)=(4,7/50)` and `27/10` for
`(s,tau)=(3,17/50)`. Thus the small exceptional set cannot be combined with
absolute coefficient-pair mass.

## 3. Correct coupled target

`CONJECTURED` row--ratio discrepancy (`RRD_s`): after subtracting the
diagonal and the coherent zero packet, the signed prime-monomial
autocorrelation acts on every row-Fourier exceptional set at coefficient
energy scale `X^(s+1+o(1))`, not coefficient-mass-squared scale.

This is a bilinear restriction theorem. It may be attacked by opening a
prime and applying Cycle 48 on the structured exceptional components, while
using (1) on the complement. A proof must retain signs or an `L2` operator
norm; total variation is quantitatively incapable of closing the gap.

## Gate effect

`PROVED`: the nonlattice branch is not “show `R_C` is usually small.” It is
`ROW_RATIO_DISCREPANCY_AT_ENERGY_SCALE_OPEN`. Together with Cycle 48, the
combined gate is
`LCAM4_HS_STRUCTURED_PLUS_RRD4_OPEN`.
