# Cycle 81 discovery candidate: exact q-transform

## Status

`CONJECTURED`: this is a discovery note. It selected the candidate identity;
it is not a proof artifact and cannot promote a claim.

## Candidate

For smooth compactly supported weights `W,V`, write `e(x)=exp(2 pi i x)`,
`beta=2 pi`, and

```text
S_k(W,V)=sum_(d,q) W(d/D)V(q/Q)e(k c0 q exp(beta d/D)).
```

Poisson summation introduces `(h,r)` and the integral

```text
I_(h,r)=int int W(d/D)V(q/Q)
 e(k c0 q exp(beta d/D)-h d-r q) dq dd.
```

The phase is linear in `q`.  If

```text
u=k c0 exp(beta d/D),
y=Q(u-r),
L=hD/beta,
a=L/(Qr),
x_r=beta^(-1)log(r/(kc0)),
```

then exact Fourier inversion suggests

```text
I_(h,r)
 =D/(beta r) W(x_r)V(a)e(L log(kc0/r))
  +O_(W,V)(D/(Q r^2))                         (1)
```

uniformly on the stationary support `r~k`, `h~kQ/D`.  The error comes from
expanding only `log(1+y/(Qr))`; `y` is localized by the Schwartz transform
of `V`.  Summing the error over `r~k`, `h~kQ/D` should cost `O(1)` per `k`.

## Why this may matter

If (1) is correct with uniform boundary charts, the Cycle-79 stationary
remainder problem disappears.  The full Fourier-range accumulated error is
then `O(X^(83/75+o(1)))`, which is below `X^(31/25)` by `2/15`.  The only
remaining E14D task is cancellation in an explicit logarithmic dual sum.

## Falsifiers

1. The Fourier sign produces `V(-a)` rather than `V(a)` under the frozen
   transform convention.
2. A boundary chart contributes more than `D/(Qr^2)` per central `(h,r)`.
3. Summed nonstationary tails are not power-negligible uniformly in the full
   Cycle-79 frequency range.
4. The claimed per-`k` error omits a factor growing as a power of `k`, `Q`,
   or `D`.

