# Excess-spectrum reduction for a hypothetical 20-block cover

Claim boundary: the argument below gives a `PROVED` support constraint and
one resulting replication-pattern exclusion for a hypothetical 20-block cover
of pairs on 23 points.  It does not decide `C(23,6,2)`.

Let `N` be the `23 x 20` point--block incidence matrix.  Write

```text
r_v = 5 + e_v,       e_v >= 0,       sum_v e_v = 5,
```

where the last equality follows from the 120 incidences.  Let `A` be the
off-diagonal adjacency matrix of the excess multigraph: for distinct `u,v`,
`A_uv = lambda_uv - 1`, where `lambda_uv` is the number of blocks covering
`{u,v}`.  Then a direct diagonal/off-diagonal comparison gives

```text
N N^T = 4 I + J + A + diag(e) = J + B,
B := 4 I + A + diag(e).
```

Also, the excess degree at `v` is exactly

```text
sum_{u != v} A_uv = 5 r_v - 22 = 3 + 5 e_v.                 (1)
```

Since `rank(N N^T) <= 20`, its kernel has dimension at least three.  Its
intersection with the codimension-one space `1^perp` therefore has dimension
at least two.  For every `x` in that intersection, `Jx=0` and hence `Bx=0`.
Thus

```text
nullity(B) >= 2.                                             (2)
```

## `PROVED` support theorem

Let `H={v:e_v>0}` and `L=V\H`.  For every `v` in `L`, (1) says that the
nonnegative off-diagonal row sum of `A_LL` is at most three.  Consequently

```text
B_LL = 4 I + A_LL
```

is strictly diagonally dominant by rows, hence nonsingular.  Schur
elimination of the `L` coordinates gives

```text
nullity(B) <= |H|.                                      (3)
```

Together with (2), every hypothetical 20-block cover must satisfy

```text
|H| >= 2.                                                (4)
```

## `PROVED` strengthening: in fact `|H| >= 3`

Suppose for contradiction that `|H|=2`. Then (2)--(3) give
`nullity(B)=2`. In the Schur decomposition with respect to `L,H`, the Schur
complement has size two and has this same nullity, so it is the zero matrix.
Since `B_LL` is positive definite (strict diagonal dominance with positive
diagonal and symmetry), the corresponding block congruence shows that `B` is
positive semidefinite.

For positive semidefinite matrices, the kernel of a sum is the intersection
of the kernels. Hence

```text
ker(J+B) = ker(J) intersect ker(B).                       (5)
```

The two-dimensional subspace used in (2) lies in
`ker(B) intersect 1^perp`. Since `ker(B)` itself has dimension two, it is all
of `ker(B)`. Thus `J` vanishes on `ker(B)`, and (5) gives

```text
nullity(J+B) = 2.
```

But `J+B=N N^T` has rank at most 20, so its nullity is at least three. This
contradiction proves

```text
|H| >= 3.                                                (5a)
```

## `PROVED` exclusion: excess partition `(5)`

If one point `h` has `e_h=5` and every other point has `e_v=0`, then
`|H|=1`, contradicting (4).  Therefore no 20-block cover can have
replication multiset

```text
{10, 5, 5, ..., 5}.
```

In the central-star multiplicity-four branch, degree 10 for the repeated
star point forces precisely this global excess partition, so that degree case
is impossible without SAT. The strengthening also excludes excess partitions
`(4,1)` and `(3,2)`. The surviving partitions of the total excess five are
therefore only `(3,1,1)`, `(2,2,1)`, `(2,1,1,1)`, and `(1,1,1,1,1)`; this
does not yet decide the covering number.
