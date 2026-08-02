# Cycle 116: weak turnover has mode exponent at most `7/25`

Let `G1,G2` be the two errors in the exponentiated projective stationary
equations. The smooth height variables have length `H0~KQ/D`, while the
phase is multiplied by `c=D/(2pi)`. Repeated integration by parts outside
the stationary window shows that a surviving cell must satisfy

```text
|G1|+|G2| <<1/(cH0)<<1/(KQ).                      (1)
```

The exact elimination with errors is

```text
A-B g^u exp(G1)-C g^(u+v)exp(G1+G2)=0.            (2)
```

Since `B,C<=Q`, equations (1)--(2) imply the Laurent residual at zero error
obeys

```text
delta=|A-Bg^u-Cg^(u+v)|<<1/K.                    (3)
```

`PROVED`. Cycle 115 says a weak transition requires
`delta>>S2/D^2`. Combining with (3),

```text
S2=Ba^2+Cb^2 <<D^2/K.                             (4)
```

If the active coefficient height is `Zc<=min(B,C)`, then

```text
max(|a|,|b|)<<D/sqrt(K Zc).                       (5)
```

For `K=X^(xi)`, the mode exponent in (5) is
`3/5-xi/2-zeta/2`, where `Zc=X^zeta`. Throughout the active lower band
`xi>=16/25`, its maximum is

```text
3/5-(16/25)/2=7/25.                               (6)
```

Thus the old weak range of exponent `3/5` collapses to a low-energy sector
of exponent at most `7/25`. This is an exact inverse constraint, not yet a
sum over that sector. Coefficient aggregation, simple-root averages, the
complete moment, density gain, and interval gain remain open.
