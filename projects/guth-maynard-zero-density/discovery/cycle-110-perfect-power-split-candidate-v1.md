# Cycle 110 discovery candidate: the split entropy cancels arithmetically

`CONJECTURED` before exact closure: multiplying the three coefficient bases
gives

```text
K*B0*C0
 =d*u*v*n0^(u+d)*r0^(v+d)/(x*y)^3.
```

Hence

```text
J(u,v)
 =(x*y)^(3/2)
  /sqrt(d*u*v*n0^(u+d)*r0^(v+d)).
```

The apparently dangerous `d-1` primitive splits should be harmless:

- for `(n0,r0)=(1,1)`, exact cross gcds are `x=y=1` and the sum is
  `d^(-1/2) sum 1/sqrt(u(d-u))`;
- if exactly one base coordinate is nonunit, its `d`th-power denominator
  gives exponential decay which dominates the largest possible cross gcd;
- if both are nonunit, the common `2^d` decay dominates every polynomial
  split count.

If this survives, all degrees attached to one mode cost only `tau(|w|)`.
The remaining question is then the common chart/anchor normalization across
distinct modes, not primitive-split entropy.
