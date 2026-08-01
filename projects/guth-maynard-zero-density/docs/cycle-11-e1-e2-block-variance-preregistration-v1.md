# Cycle 11 E1+E2 block-variance preregistration v1

## Claim boundary

`OBSERVED`: this document freezes an exact E1+E2 hybrid calculation. It
proves no large-value saving, zero-density gain, short-interval improvement,
Base/CRR incompatibility, or L-function extension.

The motivating question is whether partitioning one source detector into
coefficient blocks creates frame diversity that reduces the E2 two-step
excess. The registered adverse outcome is that the original detector survives
as a rank-one PSD component and already saturates the critical scale.

## Frozen block-frame objects

Let `d_1,...,d_K` be arbitrary columns in `C^R`, let

```text
d=sum_j d_j,
F=sum_j d_j d_j*,
z_j=d_j-d/K,
Z=sum_j z_j z_j*.
```

Freeze the exact identity

```text
F=d d*/K+Z.                                             (1)
```

The theorem note must prove `Z>=0`, identify its diagonal as
`sum_j |d_j(t)-d(t)/K|^2`, and state explicitly that a lower bound for
`|d(t)|` alone forces no positive lower bound for `Z`.

## Frozen rank-one E2 benchmark

For integer `R>=3`, positive `a`, and a vector `u` with `|u_t|=1`, put

```text
P=a u u*,
A=P-aI,
r_t=sum_(s!=t)|A_(t,s)|^2,
C_2=A^2-diag(r_t).
```

Freeze the eigenvalue and return rows

```text
lambda_max(P)=R a,
r_t=(R-1)a^2,
spec(A)={(R-1)a,-a [multiplicity R-1]},
spec(C_2)={(R-1)(R-2)a^2,(2-R)a^2 [multiplicity R-1]}.
```

The critical translation uses `a=V^2/K`,
`R>=v^(8-delta)`, `V>=v^(7-delta)`, and `K<=v^delta`. It must record

```text
lambda_max(P)>=v^(22-4delta),
||C_2||_op>=v^(44-o(1))
```

with an explicit finite-`v` exponent/constant row, not merely the asymptotic
abbreviation. No claim that an actual Dirichlet block partition has constant
block values is authorized; this is the exact rank-one component already
present in every decomposition (1).

## Frozen random-colouring identity

Let a finite coefficient set `I` have complex coefficients `c_n`. Colour
each `n` independently and uniformly in `{1,...,K}` and define

```text
D_j(t)=sum_(chi(n)=j)c_n n^(it),
D(t)=sum_n c_n n^(it),
G_c(t,s)=sum_n |c_n|^2 n^(i(t-s)).
```

Freeze

```text
E_chi sum_j D_j(t) conjugate(D_j(s))
 =D(t)conjugate(D(s))/K+(1-1/K)G_c(t,s).                (2)
```

Finite corroboration enumerates every colouring for exact rational evaluation
matrices with `2<=|I|<=5` and `K in {2,3}`. No RNG is authorized.

## Falsifiers and outcomes

- `BLOCK_VARIANCE_DECOMPOSITION`: (1), positivity, and the zero-variance
  model are exact.
- `RANK_ONE_COHERENT_SATURATION`: the rank-one component alone saturates the
  coherent E2 branch at the frozen critical exponent.
- `RANDOM_COLOUR_EXPECTATION`: (2) is exact.
- `CONTAINED_FAIL`: an exact algebra, frozen-source, or replay check fails;
  contain that row and continue safe work on E3/E4.

A proof that source-derived multiplicative blocks force a nontrivial `Z`
would refute the zero-variance model in that narrower arithmetic class and is
the next affirmative gate. A finite model with `Z=0` refutes no arithmetic
claim.

## Compute and review rules

- CPython `3.12.3`, optimization level zero, integers/Fractions, no third-
  party numerical libraries, no RNG, no network.
- Builder cap: 30 seconds and 256 MiB peak RSS.
- Exact source/artifact hashes are frozen in the builder before sealing.
- Research-stage review is limited to source, algebra, replay, and
  constructive countermodel checks. Hostile audit remains deferred to paper
  stage.
