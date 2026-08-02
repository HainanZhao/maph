# Cycle 121: the projective coarea weight collapses to `c z_v/m`

Cycle 112 gives the corrected full triple-B symbol

```text
A*=c^(3/2)sqrt(Delta)/(m sqrt(H(H-Delta))).        (1)
```

Put `Delta=zH`. Then (1) becomes

```text
c^(3/2)sqrt(z)/(m sqrt(1-z)sqrt(H)),               (2)
```

while `dH dDelta=H dH dz`. Hence the amplitude in the projective integral
is

```text
c^(3/2)H^(1/2)sqrt(z/(1-z))/m.                    (3)
```

Cycle 120 writes the phase as `H P(z)` with

```text
P''(z_v)=c/[z_v(1-z_v)]>0.
```

Use `Hc` as the large parameter. On a fixed compact `z` chart, the leading
one-dimensional stationary factor is

```text
e(1/8)sqrt(z_v(1-z_v)/(Hc)).                      (4)
```

Multiplying (3) and (4) cancels the full `H` dependence and gives

```text
e(1/8)c z_v/m.                                    (5)
```

Since `z_v=Cg^v/(B+Cg^v)` and `C=q0m`, the unsigned part of (5) is also

```text
c q0 g^v/(B+Cg^v).                                (6)
```

The corrected Cycle-112 cutoffs become

```text
V(n/Q), V(n'/Q),
W(beta^-1 log(m/(n z c0))),
W(beta^-1 log((1-z)m/(n' z c0))),                 (7)
```

so they are independent of `H`. For a dyadic radial cutoff `U(H/H0)`, the
leading radial integral is therefore exactly the profile

```text
e(1/8) (c z_v/m) A(z_v)
 H0 hat(U)(-H0 P(z_v)),                            (8)
```

where `A` denotes the smooth factors in (7) and the Fourier convention is
`hat(U)(y)=int U(t)e(-yt)dt`.

The standard one-dimensional stationary expansion, applied with parameter
`Hc`, has `z`-remainder

```text
O(1/(mH))
```

uniformly on the fixed chart with fixed smooth symbol norms. Integrating
over `H~H0` costs only `O(1/m)`. Thus neither the leading projective
amplitude nor its summed remainder contains an unresolved power of the
radial height.

Formula (8), with
`P(z_v)=c log(A/(Bg^u+Cg^(u+v)))`, is the explicit signed operator left by
the simple-root branch. No cancellation across its arithmetic labels,
simple-root closure, complete moment, density gain, or interval gain is
proved here.
