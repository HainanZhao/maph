# Cycle 34 stable-anchor prime-kernel preregistration v1

## Claim boundary

This cycle may translate stable anchor reconstruction of the original
rank-one detector into an unweighted prime-kernel large-values problem and
compute its exact exponent gap. It may not prove that kernel bound, handle
unstable anchors or transverse reconstruction, close the skeleton target, or
promote density/interval consequences.

## Frozen normalized convention

Let

```text
x_t=M^(-1/2)(p^(-it))_(X<p<=2X),
b=M^(-1/2)(a_p)_p,
H(t,s)=<x_t,x_s>=M^(-1)K(t-s),
K(h)=sum_(X<p<=2X)p^(-ih).
```

Assume the separated skeleton `C` satisfies

```text
|<x_t,b>|>=sqrt(rho),
rho=X^(-3/5-o(1)).
```

## Frozen one-anchor reduction

If for some anchor `a in C` and scalar `gamma`,

```text
||b-gamma x_a||<=epsilon,
epsilon=o(sqrt(rho)),
```

then norm comparison gives `||gamma|-1|<=epsilon`. For every `t in C`,

```text
|H(t,a)|>=(sqrt(rho)-epsilon)/(1+epsilon)
          >=sqrt(rho)/2
```

for sufficiently large `X`. Hence

```text
|K(t-a)|>=M sqrt(rho)/2=X^(7/10-o(1)).
```

The differences preserve `X^(3/5)` separation and lie in the frozen
polynomial height range.

## Frozen stable multi-anchor reduction

If

```text
||b-sum_(a in A)gamma_a x_a||<=epsilon,
|A|=X^o(1), sum_a|gamma_a|=X^o(1),
```

then for each row some anchor satisfies

```text
|K(t-a)|>=X^(7/10-o(1)).
```

Color by such an anchor. One anchor captures `|C|X^(-o(1))` rows, so a
one-anchor kernel theorem loses no fixed power.

## Frozen exponent ledger

The checked classical large-values/cluster theorem gives generic skeleton
exponent `1`; the target is `21/25`. Register missing saving `4/25` for the
unweighted kernel problem:

```text
# {h: X^(3/5)-separated, |h|<=X^(12/5),
       |K(h)|>=X^(7/10-o(1))}
 <= X^(21/25+o(1)).
```

This is a sufficient theorem for the stable-anchor branch only.

## Checks

- Exact finite norm/triangle constants.
- Exact exponents `rho/2 -> 7/10`, generic `1`, target `21/25`, gap `4/25`.
- Pin Cycles 18, 26, and 33 v2.
- CPython `3.12.3`, `Fraction`, no RNG/network.
