# Cycle 99 preregistration: critical rational-ray compiler

## Claim boundary

This cycle may compile sufficiently localized Cycle-97 near-double rows into
unique and injective reduced rational labels. It may not bound the full
factorization fiber, cover weakly localized near-double rows, close the alias
moment, or promote a density/interval gain.

## Frozen notation

- `B,C,Q,M,D` are positive integers with `B,C<=Q`.
- `a,b` are nonzero integers of opposite signs with
  `max(|a|,|b|)<=M`; put `w=a-b`.
- `x=2pi/D` and `t*` is the unique critical point.
- `r=-Cb/(Ba)>0`, reduced as `r=N/R`.
- `H=QM`; then `N,R<=H`.
- Freeze a compact exponent envelope `L>=max(|wx|,|wt*|)` and put
  `E=exp(L)`.
- Let `rho=|t*-x|` and `delta_ray=E|w|rho`.

## Preregistered gates

1. Prove `r=exp(wt*)`, `1<=|w|<=2M`, and reduced height at most `H`.
2. Prove `|r-exp(wx)|<=delta_ray` by the mean-value theorem.
3. If `delta_ray<1/(2H^2)`, prove uniqueness of the reduced rational label
   of height at most `H` for fixed `w`.
4. If also `delta_ray<exp(-L)(exp(x)-1)/2`, prove that reduced labels for
   distinct integers `w` are distinct.
5. Substitute Cycle 97's `rho<=2eta/ell` and record the sufficient strong
   localization threshold

```text
2E|w|eta/ell < min(1/(2H^2), exp(-L)(exp(x)-1)/2).
```

6. Define the surviving fiber exactly by
   `C|b|R=B|a|N`, `a-b=w`, with the original sign orientation retained.

## Falsifiers

- Two distinct reduced height-`H` rationals inside the fixed-`w` threshold
  halt uniqueness.
- Equal rational labels for distinct `w` inside the exponential-spacing
  threshold halt injectivity.
- A multiplicity claim that discards `(B,C,a,b)` or sign orientation halts
  the compiler.
