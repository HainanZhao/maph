# Cycle 172: primitive eligible fibre does not force a divisor-moment surplus

## Claim boundary

`PROVED`: reduced source-packet data collapse Cycle 171's projective content
to two coprime cross-edge factors. Nevertheless, the listed **signed abstract**
local primitive, divisibility, range, balance, and beta-seed conditions do not
force its eligible divisor moment to exceed mass. An explicit labelled affine
family has `M=W/2` and fails only target denominator capacity.

This is a countermodel for the *signed local interface*. Its values
`alpha=-4/5` and `alpha_plus=-7/10` are outside the actual positive
exponential curve `alpha_ell=exp(2pi ell/Delta)-1`. It therefore cannot
obstruct the actual Cycle-165--166 census, does not contradict a global
exponential/fibre coupling theorem, and proves no recurrence, skeleton,
density, or interval result.

## Primitive pullback

For a reduced source packet `gcd(d,b)=1`, Cycle 171's factorization becomes

```text
g=gcd(|qd|,|a(d+b)-qd|)
 =gcd(|d|,a) gcd(q,|d+b|)=u v.                       (1)
```

The factors are coprime: a common prime would divide both `d` and `d+b`, or
both `a` and `q`. Hence the eligible labelled divisor expansion is the genuine
two-factor expression

```text
uv = sum_(r|u) sum_(s|v) phi(r) phi(s).              (2)
```

Reducedness alone supplies neither a lower bound for `u` nor one for `v`.

## Exact avoidance family

For each integer `m>=1`, set

```text
H=10m,       K_S=2m,       K_E=5m,       L=2m,
alpha=-4/5, E=3/2, alpha_plus=-7/10,
d=5, b=-4, q=2, a=3, beta=0.
```

For `0<=t<=floor(m/3)`, retain the full labelled rows

```text
h_t=15(m+t),       j_t=-12(m+t),
h_t_plus=10(m+t),  j_t_plus=-7(m+t).                (3)
```

They have exact source and target beta-strip residual zero. Moreover

```text
5 alpha-(-4)=0,
2E-3=0,
1+alpha_plus=E(1+alpha),
h_t_plus=2h_t/3,  j_t_plus=j_t+h_t-h_t_plus.         (4)
```

Thus source and target lie in `[H,2H]`, every source row is divisible by
`a=3`, and the affine cross edge is integral. The source packet and edge
depth ledgers are saturated:

```text
d K_S=H,        q K_E=H,
2 H (1/5)/(a K_E)=4/15<=1.                           (5)
```

So this is a complete primitive, range-valid, balance-valid, beta-retaining
fibre of `1+floor(m/3)` labelled rows.

## Typed obstruction and moment

The projective data are independent of `m`:

```text
D=10,       N=-7,       g=c=u=v=1,       Q=10,
Lambda=0.
```

The requested depth is `L=2m`, but target capacity is `floor(H/Q)=m`.
Equivalently the Cycle-171 threshold is

```text
G_req=ceil(|D|L/H)=2,       g/G_req=1/2.             (6)
```

For arbitrary nonnegative weights on the retained labelled rows,

```text
M=sum w g/G_req = W/2.                               (7)
```

The entire family is therefore a typed denominator-capacity obstruction,
while both cross-factor divisors avoid every nontrivial divisor.

## Consequence

No theorem using only reduced source packets and the frozen **signed abstract**
local integrality/range/balance/seed rules can force `M>W`. The actual
positive-exponential primitive-fibre question remains open. A positive route
must use that curve or another global exponential/fibre invariant to produce
numerator or denominator divisor incidence beyond the local interface.
