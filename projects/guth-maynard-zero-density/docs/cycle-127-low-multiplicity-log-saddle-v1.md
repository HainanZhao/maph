# Cycle 127: low multiplicity is a sampled Mellin large-sieve problem

Put `M=X^mu` and

```text
L=Q/M.
```

Cycle 92 reduces a dyadic collision class to primitive lattice points

```text
|a-(D/(2pi))log(p/q)| << delta,
p,q~L,                 delta=D/(KQ).               (1)
```

For fixed `q`, the third derivative of the logarithmic curve in `p` has size
`D/L^3`. Applying the checked order-three Huxley--Sargos theorem, summing over
the `L` denominators, and restoring multiplicity `M` gives the four collision
exponents

```text
derivative: 3/5-mu/2,
tube:       34/45-mu-xi/3,
ratio:      5/9-mu-xi/3,
constant:   1/3.                                  (2)
```

The target is `Q=X^(1/3)`. The derivative term in (2) misses it by

```text
4/15-mu/2,                                        (3)
```

and does not close any part of the registered low-multiplicity range
`mu<=(1-xi)/4`. This is a limitation of the denominator-by-denominator
application, not of the two-dimensional logarithmic surface.

Indeed, the joint volume in (1) is `L^2delta`. After multiplication by `M`
its exponent is

```text
14/15-xi-mu,                                      (4)
```

which is below `1/3` by

```text
xi+mu-3/5 >= 1/25.                                (5)
```

Thus a volume-scale joint theorem would close the entire low branch.

There is an exact harmonic formulation. A Fejer majorant in (1) produces

```text
delta L^2
 +delta sum_(1<=h<=H)|P(hD)|^2,                  (6)

P(t)=sum_(n~L)w(n)n^(it),
H=1/delta=KQ/D.                                   (7)
```

The desired sampled Mellin large sieve is

```text
sum_(h<=H)|P(hD)|^2 << H L X^epsilon.             (8)
```

Equation (8) turns (6) into `O(LX^epsilon)` labels and hence
`O(QX^epsilon)` weighted collisions. It is exactly diagonal size.

A generic time large sieve sees the full span `HD` and produces an `HD*L`
term rather than `H*L`, losing a factor `D`. The missing theorem must exploit
the arithmetic progression of Mellin samples or return the pairs for which
`D log(m/n)` lies near an integer as an explicit logarithmic-major-arc web.

No estimate (8), low-multiplicity closure, simple-root closure, complete
moment, density gain, or interval gain is proved here.
