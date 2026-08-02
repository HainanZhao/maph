# Cycle 55: diagonal centering cannot replace the last contraction

## Claim boundary

`PROVED`: equal row norms, a common large coefficient direction, Gram
positivity, and subtraction of the scalar diagonal do not force any positive
centered even trace while `R rho<=1`. This boundary is exact, including the
endpoint. At the Cycle-54 penultimate stage, `R rho=X^(-3/50+o(1))`, so a
plain centered second, fourth, or higher even Gram trace cannot supply the
missing `3/50`.

This is an abstract information boundary. It does not obstruct E12 after
actual prime-coordinate or Cycle-51 partition information is inserted before
the trace, and it proves no analytic, density, or interval gain.

## Exact construction

Let `b` be a unit vector and fix `0<=rho<=1/R`. On an orthogonal residual
space choose vectors `y_1,...,y_R` with Gram matrix

```text
B = I_R-rho J_R.
```

This matrix is positive semidefinite: its eigenvalues are `1` with
multiplicity `R-1` and `1-R rho` in the constant direction. Define

```text
x_t = sqrt(rho)b+y_t.
```

Then every row has the required common projection
`|<b,x_t>|^2=rho`, while

```text
G=(<x_t,x_u>) = rho J_R+B = I_R.
```

Consequently `H=G-I_R=0` and
`tr(H^(2k))=0` for every `k>=1`. At `R rho=1`, the residual Gram merely
becomes singular; the centered conclusion remains exact. A strict
off-diagonal conclusion therefore requires `R rho>1` unless additional
structure is used.

## Exponent transfer

Cycle 54's signed gap `3/50` says precisely

```text
R rho = X^(-3/50+o(1)).
```

Thus increasing the trace order or subtracting only `N I_R` cannot repair
the penultimate coordinate loss. The obstruction is not a bad fourth-moment
estimate: the entire centered matrix may vanish.

## E12 redesign

`CONJECTURED`: build the trace only after applying a prime-coordinate
connected projection. The first object is the edge covariance

```text
C((t,u),(t',u'))
 = k((t-u)-(t'-u'))-k(t-u)conj(k(t'-u')),
```

where `k(h)=K(h)/M`. It is a positive semidefinite Gram kernel of the
centered prime phases `p^(-ih)-k(h)` and vanishes when an edge is diagonal.
For separate prime coordinates, Schur products of these edge kernels retain
positivity while removing scalar backtracks coordinate-by-coordinate.

The next theorem must use this actual kernel, or the signed Möbius cumulant
of the Cycle-51 support partitions, to gain `3/50`. Merely replacing a second
trace by a fourth trace is now removed from the plan.

## Gate effect

E12 remains open as `PRIME_PARTITION_CUMULANT_3_50_OPEN`. Its first task is an
exact edge-kernel/partition expansion followed by an exponent ledger for
genuine four-row parallelograms.
