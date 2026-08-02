# Cycle 38: vector harmonics require a two-scale prime-monomial lift

## Claim boundary

`PROVED`: flattening all harmonic evaluations `K(mt)` into one rescaled row
set has sharp collision multiplicity equal to the harmonic range, even when
the original rows are separated. Retaining the original large value produces
an injective two-scale prime-monomial polynomial
`K(t)K(mt)` with exactly `M^2` coefficients for every `m>=2`.

`OBSERVED`: no vector-valued mean estimate for this sparse family is proved,
and entropy excess does not automatically lower-bound its actual harmonic
energy at the transition where cancellation with the von Mises baseline is
possible. No kernel-count, density, or interval improvement is claimed.

## 1. Rescaling collisions are sharp

Let the harmonic range contain the integers `A<=m<2A`, and fix

```text
u=4A^2 Delta,              t_m=u/m.                    (1)
```

For adjacent indices,

```text
t_m-t_(m+1)=u/[m(m+1)]>Delta,                          (2)
```

because `m(m+1)<4A^2`. Thus the `A` ordinates are `Delta`-separated. They
also lie below `4A Delta`, hence inside the original height whenever
`A Delta<=H/4`. Nevertheless

```text
m t_m=u                                                       (3)
```

for every `m`. Therefore the flattened multiset `{mt}` has collision
multiplicity `A`.

At `A=X^(3/10)`, this loss has exponent `3/10`, larger than the missing
`4/25`. Fixed `m` preserves or enlarges separation, but mixing the harmonic
orders does not. The expanded height is

```text
A H=X^(27/10).                                         (4)
```

`PROVED` scoped no-go: a scalar large-values theorem applied after flattening
cannot exploit the vector without an additional de-collision mechanism.

## 2. Keep both scales

Every source row already has `|K(t)|>=V`. Instead of discarding it, define

```text
D_m(t)=K(t)K(mt)=sum_(p,q)(p q^m)^(-it).               (5)
```

For each integer `m>=2`, unique factorization makes

```text
(p,q)->p q^m                                           (6)
```

injective on ordered prime pairs. If `p!=q`, the prime valuations `1` and
`m` identify `p` and `q`; if `p=q`, the sole valuation is `m+1`, which cannot
equal the two-prime pattern. Hence (5) has exactly `M^2` distinct
coefficients, all equal to one, and

```text
sum_n|a_m(n)|^2=M^2.                                   (7)
```

Its ambient integer support is near `X^(m+1)`, so replacing that ambient
length by the sparse cardinality `M^2` is not licensed. The new object is a
prime-monomial curve with one exponent-one coordinate and one exponent-`m`
coordinate.

## 3. Exact vector energy ledger

If a row has actual harmonic energy

```text
sum_(m<=A)|K(mt)/M|^2>=E,                              (8)
```

then exactly

```text
sum_(m<=A)|D_m(t)|^2
 =|K(t)|^2 sum_(m<=A)|K(mt)|^2
 >=V^2 M^2 E.                                         (9)
```

Writing `E=X^(-e)`, the per-row exponent in (9) is

```text
7/5+2-e=17/5-e.                                       (10)
```

For the registered scales:

```text
e=3/5: per row 14/5, target-family sum 91/25;
e=6/5: per row 11/5, target-family sum 76/25.           (11)
```

Thus either vector estimate

```text
sum_(t in C)sum_(m<=A)|D_m(t)|^2
 <=X^(91/25+o(1))   or   X^(76/25+o(1))               (12)
```

under its corresponding energy hypothesis would close the skeleton target.
Equation (12) is a sufficient target, not a proved mean value.

## 4. Entropy-to-energy seam

Cycle 37 controls the Fourier vector relative to the von Mises projection.
Let `v` be the actual higher-harmonic vector, `b` the von Mises vector, and
`e=v-b`. Then

```text
||v||_2 >= ||e||_2-||b||_2,
||b||_2^2 asymp r^4.                                   (13)
```

Consequently excess energy much larger than `r^4` transfers to (8) without
fixed-power loss. At excess comparable to `r^4`, cancellation in (13) is
possible; the quadratically tiny branch instead returns Cycle 36 rigidity.
This transition cannot be silently routed into (12).

## Gate effect

`PROVED` reduction: E7 is now a two-scale, vector-valued sparse
prime-monomial problem. A useful theorem must retain the pair `(t,mt)`, use
the injective coefficient labels `p q^m`, and avoid both the collision loss
`A` and the enormous ambient length `X^(m+1)`. Otherwise the independent E9
sifted-curvature engine is the principal route.
