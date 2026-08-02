# Cycle 39: fixed moments turn the harmonic vector into a closing target

## Claim boundary

`PROVED`: for each fixed integer `s>=1`, the mixed polynomial

```text
F_(m,s)(t)=K(t)^s K(mt)
```

has coefficient-square norm `X^(s+1+o(1))`, uniformly for every integer
`m>=2`. Conditional on one explicit hollow separated vector-restriction
estimate at the coefficient-cardinality scale, `s=3` closes the
`X^(-3/5)` harmonic-energy branch and `s=4` closes the `X^(-6/5)` branch,
with margins `17/50` and `7/50` respectively.

`CONJECTURED`: the required vector-restriction estimate holds for the actual
dyadic prime kernel. It is substantially stronger than an ordinary ambient
length mean value and must exploit the sparse prime-monomial labels and the
two linked scales `(t,mt)`.

`OBSERVED`: no kernel-count, density, or interval improvement is proved.

## 1. Coefficient multiplicity stays bounded

Expanding gives

```text
F_(m,s)(t)=sum_(p_1,...,p_s,q)
             (p_1 ... p_s q^m)^(-it).                 (1)
```

Fix an integer represented in (1). A candidate for `q` must be a prime whose
valuation is at least `m`. Since the total prime degree is `s+m`, the number
of candidates is at most

```text
floor((s+m)/m) <= 1+floor(s/2).                       (2)
```

After `q` is chosen, the residual prime multiset has total degree `s` and
has at most `s!` orderings. Thus every coefficient is at most

```text
C_s=(1+floor(s/2))s!,                                 (3)
```

uniformly in `m>=2`. The coefficient sum is exactly `M^(s+1)`. Since the
coefficients are nonnegative integers,

```text
M^(s+1) <= sum_n |a_(m,s)(n)|^2
          <= C_s M^(s+1).                             (4)
```

Hence the square norm has exponent `s+1`. In particular, `C_3=12` and
`C_4=72`. This is a fixed-`s` statement; the constants are uniform in the
growing harmonic order `2<=m<=A`.

## 2. The amplified restriction gate

Retain the Cycle 35 hollow geometry

```text
C subset {t: Delta<=|t|<=H},   |t-t'|>=Delta,
H=X^(12/5), Delta=X^(3/5), A=X^(3/10).                (5)
```

The new analytic target, for fixed `s`, is

```text
sum_(t in C) sum_(2<=m<=A)|F_(m,s)(t)|^2
   <= X^(s+31/10+o(1)).                               (AMPR_s)
```

The exponent is the proposed sparse coefficient energy `s+1`, plus the
separated time-cell exponent `12/5-3/5=9/5`, plus the harmonic range
`3/10`. This decomposition is an exponent ledger, not a proof of
`(AMPR_s)`. An ambient support estimate sees integers near `X^(s+m)` and is
useless when `m` grows. Even off the origin, coherent or near-resonant prime
phases could violate `(AMPR_s)` unless an actual prime-log uncertainty or
spacing mechanism excludes them.

## 3. Exact closure calculation

Suppose every row has `|K(t)|>=V=X^(7/10)` and actual harmonic energy

```text
sum_(2<=m<=A)|K(mt)/M|^2 >= X^(-e).                   (6)
```

Then

```text
sum_m |F_(m,s)(t)|^2
 =|K(t)|^(2s) sum_m|K(mt)|^2
 >=X^(7s/5+2-e-o(1)).                                 (7)
```

Combining (7) with `(AMPR_s)` gives the conditional row-count exponent

```text
|C| <= X^(11/10+e-2s/5+o(1)).                        (8)
```

The two registered branches are:

| harmonic energy | least fixed `s` | `(AMPR_s)` exponent | row-count exponent | margin below `21/25` |
|---|---:|---:|---:|---:|
| `e=3/5` | 3 | `61/10` | `1/2` | `17/50` |
| `e=6/5` | 4 | `71/10` | `7/10` | `7/50` |

Both margins are strict. By contrast, Cycle 38 is `s=1`; even granting the
same cardinality-scale restriction, (8) gives `13/10` and `19/10`. Thus an
unamplified second-moment treatment cannot close either registered branch.

## 4. What theorem is actually left

The central E7 target is now the pair of fixed-moment estimates
`(AMPR_3)` and `(AMPR_4)`, not a scalar selection of a harmonic and not an
unweighted mean square for `K(t)K(mt)`. A proof may proceed by:

1. a sparse large sieve for the labels `p_1...p_s q^m` that is uniform in
   `m` and retains the linked sample geometry `(t,mt)`;
2. a multiscale prime-log uncertainty theorem excluding coherent rows before
   applying a cardinality-scale mean value; or
3. a shifted-prime/monomial near-collision estimate strong enough to supply
   the same exponent after dyadic decomposition.

The theorem must remain hollow, separated, fixed in `s`, and uniform over
`2<=m<=X^(3/10)`. Dropping any of these qualifiers changes the claim.

## Gate effect

`PROVED` conditional reduction: moment amplification converts the Cycle 38
two-scale family into two concrete, positive-margin analytic targets. E7 is
therefore `MOMENT_AMPLIFIED_PRIME_MONOMIAL_RESTRICTION_OPEN`. The next task is
to derive a bilinear or near-collision formulation of `(AMPR_s)` and test
which part of its `X^(9/5)` separated-time factor can be proved without
assuming ambient frequency spacing.
