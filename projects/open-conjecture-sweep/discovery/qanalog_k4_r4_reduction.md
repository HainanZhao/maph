# k=4, r=4 coefficient-difference reduction

Claim boundary: the divisible-by-four branch is proved below. The remaining
four-section dominance lemma is `CONJECTURED`; the note is not a resolution of
GOAL.md topic 2.

Let

```text
A(q) = product_i [a_i]_q,       D = deg A = sum_i (a_i-1),
P_b(q) = A(q)[b]_{q^4}.
```

## Divisible branch

`PROVED`: If some `4 | a_i`, Lemma 4.2 and Corollary 4.3 of
Connelly--Ito--Martinez--Shevchenko--Yang apply with `r=4`:
`[a_i]_q[b]_{q^4}` is symmetric unimodal. Each remaining `[a_j]_q` is
symmetric unimodal, and products of nonnegative symmetric unimodal
polynomials are symmetric unimodal. Thus this entire disjunct of the stated
claim is already a theorem with its hypotheses checked.

## Formal quotient

Assume henceforth that no `a_i` is divisible by four. Define the formal power
series

```text
Q(q) = A(q)/[4]_q = sum_{t>=0} Q_t q^t,
```

with `Q_t=0` for `t<0`. Since

```text
(1-q)/(1-q^4) = 1/[4]_q,
```

direct algebra gives

```text
(1-q)P_b(q) = Q(q)(1-q^(4b)).
```

`PROVED`: If `p_t=[q^t]P_b`, then

```text
p_t-p_(t-1) = Q_t-Q_(t-4b).                         (1)
```

As `P_b` is symmetric, unimodality is equivalent to nonnegativity of (1) for

```text
t <= floor((D+4(b-1))/2).                           (2)
```

Write `a_i=4c_i+s_i`, with `s_i in {1,2,3}`, and put
`C=sum c_i`, `R=sum(s_i-1)`, so `D=4C+R`. The hypothesis is
`b<=C+1`.

If `t-4b>=0`, (2) implies

```text
(t-4b)+t <= D-4.                                    (3)
```

If `t-4b<0`, the desired difference is simply `Q_t`; the same hypothesis
implies `t<=D-ceil(R/2)`.

Thus the inequality branch follows from the following precise lemma.

## Remaining lemma

`CONJECTURED` (four-section dominance): For four positive lengths not
divisible by four, the coefficients of the formal series
`Q=product_i[a_i]_q/[4]_q` satisfy:

1. `Q_n >= Q_m` whenever `0<=m<n`, `n=m (mod 4)`, and `m+n<=D-4`;
2. `Q_n >= 0` for `0<=n<=D-ceil(R/2)`.

`PROVED`: this lemma implies the non-divisible branch immediately by (1)--(3).

`OBSERVED`: exhaustive exact checks found no violation of the lemma for every
nondecreasing quadruple `a_i<=40` with `4` not dividing any `a_i`.

## Inductive structure

`PROVED`: Increasing one length `a` to `a+4` gives an especially simple
update. If `B` is the product of the other three intervals, then

```text
[a+4]_q = [a]_q + q^a[4]_q,
Q_new = Q_old + q^a B.                              (4)
```

The coefficient sequence of `B` is symmetric and unimodal. Away from the
four new central boundary diagonals, (4) preserves four-section dominance
directly. On a new boundary write `m+n=D+1-h`, `0<=h<=3`, and
`L=(n-m)/4`. Symmetry reduces the required increment to

```text
sum_(j=1)^L B_(m+4j) >= sum_(j=1)^L B_(m+h+4j).     (5)
```

Exact expansion confirms (5) for products of three intervals in all tested
parameters. A uniform proof of (5), plus the finite base cases
`s_i in {1,2,3}`, would prove the remaining four-section lemma by induction.
No bounded computation is being promoted as that proof.

## Equivalent three-interval tail statement

`PROVED`: Set

```text
C(q) = B(q)[L]_(q^4),       t = m + 4L.
```

Then the left and right sides of (5) are respectively the coefficients
`C_t` and `C_(t+h)`.  Indeed, expanding the `q^4`-interval reverses the
summation order:

```text
C_t = sum_(j=1)^L B_(m+4j),
C_(t+h) = sum_(j=1)^L B_(m+h+4j).
```

Moreover the center of `C` is `(deg(B)+4(L-1))/2`, while the boundary
relation gives

```text
t - center(C) = (a+8-h)/2 > 0.
```

Thus (5) follows from tail monotonicity of the particular three-interval
product `B(q)[L]_(q^4)` at and to the right of this explicitly located
coefficient.  This is not a proof of (5): it identifies the missing bridge
as a constrained `k=3,r=4` tail statement, rather than an unspecified
four-factor phenomenon.

## Symmetric-window form

`PROVED`: write `d=deg(B)`.  From the boundary relation used above,

```text
d = 2m + 4L - a - 4 + h.
```

Symmetry `B_i=B_(d-i)` converts the right side of (5) into

```text
sum_(j=1)^L B_(m+h+4j)
  = sum_(k=0)^(L-1) B_(m-a-4+4k).
```

Consequently (5) is exactly the equal-window comparison

```text
sum_(k=0)^(L-1) B_(m+4+4k)
  >= sum_(k=0)^(L-1) B_(m-a-4+4k).                 (6)
```

The midpoint of the left sampled window is to the right of `d/2` by
`(a+8-h)/2`; the midpoint of the reflected right window is to the left of
`d/2` by `(a+8+h)/2`.  Thus the left window is closer to the symmetry center
by exactly `h`.  Ordinary unimodality would prove (6) if the windows occupied
the same residue class; their residue mismatch is the precise remaining
issue.

For the induction one may always decrement a largest target length.  The
corresponding old length `a` then satisfies every interval length in `B` is
at most `a+4`.  Hence it is enough to prove (6) under this additional size
condition; no arbitrary choice of the incremented factor is required.
