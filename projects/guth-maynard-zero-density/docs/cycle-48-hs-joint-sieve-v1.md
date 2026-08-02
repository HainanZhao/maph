# Cycle 48: the checked near-curve input reaches the `s=4` auxiliary margin

## Claim boundary

`PROVED`: inserting the Cycle 47 order-three Huxley--Sargos wrap count into
the Cycle 45 joint large sieve gives saving exactly `7/50` at Fourier
resolution `11/25`. This improves the earlier `2/25` by `3/50`, reaches the
registered Cycle 39 `s=4` auxiliary margin, and remains `1/50` short of the
full `4/25` saving.

`OBSERVED`: the equality is not yet an `LCAM_4` theorem. Cycle 45 bounded one
opened-prime joint sum; the full localized-comb expansion, its weights, all
prime openings, and the nonlattice row branch have not been restored. No
zero-density or interval gain is promoted.

## 1. Uniform wrap count

For `h=X^nu`, the order-three derivative term from Cycle 47 is

```text
h (Delta/h^3)^(1/6)=X^(1/10)h^(1/2).
```

The other Huxley--Sargos terms are smaller throughout
`0<=nu<=11/25`. Combining with the trivial count `h` gives

```text
A(h) <= min(h, X^(1/10)h^(1/2)) X^o(1).             (1)
```

Thus the wrap exponent is `a(nu)=min(nu,1/10+nu/2)`, with transition
`nu=1/5` and endpoint `a(11/25)=8/25`.

## 2. Joint large-sieve ledger

Colouring into `A=X^a` classes and retaining both large-sieve terms gives

```text
sum_k |P(theta_k)|^2
 << A(X+Delta/h)X^(1+o(1)).                          (2)
```

At `nu=11/25`, the two exponents in (2) are

```text
a+2       =58/25,
a+8/5-nu =37/25.
```

The direct term dominates. Cauchy--Schwarz over `X^(3/5)` resonance indices
therefore gives joint exponent

```text
3/10 + (58/25)/2 =73/50.
```

Against the trivial exponent `8/5=80/50`, the saving is exactly `7/50`.

## 3. Interpretation

The equality with the `s=4` margin is a real threshold event: classical
near-curve technology supplies precisely the previously hypothetical
`mu=8/11` de-aliasing level. It does not reach the `mu=7/11` level needed for
the full `4/25` saving, and it offers no positive slack against any additional
fixed-power loss.

The next proof obligation is structural, not another exponent comparison:
write the complete `LCAM_4` off-diagonal sum as a bounded number of terms of
the form controlled by (2), or identify the exact residual terms. If the
bridge is lossless up to `X^o(1)`, the lattice-like `s=4` branch closes at its
registered exponent. If it costs a fixed power, the logarithmic major-arc
engine must recover that power, beginning with the remaining `1/50` to the
full joint target.

## Gate effect

`PROVED` auxiliary threshold attainment. E7 becomes
`LCAM4_HS_BRIDGE_OR_LOG_MAJOR_ARC_1_50_OR_NONLATTICE_OPEN`.
