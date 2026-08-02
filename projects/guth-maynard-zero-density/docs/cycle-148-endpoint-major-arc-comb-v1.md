# Cycle 148: one endpoint ray has a `Q/N` resonant comb

## Claim boundary

`PROVED`: on any strict endpoint band `N<=QX^(-delta)`, a positive
fixed-chart endpoint operator has second moment at least `Q/N` times its
diagonal energy.  Frequencies divisible by the reduced endpoint denominator
form the resonant comb; all nonmultiples are power-negligible by exact Poisson
summation in the length-`Q` coefficient variable.

This is an isolated-cell lower bound.  It neither proves target-sized mass
for the cell nor excludes cancellation between endpoint cells in the full
fixed polynomial.  No full second moment, endpoint, density gain, or interval
gain is proved.

## Bounded anchors preserve the endpoint height

Let the bounded rational anchor be `c0=A/B` in lowest terms, and let `p/q`
be a reduced endpoint approximation to `g^a`.  If

```text
c0 p/q=r/h
```

is reduced, then

```text
h=Bq/gcd(Ap,Bq),
q/A<=h<=Bq.                                       (1)
```

Indeed every common prime factor in `gcd(Ap,Bq)` divides either `Aq` or
`Bp`, and coprimality gives the displayed bounded loss.  Thus `h~N` whenever
`q~N`.

Freeze a strict endpoint buffer

```text
|c0 g^a-r_a/h_a|<=c_*/(KQ),
h_a~N,                 N<=QX^(-delta),            (2)
```

where `c_*` is small relative to the fixed support ceiling of `V`.
Cycle 132 supplies (2) on shells with `S>>KQ/q`, since
`|g^a-p/q|<1/(qS)`.

## Poisson separates multiples from nonmultiples

For one mode put

```text
S_a(k)=sum_n V(n/Q)e(k n c0 g^a),                 (3)
```

where `V>=0` is fixed, smooth, and compactly supported inside the positive
axis.  Exact Poisson summation gives

```text
S_a(k)=Q sum_m hat V(Q(m+k c0g^a)),               (4)
```

up to the frozen Fourier-sign convention.

If `h_a` does not divide `k`, reducedness gives

```text
||k r_a/h_a||>=1/h_a.                             (5)
```

The perturbation in (2) is `O(1/Q)`, whereas `h_a/Q<=X^(-delta)`.  Hence
`||k c0g^a||>>1/h_a`, and Schwartz decay in (4) yields, for every fixed
`J`,

```text
S_a(k)<<_(J,V) Q(Q/N)^(-J).                       (6)
```

If `h_a|k`, the rational phase is integral.  For `K<=k<=2K`, the endpoint
buffer makes the residual phase on the support of `V(n/Q)` lie inside a
fixed `pi/6` wedge.  Therefore

```text
Re S_a(k)>=c_V Q                                  (7)
```

for a fixed `c_V>0`.

## The comb lower bound

For a set `C` of endpoint modes with fixed interior-chart weights
`0<u_0<=u_a<=u_1`, put

```text
T_C(k)=sum_(a in C)u_a S_a(k),
F_C(k)=sum_(a in C, h_a|k)u_a.                    (8)
```

Choose `J` in (6) large enough relative to the fixed `delta` and the mode
range.  Uniformly on `K<=k<=2K`, all nonmultiple terms are then negligible
against one resonant term, and

```text
|T_C(k)|>=c F_C(k)Q                               (9)
```

whenever `F_C(k)>0`.  Since all terms in `F_C(k)^2` are nonnegative,

```text
sum_(k~K)F_C(k)^2
 >=sum_(a in C)u_a^2 #{k~K:h_a|k}
 >>K/N sum_(a in C)u_a^2.                         (10)
```

Combining (9)--(10) proves

```text
sum_(k~K)|T_C(k)|^2
 >>KQ^2/N sum_(a in C)u_a^2.                      (11)
```

The diagonal atom energy of this cell is comparable to

```text
KQ sum_(a in C)u_a^2.                             (12)
```

Thus the exact excess factor is

```text
Q/N=X^(1/3-rho+o(1)).                             (13)
```

It is a fixed power on every band `rho<1/3`.

## Structural consequence

The lower-band diagonal moment cannot be proved by decomposing into strict
continued-fraction endpoint operators and summing their second-moment norms:
each such positive chart is already super-diagonal by (13).  The required
cancellation is necessarily cross-cell—between rational combs or between
their coefficient-faithful core and halo—and must use the common coefficient
vector before the endpoint norm is taken.

This is not yet a counterexample to the full fixed polynomial.  Cross-cell
terms can be negative, and no theorem here says that one endpoint class
carries a target-sized share of the original moment.

## Gate effect

The gate becomes `CROSS_ENDPOINT_COMB_CANCELLATION_OR_INVERSE_OPEN`.
