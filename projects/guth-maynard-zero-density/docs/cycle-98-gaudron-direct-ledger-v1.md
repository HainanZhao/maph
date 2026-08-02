# Cycle 98: the direct pointwise transcendence ledger saturates

## Claim boundary

`PROVED`: direct worst-case insertion of the Cycle-97 algebraic root into
Gaudron's Theorem 1.1 guarantees only

```text
|D log(alpha)-2pi| >= exp(-X^(12/5+o(1))).          (1)
```

This is too weak to certify any fixed-power separation. The conclusion is
scoped to this theorem with the generic Cycle-97 degree/height envelope. It
does not exclude sparse-trinomial refinements, averaged mode estimates,
special low-degree rows, or direct counting of the near-double branch.

## Actual mode support

The Cycle-95 stationary equations are

```text
2pi u/D=log((h-Delta)n/(hn')),
2pi v/D=log(c0 Delta n'/(m(h-Delta))).              (2)
```

All ratios in (2) lie in fixed compact subsets of `(0,infinity)` on the
registered smooth dyadic supports. Therefore

```text
|u|+|v|<<D,       M=max(|u|,|u+v|)<<D,             (3)
D=X^(3/5+o(1)).
```

Cycle 97 gives `deg(alpha)<=2M`, hence for `k=Q(i,alpha)`

```text
d=[k:Q]<=2deg(alpha)<=4M=X^(3/5+o(1)).             (4)
```

## Source specialization

Use Gaudron's Theorem 1.1 with `n=2,t=1`,

```text
u1=log(alpha),       u2=log(-1)=i*pi,
beta1=D,             beta2=2i.
```

The resulting form is

```text
Lambda=D log(alpha)+2i log(-1)=D log(alpha)-2pi.    (5)
```

For `alpha!=1`, the two logarithms are `Q`-linearly independent because the
first is real nonzero and the second purely imaginary nonzero. The root
`alpha=1` is elementary and is separated before invoking the theorem.
The field, logarithm, and coefficient-height hypotheses are checked in
`cycle-98-gaudron-source-v1.md`.

## Exponent calculation

Fix Gaudron's free parameter `e` as an absolute constant. Root and coefficient
heights contribute powers of `log X`, hence `X^o(1)`, while (4) contributes
the positive powers. In the notation of Theorem 1.1,

```text
a0                                      =X^(3/5+o(1)),
log b+a0 log e                          =X^(3/5+o(1)),
(1+d log a/log e)^2                     =X^(6/5+o(1)).
```

Their product has exponent

```text
3/5+3/5+6/5=12/5,                       (6)
```

which proves (1). But a useful power separation `X^(-C)` has negative
logarithm only `C log X=X^o(1)`. Thus (1) is asymptotically much smaller and
cannot close even one lower-band block by direct pointwise insertion.

## Structural consequence

The exact/nonexact distinction is no longer the right battlefield. The
remaining engine must use at least one feature discarded by the generic
pointwise theorem:

1. sparsity of the defining trinomial;
2. averaging over integer modes and coefficients;
3. the explicit algebraic critical relation in the near-double branch; or
4. a compiler turning recurrent roots into a rational transport web.

## Gate effect

E14D-L advances to
`POINTWISE_TRANSCENDENCE_SATURATED_SPARSE_AVERAGED_OR_CRITICAL_COUNT_OPEN`.
