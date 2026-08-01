# Cycle 21: continuum volume theorem and prime quadrature gate

## Claim boundary

`PROVED`: the continuous log-frequency frame has a determinant lower bound
that contradicts the Cycle-20 collapse after subpower coloring. `PROVED`
conditional reduction: the same conclusion holds for prime rows under a
specified normalized operator-discrepancy estimate. `OBSERVED`: that prime
estimate is open. No density or interval result is promoted.

## Continuous frame theorem

For normalized functions

```text
f_t(y)=B^(-1/2)e^(-ity),    0<=y<=B,
```

the off-diagonal Gram kernel has modulus at most `2/(B|t-s|)`. If
`t_1<...<t_k` are `Delta`-separated, then

```text
sum_(s!=t)|H_0(t,s)| <= 4H_(k-1)/(B Delta)=epsilon.
```

Gershgorin places every eigenvalue in `[1-epsilon,1+epsilon]`, so

```text
det(H_0)>=(1-epsilon)^k.
```

This uses the order of the sample points: the `j`th neighbor on either side
is at distance at least `j Delta`.

## Prime perturbation theorem

Let `H_P` be the prime-phase Gram matrix normalized to diagonal one and put

```text
eta_C=||H_P-H_0||_op.
```

Weyl's inequality gives

```text
det(H_P)>=(1-epsilon-eta_C)^k.
```

When the total error is at most `1/2`, this implies

```text
log det(H_P) >= -2k(epsilon+eta_C).
```

## Exact critical bridge

Color an `X^(3/5)`-separated skeleton cyclically with
`L=ceil((log X)^2)` colors and retain a largest color. It has subpower-loss
size and separation at least `L X^(3/5)`. Consequently

```text
epsilon=O(X^(-3/5)/log X)=o(rho),    rho=X^(-3/5).
```

If, uniformly on the retained color class,

```text
eta_C=o(X^(-3/5)),
```

then the prime determinant lower bound is `exp(-o(k rho))`. Cycle 20 forces
the upper bound `exp(-(1-o(1))k rho)`, where
`k rho=X^(6/25-o(1))`, giving a contradiction.

Thus E8 no longer asks vaguely for “prime-log rigidity.” Its sufficient
arithmetic input is normalized operator-norm quadrature at scale
`o(X^(-3/5))` after subpower separation amplification. This condition is not
claimed necessary and is not yet proved.
