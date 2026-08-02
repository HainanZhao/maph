# Cycle 45: joint large sieve saves `2/25`; wrap de-aliasing is the lock

## Claim boundary

`PROVED`: a direct joint large-sieve treatment of the prime and resonance
indices saves `2/25` at the Cycle 43 Fourier resolution, twice the best
checked one-variable derivative saving but only half the missing `4/25`.
The exact loss is the `h`-fold wrap coloring of the curved frequencies.

`CONJECTURED`: curvature reduces the effective wrap multiplicity enough to
recover the remaining saving. No curved prime-pair estimate, `LCAM_s`,
density, or interval gain is proved.

## 1. Wrap coloring

Fix a constant `c_0>0` small enough that `k<=c_0 Delta` keeps the exponential
factor bounded, and define

```text
theta_k=h(exp(2pi k/Delta)-1) mod 1.                  (1)
```

Before reduction modulo one, consecutive frequencies have spacing comparable
to `h/Delta`, and the total lifted range has length `O(h)`. Any circular arc
of length `c h/Delta` therefore meets `O(h)` frequencies: each of the `O(h)`
integer lifts contains only `O(1)` indices. Greedy coloring gives `O(h)`
classes, each `c h/Delta`-separated modulo one.

This bound is uniform for `1<=h<=X^(11/25)<Delta`.

## 2. Classical large sieve

Let

```text
P(theta)=sum_(X<n<=2X) a_n exp(2pi i n theta),
sum_n|a_n|^2=X^(1+o(1)).                              (2)
```

The classical separated-frequency large sieve in the form displayed as
(1.32) in Helfgott's
[The ternary Goldbach problem](https://arxiv.org/abs/1501.05438), applied
with `delta_0 asymp h/Delta` to every color, gives

```text
sum_(k<=c_0 Delta)|P(theta_k)|^2
 <<h(X+Delta/h) sum_n|a_n|^2
 <<(hX+Delta)X^(1+o(1)).                              (3)
```

Since `X>Delta`, the exponent of (3), for `h=X^nu`, is `2+nu`.
The hypotheses used here are exactly: coefficient support length `X`,
within-color separation `h/Delta`, and `O(h)` colors. Primality is not used.

## 3. Joint first moment

Cauchy--Schwarz over `K=X^(3/5)` resonance indices yields

```text
sum_(k<=K)|P(theta_k)|
 <=K^(1/2)(sum_k|P(theta_k)|^2)^(1/2)
 <=X^(13/10+nu/2+o(1)).                              (4)
```

The trivial exponent is `1+3/5=8/5`, so (4) saves

```text
3/10-nu/2.                                           (5)
```

At the required resolution `nu=11/25`, this is

```text
3/10-11/50=2/25.                                     (6)
```

This is a genuine joint-variable improvement over Cycle 44's `12/175`, but
it remains below `4/25`.

## 4. Exact de-aliasing target

Parameterize an improved frequency decomposition by an effective color loss
`h^mu`, `0<=mu<=1`. Repeating (3)--(5) gives saving

```text
3/10-mu nu/2.                                        (7)
```

At `nu=11/25`, recovering the full missing `4/25` requires

```text
mu<=7/11.                                             (8)
```

Recovering only the narrower Cycle 39 margin `7/50` requires `mu<=8/11`.
Complete de-aliasing (`mu=0`) would save `3/10`; naive coloring is `mu=1`.

Thus the next theorem is quantitative and falsifiable: exploit exponential
curvature to reduce effective wrap multiplicity from `h` to at most
`h^(7/11+o(1))`, with prime weights and the curved prime-pair condition
retained. Merely improving a constant or the fixed-`h` derivative bound does
not address this lock.

## Gate effect

`PROVED` partial analytic gain in the joint auxiliary sum: `2/25` is banked,
but it is not yet an `LCAM_s` or density gain. E7 becomes
`WRAP_DEALIASING_7_11_OR_NONLATTICE_ROW_OPEN`.
