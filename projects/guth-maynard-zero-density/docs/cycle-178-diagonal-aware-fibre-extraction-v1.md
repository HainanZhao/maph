# Cycle 178: diagonal-aware extraction from actual fixed-beta fibres

## Claim boundary

`PROVED`: let `N>=3` distinct integer rows `(h,j)` at one fixed label satisfy

```text
|j+beta-h alpha| <= C/X,       h in [H,2H],
4CH/X < 1.                                                    (1)
```

Then that actual fibre itself supplies a primitive Cycle-67 packet: for
`K=floor((N-1)/2)`, some retained row is a seed for coprime integers `(a,q)`
with

```text
qK <= H,
|q alpha-a| <= C/(KX),                                      (2)
```

and the packet produces `K+1` in-range forward rows in the enlarged
`2C/X` strip.  This retains the fixed label, beta, seed, numerator, and
approximation error.  The numerator may be zero or negative.

Consequently, for `R=ceil(X^(6/25))`, a fixed-beta Cycle-63 census has the
exact alternative: a fibre with `N_ell>=2R+1` gives a seeded packet of depth
at least `R`, or, if every fibre is light, its ordered distinct-label mass

```text
U_cross=sum_(ell != ell') N_ell N_ell'
```

satisfies `U_cross>=T(T-2R)`, where `T=sum_ell N_ell`.  For `X>=256`, a
failure `T>=X^(16/25)` in the light branch therefore has
`U_cross>=X^(32/25)/2`.

This is an actual-row inverse and a diagonal extraction—not a cross-label
analytic upper bound, a full E7/E9 recurrence bound, a density improvement,
or a prime-interval theorem.

## Determinant forcing

Order the fibre by its row coordinate and choose an adjacent pair with the
smallest gap, denoted `(h0,j0),(h1,j1)`.  Put

```text
d0=h1-h0,       a0=j1-j0.
```

For any retained row `(h,j)`, put `d=h-h0`, `b=j-j0`.  Subtracting (1) from
the base row gives

```text
|d alpha-b| <= 2C/X,       |d0 alpha-a0| <= 2C/X.             (3)
```

The integer determinant has the exact estimate

```text
|d0*b-d*a0|
 <= d0 |b-d alpha| + |d| |a0-d0 alpha|
 <= 2C(d0+|d|)/X
 <= 4CH/X < 1.                                               (4)
```

It is therefore zero.  Let `g=gcd(d0,a0)`, where `gcd(d0,0)=d0`, and set
`q=d0/g`, `a=a0/g`.  Then `(a,q)=1`, and (4) says

```text
q b=d a.
```

Hence `q` divides every `d`, all the actual rows lie in one `q` residue
class, and their `j` values have the common slope `a/q`.  No positivity
assumption on `a` has appeared.

## Span turns population into depth

Let `(h_-,j_-)` and `(h_+,j_+)` be the first and last rows.  (They need not
be the minimum-gap pair.)  Write

```text
D=(h_+-h_-)/q.
```

The common-residue conclusion makes `D` an integer; the `N` distinct rows
give `D>=N-1`.  Applying (3) to the two endpoints and using
`j_+-j_-=Da` yields

```text
|q alpha-a| <= 2C/(DX) <= 2C/((N-1)X) <= C/(KX).              (5)
```

Because `d0` was the least adjacent gap,

```text
(N-1)d0 <= h*-h0 <= H,
qK <= d0 (N-1)/2 <= H/2.                                    (6)
```

Moreover `K<=D`, so the first row is an actual seed and for `0<=k<=K`, the rows

```text
(h_-+kq, j_-+ka)
```

remain between the first and last original row.  Their residual is at most
`C/X+k*C/(KX)<=2C/X`.  Thus the packet is not merely beta-free admissible:
the starting row is an actual seed and it has an in-range actual fan.  This
is the missing composition of Cycles 64--67 for an actual heavy fibre.

## Heavy/light diagonal extraction

For a full fixed-beta census write

```text
T=sum_ell N_ell,
U_cross=T^2-sum_ell N_ell^2.                               (7)
```

Set `R=ceil(X^(6/25))`.  If some `N_ell>=2R+1`, the preceding theorem gives
`K=floor((N_ell-1)/2)>=R`: a critical-depth seeded recurrence packet,
with the original beta and its error.  Otherwise `N_ell<=2R` for every label,
so

```text
sum_ell N_ell^2 <= 2R T,
U_cross >= T(T-2R).                                        (8)
```

For `X>=256`, `4R<=X^(16/25)` (use
`R<=2X^(6/25)` and `X^(2/5)>=8`).  Hence a direct-target failure in this
light branch has `T>=4R` and (8) gives

```text
U_cross >= T^2/2 >= X^(32/25)/2.                           (9)
```

The Cycle-177 rational-root ray belongs visibly to the first branch: its
one-label fibre has depth `X^(11/25-o(1))`.  It cannot be confused with
evidence for (9).

## Gate effect

The raw pair route remains saturated.  `PROVED` heavy actual fibres now have
a seed-and-error-preserving route to the Cycle-67 recurrence input.  The
only unstructured obstruction to a direct triple census is a quantitatively
large **cross-label** population.  The next engine must either bound that
population by a coefficient-preserving cross-label argument or construct an
actual cross-label saturator.  No density or interval ledger may be reopened
until one of those analytic tasks is completed.
