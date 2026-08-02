# Cycle 137: a first weighted exceptional-multiplier range closes

Let `|E_d|~J=X^j` and retain the strict Cycle-136 condition `S>>N^3`.
An exceptional difference has

```text
|g^d-r_d| << N^2/S^2,       height(r_d)<=N^2.      (1)
```

There are `O(N^4)` compact rationals of height at most `N^2`.  Each interval
in (1) contains at most `O(1+D N^2/S^2)` points of the `g^d` mode grid.
Therefore

```text
B_exc << X^epsilon (N^4+D N^6/S^2).               (2)
```

The count must be compared with the edge-weighted target, not merely with the
number of available differences.  A coherent exceptional class contributes
at most its square edge multiplicity, so the diagonal budget is met when

```text
B_exc J^2 << (Q/M)^2 X^epsilon.                   (3)
```

In exponent notation, the two terms in (2) are

```text
4rho,       3/5+6rho-2tau,                        (4)
```

while (3) allows `2/3-2mu-2j`.  Hence this elementary average closes exactly
in the strict region

```text
j < min(1/3-mu-2rho,
        1/30-mu+tau-3rho).                        (5)
```

The region is nonempty.  At

```text
xi=16/25, mu=0, rho=7/45,
tau=xi+1/3-rho=184/225,
```

the two edge ceilings are `1/45` and `173/450`; thus every fixed
`j<1/45` closes strictly.

Outside (5), the surviving weighted graph retains, for every difference,
`E_d`, `r_d`, its convergent denominator, the next-denominator lower bound
`S^2/N^4`, the next partial quotient `S^2/N^6`, and the signed phase anchor.
Across much of the upper exact region the first obstruction is the `N^4`
rational-discretization term, not volume.

No high-edge or full exceptional average, paired norm, endpoint, moment,
density, or prime-interval theorem is proved.
