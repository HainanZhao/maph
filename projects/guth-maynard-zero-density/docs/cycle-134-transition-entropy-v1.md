# Cycle 134: determinant lifts have power-sized shear entropy

Fix a primitive rational column `(p,q)` and an orientation `s`.  If
`(P0,R0)` is one solution of

```text
Pq-pR=s,       s in {+1,-1},                       (1)
```

then every solution is

```text
(P,R)=(P0+tp,R0+tq),       t in Z.                 (2)
```

Indeed the difference of two solutions is an integer multiple of the
primitive vector `(p,q)`.  In matrix form,

```text
[[P0+tp,p],[R0+tq,q]]
  =[[P0,p],[R0,q]] [[1,0],[t,1]].                  (3)
```

For `q~N`, a nonempty interior block `R~S` therefore contains order `S/N`
formal determinant lifts.  Its shear-entropy exponent is

```text
tau-rho >= xi+1/3-2rho.                            (4)
```

At the full endpoint `rho=1/3-mu`, the minimum in (4) is

```text
xi+2mu-1/3 >=23/75.                               (5)
```

Thus determinant, orientation, rational label, and dyadic size alone leave
a fixed-power family of possible transition matrices.  The cocycle of Cycle
133 is exact, but it cannot distinguish these shears.

The actual next-convergent phase supplies precisely the datum that (1)--(3)
discard.  Put

```text
delta=|g^a-p/q|,
theta=(1/(q delta)-R)/q.                           (6)
```

The consecutive shell

```text
1/[q(R+q)] < delta < 1/(qR)
```

is equivalent to `0<theta<1`, and

```text
delta=1/[q(R+theta q)]                             (7)
```

holds exactly.  Hence `theta` is the missing continued-fraction tail/phase
anchor that selects the actual shear.

This proves a scoped data-loss statement: any transition compiler using
only rational labels, determinant signs, and dyadic sizes retains power
entropy and cannot obtain subpower transition concentration from those data
alone.  It does not obstruct a compiler that retains `theta`, the signed
collision residual, or the full Fourier phase.

No phase-coupled transition concentration, recurrence seed, endpoint,
moment, density, or prime-interval theorem is proved.
