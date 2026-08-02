# Cycle 141: transition repetition is impossible; continuation is the lock

Fix one Cycle-140 class `(u,v,A,B)`.  Its input and output rational columns
are

```text
c0=(v p0,u q0)^T,
c1=((A/u)p0,(B/v)q0)^T.                           (1)
```

Suppose one matrix `T` maps `c0` to `c1` for two distinct core ratios
`p0/q0`.  Those two input columns are linearly independent, so (1) forces

```text
T=diag(A/(uv),B/(uv)).                             (2)
```

If `T` is integral and unimodular, its two positive diagonal entries are
integers with product one.  Hence

```text
A=B=uv=1.                                         (3)
```

The multiplier is then one; injectivity of the rational labels forces
`d=0`.  Therefore, for every nonzero represented difference, a fixed
`GL_2(Z)` transition can label at most one edge in a fixed divisor class.
Transition concentration is not the recurrence mechanism.

The cross-gcd color count is still subpower, so one class has
`L>=JX^(-o(1))` edges.  But its graph on the `R` mode vertices is a disjoint
union of paths.  Exactly as in Cycle 126,

```text
longest guaranteed chain >=ceil(L/(R-L)),
number of length-two starts >=max(0,2L-R),
depth k is forced if L>=ceil(kR/(k+1)).            (4)
```

Cycle-140 fiber saturation compares `L` with the arithmetic fiber capacity
`N^2/H`; (4) compares `L` with the mode-set size `R`.  These are independent
denominators.  Near saturation of the first does not imply positive
continuation density in the second.

The replacement invariant is therefore the class-colored continuation
profile

```text
|E_(d,c) intersect (E_(d,c)-d)|,
|E_(d,c) intersect (E_(d,c)-d) intersect
                 (E_(d,c)-2d)|, ...               (5)
```

together with the signed tails on every surviving edge.  A recurrence
compiler must estimate or invert (5); it must not identify equal transition
matrices.

No positive continuation density, recurrence, full paired norm, endpoint,
moment, density, or prime-interval theorem is proved.
