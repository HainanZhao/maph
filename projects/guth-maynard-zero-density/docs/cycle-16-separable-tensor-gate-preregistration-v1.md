# Cycle 16 separable tensor gate preregistration v1

## Claim boundary

`OBSERVED`: Cycle 15 identifies a symmetric rank-one coefficient tensor but
does not show how the Guth--Maynard trace should retain it. This cycle freezes
the exact tensor operator, the coefficient-sensitive norm relevant to large
values, and the spectral-overlap certificate produced by failure.

The cycle may prove finite-dimensional linear-algebra identities and a sharp
abstract countermodel. It may not claim an arithmetic bound for prime rows,
a saving in the rank-one semiprime theorem, or a density consequence.

## Frozen tensor conventions

Let `U` be an `R by m` complex sampling matrix with rows `u_t`. Define the
ordered symmetric-square sampling operator `S` by

```text
S_(t,(i,j))=U_(t,i)U_(t,j),       1<=i,j<=m.
```

Set `H_2=S^*S` on the ordered tensor square and `C_2=SS^*` on rows. For a
coefficient vector `a`, put `z=a tensor a` and `P=Ua` (with the frozen direct
bilinear evaluation convention). Register

```text
S(a tensor a)=P coordinatewise squared,
z^*H_2z=sum_t |P_t|^4,
||z||_2^2=||a||_2^4,
(C_2)_(t,s)=<u_t,u_s>^2.
```

The last inner product is linear in the first row and conjugate-linear in the
second; its square, not its absolute square, is the matrix entry. `C_2` is
Hermitian PSD by construction.

## Frozen separable norm and large-value reduction

Define

```text
Sep(H_2)=sup_(a!=0) <a tensor a,H_2(a tensor a)>/||a||_2^4.
```

If `|P_t|>=V` for all `t` in `W` and `||a||_2^2=m`, then

```text
|W| V^4 <= Sep(H_2) m^2.
```

At the Cycle-15 prime scales, the desired count `X^(36/25)` is implied by

```text
Sep(H_2) <= X^(56/25+o(1)).
```

The generic fourth-moment input gives only `X^(12/5+o(1))`, so the required
separable-norm saving is `4/25` in `X`.

## Frozen spectral-overlap certificate

Let the eigenvalues of `H_2` be at most `lambda_max`, and let `Pi_>L` project
onto eigenvalues greater than `L`. For a unit rank-one tensor `z`, write
`xi=||Pi_>L z||_2^2`. Then

```text
<z,H_2z> <= L+(lambda_max-L)xi.
```

Consequently, if `<z,H_2z>>=A>L`, then

```text
xi >= (A-L)/(lambda_max-L).
```

This is an exact within-architecture exhaustiveness statement: failure of a
separable-norm target must combine a high spectral branch with overlap of the
same common rank-one coefficient tensor. It is not a theorem that all future
methods must use this gate.

## Frozen countermodel and arithmetic obligation

If all rows of `U` are identical, then `H_2` has a rank-one top eigentensor
which is itself separable and

```text
Sep(H_2)=lambda_max(H_2)=R ||u||_2^4.
```

Thus rank-one coefficients alone force no saving. The live arithmetic input
must use the separated prime-phase rows
`u_t=(p^(it))_(p in [X,2X])` to show either a spectral loss or a rank-one
overlap loss. The identical-row example is a countermodel to an abstract
tensor-only theorem, not to the prime-phase conjecture.

## Exact finite checks

- Enumerate fixed integer matrices of sizes up to `3 by 3` and check every
  tensor/Gram identity exactly.
- Check the identical-row formula for `1<=R,m<=4`.
- Check the spectral-overlap inequality on registered diagonal PSD matrices
  and rational unit vectors; no floating point or eigensolver is used.

## Compute and review rules

- CPython `3.12.3`, optimization level zero, integers/Fractions only, no RNG,
  third-party libraries, or network.
- Enumeration cap: 1,000 finite rows.
- Builder cap: 30 seconds and 256 MiB RSS.
- Hostile audit remains deferred to paper stage.
