# Cycle 44: fixed-slope Beatty results and derivative tests do not close the strip

## Claim boundary

`PROVED` from checked published hypotheses and exact exponent arithmetic:
the cited fixed-slope Beatty-prime results do not apply uniformly to the
Cycle 43 slopes, and the explicit van der Corput derivative theorem supplies
at most saving `12/175` at the Fourier resolution needed for the target
strip. This is below both Cycle 39 margins.

This is scoped to the cited theorems. It is not a universal obstruction to
Beatty methods, exponent pairs, averaging in `(p,k)`, or a purpose-built
two-variable estimate. No density or interval gain is proved.

## 1. Literature boundary

Banks--Shparlinski, Theorem 5.1 of
[Prime numbers with Beatty sequences](https://arxiv.org/abs/0708.1015),
assumes fixed real `alpha,beta`, with `alpha` irrational of finite type; its
implied constants depend on those fixed parameters. Their Theorems 4.1--4.2
likewise begin with a fixed irrational `gamma` of finite type.

Cycle 43 instead has the triangular family

```text
alpha_k(X)=exp(2pi k/X^(3/5))-1,                      (1)
```

which depends on `X` and tends to zero for fixed `k`. The required
uniformity is therefore absent from the checked hypotheses.

Banks--Guo, Theorem 1.1 of
[Consecutive primes and Beatty sequences](https://arxiv.org/abs/1612.01468),
treats fixed irrational finite-type slopes and assumes a strong
Hardy--Littlewood conjecture for every finite shift set. It does not supply
the unconditional, shrinking-slope weighted prime-pair estimate required by
`LCAM_s`.

## 2. Exact derivative scales

To resolve the fractional parts in (1), consider

```text
f_(p,h)(x)=h p(exp(2pi x/Delta)-1),
Delta=X^(3/5), h=X^nu, p asymp X.                     (2)
```

On `x` in a fixed-proportion subinterval of `[1,Delta]`,

```text
f^(d)(x) asymp X^(nu+1-3d/5).                        (3)
```

The hypotheses of the explicit theorem in Juan Arias de Reyna,
[Explicit van der Corput's d-th derivative estimate](https://arxiv.org/abs/2407.02094),
hold with `lambda` and `Lambda` comparable. Its displayed Theorem (2), for
`D=2^d`, bounds the normalized sum by the maximum of three terms. Translating
them to power savings over a sum of length `Y=X^(3/5)` gives

```text
A_d:  (6/5)/2^d,
B_d:  (3d/5-1-nu)/(2^d-2),
C_d:  2(nu+1)/2^d.                                   (4)
```

The guaranteed saving is the minimum of (4).

## 3. Resolution mismatch

The subunit Cycle 43 strip requires Fourier cutoff

```text
h<=X^(11/25),       nu=11/25.                         (5)
```

At this resolution:

```text
d=3: saving 3/50,
d=4: saving 12/175,
d>=5: A_d ceiling <=3/80.                             (6)
```

Thus `d=4` is best within the checked derivative theorem, with

```text
12/175 < 7/50 < 17/50.                               (7)
```

For comparison, at the single lowest Fourier mode `d=3` gives `2/15`, but
that mode resolves only intervals of width `X^o(1)`, not the required
`X^(-11/25)` strip.

## 4. Gate effect

`PROVED` scoped boundary: neither fixed-slope Beatty distribution nor a
one-variable derivative test closes the lattice-row branch. The next engine
must average jointly over `p` and `k`, exploit the prime weights before
Fourier truncation, or obtain a genuinely two-variable exponent-pair/sieve
estimate. The gate becomes `JOINT_PK_CURVATURE_OR_NONLATTICE_ROW_OPEN`.
