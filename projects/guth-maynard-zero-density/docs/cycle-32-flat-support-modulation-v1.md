# Cycle 32: flat-support reduction for reconstructed block modulations

## Claim boundary

`PROVED`: every reconstructed direction at the self-dual block scale has a
dyadic amplitude component that is nearly flat on `s=X^(lambda+o(1))` blocks,
carries logarithmically large norm, and remains reconstructed with the same
stretched-exponential exponent. This yields a one-parameter support ladder;
no rung is yet excluded, and no skeleton, density, or interval result is
proved.

## Dyadic flattening

Let `E` be the self-dual block basis from Cycle 31,
`J=X^(4/25+o(1))`, and suppose the unit direction `d=Ey` satisfies

```text
||d-v||<=epsilon,
epsilon=exp(-X^(2/25-o(1))),                           (1)
```

for a vector `v` in the span of the scaled prime-phase rows.

Coordinates with `|y_j|<1/(2sqrt(J))` carry total squared mass at most
`1/4`. Split the remaining coordinates into dyadic amplitude bins. There are
`L=O(log X)` relevant bins, so one bin `S` obeys

```text
mu^2=sum_(j in S)|y_j|^2>=3/(4L).                      (2)
```

Project (1) onto the union of blocks in `S` and normalize. With

```text
z_j=y_j/mu,  s=|S|,  d_S=sum_(j in S)z_j e_j,
```

dyadic comparability and (2) give

```text
1/(2sqrt(s))<=|z_j|<=2/sqrt(s),                        (3)
||d_S-mu^(-1)P_Sv||<=sqrt(4L/3)epsilon
 =exp(-X^(2/25-o(1))).                                 (4)
```

Thus arbitrary modulation amplitudes reduce to a factor-four window in
squared magnitude without weakening the stretched-exponential exponent.

## Support ladder

Write

```text
s=X^(lambda+o(1)),  0<=lambda<=4/25.
```

Each selected block contains `X^(21/25-o(1))` primes. Equations (3)--(4)
therefore produce a nearly flat normalized detector on

```text
X^(21/25+lambda+o(1))
```

prime coordinates, with per-prime coefficient magnitude

```text
X^(-(21/25+lambda)/2+o(1)).
```

The separated row exponent remains `21/25`. The exact ladder is:

| `lambda` | prime-coordinate exponent | row exponent | coordinate excess |
|---|---:|---:|---:|
| `0` | `21/25` | `21/25` | `0` |
| `1/25` | `22/25` | `21/25` | `1/25` |
| `2/25` | `23/25` | `21/25` | `2/25` |
| `3/25` | `24/25` | `21/25` | `3/25` |
| `4/25` | `1` | `21/25` | `4/25` |

## Gate effect

`PROVED`: the arbitrary adaptive direction from rank-`J` leverage is reduced
to one of five exponent regimes, up to finer `lambda` subdivision. The
`lambda=0` rung is square in exponent—`X^(21/25)` rows against
`X^(21/25)` prime samples—and is the first generalized-prime-Vandermonde
target. Positive `lambda` rungs have exactly quantified coordinate excess and
should be routed to multiplicative-energy or support-pruning estimates.
