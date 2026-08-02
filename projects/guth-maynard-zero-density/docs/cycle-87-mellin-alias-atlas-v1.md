# Cycle 87: the signed second moment has a Mellin-alias atlas

## Claim boundary

`PROVED`: the signed second moment has an exact primal pair kernel whose atom
diagonal is the desired `X^(xi+14/15+o(1))`.  In the exact Cycle-81 dual
coordinates, every off-diagonal interaction belongs to one of three explicit
branches: same `h`, nonstationary small `h-h'`, or a stationary integer alias
`1<=|m|<<Q`.

No diagonal-strength second-moment bound, new Fourier-band closure, large-
value theorem, packet closure, density gain, or interval gain is proved.

## Primal pair kernel

Let

```text
z_(d,q)=c0 q exp(2pi d/D),
S_k=sum_(d,q)a_(d,q)e(kz_(d,q)),
```

with the frozen smooth dyadic weights absorbed into `a_(d,q)`.  For a fixed
smooth `U(k/K)`, expansion and Poisson summation give exactly

```text
M2(K)=sum_k U(k/K)|S_k|^2
     =sum_(u,v)a_u conjugate(a_v)
       K sum_(m in Z)hat U(K(m-(z_u-z_v))).         (1)
```

Identical atoms `u=v` contribute

```text
K*DQ=X^(xi+14/15+o(1)),                            (2)
```

which is precisely the Cycle-86 target.  The periodic pair kernel in (1)
has circle mean `U(0)=0`, because `U` is supported away from zero.  Hence an
absolute near-collision count destroys the cancellation needed for (2).

## Dual cross phase

Cycle 81 writes one dual column, up to smooth amplitudes, as

```text
e((hD/(2pi))log(kc0/r)),
r~K, h~KQ/D.                                       (3)
```

Crossing `(h,r)` with `(h',r')` and applying Poisson in `k` leaves, up to
terms independent of `k`,

```text
Phi(k)=t log k-mk,
t=D(h-h')/(2pi).                                   (4)
```

For `h!=h'`,

```text
Phi'(k)=t/k-m,
Phi''(k)=-t/k^2.                                   (5)
```

A stationary alias therefore satisfies

```text
k=t/m=D(h-h')/(2pi m),                             (6)
Phi''(t/m)=-m^2/t,
amplitude=|Phi''|^(-1/2)=sqrt(|t|)/|m|
                              ~sqrt(K/|m|).         (7)
```

The sign of `m` matches the sign of `h-h'`; displays use absolute values for
support statements.

## Exact support trichotomy

The dual support has

```text
|h|,|h'|<<KQ/D.
```

Equation (6) gives

```text
|m|~D|h-h'|/K.                                    (8)
```

Thus all interactions split into:

1. `h=h'`: a logarithmic correlation in `(r,r')`; this is not the primal
   atom diagonal and still requires cancellation.
2. `0<|h-h'|<<K/D`: no nonzero integer `m` lies in the stationary range;
   this is the nonstationary branch.
3. `K/D<<|h-h'|<<KQ/D`: stationary aliases with
   `1<<|m|<<Q`.

The alias index lands exactly on the original denominator scale.  This is a
self-dual arithmetic obstruction, not a generic stationary remainder.

## New theorem contract

The Cycle-86 moment follows if the combined contribution of the three
branches is

```text
<<X^(xi+14/15+o(1))                                (9)
```

uniformly for `16/25<=xi<58/75`.  A failure must now be reported with its
branch and, in the stationary case, its explicit `(m,h-h',r,r')` alias data.
That output can be tested against the Cycle-78 valuation web instead of being
discarded as an anonymous large-sieve exception.

## Gate effect

E14D-low advances to
`MELLIN_ALIAS_TRICHOTOMY_BOUND_OR_WEB_OPEN`.

