# Cycle 113: weighted aggregation closes every smooth strong core

`PROVED`. For a reduced label `N/R`, primitive `u+v=d`, and cross factors
`x=(u,R)`, `y=(v,N)`, exact algebra gives

```text
(K B0 C0)^d
 =(d u v)^d N^(d+u) R^(2d-u)/(xy)^(3d).          (1)
```

On the fixed compact ratio chart, with `Z=min(N,R)`, the normalized weight is
therefore comparable to

```text
(xy)^(3/2)/(Z^(3/2)sqrt(d u v)).                  (2)
```

If `Z<=d^(1/3)`, use `x,y<=Z` and
`sum 1/sqrt(u(d-u))<=4` to bound the whole split sum by
`O(Z^(3/2)/sqrt(d))=O(1)`.

If `Z>=d^(1/3)`, freeze dyadic boxes for `u,v` and exact divisors
`x|R,y|N`. Since `(N,R)=1`, also `(x,y)=1`; the two divisibilities select at
most `1+d/(xy)` values of `u`. Substitution into (2), using
`xy<=uv`, `xy<=O(Z^2)`, and `uv<=d^2`, bounds each divisor-pair/dyadic cell
by `O(1)`. There are only `(dNR)^o(1)` such cells. Hence

```text
sum_(u+v=d,(u,v)=1)(K B0 C0)^(-1/2)=(dNR)^o(1).  (3)
```

This includes irrational labels and proves that primitive-split entropy is
not the large-degree obstruction. It does **not**, by itself, close the scale
sum. Write

```text
lambda=lambda_BC*ell,
lambda_BC=lcm(p0/(p0,B0),q0/(q0,C0)),
```

and let `E` be the first `ell` meeting the fixed support. Absolute summation
of Cycle 112's coefficient kernel gives the factor

```text
3*p0*sqrt(q0)/(lambda_BC^(3/2)*sqrt(E))
```

times (3). Support gives `E lambda_BC>=a max(p0,q0)`, but this leaves as much
as `O(p0/lambda_BC)` when `p0` and `q0` are comparable. Pointwise anchor
absorption therefore does not imply uniform absorption of the whole support
window.

This is a versioned containment of Cycle 112's final aggregation claim: its
full-symbol identity and cutoff formulas remain `PROVED`, but the promoted
`X^(3/5+o(1))` total is withheld pending a coupled anchor-scale-label sum.
Weak localization, simple roots, nonsmooth payload variants, the complete
moment, density gain, and interval gain remain open.
