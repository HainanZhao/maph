# Cycle 123: the joint saddle exposes a separable alias phase

For

```text
S=p0n'g^u+q0m g^(u+v),
Phi_ell(H,n)=Hc log(p0n/S)-ell n,                 (1)
```

the two stationary equations are

```text
c log(p0n/S)=0,
Hc/n-ell=0.
```

They have the unique interior solution

```text
n*=S/p0,                 H*=ell S/(p0c).          (2)
```

As in Cycle 122, support forces `ell~K`. The Hessian is

```text
[[0,   c/n],
 [c/n,-Hc/n^2]],

det Hess=-(c/n)^2.                                 (3)
```

It has one positive and one negative eigenvalue, so the joint signature is
zero. The stationary value and amplitude are

```text
Phi_ell(H*,n*)=-ell S/p0,
|det Hess|^(-1/2)=S/(p0c).                        (4)
```

Multiplying (4) by the Cycle-121 projective factor
`e(1/8)c z_v/m` gives the exact collapse

```text
e(1/8) z_v S/(p0m)
 =e(1/8)(q0/p0)g^(u+v).                           (5)
```

Here `z_v=Cg^v/(B+Cg^v)`, `B=p0n'`, and `C=q0m`. Thus all powers of
`H,n,m,c` disappear from the leading amplitude.

The corrected smooth symbol simplifies at the same saddle. Besides

```text
V(n'/Q),  V(S/(p0Q)),  U(ell S/(p0cH0)),          (6)
```

the two logarithmic cutoff arguments are exactly

```text
-(u+v)/D,             -v/D.                       (7)
```

Finally, the stationary phase separates:

```text
e(-ell S/p0)
 =e(-ell n'g^u)e(-ell(q0/p0)m g^(u+v)).           (8)
```

This is the first fully normalized simple-root alias operator: the two
coefficient sums have separate exponential phases, coupled only through the
smooth support in (6) and the projective mode coordinates.

For the remainder, rescale `H=H0h`, `n=Qx`. The phase has large parameter
`H0c~KQ`, and (3) becomes a uniformly nondegenerate fixed-chart saddle.
The standard two-dimensional stationary expansion therefore makes the first
remainder smaller than the leading stationary scale by `O((KQ)^(-1))`, for
fixed smooth symbol norms. The inherited Cycle-121 projective remainder
remains separate.

No bilinear estimate for (8), simple-root closure, complete moment, density
gain, or interval gain is proved here.
