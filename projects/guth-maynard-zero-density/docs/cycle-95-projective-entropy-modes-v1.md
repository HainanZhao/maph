# Cycle 95: every exact projective entropy mode is central

## Claim boundary

`PROVED`: after Poisson summation in the two projective height variables,
the Cycle-94 entropy phase has no exact noncentral stationary mode. Exact
stationarity occurs only at `u=v=0`, where it reproduces

```text
p0(n-n')=q0m.                                      (1)
```

This is qualitative. No uniform lower bound for near-stationary noncentral
modes, full alias estimate, moment theorem, density gain, or interval gain is
proved.

## Mode equations

Let `c=D/(2pi)` and subtract Poisson modes `u h+v Delta` from `cF`. The
stationary equations are

```text
F_h     =2pi u/D,
F_Delta =2pi v/D.                                  (2)
```

Put `g=exp(2pi/D)`. Exponentiating (2) and using the Cycle-94 derivatives
gives

```text
(h-Delta)n/(hn')=g^u,
c0 Delta n'/(m(h-Delta))=g^v.                      (3)
```

Eliminating `h,Delta` from (3) yields

```text
c0 n-c0 n'g^u-mg^(u+v)=0.                         (4)
```

For the reduced rational anchor `c0=p0/q0`, equation (4) is the integer
Laurent relation

```text
p0 n-p0 n'g^u-q0 m g^(u+v)=0.                     (5)
```

## Transcendence input

The checked Gelfond--Schneider theorem states that if algebraic
`alpha!=0,1` and algebraic irrational `beta` are fixed, every value of
`alpha^beta` is transcendental. Take

```text
alpha=-1, beta=-2i/D, Log(-1)=i*pi.
```

Then one value is `exp(2pi/D)=g`, so `g` is transcendental. The hypotheses
and source are recorded in `cycle-95-gelfond-schneider-source-v1.md`.

## Complete exponent-coincidence split

Multiply (5) by a power of `g` if necessary. Since `g` is transcendental,
the coefficient of every distinct exponent among

```text
0, u, u+v                                           (6)
```

must vanish.

- If `u=0` but `v!=0`, the isolated coefficient `-q0m` cannot vanish.
- If `u+v=0` but `u!=0`, the isolated coefficient `-p0n'` cannot vanish.
- If `v=0` but `u!=0`, the isolated constant coefficient `p0n` cannot
  vanish.
- If the three exponents are distinct, the same constant coefficient is
  isolated.
- Only `u=v=0` remains. Then (5) is exactly (1).

All indices and anchor components are positive, so no discarded coefficient
can vanish accidentally.

## Quantitative boundary

Gelfond--Schneider proves only that a noncentral Laurent trinomial is nonzero.
It does not provide a lower bound uniform in the growing integer `D`, modes,
or coefficients. Therefore near-stationary noncentral modes remain a genuine
quantitative transcendence/discrepancy problem and are not removed by this
cycle.

## Gate effect

E14D-L advances to
`EXACT_ALIASES_CENTRAL_NEAR_PROJECTIVE_MODES_QUANTITATIVE_OPEN`.

