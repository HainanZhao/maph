# Cycle 122: the radial profile has no continuous volume term

Let

```text
K_H0(y)=H0 hat(U)(-H0 y),                          (1)
```

where the original dyadic cutoff `U` is smooth and compactly supported away
from zero. Fourier inversion gives, for every integer `j>=0`,

```text
int y^j K_H0(y)dy=0,                               (2)
```

because `U^(j)(0)=0`. Thus the cancellation is not an assumed sign pattern;
it is inherited exactly from the frozen frequency block.

Fix the remaining labels and put

```text
S=Bg^u+Cg^(u+v),  y=c log(p0n/S).
```

The zero Poisson mode in the integer variable `n` is an integral of (1)
against the corrected smooth symbol. After the displayed change of variables,
its density and all corrected cutoffs are smooth on a fixed compact `y`
interval. Their `j`th derivatives cost `O(c^(-j))`, while the density has
size `Q/c`. Taylor expansion against (2), with the Schwartz tail treated
before the compact support edge, proves for every fixed `N`

```text
zero mode <<_N (Q/c)(cH0)^(-N).                   (3)
```

Here bounded `p0` is supplied by Cycle 114. Since `cH0~KQ`, (3) is
power-negligible. This removes the `Q^2D^2/K` continuous volume term that
blocked the positive majorant in Cycle 119.

The nonzero Poisson modes are explicit. Using the integral representation
of (1), their phase in `n` is

```text
Phi_ell(n)=Hc log(p0n/S)-ell n.                   (4)
```

For `H>0`, negative `ell` is nonstationary. A positive mode has

```text
n*=Hc/ell,
Phi_ell(n*)=Hc[log(p0Hc/(ell S))-1],
|Phi_ell''(n*)|=ell^2/(Hc),                        (5)
```

and stationary amplitude

```text
sqrt(Hc)/ell=n*/sqrt(Hc)~sqrt(Q/K).               (6)
```

Because `n~Q`, `H~H0~KQ/D`, and `c~D`, stationary support forces
`ell~K`. The simple branch has therefore become a volume-free, signed alias
operator at the original frequency scale. Formulae (4)--(6) preserve
`(p0,S,H,ell)` and the Cycle-121 weight `c z_v/m`; they are not an anonymous
large-sieve remainder.

No bound for the `ell~K` aliases, simple-root closure, complete moment,
density gain, or interval gain is proved here.
