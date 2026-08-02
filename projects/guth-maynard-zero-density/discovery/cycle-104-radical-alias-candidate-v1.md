# Cycle 104 discovery candidate: the critical number is one radical

`CONJECTURED` before proof sealing.

At criticality the two summands in `K` are proportional. With
`h=(s,t)`, `u=s/h`, `v=t/h`, and `d=u+v`, the Cycle-102 substitutions suggest

```text
K=(W/t)B0*r^(s/W)
 =(d*R2/y)*(N/R)^(u/d).
```

Because `(u,d)=1`, this is rational exactly when the reduced numerator and
denominator `N,R` are both `d`th powers. Otherwise, if `K^d=P/S` in lowest
terms, the factorization of `q^d K^d-m^d` over the `d`th roots of unity gives

```text
|qK-m| >= 1/(S*(qK+|m|)^(d-1)).
```

This is weak for large `d` but polynomial for every fixed radical degree. It
is a native bound for the actual critical core, unlike the generic
degree-`W` logarithmic-form insertion.
