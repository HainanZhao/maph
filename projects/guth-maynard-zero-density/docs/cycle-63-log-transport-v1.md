# Cycle 63: E13 is a two-dimensional transport census

## Claim boundary

`PROVED`: summing the Cycle-46 inverse-log wrap count over
`h in [H,2H]`, `H=X^(11/25)`, is equivalent up to absolute strip constants
to counting

```text
|j+beta-h alpha_ell|<=C/X,
alpha_ell=exp(2pi ell/Delta)-1,                      (1)
```

for `ell<=cDelta`, `Delta=X^(3/5)`. The surface
`F(h,ell)=h alpha_ell` has everywhere nonzero Monge--Ampere determinant, and
differencing in `h` removes `beta` exactly.

To improve the powered-coordinate saving beyond `1/5`, the total census in
(1) must have exponent strictly below `16/25`. Summing the checked pointwise
Huxley--Sargos bound gives `19/25`; E13 must therefore save more than `3/25`
through the `h` average.

No such two-dimensional estimate is proved here, and no `LCAM_s`, density,
or interval gain follows.

## Inversion and volume scales

Cycle 46's condition

```text
||(Delta/(2pi))log(1+(j+beta)/h)||<=C Delta/(hX)
```

is inverted by the mean-value theorem to (1). For each `(h,ell)` the strip
has width `X^(-1)` in `j`, so `j` is unique when it exists.

The parameter box has exponents

```text
h count:       11/25,
ell count:     15/25,
strip density: -25/25.
```

Its random-volume heuristic is therefore only `X^(1/25)`, far below the
required `X^(16/25)`. The large gap is room for resonant rational families;
it is not evidence for a proved random bound.

## Exact transport curvature

For `c_*=2pi/Delta`,

```text
F_hh=0,
F_(h ell)=c_* exp(c_*ell),
F_(ell ell)=h c_*^2 exp(c_*ell),
det Hess(F)=-c_*^2 exp(2c_*ell).                    (2)
```

Thus the Hessian determinant is a negative square, uniformly nonzero, with
exponent `-6/5`. This is stronger structural information than the pointwise
one-dimensional identity: the family is a nondegenerate saddle surface even
though it is linear in `h`.

## Beta-free differencing

Let `N_ell` count the `h` satisfying (1), and let `T=sum_ell N_ell`. Two hits
at `h` and `h+d` imply

```text
||d alpha_ell||<=2C/X,                              (3)
```

because

```text
F(h+d,ell)-F(h,ell)=d alpha_ell.                    (4)
```

The phase shift `beta` has disappeared. Define the weighted necessary-pair
census

```text
P=sum_(1<=d<=H)(H-d)
    #{ell<=cDelta: ||d alpha_ell||<=2C/X}.           (5)
```

Cauchy--Schwarz gives

```text
T^2 <= Delta(T+2P).                                 (6)
```

Therefore the sufficient pair target for `T<X^(16/25+o(1))` is

```text
P<X^(17/25+o(1)),                                   (7)
```

with a strict margin for the powered saving. Pointwise Huxley--Sargos inserted
termwise in (5) gives exponent `6/5`, while the random difference-volume
scale is `12/25`. The new theorem must recover more than `13/25` over that
crude pair sum, or attack the triple census directly.

## Analytic routes

`CONJECTURED` candidates:

1. a two-dimensional determinant/large-sieve theorem using (2), with the
   `h` weight retained rather than maximizing first;
2. a first-spacing/second-spacing argument on the beta-free curves (3),
   separating rational approximants shared by many `d`;
3. a bilinear sieve in `(d,ell)` after exponentiation, exploiting that the
   near-integer shift is unique at width `1/X`.

The proof target is now the explicit weighted census (5)--(7), not an
unspecified “extra curvature saving.”

## Gate effect

E13 advances to `LOG_TRANSPORT_PAIR_CENSUS_LT_17_25_OPEN`.
