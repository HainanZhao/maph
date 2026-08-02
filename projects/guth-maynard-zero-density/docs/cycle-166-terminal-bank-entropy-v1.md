# Cycle 166: terminal-bank entropy forces a massed anchored web

## Claim boundary

`PROVED`, conditional on the Cycle-165 critical fixed-beta four-anchor
input: a labelled terminal bank of size `X^(38/25-o(1))` contains either

1. a rank-one anchored exponential-shift/lattice web with
   `X^(1/25-o(1))` parent witnesses;
2. a rank-two low-plane induced anchored shift web with
   `X^(1/25-o(1))` parents; or
3. a genuinely beta-seeded packet state with `X^(2/25-o(1))` parents.

The statement retains every parent four-anchor label. It does not bound the
original census or any web, prove a skeleton bound, improve zero density, or
improve prime intervals.

## Canonical rank-one states

For a rank-one witness put `ell'=ell+u`,
`E_u=exp(2pi u/Delta)`, `A=r-sE_u`, and `B=r-s+t`. The Cycle-165 relation is

```text
|A exp(2pi ell/Delta)-B|<=4C_*/X.                   (1)
```

Canonicalize the four anchors by primitive direction and least common
parameter zero. A witness is then a primitive four-subset of the common
parameter fibre

```text
{n: h_0+rn in H_ell, h'_0+sn in H_(ell+u)}.          (2)
```

Its fourth subsets are counted only when the three positive parameters have
gcd one. Otherwise the same four rows belong to a rescaled `(r,s,t)` state.
This makes the projection from witnesses to canonical states label-faithful.
The fixed-beta strip equations imply that every member of (2) has exact
label-difference slope `t` once `H/X` is below the integer-forcing cutoff.

In the near branch `|A|<=X^(-2/5+eta)`, boundedness of the exponential range
and (1) force the integer `B` to be zero. Hence

```text
t=s-r,             |r-sE_u|<=4C_*/X.                (3)
```

After gcd reduction this is a labelled rational approximation packet for
`E_u`; it retains the whole canonical fibre.

In the transverse branch, two distinct values of `ell` for fixed
`(u,r,s,t)` would give

```text
|A| (exp(2pi/Delta)-1) <= 8C_*/X.                   (4)
```

But its left side is `>>X^(-1+eta)`, a contradiction for large `X`.
Thus `ell`, and then the integral `t`, are unique for fixed `(u,r,s)`.
Both near and transverse rank-one states therefore number at most
`O(Delta H^2)=X^(37/25+o(1))`.

## Low planes and seeded packets

For a rank-two low plane, Cycle 165 gives

```text
|D alpha_ell-N|, |D alpha_(ell+u)-N'| << H/X.
```

Set `R=D+N`, `S=D+N'`. Since `1+alpha_(ell+u)=E_u(1+alpha_ell)`,

```text
|S-E_u R| << H/X.                                   (5)
```

Here `R` is a nonzero integer of size `O(H^2)`; for each `(u,R)` the integer
`S` is unique because `H/X=o(1)`. Thus low-plane shift states `(u,R,S)` also
number `O(Delta H^2)=X^(37/25+o(1))`, with the full plane/anchor fibre kept.

A high-content Cycle-165 branch has a beta seed and a canonical maximal
packet depth (using the frozen Cycle-67 enlarged-strip constant) determined
by `(ell,a/q)`. Its critical depth gives
`q<=X^(1/5+o(1))`; on the bounded alpha range `a=O(q)`. Consequently seeded
states `(beta,ell,a,q,h_0,j_0,K_max)` number at most

```text
O(Delta * sum_(q<=X^(1/5)) q * H)=X^(36/25+o(1)).   (6)
```

## Entropy conclusion

Cycle 165 has only finitely many terminal branches. One retains a fixed
share of its `X^(38/25-o(1))` witnesses. If it is rank-one or low-plane,
(2)--(5) and pigeonhole give one state with

```text
X^(38/25-37/25-o(1))=X^(1/25-o(1))
```

parent witnesses. If it is seeded packet, (6) gives
`X^(2/25-o(1))` parents. These are exactly the three stated web outputs.

The finite exponent margins are strict: with `eta=1/100`, a branch with all
state fibres below `X^eta` has rank/plane mass at most `X^(149/100+o(1))`
and packet mass at most `X^(145/100+o(1))`, both below the registered
`X^(151/100)` threshold.
