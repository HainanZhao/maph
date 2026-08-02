# Cycle 90: equal height is a shorter saddle-discrepancy problem

## Claim boundary

`PROVED`: the `h=h'` part of the Cycle-87 signed second moment has a positive
quadratic-form representation.  A smooth B-process in its `r` variable
reduces the inner length from `K` to `Q`.  The dual diagonal has exactly the
required exponent `xi+14/15`; the B-process remainder lies below it by
`1/3`.  The off-diagonal obstruction is the affine saddle collision

```text
|n'-n exp(2pi a/D)| << 1/K,  a~D, n,n'~Q.          (1)
```

Its volume is below the required count by `xi-3/5`, at least `1/25` on the
whole lower band.

No bound for (1), full equal-height estimate, diagonal second moment, new
Fourier-band closure, density gain, or interval gain is proved.

## Exact equal-height form

For the Cycle-81 leading column write

```text
A_(k,h,r)=D/(beta r) W(beta^-1 log(r/(kc0)))
           V(hD/(beta Qr))
           e((hD/beta)log(kc0/r)).
```

After expanding the second moment, the equal-height branch is

```text
E_0=sum_k U(k/K) sum_h |sum_r A_(k,h,r)|^2.        (2)
```

Here `r~K`, `h~H=KQ/D`, and one leading amplitude has size `D/K`.  The
same-`r` diagonal in (2) has exponent

```text
K * H * K * (D/K)^2 = K D Q,
xi+14/15.                                          (3)
```

Thus square-root cancellation in the `r` polynomial, averaged over `h`, is
exactly sufficient and no stronger estimate is required.

## B-process in the logarithmic variable

Put `t=hD/beta`.  Up to a common unit phase, the `r` phase is `-t log r`.
Poisson summation produces phases

```text
-t log r+n r.
```

Their positive stationary branch satisfies

```text
r=t/n,  n~t/K~Q,
phase=t(1-log(t/n)),
second derivative=n^2/t,
amplitude=sqrt(t)/n~sqrt(K/Q).                     (4)
```

The standard smooth B-process remainder is no larger than one stationary
cell on the fixed interior charts; after inserting `D/K` and summing `k,h`,
its second-moment exponent is `xi+3/5`, below (3) by `1/3`.  Boundary charts
are handled by the same smooth zero-extension convention as Cycle 81.

The transformed polynomial has length `Q`, whereas the number of `h`
samples is

```text
H=KQ/D,  H/Q=K/D=X^(xi-3/5+o(1)).                 (5)
```

At `xi=16/25`, the surplus in (5) is already `X^(1/25)`.

## The collision surface

In a dual cross term, all `h`-dependent phases except

```text
e((hD/beta)log(n/n'))
```

cancel.  Poisson localization of the smooth `h` sum at an integer `a`
therefore gives

```text
|(D/beta)log(n'/n)-a| << 1/H.
```

Since `n~Q` and `DH=KQ`, this is equivalent up to fixed window constants to
(1).  The index `a` has length `D`.  The expected volume of (1) is

```text
D*Q*(1/K)=X^(14/15-xi+o(1)).                       (6)
```

The target is `Q=X^(1/3+o(1))`; target minus volume is precisely
`xi-3/5`, the same surplus as (5).

For

```text
F(a,n)=n exp(beta a/D),
```

direct differentiation gives

```text
F_aa=(beta^2 n/D^2)exp(beta a/D),
F_an=(beta/D)exp(beta a/D),
F_nn=0,
det Hess F=-(beta^2/D^2)exp(2beta a/D).             (7)
```

Thus the remaining surface is an affine nondegenerate saddle, not a flat
rational-approximation strip.

## New theorem contract

`CONJECTURED`: on every fixed smooth annulus, the Schwartz-weighted count in
(1) is `O(X^(1/3+o(1)))`, or else its excess yields an explicit anchored
collision web.  Annular polynomial losses must be absorbed by the frozen
Schwartz decay before summation.

This contract closes the equal-height branch if proved.  It is genuinely
two-dimensional: fixing `n` and applying the existing one-variable order-
three estimate loses the averaging that creates the margin in (6).

## Gate effect

E14D-L advances to
`EQUAL_HEIGHT_BPROCESS_SADDLE_DISCREPANCY_OR_WEB_OPEN`.

