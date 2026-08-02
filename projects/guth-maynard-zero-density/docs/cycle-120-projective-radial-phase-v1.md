# Cycle 120: the Laurent residual is the surviving radial phase

Let `c=D/(2pi)`, `g=exp(1/c)`, and use the exact Cycle-94 entropy phase.
Write `Delta=zH`, `0<z<1`. Homogeneity gives the exact normal form

```text
cF(H,Delta)-uH-vDelta = H P_(u,v)(z),              (1)

P_(u,v)(z)
 =c[z log(c0 z/m)+log n+(1-z)log((1-z)/n')]-u-vz.
```

Thus the zero determinant found in Cycle 94 has a precise meaning: the
projective variable is curved and the radial variable is linear. Direct
differentiation gives

```text
P'(z)=c log(c0 z n'/(m(1-z)))-v,
P''(z)=c/[z(1-z)]>0.                               (2)
```

Put

```text
(A,B,C)=(p0 n,p0 n',q0 m).
```

The unique projective saddle in (2) is

```text
z_v=Cg^v/(B+Cg^v).                                 (3)
```

Euler's identity for the homogeneous entropy phase, or direct substitution,
then yields

```text
P(z_v)=c log(A/(Bg^u+Cg^(u+v))).                   (4)
```

Equation (4) is the missing phase-carrying version of the Cycle-95 Laurent
relation. If

```text
R=A-Bg^u-Cg^(u+v),  |R|<=A/2,
```

then the mean-value theorem applied to `-log(1-R/A)` proves

```text
sign(P(z_v))=sign(R),
(2c/(3A))|R| <= |P(z_v)| <= (2c/A)|R|.             (5)
```

The projective saddle has positive curvature and a fixed stationary
signature. The remaining radial integral is a smooth Fourier transform at
frequency `H0 P(z_v)`, not a positive indicator of `|R|<=1/K`. Since

```text
H0~KQ/D,  A~Q,  c~D,
```

(5) shows that radial coherence `H0|P(z_v)|=O(1)` is equivalent, up to fixed
constants, to the already proved tolerance `|R|=O(1/K)`. This independently
recovers Cycle 116 while retaining the sign and full nonlinear phase.

The new lower-band operator is therefore a signed sum of radial Fourier
profiles at

```text
(KQ/D)c log(A/(Bg^u+Cg^(u+v))),                    (6)
```

with the projective stationary amplitude and arithmetic payload attached.
Cycle 119 shows why replacing (6) by its support indicator loses too much.
No cancellation estimate for (6), simple-root closure, complete moment,
density gain, or interval gain is proved here.
