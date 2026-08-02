# Cycle 133: exact multiplicative energy below the determinant threshold

Let `A` be the mode set of an excessive Cycle-132 block.  Write

```text
x_a=p_a/q_a,       q_a~N=X^rho,       R_a~S=X^tau,
|x_a-g^a| << 1/(NS).                                 (1)
```

For `a1+a2=a3+a4`, the corresponding powers of `g` have equal products, so

```text
|x_1 x_2-x_3 x_4| << 1/(NS).                        (2)
```

If the two rational products differ, their reduced denominators are at most
of order `N^2`, and hence

```text
|x_1 x_2-x_3 x_4| >> 1/N^4.                         (3)
```

Consequently every additive quadruple becomes an exact multiplicative
quadruple whenever

```text
S >> N^3,       equivalently tau>3rho.              (4)
```

Cycle 132 supplies `tau>=xi+1/3-rho`.  Thus (4) is automatic in the strict
range

```text
rho < rho_F=(xi+1/3)/4.                             (5)
```

This genuinely extends the Cycle-131 ceiling.  The extension is

```text
rho_F-(7/45-2mu/3)
  =xi/4-13/180+2mu/3 >=79/900.                      (6)
```

The width from `rho_F` to the full endpoint `1/3-mu` is exactly

```text
(1-xi)/4-mu.                                       (7)
```

It vanishes at the boundary `mu=(1-xi)/4`; equality cases in (4)--(5) still
require a constant-level argument and are not included.

The additive energy lower bound

```text
E_+(A) >= |A|^4/(2D-1)                             (8)
```

has exponent `11/15-4mu` when `|A|=Q/M`.  In the range (5), every quadruple
counted by (8) gives

```text
x_1 x_2=x_3 x_4.                                   (9)
```

Hence each prime valuation of `x_a` is a Freiman `2`-homomorphism on `A`.

The next-convergent decoration gives a second exact object.  Put

```text
U_a=[[P_a,p_a],[R_a,q_a]],       det(U_a)=s_a=+-1,
T_(a,b)=U_b U_a^(-1) in GL_2(Z).                    (10)
```

Then

```text
T_(b,c) T_(a,b)=T_(a,c),
det T_(a,b)=s_a s_b.                               (11)
```

This integral transition cocycle preserves the orientation and the next
denominator data discarded by a bare rational ray.

The remaining lock is now precise.  Neither (8)--(11) nor energy alone
forces the matrices `T_(a,a+d)` for one popular difference `d` to repeat.
Such transition concentration (or an equivalent phase-anchored edge
invariant) would turn the valuation web into a genuine geometric chain and
feed Cycle 126.  It is not proved here.

No transition concentration, recurrence seed, endpoint, lower moment,
density, or prime-interval theorem follows from this cycle.
