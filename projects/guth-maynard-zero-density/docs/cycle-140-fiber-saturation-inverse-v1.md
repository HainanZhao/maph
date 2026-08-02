# Cycle 140: surviving multiplier fibers carry a divisor seed

Refine the Cycle-138 bound by writing the actual multiplier height as

```text
H=N^2/(JZ),       Z=X^zeta>=1.                    (1)
```

The exceptional rational count is now

```text
H^2(1+D N^2/S^2).
```

After multiplication by `J^2`, its discretization and volume exponents are

```text
4rho-2zeta,
3/5+6rho-2tau-2zeta.                              (2)
```

Against the target `2/3-2mu`, the block closes whenever

```text
zeta>2rho-1/3+mu,
zeta>3rho-tau+mu-1/30.                            (3)
```

Thus every survivor has explicitly bounded height slack.  The same slack
strengthens its continued-fraction certificate.  Since the approximation
width remains `N^2/S^2`, Legendre's margin, the next-denominator exponent,
and the next-partial-quotient exponent become respectively

```text
2tau+2j+2zeta-6rho,
2tau-4rho+j+zeta,
2tau-6rho+2j+2zeta.                               (4)
```

There is also an exact arithmetic seed.  Write `r=A/B`, and for a realizing
label `p/q` put

```text
u=gcd(A,q),       v=gcd(B,p).
```

Cycle 138 gives `uv~H`.  The number of divisor pairs is subpower, so one
fixed pair `(u,v)` carries at least `JX^(-epsilon)` edges.  On that class,

```text
p=v p0,       q=u q0,
x_a       =v p0/(u q0),
x_(a+d)  =(A/u)p0/((B/v)q0).                      (5)
```

Every edge still carries its original mode, orientation, next-convergent
matrix, and signed tail.  If `zeta=o(1)`, the class in (5) occupies an
`X^(-o(1))` fraction of its capacity `JZ`, so it is a genuine saturated
divisor-class seed rather than a bare rational ray.

The theorem does not force `zeta=o(1)` for every surviving block.  No
recurrence, full paired norm, endpoint, moment, density, or prime-interval
theorem is proved.
