# Cycle 71: the primitive-fraction wedge closes unconditionally

## Claim boundary

`PROVED`: every dyadic packet cell satisfying

```text
2 theta+kappa<6/25                                  (1)
```

meets the strict packet-count target and contributes strictly less than
`X^(17/25+o(1))` to the weighted beta-free pair census. Equality in (1)
only ties and is not promoted without an additional margin.

This closes a region of the E13 packet atlas, not the full pair census. No
powered, density, or interval gain is proved.

## Primitive-fraction count

On a fixed bounded `alpha` interval, a denominator `q` admits only `O(q)`
possible numerators `a`. There are `X^(theta+o(1))` denominators in the
dyadic block `q=X^(theta+o(1))`. Hence the number of reduced fractions in
the block is at most

```text
sum_(q~Q) O(q)=X^(2theta+o(1)).                      (2)
```

Cycle 64 proves that distinct primitive packets cannot share a reduced
fraction, so (2) is also an upper bound for the packet count
`N(theta,kappa)`.

Cycle 65 requires

```text
N(theta,kappa)<X^(6/25-kappa)                       (3)
```

with strict exponent margin. Comparing (2) and (3) gives exactly (1).

## Weighted pair contribution

One depth-`K` packet has pair weight exponent `11/25+kappa`. Combining this
with (2) gives total exponent

```text
11/25+kappa+2theta.
```

Condition (1) makes this strictly smaller than `17/25`, exactly the Cycle-63
pair target. Thus the packet and weighted formulations close on the same
open wedge; no conversion loss occurs.

At `kappa=0`, the wedge contains every `theta<3/25`. On the depth axis it
contains every `kappa<6/25`. The boundary
`2theta+kappa=6/25` is an endpoint tie.

## Residual atlas

The shallow analytic region is reduced to

```text
2theta+kappa>=6/25,
theta+kappa<=11/25,
0<=kappa<=6/25.                                     (4)
```

Only (4) needs the Cycle-70 unfurled-curvature theorem. Depths strictly above
`6/25` remain in the structured branch, where a beta-free packet must still
acquire a genuine seed before recurrence is realized.

## Literature boundary

`OBSERVED` source check: Jing-Jing Huang, *Rational points near planar curves
and Diophantine approximation*, arXiv:1403.7388, definition (1.1) and
Theorem 1, counts points `(a/q,b/q)` whose two coordinates have a common
denominator. The E13 packets instead combine the frozen grid `ell/Delta`
with an independent denominator `q`; Huang's theorem does not directly imply
(3). The elementary fraction budget above requires no such identification.

## Gate effect

E13 advances to
`RESIDUAL_2THETA_PLUS_KAPPA_GE_6_25_UNFURLED_CURVATURE_OPEN`.
