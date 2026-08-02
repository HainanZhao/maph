# Cycle 34: stable anchors reduce to the unweighted prime kernel

## Claim boundary

`PROVED`: a one-anchor, or coefficient-stable subpower multi-anchor,
reconstruction of the original detector forces an unweighted prime kernel to
be large on a separated set of the same cardinality up to subpower loss. The
remaining kernel theorem needs a `4/25` saving. That theorem, unstable anchor
representations, and transverse reconstruction remain open; no density or
interval result is proved.

## One anchor

Normalize the dyadic prime rows and original coefficient vector by

```text
x_t=M^(-1/2)(p^(-it))_p,
b=M^(-1/2)(a_p)_p.
```

The source large-value hypothesis is

```text
|<x_t,b>|>=sqrt(rho),   rho=X^(-3/5-o(1)).             (1)
```

Suppose Cycle 26's reconstruction is captured by one row:

```text
||b-gamma x_a||<=epsilon,
epsilon=o(sqrt(rho)).                                  (2)
```

Because `b` and `x_a` are unit, (2) implies
`||gamma|-1|<=epsilon`. Combining (1)--(2),

```text
|<x_t,x_a>|
 >=(sqrt(rho)-epsilon)/(1+epsilon)
 >=sqrt(rho)/2                                         (3)
```

for all sufficiently large `X`. With

```text
K(h)=sum_(X<p<=2X)p^(-ih),
<x_t,x_a>=M^(-1)K(t-a),
```

(3) becomes

```text
|K(t-a)|>=M sqrt(rho)/2=X^(7/10-o(1)).                 (4)
```

Translation by `a` preserves the skeleton's `X^(3/5)` separation and its
height bound `X^(12/5)`.

## Stable subpower many anchors

More generally, suppose

```text
||b-sum_(a in A)gamma_a x_a||<=epsilon,
|A|=X^o(1),  sum_a|gamma_a|=X^o(1).                    (5)
```

For every row, (1) and (5) force at least one anchor with

```text
|K(t-a)|>=X^(7/10-o(1)).                               (6)
```

Color rows by a witnessing anchor. Since `|A|=X^o(1)`, one anchor captures a
subpower proportion. Thus a one-anchor theorem proves the entire stable
multi-anchor branch without fixed-power loss.

## Exact remaining theorem

The necessary kernel statement is

```text
# {h: h are X^(3/5)-separated, |h|<=X^(12/5),
       |sum_(X<p<=2X)p^(-ih)|>=X^(7/10-o(1))}
 <=X^(21/25+o(1)).                                     (7)
```

The checked generic large-values and cluster estimates give skeleton exponent
`1`; (7) requires exactly `4/25` saving. Unlike the original problem, its
coefficient vector is fixed and unweighted. Unlike Cycle 25, the kernel value
is only `X^(-3/10)` after normalization, not near one, so the existing
three-prime Matveev argument does not apply.

## Gate effect

`PROVED`: stable anchor reconstruction is now completely reduced to (7).
The live branches are:

1. prove the unweighted prime-kernel recurrence bound (7);
2. show Cycle 26's reconstruction coefficients admit a stable subpower
   anchor approximation;
3. treat unstable or genuinely transverse reconstruction separately.
