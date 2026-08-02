# Cycle 112: the corrected full symbol absorbs the rational anchor

`PROVED`. The paired Cycle-81 outer amplitude is `c^2/(r r')`. Multiplying
by the three B-process Hessian factors and substituting

```text
k*=c Delta/m,  r*=cH/n,  r'*=c(H-Delta)/n'
```

gives exactly

```text
A*=c^(3/2)sqrt(Delta)/(m sqrt(H(H-Delta)))
  =c^2 sqrt(k*/(r*r'))/sqrt(m n n').              (1)
```

The frozen cutoffs become

```text
V(n/Q), V(n'/Q),
W(beta^-1 log(Hm/(n Delta c0))),
W(beta^-1 log((H-Delta)m/(n'Delta c0))).           (2)
```

Thus `c0` only translates logarithmic `W` coordinates; it is not a size
prefactor, and fixed smooth mixed norms are uniform in the anchor.

Write `c0=p0/q0`. At actual scale `lambda`,
`n'=lambda B0/p0`, `m=lambda C0/q0`, while `B0,C0<=Q`. On a fixed interior
`V` chart, `n',m>=aQ` for fixed `a>0`, so

```text
lambda>=a p0,       lambda>=a q0.                 (3)
```

Consequently the apparent conversion factor
`p0 sqrt(q0)/lambda^(3/2)` is `O_a(1)`. Combining (1)--(3) with Cycle 110
gives normalized weight `O(tau(|w|))` per signed strong mode. Summing
`|w|<=2M` costs

```text
M^(1+o(1))=X^(3/5+o(1)),                          (4)
```

a strict `1/30` arithmetic-multiplicity saving relative to the generic
`X^(19/30+o(1))` branch, after the common analytic chart factor is removed.

This closes the registered smooth perfect-power strong branch. Nonsmooth
coefficient payloads, irrational large-degree cores, weak localization,
simple roots, the full moment, density gain, and interval gain remain open.
