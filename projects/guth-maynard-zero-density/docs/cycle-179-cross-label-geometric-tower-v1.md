# Cycle 179: exact-rational cross-label towers and affine-area transport

## Claim boundary

`PROVED`: every finite collection of actual positive-exponential labels for
which `alpha_ell` is exactly rational gcd-compresses to one rational-base
tower. At beta zero, its exact **zero-residual** rows have ordered distinct-label mass
`O(H^2)=X^(22/25)`, uniformly in that base. Thus exact rational roots cannot
form a critical `X^(32/25)` cross-label saturator.

`PROVED`: in the Cycle-178 light branch, any direct-target failure produces
at least `X^(32/25)/4` oriented actual triangles, each satisfying a
beta-eliminated integer affine-area resonance of width `2CH/X`.

Neither statement bounds that approximate area-resonance census, controls
arbitrary fixed-beta approximate rational roots, proves an E7/E9 recurrence
bound, improves density, or improves prime intervals.

## Gcd compression of exact rational labels

Put `z=exp(2 pi/Delta)`. Let `S` be a nonempty finite set of labels with
`z^ell=1+alpha_ell in Q`, and let

```text
g=gcd{ell: ell in S},       ell=g m_ell.
```

The positive integers `m_ell` have gcd one. Choose Bézout coefficients
`c_ell` with `sum c_ell m_ell=1`. Then

```text
z^g = product_(ell in S) (z^ell)^(c_ell) in Q.               (1)
```

Write this reduced rational number as `u/v>1`. Every label in `S` is therefore
a member of the one rational-base tower

```text
1+alpha_(gm)=(u/v)^m,
alpha_(gm)=(u^m-v^m)/v^m,                                  (2)
```

and `gcd(u^m-v^m,v^m)=1`. This proves compression of an arbitrary finite
exact-rational label set; the special C177 base `(r+1)/r` was only one case.

## Exact beta-zero tower mass

At beta zero, an exact row at (2) obeys

```text
j=h(u^m-v^m)/v^m.
```

If `v>=2`, coprimality forces `v^m|h`. With
`J=floor(log_v(2H))`, only `m<=J` has a row in `[H,2H]`, and its count is at
most `H/v^m+1`. Hence

```text
sum_m N_m <= H/(v-1)+J <= 3H,                              (3)
U_exact=sum_(m!=n)N_mN_n <= 9H^2.                           (4)
```

The inequalities are uniform even if `u,v` vary with the scale. If `v=1`,
then `u>=2`; chart admissibility gives
`m<=floor(2 pi c/log u)<=9`, and each label has at most `H+1` rows. Thus
`sum N_m<=18H` for `H>=1`, and `U_exact<=324H^2`. In either case the exact
rational tower is a fixed `2/5` exponent below the Cycle-178 critical
cross-label scale.

The beta-zero/exact-row scope is essential: (3) does not bound arbitrary
width-`C/X` fixed-beta hits at a large denominator.

## Beta-eliminated affine area

Take two distinct actual rows `(h1,j1),(h2,j2)` at one label `ell`, and one
actual row `(h3,j3)` at a different label `m`. Let

```text
e_i=j_i+beta-h_i alpha_i,
A=(h2-h3)j1+(h3-h1)j2+(h1-h2)j3.                           (5)
```

`A` is an integer. The three coefficients in (5) sum to zero, so beta
cancels exactly. Because the first two labels agree, direct expansion gives

```text
|A-h3(h2-h1)(alpha_ell-alpha_m)|
 <= (C/X)(|h2-h3|+|h3-h1|+|h1-h2|)
 <= 2CH/X.                                                   (6)
```

This is an oriented, label-preserving, beta-free area resonance. Unlike a
raw pair difference, it retains the two same-label source rows and the third
physical row; it is the proposed state for the next analytic census.

## Critical triangle population

Let `L` be the number of admitted labels, `N_ell` their actual fixed-beta
fibre counts, and `T=sum N_ell`. With `R=ceil(X^(6/25))`, assume the
Cycle-178 light branch `N_ell<=2R`. The number of ordered triangles used in
(5) is exactly

```text
Q_tri=sum_ell N_ell(N_ell-1)(T-N_ell).                       (7)
```

Since `n(n-1)>=n-1` for every nonnegative integer `n`,

```text
Q_tri >= (T-2R) sum_ell N_ell(N_ell-1)
      >= (T-2R)(T-L).                                       (8)
```

Here `L<=Delta=X^(15/25)`. For `X>=2^25`, direct-target failure
`T>=X^(16/25)` implies `T>=4R` and `T>=2L`; hence

```text
Q_tri>=T^2/4>=X^(32/25)/4.                                  (9)
```

Thus the remaining critical problem is an upper bound—or an actual
saturator—for the labelled area-resonance population (6), not for independent
rational roots.

## Gate effect

The exact-rational cross-label candidate is banked as subcritical. The active
E13 task is now a coefficient-preserving estimate for the approximate
three-row affine-area census in (6), or a realized actual saturator for it.
This is a new analytic engine; no density or interval claim is promoted.
