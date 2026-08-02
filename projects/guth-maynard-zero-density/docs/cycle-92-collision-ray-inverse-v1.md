# Cycle 92: excess equal-height collisions form a rational-ray web

## Claim boundary

`PROVED`: every fixed-`a` class of Cycle-90 saddle collisions lies on one
primitive rational ray, and distinct `a` values carry distinct primitive
labels.  A class of multiplicity `M` has primitive denominator `O(Q/M)`.
Consequently any excess collision count yields a quantitative dyadic web of
injectively labelled `a` values.

This is an inverse lemma, not the analytic collision bound.  It does not
convert the web to a transport seed, close the equal-height branch, prove the
full signed moment, or promote a density or interval gain.

## Collision relation

Fix positive dyadic windows and suppose

```text
|n'-n alpha_a|<=C/K,
alpha_a=exp(beta a/D),  beta=2pi,
n,n'~Q, |a|<=cD.                                   (1)
```

Writing `(p,q)=(n'/g,n/g)`, `g=gcd(n,n')`, gives the primitive rational
label `p/q=n'/n`.  Equation (1) implies

```text
|p/q-alpha_a| << 1/(KQ).                           (2)
```

## One ray for each `a`

Suppose two collisions at the same `a` have distinct reduced labels `p/q`
and `r/s`. Since `q,s<<Q`, Farey separation gives

```text
|p/q-r/s| >= 1/(qs) >> Q^-2.                       (3)
```

But (2) and the triangle inequality give `O((KQ)^-1)`.  Their ratio is
`K/Q`, whose minimum exponent on the registered lower band is

```text
16/25-1/3=23/75>0.                                (4)
```

Thus (3) is impossible for sufficiently large `X`: all collisions at fixed
`a` are integer multiples `(n',n)=t(p,q)` of one primitive ray.

## Distinct `a` values have distinct labels

On `|a|<=cD`, the derivative of `alpha_a` is comparable to `1/D`.  If the
same reduced `p/q` served distinct integers `a,b`, (2) would imply

```text
|alpha_a-alpha_b| << 1/(KQ),
```

whereas the mean-value theorem gives `>>|a-b|/D>=1/D`.  The ratio `KQ/D`
has minimum exponent

```text
16/25+1/3-3/5=28/75>0.                            (5)
```

This is again impossible for sufficiently large `X`.  The map from occupied
`a` values to primitive rational rays is injective.  No transcendence or
unproved Diophantine lower bound is used.

## Multiplicity and dyadic extraction

If a ray `(p,q)` has `M` multiples in the fixed dyadic box, every multiplier
`t` satisfies `tq<<Q`. Therefore

```text
M << Q/q,  hence q << Q/M.                         (6)
```

Partition the nonzero class sizes into dyadic intervals `[M,2M)`. There are
`O(log Q)` such intervals.  If the total collision count is `C_tot`, one
interval contains `>>C_tot/log Q` collisions and hence at least

```text
>> C_tot/(M log Q)                                 (7)
```

distinct `a` values.  By (5), their primitive labels are injective; by (6),
all their denominators are `O(Q/M)`.

## Bound-or-web output

For every fixed `epsilon>0`, either

```text
C_tot <= Q X^epsilon,                              (8)
```

which is the Cycle-90 analytic target up to `X^epsilon`, or (7) exports a
dyadic rational-ray web above that threshold.  The web retains `a`, its
primitive `(p,q)`, and class multiplicity `M`; it is suitable input to E16
but is not yet a genuine original transport seed.

## Gate effect

The equal-height branch advances to
`EQUAL_HEIGHT_ANALYTIC_BOUND_OR_INJECTIVE_RAY_WEB_TO_E16_OPEN`.

