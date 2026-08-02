# Cycle 183: intercept-cleared primitive ray boxes

## Claim boundary

`PROVED`: every Cycle-181 stable common-intercept packet is an exact family of
primitive integer rays. Every stable four-row rectangle retains its physical
pair multipliers and has a nonzero primitive determinant. A critical packet
therefore contains a populated frozen dyadic ray box of
`X^(21/25-o(1))` actual rectangles, each carrying its labels, full fibres,
residuals, base residues, determinant, and product shell.

This is a scoped nonrational candidate saturation class. It proves no upper
bound inside that class, no aggregate recurrence, density improvement, or
prime-interval theorem.

## Clearing the common intercept

Cycle 182 gives the line

```text
j = (A/U)h + p/v,       U=v*u,       gcd(A,U)=gcd(p,v)=1. (1)
```

Multiplying (1) by `v` shows `A*h/u=v*j-p` is integral. Since
`gcd(A,u)=1`, every actual height is divisible by `u`. Thus the complete
fibre becomes the integral ray segment

```text
t=h/u,       J=v*j-p=A*t,                                (2)
```

with one residue class of `t` modulo `v`. Its original residual and the full
primitive-line record remain attached. From the extreme pair estimate of
Cycle 182,

```text
||U alpha_ell|| <= |A-U alpha_ell|
                  <= 2C/((N_ell-1)X).                    (3)
```

This is a row-depth-sensitive near-integer exponential orbit condition, not
an unweighted rational approximation assertion.

## Primitive cross-ray determinant

For two labels write `U=v*u`, `V=v*w`, with ray numerators `A,B`. Select
physical pair multipliers `k,q`, so

```text
d=kU,  a=kA,       e=qV,  b=qB.
```

The Cycle-180 integer determinant factors exactly:

```text
D=e*a-d*b = k*q*v*F,
F=w*A-u*B.                                                 (4)
```

For the inherited actual chart `1<=ell,m<=c Delta`, `0<c<1`, put
`r=|ell-m|<Delta`. C180's stable comparison, divided by `kqv`, gives

```text
pi*r*U*V/(v Delta)
 <= |F|
 <= (2pi*exp(2pi*c)+pi)*r*U*V/(v Delta).                  (5)
```

In particular `F` is nonzero. The divided error and the original `D`, both
physical pair multipliers, and the stable product condition remain in the
record. Equation (5) is not a scalar replacement for the rectangle census.

## Frozen populated ray box

In the light branch, `N_ell,N_m<=2R`; a physical pair multiplier is at most
its fibre depth, the primitive denominators satisfy `U,V<=H`, and `r<Delta`.
Assign every stable rectangle, before inspecting populations, the seven
dyadic fields

```text
(N_ell,N_m,U,V,k,q,r).
```

The number of boxes is at most

```text
B_box = bit_length(2R)^4 * bit_length(H)^2 * bit_length(Delta). (6)
```

Therefore a stable packet of mass `W` has one full box of mass at least
`W/B_box`. C181 supplies `W>=X^(21/25)/64` under a critical light census, so
one exact primitive-ray exponential near-orbit box has at least

```text
X^(21/25)/(64 B_box) = X^(21/25-o(1))                     (7)
```

ordered actual rectangles. This is the first populated candidate saturation
class that retains every coefficient-sensitive field through the C180--182
reductions.

## Gate effect

The active E13 object is now one populated primitive-ray box with fixed
dyadic depth, denominator, pair-multiplier, and label-gap scales. The next
engine must bound this box or construct it on the actual nonrational
exponential curve. A line partition, scalar denominator count, beta-free
pair count, exact-rational beta-zero tower, low-product rectangle, or an
unpopulated dyadic interface does not advance the gate.
