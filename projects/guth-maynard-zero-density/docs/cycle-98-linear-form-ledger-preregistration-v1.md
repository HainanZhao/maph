# Cycle 98 preregistration: direct linear-form exponent ledger

## Claim boundary

This cycle may determine the strength obtained by direct worst-case insertion
of Cycle 97 into Gaudron's Theorem 1.1. It may not claim that all effective
transcendence methods, sparse-polynomial methods, bounded-degree sectors, or
averaged mode estimates saturate.

## Frozen exponents and hypotheses

- Actual scale: `D=X^(3/5+o(1))`, `Q=X^(1/3+o(1))`.
- Worst projective mode radius: `M<=X^(3/5+o(1))`.
- Cycle-97 root: `deg(alpha)<=2M` and logarithmic height `X^o(1)`.
- Field degree: `d=[Q(i,alpha):Q]<=4M=X^(3/5+o(1))`.
- Coefficient-height and root-height parameters have logarithms `X^o(1)`;
  they may carry powers of `log X` but no positive power of `X`.
- Required useful output is a polynomial separation `X^(-C)` for fixed `C`,
  whose negative logarithm is `X^o(1)`.

## Preregistered calculation

For `n=2,t=1` and fixed `log e`, compute exponent costs in Gaudron's bound:

1. `a0=d X^o(1)`, exponent `3/5`;
2. `log b+a0 log e=d X^o(1)`, exponent `3/5`;
3. `(1+d log a/log e)^2=d^2 X^o(1)`, exponent `6/5`;
4. total negative-log exponent `12/5`.

The gate advances only if the exact sum is `12/5` and the direct guarantee is

```text
|D log(alpha)-2pi| >= exp(-X^(12/5+o(1))),
```

which is asymptotically weaker than every fixed power `X^(-C)`.

## Falsifiers

- A checked hypothesis that forces field degree `X^o(1)` on every actual
  simple-root row invalidates the worst-case saturation conclusion.
- A missing coefficient/independence hypothesis halts the source insertion.
- The result must be described as saturation of this direct insertion only.
