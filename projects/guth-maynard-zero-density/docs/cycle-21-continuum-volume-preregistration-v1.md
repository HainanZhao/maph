# Cycle 21 continuum-volume preregistration v1

## Claim boundary

This cycle may prove an elementary determinant lower bound for a continuous
log-frequency frame and an exact conditional bridge from a prime quadrature
operator discrepancy to the skeleton target. It may not assert the required
prime discrepancy, a density gain, or an interval result.

## Frozen continuous frame

Let `B>0` be fixed and define normalized rows

```text
f_t(y)=B^(-1/2) exp(-ity),    0<=y<=B.
```

Their Gram kernel is

```text
H_0(t,s)=B^(-1) integral_0^B exp(-i(t-s)y)dy.
```

For distinct rows, register

```text
|H_0(t,s)| <= 2/(B|t-s|).
```

If ordered times are `Delta`-separated, the absolute off-diagonal row sum is
at most

```text
epsilon = 4 H_(k-1)/(B Delta),
```

where `H_n` is the harmonic number. Gershgorin therefore gives

```text
det(H_0) >= (1-epsilon)^k
```

when `epsilon<1`.

## Frozen prime comparison

Let `H_P` be the normalized Gram matrix of the prime rows
`(p^(-it))_(X<p<=2X)`. Register the operator discrepancy

```text
eta_C = ||H_P-H_0||_op.
```

If `epsilon+eta_C<1`, Weyl's eigenvalue inequality gives

```text
det(H_P) >= (1-epsilon-eta_C)^k.
```

For `epsilon+eta_C<=1/2`, use the weaker explicit lower bound

```text
log det(H_P) >= -2k(epsilon+eta_C).
```

## Frozen coloring and sufficiency gate

Start with an `X^(3/5)`-separated skeleton of size
`R>=X^(21/25)`. Color its ordered rows cyclically with
`L=ceil((log X)^2)` colors. One color has
`k>=R/L` rows and separation `Delta>=L X^(3/5)`.

For fixed `B`,

```text
epsilon = O(X^(-3/5)/log X)=o(X^(-3/5)).
```

The common-projection determinant upper bound from Cycle 20 uses
`rho=X^(-3/5)` and has negative logarithmic scale

```text
k rho = X^(6/25-o(1)).
```

Therefore the registered conditional prime gate is

```text
eta_C=o(X^(-3/5))
```

uniformly for the selected color class. Under this gate, the continuum lower
bound is `exp(-o(k rho))`, contradicting the Cycle-20 upper bound
`exp(-(1-o(1))k rho)`.

This is a sufficient operator discrepancy theorem, not an equivalence and
not a currently proved estimate for primes.

## Compute and review rules

- CPython `3.12.3`, optimization level zero, exact `Fraction` arithmetic for
  exponent identities and deterministic rational finite checks.
- No RNG, third-party library, or network.
- Builder cap: 30 seconds and 256 MiB RSS.
- Hostile audit remains deferred to paper stage.
