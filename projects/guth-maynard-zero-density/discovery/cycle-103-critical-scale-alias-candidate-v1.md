# Cycle 103 discovery candidate: the discarded critical value

`CONJECTURED` before proof sealing.

Cycle 100 counts coefficient pairs satisfying the critical derivative, but a
strong near-double row also has small value at that critical point. For a
fixed Cycle-102 core,

```text
B=lambda*B0, C=lambda*C0,
r=C0*t/(B0*s)=N/R,
t*=log(r)/(s+t).
```

Hence the critical exponential sum is homogeneous in `lambda`:

```text
f(t*)=A-lambda*K,
K=B0*r^(s/(s+t))+C0*r^(-t/(s+t)).
```

The number `K` lies in `Q(r^(1/(s+t)))`, so it is positive algebraic of
degree at most `s+t`. If many scales have small critical value, their
differences force a short near-integer multiple of `K`. This converts the raw
scale multiplicity into an algebraic alias rather than trying to bound it by
divisor counting alone.

Kill tests: verify the derivative identity and critical-value homogeneity on
every small exact core; then test the spacing inverse using exact rational
surrogates. A surviving short alias is structured output, not a failed test.
