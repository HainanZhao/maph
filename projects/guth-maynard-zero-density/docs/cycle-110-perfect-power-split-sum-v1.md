# Cycle 110: perfect-power primitive splits have bounded total Jacobian

## Exact coefficient weight

`PROVED`. Fix a perfect-power label `N/R=(n0/r0)^d` and a primitive split
`u+v=d`, `(u,v)=1`. Cycle 102 makes the cross factors deterministic:

```text
x=(u,r0^d),                 y=(v,n0^d).
```

Cycles 104 and 106 then give

```text
K =d*n0^u*r0^v/(xy),
B0=v*r0^d/(xy),             C0=u*n0^d/(xy).
```

Therefore the normalized Cycle-109 Jacobian weight is

```text
J(u,v)=1/sqrt(K B0 C0)
      =(xy)^(3/2)
       /sqrt(d*u*v*n0^(u+d)*r0^(v+d)).             (1)
```

The actual-scale base `lambda0` contributes the additional factor
`lambda0^(-3/2)<=1`; summation over its multiples was closed in Cycle 109.

## Uniform split theorem

`PROVED`. Uniformly for every reduced positive base `(n0,r0)` and every
`d>=2`,

```text
sum_(u+v=d,(u,v)=1) J(u,v)<4.                     (2)
```

It is enough to sum over all positive splits.

If `n0=r0=1`, then `x=y=1`. By symmetry, `d-u>=d/2` on half the range and
`sum_(u<=T)u^(-1/2)<=2sqrt(T)`, whence

```text
sum J <=d^(-1/2) sum 1/sqrt(u(d-u)) <=4/sqrt(d)<4.
```

If `n0=1` and `r0>=2`, then `y=1`, `x<=u`, and, writing `v=d-u`,

```text
J<=sqrt(d)*v^(-1/2)*2^(-(d+v)/2).
```

Now `sum v^(-1/2)2^(-v/2)<sqrt(2)+1` and
`sqrt(d)2^(-d/2)<=2^(-1/2)` for `d>=2`, so the total is `<2`. The case
`r0=1<n0` is symmetric.

Finally, if both base coordinates are at least two, `x<=u`, `y<=v`, and

```text
sum J <=[sum_(u=1)^(d-1)u(d-u)]/[sqrt(d)2^(3d/2)]
       <d^(5/2)/(6*2^(3d/2))<1.
```

The final inequality holds at `d=2` and its successive ratio is below one.
This proves (2).

## Aggregation consequence and boundary

`PROVED`. For a fixed mode magnitude `W`, every primitive degree is
`d=W/(s,t)`, hence `d|W`. Cycle 99 supplies at most one strong critical label
for each signed mode, and a reduced positive rational has at most one
positive `d`th root. Thus the normalized perfect-power split weight over all
degrees attached to that mode is at most

```text
4*tau(W)=W^o(1).                                  (3)
```

This removes both coefficient-scale multiplicity and primitive-split entropy
from the smooth perfect-power branch. It does **not** yet bound the common
compact-chart/anchor prefactor uniformly across modes, nor nonsmooth
arithmetic payloads. Large-degree irrational cores, weak localization,
simple roots, the full signed moment, density, and interval endpoints remain
open.
