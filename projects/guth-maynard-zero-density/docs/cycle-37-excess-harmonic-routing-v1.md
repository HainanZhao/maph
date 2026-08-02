# Cycle 37: entropy excess can hide at arbitrary harmonic order

## Claim boundary

`PROVED`: on an equal-arc phase histogram, entropy excess controls total
Fourier mass but does not select a bounded harmonic. There are exact positive
histogram perturbations preserving the first moment while placing their new
mass at any prescribed order `2<=m<=L-2`. At the Cycle 36 arc resolution,
scalar pigeonholing loses `X^(3/10)` and the resulting individual harmonic
thresholds are below the existing useful scales.

This is a scoped abstract histogram no-go, not an actual-prime
counterexample. Joint prime-row coupling or a vector-valued estimate over
all harmonics remains open. No kernel-count, density, or interval gain is
claimed.

## 1. Fourier form of excess

For the cyclic group of `L` equal arcs, write `u_j=1/L` and

```text
hat f(m)=sum_(j=0)^(L-1) f_j exp(2pi i m j/L).
```

Parseval gives exactly

```text
chi^2(q||u)=L sum_j|q_j-u_j|^2
            =sum_(m=1)^(L-1)|hat q(m)|^2.              (1)
```

If the von Mises projection satisfies
`1/2<=qstar_j/u_j<=2` and the relative perturbation is at most `1/2`, the
elementary Taylor bounds for `(1+x)log(1+x)` give

```text
D(q||qstar) asymp sum_j |q_j-qstar_j|^2/qstar_j
                 asymp sum_m|hat(q-qstar)(m)|^2.       (2)
```

Thus excess entropy is a vector-valued higher-harmonic quantity. Passing to
one scalar harmonic costs up to `L` in squared magnitude.

## 2. Exact harmonic hiding

Fix any `m` with `2<=m<=L-2` and put

```text
q_j=qstar_j+(2a/L)cos(2pi m j/L).                      (3)
```

For sufficiently small absolute `|a|`, (3) is positive. Cyclic
orthogonality gives exactly

```text
sum_j(q_j-qstar_j)=0,
sum_j(q_j-qstar_j)exp(2pi i j/L)=0,
hat(q-qstar)(m)=hat(q-qstar)(L-m)=a.                  (4)
```

Therefore total mass and the first Fourier coefficient are unchanged, while
the new Fourier mass occurs only at the prescribed pair `m,L-m`. Equation
(2) gives

```text
D(q||qstar) asymp a^2                                (5)
```

with constants independent of `m`. `PROVED`: raw KL excess cannot prefer
low order even when the first moment is fixed exactly.

## 3. Frozen exponent loss

Cycle 35 uses `L=X^(3/10+o(1))`. If one knows only
`E(q)>=X^(-e)`, (1)--(2) force at best one harmonic with normalized size

```text
X^(-(e+3/10)/2+o(1)),
```

or unnormalized prime-kernel size

```text
X^(1-(e+3/10)/2+o(1)).                                (6)
```

Two registered boundaries are

```text
E comparable to r^4=X^(-6/5):  kernel exponent 1/4,
E comparable to r^2=X^(-3/5):  kernel exponent 11/20.
```

The first is below the Cycle 19 `X^(2/5)` popular-kernel scale; the second
is still below the original `X^(7/10)` threshold. If the witnessing harmonic
varies by row, scalar colouring also costs `L=X^(3/10)`, larger than the
entire missing saving `4/25`.

## Gate effect

`PROVED` scoped saturation: KL excess plus scalar Fourier pigeonholing cannot
close the kernel gate. E7 must retain the whole harmonic vector, prove that
actual prime rows forbid high-order hiding, or combine harmonic order with
E10 detector surgery. The independent E9 sifted-curvature route is promoted
to equal priority.
