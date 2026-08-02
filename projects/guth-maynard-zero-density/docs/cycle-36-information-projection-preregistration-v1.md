# Cycle 36 information-projection preregistration v1

## Claim boundary

This cycle may determine whether Cycle 35's phase entropy contains
information beyond the common first-harmonic projection already measured by
the determinant collapse. It may prove exact finite/continuous entropy
identities and asymptotic exponent/constant ledgers. It may not claim a
prime-kernel, density, or interval improvement without a new prime-specific
bound with strict margin.

## Frozen model

For a probability measure `mu` on the circle with rotated first moment
`r in [0,1)`, let `nu_r` be the von Mises information projection

```text
dnu_r(theta)=exp(kappa(r)cos(theta))/I_0(kappa(r)) du(theta),
I_1(kappa(r))/I_0(kappa(r))=r,
```

where `du=dtheta/(2pi)`. Define

```text
J(r)=D(nu_r||u),       E(mu)=D(mu||nu_r).
```

The registered identity is

```text
D(mu||u)=J(r)+E(mu).
```

At the prime-kernel scale freeze `r^2=rho=X^(-3/5)`,
`k=X^(21/25)`, so `k rho=X^(6/25)` and `k rho^2=o(1)`.

## Registered comparisons

1. Derive `J(r)=r^2+r^4/4+O(r^6)` from the Bessel series.
2. Compare `kJ(sqrt(rho))` with the sharp common-component determinant
   collapse

   ```text
   -(k-1)log(1-rho)-log(1+(k-1)rho).
   ```

3. Record whether their leading constants agree.
4. If they agree, replace raw entropy by the excess `E(mu)` as the only new
   arithmetic statistic. State the small-excess von Mises rigidity and the
   large-excess branch without asserting either occurs for prime rows.

## Outcomes

- `NEW_ENTROPY_LEVER` if first-harmonic entropy exceeds determinant collapse
  by a fixed power or leading constant.
- `FIRST_HARMONIC_EQUIVALENT` if the two agree at leading scale; then the
  route pivots to excess entropy/higher harmonics.
- `CORRECTION` if Cycle 35's entropy budget used an incorrect scale.

Hostile audit remains deferred to paper stage.
