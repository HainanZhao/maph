# Cycle 170: projective lift of a seeded packet through the exponential edge

## Claim boundary

`PROVED`: a source-local packet and an integral, range-valid reduced-rational
cross edge have an exact signed projective target relation. The transported
edge endpoint is a beta seed for that target relation. Its usable depth is
classified by projective content, amplified error, and denominator capacity.

This proves no population of compatible pairs, no deep packet in the actual
census, no recurrence, E7/E9 skeleton, density gain, or prime-interval result.

## Lift identity and seed

Assume

```text
d alpha_ell-b=delta,       qE-a=e,
1+alpha_L=E(1+alpha_ell).
```

Set

```text
D=qd,             N=a(d+b)-qd,
g=gcd(|D|,|N|),
Q=|D|/g,          A=sgn(D)N/g.                       (1)
```

Expanding the exponential identity gives exactly

```text
D alpha_L-N = a delta+e(d+b+delta),
Q alpha_L-A = sgn(D)[a delta+e(d+b+delta)]/g.        (2)
```

If a source strip seed `(h,j,beta)` is eligible for the reduced rational
edge, put `h^+=qh/a`, `j^+=j+h-h^+`. Its target residual is exactly the
source residual minus

```text
(h/a)(1+alpha_ell)(qE-a).                            (3)
```

Thus the original beta is retained at label `L`; it is a genuine seed for the
projectively lifted target packet whenever the target row remains in range.

## Error and two depth limits

Suppose

```text
|delta|<=C_S/(K_S X)<=1,
|e|<=C_E/(K_E X).
```

Then (2) gives

```text
|D alpha_L-N| <= Lambda/X,
|Q alpha_L-A| <= Lambda/(gX),
Lambda=a C_S/K_S+(|d+b|+1)C_E/K_E.                  (4)
```

The error-supported depth and the row-range capacity are independent:

```text
K_err=floor(g/Lambda)  (interpreted as infinity if Lambda=0),
K_cap=floor(H/Q),
K_T=min(K_err,K_cap).                                (5)
```

Only `K_T`, not `g` alone, can be compared with the critical depth
`X^(6/25-o(1))`. Whenever `K_T>=1`, (5) gives both
`Lambda/g<=1/K_T` (with the zero-load inequality read as exact) and
`QK_T<=H`; hence it certifies the reduced packet inequality and admissibility
simultaneously.

## Exhaustive finite classifier

Within this projective-lift architecture, the first failed gate is exactly:

1. transported seed nonintegral or out of range;
2. projective content below the frozen content threshold;
3. error-supported depth below the critical threshold; or
4. denominator capacity below the critical threshold.

Otherwise the record is a seeded deep target packet, with all source packet,
cross-edge, beta, range, and signed projective labels retained. This is a
finite algebraic classification; it does not assert how many records land in
any branch.
