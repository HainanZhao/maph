# Cycle 94: triple B-process exposes the anchor-difference resonance

## Claim boundary

`PROVED`: combining the stationary values from the `k`, `r`, and `r'`
B-processes produces an exact entropy phase. Its central stationary equations
force the anchor-sensitive linear relation

```text
m=c0(n-n').                                         (1)
```

The phase is homogeneous of degree one in its two remaining height variables
and has identically zero Hessian determinant. Thus (1) is a banked central
web, but nonzero projective entropy aliases remain open.

No bound for the full stationary-alias branch, moment theorem, Fourier-band
closure, density gain, or interval gain is proved.

## Three stationary values

Write `c=D/(2pi)`, `Delta=h-h'`, and hence `h'=h-Delta`. The `k` B-process
has stationary value

```text
c Delta[log(c c0 Delta/m)-1].                       (2)
```

The negative logarithmic `r` phase and positive logarithmic `r'` phase have
values

```text
c h[1-log(c h/n)],
c h'[log(c h'/n')-1].                               (3)
```

Adding (2)--(3), the linear terms cancel because `h-h'=Delta`; the `log c`
terms cancel for the same reason. After dividing by `c`, the phase is

```text
F(h,Delta)
 =Delta log(c0 Delta/m)
  -h log(h/n)
  +(h-Delta)log((h-Delta)/n').                      (4)
```

The original anchor `c0` remains visible.

## Central stationary equations

Direct differentiation gives

```text
F_h     =log((h-Delta)n/(hn')),
F_Delta =log(c0 Delta n'/(m(h-Delta))).             (5)
```

The central equations `F_h=F_Delta=0` imply

```text
(h-Delta)/h=n'/n,
c0 Delta/m=(h-Delta)/n'=h/n.                       (6)
```

Since `Delta/h=(n-n')/n`, equations (6) give (1). For rational
`c0=p0/q0`, central resonance therefore requires the exact integer relation

```text
q0 m=p0(n-n').                                     (7)
```

This is the first stationary-alias output that directly retains the packet
anchor and an integer difference label.

## Projective degeneracy

The Hessian of (4) is

```text
[[1/(h-Delta)-1/h,  -1/(h-Delta)],
 [-1/(h-Delta),      1/Delta+1/(h-Delta)]].         (8)
```

Its determinant vanishes identically. Equivalently,

```text
F(lambda h,lambda Delta)=lambda F(h,Delta).
```

This degeneracy is structural: a generic two-dimensional nonzero-Hessian
bound in `(h,Delta)` cannot close the branch. The surviving curvature is in
the projective ratio `Delta/h`.

## Open alias modes

Poisson summation in `h` and `Delta` introduces nonzero integer modes. Their
stationary equations shift (5), so they are not exhausted by (1). They must
be treated as projective entropy aliases or shown to produce a translated
anchor-difference web.

## Gate effect

E14D-L advances to
`CENTRAL_ANCHOR_DIFFERENCE_WEB_BANKED_PROJECTIVE_ENTROPY_ALIASES_OPEN`.

