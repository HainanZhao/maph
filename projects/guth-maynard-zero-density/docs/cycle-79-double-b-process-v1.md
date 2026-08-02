# Cycle 79: double B-process preserves the anisotropic saddle

## Claim boundary

`PROVED`: a band-limited tube majorant converts the Cycle-77 critical count
into the exact raw Fourier target

```text
sum_(1<=k<=eta^-1)|S_k| < X^(31/25+o(1)),          (1)
S_k=sum_(d~Delta)sum_(q~Q)
    e(k c_0 q exp(2pi d/Delta)).                    (2)
```

The two-dimensional Poisson stationary map for (2) has dual indices

```text
r~k, h~kQ/Delta,                                   (3)
```

stationary amplitude `Delta/(2pi r)`, and logarithmic saddle phase

```text
Psi(k,h,r)=(hDelta/(2pi))log(kc_0/r).               (4)
```

At the Fourier ceiling, `h<=X^(21/25+o(1))`, exactly the independently frozen
prime-row skeleton scale. Frequencies `k<Delta/Q=X^(4/15)` contribute at
most `X^(6/5+o(1))` trivially, leaving strict margin `1/25` to (1).

No uniform stationary-remainder theorem, high-frequency dual bound, ACSI,
packet closure, powered saving, density gain, or interval gain is proved.

## Fourier contract

Let `eta=X^(-83/75+o(1))`. With a fixed nonnegative band-limited majorant of
the vertical tube, Poisson summation in the integer `n` gives

```text
N << eta[Delta Q+sum_(1<=k<<eta^-1)|S_k|].          (5)
```

The volume term has exponent `-13/75`, already below the packet target
`2/15`. Since

```text
2/15-(-83/75)=31/25,                               (6)
```

(1) is the exact strict `L1` target.

## Exact stationary geometry

Write `D=Delta`, `beta=2pi`, and

```text
phi_k(d,q)=k c_0 q exp(beta d/D).
```

For smooth compact dyadic weights, two-dimensional Poisson summation is the
exact sum over integrals with phase

```text
phi_k(d,q)-hd-rq.
```

The stationary equations are

```text
r=k c_0 exp(beta d/D),
h=beta q r/D.                                      (7)
```

They have inverse

```text
d=(D/beta)log(r/(kc_0)),
q=hD/(beta r).                                     (8)
```

The primal Hessian is

```text
[[beta^2 r q/D^2, beta r/D],
 [beta r/D,        0]],

det=-(beta r/D)^2.                                 (9)
```

Thus its signature is zero and the leading stationary amplitude is
`D/(beta r)`. At the stationary point, `phi_k=qr`; subtracting `rq` cancels
that term and leaves `-hd`, proving (4).

For fixed `h`, the Hessian of (4) in `(k,r)` is diagonal:

```text
Psi_kk=-(hD/beta)/k^2,
Psi_rr= +(hD/beta)/r^2,
Psi_kr=0,

det Hess_(k,r)Psi=-(hD/beta)^2/(k^2r^2).           (10)
```

The saddle therefore survives duality; complete ratio folding would erase
information that (10) retains.

## Exact support ledger

If `k=X^(xi+o(1))`, (3) gives

```text
r exponent: xi,
h exponent: xi+1/3-3/5=xi-4/15,
amplitude exponent: 3/5-xi.                        (11)
```

The Fourier ceiling is `xi=83/75`, so

```text
h_max exponent=83/75-4/15=21/25.                  (12)
```

For `xi<4/15`, no positive integer `h` lies in the stationary gradient
range. Even without exploiting this nonstationarity, the trivial contribution
of all such `k` to (1) has exponent

```text
4/15+3/5+1/3=6/5,                                  (13)
```

which is `1/25` below `31/25`. The difficult branch is therefore precisely

```text
X^(4/15)<=k<=X^(83/75),
r~k,
h~kQ/Delta<=X^(21/25).                             (14)
```

## Strategic implication

The high-frequency ACSI problem is now a logarithmic saddle on the same
`21/25` index scale as the prime skeleton, rather than an unrelated
common-denominator rational-point problem. The next step is to make the
stationary expansion uniform at the boundary and then prove cancellation in
the signed `(k,h,r)` sum, routing exact Cycle-78 valuation webs separately.

## Gate effect

E14 advances to
`DOUBLE_B_HIGH_FREQUENCY_LOG_SADDLE_OPEN`.
