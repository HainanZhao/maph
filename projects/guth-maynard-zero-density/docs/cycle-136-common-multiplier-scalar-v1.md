# Cycle 136: the paired edge has one scalar lock

Assume the strict Cycle-133 range `S>>N^3`, and fix a nonzero represented
difference `d`.  For any two edges `a -> a+d` and `c -> c+d`, the additive
rectangle

```text
(a+d)+c=(c+d)+a
```

gives the exact multiplicative relation

```text
x_(a+d) x_c=x_(c+d) x_a.                          (1)
```

Consequently every edge of difference `d` has one common reduced rational
multiplier

```text
r_d=x_(a+d)/x_a.                                  (2)
```

The Cycle-135 residual therefore factorizes exactly:

```text
x_(a+d)-g^d x_a=(r_d-g^d)x_a.                    (3)
```

Put

```text
kappa_d=NS(r_d-g^d),       L=S/N.                 (4)
```

The distinct rational labels `x_a=p_a/q_a`, with `q_a~N`, have spacing
`>>N^(-2)`.  The elementary large sieve applied to the phases
`ell*kappa_d*x_a`, after a bounded compact-support partition if needed,
gives

```text
sum_(|ell|<=L)
 |sum_(a in E_d) w_a e(ell*kappa_d*x_a)|^2
 << (L+N^2/|kappa_d|)|E_d| X^epsilon.             (5)
```

Thus the diagonal Cycle-135 target follows unless

```text
|kappa_d| << N^3/S.                               (6)
```

By (4), an exceptional multiplier satisfies

```text
|r_d-g^d| << N^2/S^2.                             (7)
```

Since `r_d` is a ratio of two labels of height `N`, its reduced denominator
is `<<N^2`.  Therefore

```text
(den r_d)^2 |r_d-g^d| << N^6/S^2.                 (8)
```

In the strict range `S>>N^3`, (8) has a fixed-power margin.  Legendre's
criterion makes `r_d` a continued-fraction convergent of `g^d`.  The standard
next-denominator inequality then yields

```text
q_next >> S^2/N^4,
A_next >> S^2/N^6.                                (9)
```

The exponent of the jump in (9) is `2(tau-3rho)>0`.  Hence the paired-tail
operator closes at diagonal strength away from one explicit scalar class;
every exceptional difference carries a rational multiplier, its convergent
index, and a power-sized next partial quotient.

No averaged exclusion of these exceptional multipliers, full paired norm,
endpoint, moment, density, or prime-interval theorem is proved.
