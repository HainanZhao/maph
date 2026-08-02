# Cycle 125: high-multiplicity collisions form an exact Freiman web

Cycle 92 assigns each occupied mode `a` one injective reduced label

```text
r_a=p_a/q_a,
|r_a-g^a| << 1/(KQ),
q_a << Q/M,                                        (1)
```

on a dyadic multiplicity class `[M,2M)`. All labels lie in a fixed compact
positive interval.

If

```text
a1+a2=a3+a4,
```

then `g^a1 g^a2=g^a3 g^a4`. Equation (1) and the compact product rule give

```text
|r_a1 r_a2-r_a3 r_a4| << 1/(KQ).                 (2)
```

If the two rational products are unequal, reduced-denominator separation
and (1) imply

```text
|r_a1 r_a2-r_a3 r_a4|
 >=1/(q_a1 q_a2 q_a3 q_a4) >> M^4/Q^4.           (3)
```

Thus, after freezing the harmless support constants,

```text
M^4 K >> Q^3                                       (4)
```

forces exact equality of the two rational products. Writing `M=X^mu` and
`K=X^xi`, because `Q^3=X`, the threshold is

```text
mu>(1-xi)/4.                                      (5)
```

It decreases from `9/100` at `xi=16/25` to `17/300` at the upper edge
`xi=58/75`. The complementary branch retains the explicit cap
`mu<=(1-xi)/4`.

Let `A` be the set of `R` occupied modes in an interval of `D` consecutive
integers. Cauchy--Schwarz on the representation function of `A+A` gives

```text
E_plus(A)>=R^4/(2D-1).                            (6)
```

In the range (4), every quadruple counted in (6) also satisfies

```text
r_a1 r_a2=r_a3 r_a4.                              (7)
```

Equivalently, for every prime `p`,

```text
nu_p(r_a1)+nu_p(r_a2)=nu_p(r_a3)+nu_p(r_a4).      (8)
```

The full prime-valuation vector is therefore a Freiman `2`-homomorphism on
the occupied mode set. If the dyadic class alone contributes more than
`QX^epsilon` collisions, then `R>>QX^epsilon/M`; ignoring the registered
epsilon buffer, (6) has exponent at least `11/15-4mu`.

This is a stronger inverse output than an unlabelled energy excess, but it is
not yet a transport seed. E16 must still extract a popular difference or
high-codegree anchored subgraph and carry its rational-label error through
the original packet phase. No low-multiplicity collision bound, seed
realization, simple-root closure, complete moment, density gain, or interval
gain is proved.
