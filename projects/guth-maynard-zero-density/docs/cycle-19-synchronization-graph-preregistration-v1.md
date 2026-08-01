# Cycle 19 synchronization graph preregistration v1

## Claim boundary

This cycle formalizes E7/E9 for a finite sampling system. It may prove exact
phase-synchronization, popular-pair, two-generation path, block-entropy, and
abstract countermodel statements. It may not infer a prime-log recurrence
bound, the skeleton target, a density improvement, or an interval result.

## Frozen Hilbert model

Let `a` be a vector with squared norm `A`. Let `u_t`, `t in C`, be `R`
sampling rows, each with squared norm `M`, and suppose

```text
|<a,u_t>| >= V.
```

Choose unit phases `z_t` aligning `<a,u_t>`, and put

```text
K(t,s)=<u_t,u_s>,    w=V^2/A.
```

The registered synchronization claim is

```text
sum_(t,s) z_t conjugate(z_s) K(t,s) >= R^2 w.
```

If `R w >= 2M`, the off-diagonal real part is at least `R^2 w/2`.
An ordered pair is popular when

```text
Re(z_t conjugate(z_s)K(t,s)) >= w/4.
```

The registered popular-pair lower bound is

```text
E >= R^2 w/(4M).
```

If `d_t` are the degrees in the resulting symmetric graph, the number of
ordered two-step paths, allowing equal endpoints, is

```text
sum_t d_t^2 >= E^2/R.
```

## Frozen critical exponents

Ignore logarithmic factors and set

```text
A=M=X,    V=X^(7/10),    w=X^(2/5).
```

At the target `R=X^(21/25)`, popular ordered pairs have exponent at least
`27/25`, average degree exponent at least `6/25`, and ordered two-step paths
have exponent at least `33/25`.

These are consequences of the registered abstract inequalities only. They
do not prove that the endpoint difference of a two-step path is popular.

## Registered adverse model

For any finite `R` and `0<w<=M`, take an orthonormal family
`e_0,e_1,...,e_R`, put `a=sqrt(A)e_0`, and

```text
u_t=sqrt(M)(sqrt(w/M)e_0+sqrt(1-w/M)e_t).
```

Then every large value equals `V=sqrt(Aw)` and every off-diagonal kernel
equals `w`. Thus all ordered pairs are popular for arbitrary `R`. Arbitrary
labels may be declared widely separated. This refutes any skeleton theorem
based only on common projection, row norm, separation labels, and scalar
pairwise coherence.

The model may also place `a` and the common component in one coordinate
block. Therefore high values alone force no positive lower bound for
phase-code block entropy.

## Closure gate

The next analytic input must use the actual rows

```text
u_t=(p^(-it))_(p in [X,2X])
```

and do at least one of:

1. show that the popular-difference graph cannot contain the registered
   number of two-step paths;
2. show that many paths force new popular endpoint differences and iterate;
3. force coefficient mass or synchronized energy across multiple genuine
   prime blocks, enabling E10 detector surgery.

## Compute and review rules

- CPython `3.12.3`, optimization level zero, exact `Fraction` arithmetic for
  exponent identities, and deterministic rational finite countermodels.
- No RNG, third-party library, or network.
- Builder cap: 30 seconds and 256 MiB RSS.
- Hostile audit remains deferred to paper stage.
