# Cycle 126: every represented difference has one rational multiplier

Let `A` be a Cycle-125 high-multiplicity mode set and let `a -> r_a` be its
exact multiplicative Freiman map. For a nonzero represented difference `d`,
put

```text
E_d={a in A:a+d in A}.
```

If `a,b in E_d`, then

```text
(a+d)+b=a+(b+d).
```

Freiman multiplicativity therefore gives

```text
r_(a+d)/r_a=r_(b+d)/r_b=:rho_d.                  (1)
```

Thus every represented difference carries one exact rational multiplier,
not merely a collection of compatible valuation equations.

If `A` has `R` points in an interval of `D` consecutive integers, the
`R(R-1)` ordered unequal pairs use at most `2D-2` nonzero signed differences.
Hence some `d` has

```text
L_d=|E_d| >= ceil(R(R-1)/(2D-2)).                 (2)
```

For fixed oriented `d`, the graph with edges `a -> a+d` is a disjoint union
of paths. With `R` vertices and `L_d` edges it has `R-L_d` components after
isolated vertices are included, so one component has at least

```text
ceil(L_d/(R-L_d))                                 (3)
```

edges. In particular,

```text
L_d>=ceil(JR/(J+1))                               (4)
```

is sufficient for a chain of `J` edges. Equations (2)--(4) expose the depth
gap: ordinary popular-difference pigeonholing does not force a power-length
chain unless the edge density is already close to one.

On a chain `a0,a0+d,...,a0+Jd`, equation (1) iterates exactly:

```text
r_(a0+jd)=r_a0 rho_d^j.                           (5)
```

Cycle 92's approximation and the fixed compact label range give

```text
rho_d=g^d(1+O(1/(KQ))).                           (6)
```

For a supported chain `J<=D`, telescoping (6) yields

```text
rho_d^J=g^(Jd)(1+O(J/(KQ))),
J/(KQ)<=D/(KQ)=X^(-(xi-4/15)+o(1)).               (7)
```

The worst lower-band margin in (7) is `28/75`. The rational recurrence is
therefore phase-accurate on every chain the mode interval can contain.

This compiler retains `d`, `rho_d`, every chain vertex, and the rational
labels. E16 must still tie a vertex to the original packet anchor and obtain
the depth required by propagation. Energy alone does not supply that depth.
No seed realization, low-multiplicity bound, simple-root closure, complete
moment, density gain, or interval gain is proved.
