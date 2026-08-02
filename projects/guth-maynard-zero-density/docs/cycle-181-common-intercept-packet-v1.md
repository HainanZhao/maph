# Cycle 181: common-intercept exactification and stable packets

## Claim boundary

`PROVED`: below the explicit asymptotic cutoff `10 C H^2/X<1`, every
Cycle-180 stable four-row rectangle has one shared reduced rational intercept

```text
rho = q/d = q'/e,
q=d*j1-a*h1,       q'=e*k1-b*s1.                           (1)
```

The denominator of `rho` divides both physical pair gaps, and at most `H`
such intercepts can occur for the fixed translate `beta`. Consequently, if
the Cycle-180 direct critical light branch supplies its stable population,
one labelled common-intercept stable packet contains
`X^(21/25-o(1))` ordered distinct-label rectangles.

This is an exact beta-sensitive packet reduction. It proves no upper bound
inside a packet, no aggregate recurrence, density improvement, or
prime-interval theorem.

## Pair intercept identity

For the left oriented pair put

```text
eta_i = j_i+beta-h_i alpha_ell,
delta = a-d alpha_ell = eta_2-eta_1,
q = d*j1-a*h1.                                             (2)
```

The original row residuals obey `|eta_i|<=C/X`; hence

```text
q+d beta = d eta_1-h1 delta,
|q+d beta| <= C(d+2h1)/X <= 5 C H/X,                       (3)
```

because `d<=H` and the first selected height is at most `2H`. The analogous
right-pair identity gives `q' + e beta` with the same bound. These identities
retain the first physical row and its residual; they are not a consequence of
the slope determinant alone.

## Exactification of the new four-row invariant

Define the beta-cancelling integer

```text
I=e q-d q'.                                                (4)
```

Using (3) at both labels cancels the common fixed beta and gives

```text
|I| <= e |q+d beta|+d |q'+e beta|
     <= 10 C H^2/X.                                       (5)
```

At the frozen cutoff this integer has absolute value below one, so

```text
I=0,                q/d=q'/e=:rho.                        (6)
```

This proof is independent of the exponential spacing and of the nonzero
slope determinant `D`; those Cycle-180 facts remain retained in the packet
state rather than replaced.

Write `rho=p/v` in lowest terms. Equation (6) forces

```text
v | d,       v | e,                                       (7)
```

and (3), after multiplication by `v/d`, gives

```text
|p+v beta| <= 5 C H/X.                                    (8)
```

For every fixed `v<=H`, the right side of (8) is below `1/2`, so there is at
most one possible integer `p`. Thus the complete stable rectangle census
partitions into at most `H` common-intercept packets. The packet index
includes `(p,v)` and every member retains both labels, four physical rows,
both gaps and numerator gaps, all residuals, `D`, and the stable product
shell.

## Population consequence

Cycle 180 gives `W_cross>=X^(32/25)/32` in a critical light branch and
places only `O_{C,c}(X^(28/25) log^2 X)` rectangles below its stable product
cutoff. Therefore, after enlarging a frozen `X_0(C,c)` once so that the latter
term is at most `X^(32/25)/64`, its stable population obeys

```text
W_stable >= X^(32/25)/64.                                  (9)
```

Partitioning (9) over at most `H=X^(11/25)` intercepts supplies one packet
with at least

```text
W_rho >= X^(21/25)/64.                                     (10)
```

ordered distinct-label stable rectangles. This is the promised
`X^(21/25-o(1))` packet. It is not an E7/E9 recurrence theorem: (10) is a
coefficient-preserving population obligation whose individual packet must
still be bounded or realized by a nonrational saturator.

## New analytic target

The active E13 census is now the stable rectangle census **inside one fixed
common rational intercept packet**, with its four-row data and determinant
and product shells intact. The next engine must either obtain a strict upper
bound there or construct a nonrational actual packet saturator. Raw pair
counts, beta-free scalar products, exact-rational beta-zero towers,
low-product rectangles, and a packet decomposition without an in-packet
estimate are non-progress.
