# Cycle 41: smooth sampling converts the hollow problem to a signed annular form

## Claim boundary

`PROVED`: hollow separated samples of each centered amplified polynomial are
controlled by its mean square on a slightly enlarged annulus, with a
power-negligible leakage term. The annular mean has an exact signed Fourier
kernel, so the Cycle 40 positive coherent floor is absent from the
formulation.

`CONJECTURED`: the resulting weighted annular vector mean has the strength
needed for `AMPR_3` or `AMPR_4`. No kernel-count, density, or interval gain is
proved.

## 1. Smooth hollow sampling

Let `f(t)=sum_j a_j exp(-it lambda_j)` with all frequencies in an interval of
length `B>=1`. After a carrier modulation, choose a Schwartz function
`phi` whose Fourier transform equals one on that interval after scaling.
Writing `phi_B(u)=B phi(Bu)` gives the exact reproducing identity

```text
f(t)=integral_R phi_B(t-u)f(u)du.                     (1)
```

Cauchy--Schwarz with measure `|phi_B(t-u)|du` yields

```text
|f(t)|^2 <= ||phi||_1 integral_R |phi_B(t-u)||f(u)|^2du. (2)
```

For a `Delta`-separated set, summing the kernels in (2) costs `O_phi(B)`.
If

```text
C subset {t:Delta<=|t|<=H},
W={u:Delta/2<=|u|<=H+Delta/2},                        (3)
```

Schwartz decay of order `N` bounds the contribution outside `W` by

```text
O_(phi,N)(sum_j|a_j|)^2 |C| (B Delta)^(-N).           (4)
```

Consequently

```text
sum_(t in C)|f(t)|^2
 <<_phi B integral_W|f(u)|^2du
    +(sum_j|a_j|)^2 |C|(B Delta)^(-N).                (5)
```

The implicit constants depend on the fixed reproducing kernel and `N`, not
on `m`, `X`, or the row set.

For `F_(m,s)`, take `B_m` comparable to `s+m`. Summing (5) over
`m<=A=X^(3/10)` and using `|C|<=X^(9/5)`, coefficient mass `X^(s+1+o(1))`,
and `N=9`, the total leakage exponent is

```text
2s+2+9/5+3/10-9(3/5)=2s-13/10.                       (6)
```

This is `47/10` for `s=3` and `67/10` for `s=4`, below their targets
`61/10` and `71/10` by `7/5` and `2/5`. The coherent zero packet is therefore
removed with strict power margin.

## 2. Exact signed annular collision form

Put `a=Delta/2`, `b=H+Delta/2`. Direct expansion gives

```text
integral_(a<=|t|<=b)|F_(m,s)(t)|^2dt
 =sum_(n,n') c_m(n)c_m(n') Psi_(a,b)(log(n/n')),      (7)

Psi_(a,b)(u)=2[sin(bu)-sin(au)]/u,
Psi_(a,b)(0)=2(b-a).                                  (8)
```

Unlike the triangular kernel in Cycle 40, `Psi_(a,b)` changes sign. This is
not a defect: cancellation among the extremely dense prime-monomial near
collisions is exactly what removes the coherent zero packet. Replacing (8)
by its absolute value would restore the forbidden global floor.

## 3. The remaining theorem

Equations (5)--(6) show that either bound

```text
sum_(2<=m<=A) (s+m) integral_W|F_(m,s)(u)|^2du
 <=X^(s+31/10+o(1))                                  (ASAM_s)
```

implies `AMPR_s`. Thus `ASAM_3` and `ASAM_4` inherit the Cycle 39 closure
margins `17/50` and `7/50`.

`ASAM_s` is a signed, annular prime-monomial cancellation theorem. It cannot
be replaced by a count of absolute near collisions. Candidate mechanisms
are a finite-difference identity in the `q` variable, shifted-prime
curvature after expanding one prime factor, or a spectral estimate for the
annular kernel matrix.

## Gate effect

`PROVED` constructive notch: E7 is
`SIGNED_ANNULAR_PRIME_MONOMIAL_CANCELLATION_OPEN`. The coherent zero packet
has been removed at the operator level with ample leakage margin. The next
cycle must exploit the sign in (8), starting with `s=3`, rather than revert
to positive near-collision counting.
