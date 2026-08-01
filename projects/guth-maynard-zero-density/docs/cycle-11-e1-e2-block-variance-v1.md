# Cycle 11 E1+E2 block-variance reduction v1

## Claim boundary

`PROVED`: every coefficient-block frame splits into the original detector's
rank-one kernel plus a positive block-variance kernel. The rank-one component
alone saturates raw Schatten traces and the coherent two-step scale forced at
the critical cell. Therefore arbitrary block splitting, sign averaging, or
random colouring cannot improve the exponent through an uncentred mixed
trace.

`PROVED`: the exact object that must carry genuinely new information is the
centred block-variance kernel. Large values of the original detector alone
force no positive lower bound for it.

This note proves no analytic saving, density improvement, shorter prime
interval, Base/CRR incompatibility, arithmetic lower bound for block
variance, or L-function extension. The no-gain statement is scoped to raw
frame traces built from a partition of one detector; it is not a no-go
theorem for E1, E2, E3, or E4.

## 1. `PROVED`: exact block-variance decomposition

Let `d_1,...,d_K in C^R` be the value vectors of disjoint coefficient blocks,
and put

```text
d=sum_j d_j,
F=sum_j d_j d_j*,
z_j=d_j-d/K,
Z=sum_j z_j z_j*.
```

Since `sum_j z_j=0`, expansion gives

```text
F = d d*/K + Z.                                         (1)
```

The matrix `Z` is positive semidefinite and

```text
Z_(t,t)=sum_j |d_j(t)-d(t)/K|^2.                        (2)
```

Thus `Z` measures block-to-block variance after removing the forced common
detector direction. If `d_j=d/K` for every `j`, then `Z=0` even when every
`|d(t)|` is large. This exact vector model shows that detector largeness alone
cannot imply block diversity. It is not claimed to be an actual integer-
frequency construction.

## 2. `PROVED`: raw frame traces retain the full old obstruction

Let `P=dd*/K`. Equation (1) says `F>=P>=0`. Eigenvalue monotonicity for
Hermitian matrices gives, for every integer `r>=1`,

```text
tr(F^r) >= tr(P^r)
        = (||d||_2^2/K)^r.                              (3)
```

If `|d(t)|>=V` on `R` rows, then

```text
tr(F^r) >= (R V^2/K)^r.                                (4)
```

The Cycle-10 E1 lower bound at the same threshold is only
`R(V^2/K)^r`. Hence the unavoidable rank-one contribution in (4) is larger
by `R^(r-1)`. A raw Schatten upper bound for `F` is therefore aimed at a
quantity already dominated by the original common detector. It cannot expose
frame diversity without first removing `P`.

After removing `P`, the residual is exactly `Z`, but (2) has no source-free
positive lower bound. This is the corrected E1+E2 seam.

## 3. `PROVED`: coherent two-step saturation of the rank-one term

Write `x=d/sqrt(K)`, so `P=xx*`, and set `a_t=|x_t|^2`. Let

```text
A=P-diag(a_t),
r_t=sum_(s!=t)|A_(t,s)|^2,
C_2=A^2-diag(r_t).
```

After conjugating by the diagonal phase matrix of `x`, the off-diagonal
entries of `C_2` are nonnegative and equal to

```text
(C_2)_(t,s)=sqrt(a_t a_s)(S-a_t-a_s),
S=sum_u a_u,                                            (5)
```

for `t!=s`. Formula (5) follows by summing the two-step paths through
`u!=t,s`; the deleted diagonal is zero.

If every `a_t>=a` and `R>=3`, every row sum of the phase-conjugated `C_2` is
at least

```text
(R-1)(R-2)a^2.
```

The Rayleigh quotient of the all-ones vector, or the minimum-row-sum bound
for a nonnegative symmetric matrix, therefore gives

```text
||C_2||_op >= (R-1)(R-2)a^2.                            (6)
```

For constant `a_t=a`, equality holds in the top eigenvalue calculation:

```text
lambda_max(P)=R a,
r_t=(R-1)a^2,
spec(A)={(R-1)a,-a [R-1 times]},
spec(C_2)={(R-1)(R-2)a^2,(2-R)a^2 [R-1 times]}.         (7)
```

Thus the rank-one detector component realizes the coherent two-step branch,
not the local-return branch.

## 4. `PROVED`: frozen critical-scale translation

Use the CRR lower bands

```text
R>=v^(8-delta),  V>=v^(7-delta),  K<=v^delta.
```

For `P=dd*/K`, (4) at `r=1` gives

```text
lambda_max(P)=||d||_2^2/K
             >=R V^2/K
             >=v^(22-4delta).                           (8)
```

In (6), `a=V^2/K>=v^(14-3delta)`. For sufficiently large `v`, the lower
bound for `R` exceeds four and `(R-1)(R-2)>=R^2/4`. Consequently

```text
||C_2(P)||_op
 >=(1/4)R^2(V^2/K)^2
 >=(1/4)v^(44-8delta).                                  (9)
```

Equation (9) is a fixed-constant realization of the `v^(44-o(1))` coherent
two-step scale. It explains why applying Cycle-10 E2 directly to the raw
block frame cannot produce a saving: the old common detector remains inside
that frame at full exponent.

No monotonicity of the nonlinear map `F -> C_2(F)` is claimed. The rigorous
raw-trace obstruction is (3)--(4); (6)--(9) identify the exact E2 behavior of
the forced rank-one component itself.

## 5. `PROVED`: random coefficient colouring retains the same term

Let `c_n` be finitely supported and colour each coefficient independently
and uniformly in `{1,...,K}`. Put

```text
D_j(t)=sum_(chi(n)=j)c_n n^(it),
D(t)=sum_n c_n n^(it),
G_c(t,s)=sum_n |c_n|^2 n^(i(t-s)).
```

Expanding the block frame, a pair `(n,m)` survives precisely when both
coefficients receive the same colour. That probability is one for `n=m` and
`1/K` for `n!=m`. Therefore

```text
E_chi sum_j D_j(t) conjugate(D_j(s))
 =D(t)conjugate(D(s))/K+(1-1/K)G_c(t,s).                (10)
```

The first term in (10) is exactly the rank-one kernel `P`. Random colouring
does not erase it; it only adds the coefficient-energy Gram kernel. The
registered exact corroboration enumerates all colourings for
`2<=|I|<=5`, `K in {2,3}` and matches (10) in every row.

## 6. Consequence and next engine

`PROVED`: the naive E1+E2 hybrid is now reduced to one missing arithmetic
statement. One must either:

1. prove that a source-derived multiplicative partition forces quantitatively
   nonzero and suitably dispersed `Z`; or
2. build a different detector ensemble whose forced PSD component is not the
   original rank-one large-value kernel.

`CONJECTURED`: E3/E4 prime-block entropy is a natural route to item 1. The
first toy question should not ask merely whether several blocks are present;
it should ask whether the block-value vectors can remain nearly equal on
`v^(8-o(1))` separated ordinates while their sum has size `v^(7-o(1))`.

The zero-variance vector model falsifies any source-free version of that
claim. An arithmetic theorem must use actual log frequencies, disjoint prime
supports, or factorization of the zero detector.

## Replay

```sh
python3 proof/build_cycle_11_e1_e2_block_variance_v1.py --write
python3 proof/build_cycle_11_e1_e2_block_variance_v1.py --check
python3 -m unittest tests/test_cycle_11_e1_e2_block_variance_v1.py
```
