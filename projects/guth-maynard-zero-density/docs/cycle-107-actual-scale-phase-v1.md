# Cycle 107: the actual scale saturator is a geometric phase

## Actual anchor sublattice

`PROVED`. Write `K=A0/S0` reduced. The identities

```text
A=p0*n=lambda*K,
B=p0*n'=lambda*B0,
C=q0*m=lambda*C0
```

hold in integers exactly when `lambda` is a multiple of

```text
lambda0=lcm(
  S0*p0/(p0,A0),
  p0/(p0,B0),
  q0/(q0,C0)).                                     (1)
```

At `lambda=lambda0`, the base actual indices are

```text
n0=lambda0*A0/(S0*p0),
n0'=lambda0*B0/p0,
m0=lambda0*C0/q0.                                 (2)
```

Every actual scale has `lambda=lambda0*ell` and indices
`(n,n',m)=ell(n0,n0',m0)`.

## Stationary and phase homogeneity

`PROVED`. The Cycle-94 stationary equations depend on

```text
(H-Delta)n/(Hn'),
c0 Delta n'/(m(H-Delta)).                         (3)
```

They are unchanged when `(H,Delta,n,n',m)` is multiplied by `ell`. Hence a
base stationary point `(H0,Delta0)` scales to
`(ell H0,ell Delta0)`.

For

```text
F=Delta log(c0 Delta/m)-H log(H/n)
 +(H-Delta)log((H-Delta)/n'),
```

all logarithmic ratios are invariant and all exterior factors are linear.
Therefore

```text
F_ell=ell F0.
```

The complete projective Poisson phase with fixed modes `mu,nu`,

```text
Phi=cF-mu H-nu Delta,
```

obeys the exact identity

```text
Phi_ell=ell Phi0.                                  (4)
```

## Geometric and weighted cancellation

`PROVED`. With `e(z)=exp(2pi i z)`, the geometric-series identity and
`|sin(pi x)|>=2||x||` give

```text
|sum_(ell<=L)e(ell Phi0)|
 <=min(L,1/(2||Phi0||)).                           (5)
```

If amplitudes are `a_ell`, Abel summation gives

```text
|sum_(ell<=L)a_ell e(ell Phi0)|
 <=min(L,1/(2||Phi0||))
   (|a_L|+sum_(ell<L)|a_ell-a_(ell+1)|).           (6)
```

Thus Cycle 106's unsigned all-scale saturator cancels unless its base phase
is near an integer and the actual amplitudes have controlled variation.

## Inverse output and boundary

A failure of (6) to save must retain the rational anchor `c0`, beta-bearing
payload, Poisson modes, base indices, stationary coordinates, and the
near-integral base phase `Phi0`. This is substantially more rigid than an
unsigned divisor web, but it is not automatically a Cycle-67 seed.

No variation estimate for the actual B-process amplitudes, phase-resonance
to seed theorem, singleton/large-degree aggregate, weak/simple-root estimate,
complete moment, density gain, or interval gain is proved here.
