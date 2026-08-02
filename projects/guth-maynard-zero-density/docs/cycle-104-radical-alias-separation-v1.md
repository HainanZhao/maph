# Cycle 104: single-radical alias separation

## Radical collapse

`PROVED`. Let `h=(s,t)`, `u=s/h`, `v=t/h`, and `d=u+v=W/h`. Then
`(u,v)=(u,d)=1`. At the critical point the derivative identity gives

```text
C0*r^(-t/W)=(s/t)B0*r^(s/W).
```

Consequently the Cycle-103 number is a single radical:

```text
K=(W/t)B0*r^(s/W).                                (1)
```

Using `u=x*s2`, `v=y*t2`, `B0=t2*R2`, and `r=N/R`, (1) becomes

```text
K=(d*R2/y)*(N/R)^(u/d).                           (2)
```

In particular

```text
K^d=(d*R2/y)^d*(N/R)^u=:P/S                      (3)
```

in lowest terms.

## Exact rational aliases

`PROVED`. The rational prefactor in (2) is irrelevant to rationality. Since
`(u,d)=1`, valuation at every prime shows that `(N/R)^(u/d)` is rational iff
every prime valuation of the reduced `N/R` is divisible by `d`. Equivalently,

```text
K is rational iff N=n0^d and R=r0^d               (4)
```

for positive integers `n0,r0`. This includes `d=1`.

## Elementary norm separation

`PROVED`. Assume (4) fails. For integers `q>=1,m`, factor over the `d`th
roots of unity:

```text
product_{j=0}^{d-1}(q*zeta_d^j*K-m)
 =q^d*K^d-m^d
 =(q^d*P-m^d*S)/S.
```

The integer numerator is nonzero and hence has modulus at least one. Every
factor other than `qK-m` has modulus at most `qK+|m|`, so

```text
|qK-m|>=1/(S*(qK+|m|)^(d-1)).                     (5)
```

For `q<=Lambda` and nearest-integer `m`, put `U=max(1,P/S)`. Since
`K<=(max(1,K^d))=U` and `|m|<=qK+1/2`, (5) gives the rational, exactly
computable bound

```text
|qK-m|>=1/(S*(2*Lambda*U+1/2)^(d-1)).             (6)
```

## Closed sector and boundary

`PROVED`. If twice the Cycle-103 critical-value tolerance is strictly below
(6), no `q<=Lambda` short alias exists, so at most one coefficient scale
survives on this core.

For fixed `d`, (6) is polynomial in the rational height and scale ledgers.
For large `d` it can be too small; those cores remain an aggregate
single-radical branch. No complete exceptional-web, weak/simple-root, moment,
density, or interval theorem is claimed.
