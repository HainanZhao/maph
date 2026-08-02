# Cycle 171: eligibility-weighted projective-content divisor web

## Claim boundary

`PROVED`: for a complete **seed/range-valid** Cycle-170 source-packet/cross-
edge pair, its target packet is depth `L` precisely when its projective
content clears one explicit threshold. That content has an exact labelled
three-factor divisor decomposition. Its Euler-divisor moment gives a sharp
conditional lower bound on the weighted population of seeded deep packets.

No actual lower bound for that moment or for compatible pairs is proved. In
particular this proves no actual census population, recurrence, E7/E9
skeleton, density improvement, or prime-interval result.

## Content is the simultaneous depth certificate

Use the signed Cycle-170 data

```text
D=q d,       N=a(d+b)-qd,       g=gcd(|D|,|N|),
Q=|D|/g,
Lambda=a C_S/K_S+(|d+b|+1)C_E/K_E.
```

Fix an integer depth `L>=1` and height cap `H`. On a pair whose transported
beta seed is integral and in range, the two Cycle-170 requirements are

```text
Lambda/g <= 1/L,                 |D|L/g <= H.        (1)
```

They hold if and only if

```text
g >= G_req := ceil(max(L Lambda, |D|L/H)).            (2)
```

This includes `Lambda=0`: the first inequality is exact and imposes no
positive lower threshold. Thus no separate denominator-only or raw-content
surrogate is valid.

The ordered Cycle-170 failure is retained: if `g<ceil(L Lambda)`, it is the
amplified-error failure; otherwise, if `g<ceil(|D|L/H)`, it is the capacity
failure. The complement of the seed/range-valid pair set remains its own
first obstruction bank.

## Exact factor web

Put

```text
c=gcd(|d|,|b|),       d0=d/c,       b0=b/c,
u=gcd(|d0|,a),        v=gcd(q,|d0+b0|).               (3)
```

Since `gcd(d0,d0+b0)=1` and `gcd(a,q)=1`, prime-by-prime separation gives

```text
gcd(|qd|,|N|) = gcd(|qd|,|a(d+b)|)
              = c gcd(|q d0|,|a(d0+b0)|)
              = c u v.                               (4)
```

The two edge factors `u,v` are coprime. The source-core factor `c` need not
be coprime to either; for example `(d,b,q,a)=(4,2,1,2)` gives `(c,u,v)=(2,2,1)`.
This counterexample rules out the stronger primitive-factor claim. Every
divisor row retains the complete source/cross-edge/target label together with
`(c,u,v)`.

For a below-threshold pair, define the frozen log-balanced thresholds

```text
C=ceil(G_req^(1/3)),
U=ceil((G_req/C)^(1/2)),
V=ceil(G_req/(CU)).                                  (5)
```

Then `CUV>=G_req`; hence the ordered conditions `c<C`, then `u<U`, then
`v<V` are exhaustive. This is an independent refinement of the retained
Cycle-170 error/capacity label, not a replacement for it.

## Labelled divisor moment and sharp population transfer

Let `w_gamma>=0` be any frozen complete-pair weights on the seed/range-valid
bank, and set

```text
W = sum w_gamma,
M = sum w_gamma g_gamma/G_req(gamma)
  = sum w_gamma/G_req(gamma) sum_(r | c_gamma u_gamma v_gamma) phi(r).  (6)
```

The second identity is the exact Euler expansion `sum_(r|g) phi(r)=g`; it
does not deduplicate divisors or pairs. Since `g` divides `D` and (2) retains
the capacity term,

```text
g/G_req <= H/L.                                      (7)
```

For `H>L`, write `W_deep` for the weight of pairs with `g>=G_req`. The
pointwise bound `g/G_req<1` off that set and (7) on it yield

```text
W_deep >= max(0, (M-W)/(H/L-1)).                      (8)
```

No stronger universal linear consequence follows from only the threshold and
the cap: take subcritical normalized contents tending to `1` from below and
a deep level tending to `H/L`. Thus (8) is supremally sharp for this data.

## What remains

The new genuine bridge is a lower bound for `M` on the actual labelled
Cycle-166/Cycle-170 compatible bank, or a quantitative theorem that the
seed/range, error, capacity, source-core, numerator-absorption, or
denominator-absorption bank carries the required mass. Formula (8) alone
does not generate that input.
