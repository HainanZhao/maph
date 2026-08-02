# Cycle 30 block-subspace extremizer preregistration v1

## Claim boundary

This cycle may construct a sharp abstract Hilbert-space family simultaneously
realizing block synchronization, a polynomial detector subspace, exact
detector reconstruction, and cancellation of the bulk-renormalized residual
shift. It may prove saturation only for the architecture that forgets the
actual prime phase curve. It may not assert that primes realize the model,
close the skeleton target, or promote density/interval consequences.

## Frozen construction

Let `k>=2`, `J>=1`, `0<rho<1`, and assume `k rho` is large enough for the
parameter below to lie in `(0,1)`. Let `f_1,...,f_J` be orthonormal detector
block directions and put

```text
b=J^(-1/2)sum_j f_j.
```

Let `B_epsilon` be the `k by k` correlation matrix with eigenvalue `epsilon`
on the all-ones direction and eigenvalue `(k-epsilon)/(k-1)` on its
orthogonal complement. Equivalently its diagonal is one and every
off-diagonal entry is `(epsilon-1)/(k-1)`.

Choose unit residual rows `r_t` with Gram `B_epsilon`, orthogonal to the
detector subspace, and define

```text
x_t=sqrt(rho)b+sqrt(1-rho)r_t.
```

Freeze

```text
L_target=(1-rho)^(-k)-1,
epsilon=k rho/((1-rho)L_target).
```

## Frozen conclusions

The builder must verify:

1. every row has norm one and detector projection squared `rho`;
2. every detector block contribution against `f_j/sqrt(J)` equals
   `sqrt(rho)/J`, so all nontrivial Hadamard signings vanish and the
   multiblock branch is perfectly synchronized;
3. the normalized residual is `B_epsilon` and
   `s=sqrt(rho/(1-rho))1`;
4. inverse leverage is exactly
   `s*B_epsilon^(-1)s=L_target`;
5. the determinant shift is exactly
   `k log(1-rho)+log(1+L_target)=0`;
6. the reconstruction error is exactly `L_target^(-1/2)`;
7. labels may be assigned arbitrarily, including `X^(3/5)` separation,
   because the abstract architecture does not couple labels to rows.

## Frozen finite and asymptotic rows

- Finite exact check: `k=4`, `rho=1/4`, giving
  `L_target=175/81`, `epsilon=108/175`, residual off-diagonal `-67/525`,
  and full Gram off-diagonal `27/175`.
- Critical asymptotic check:
  `k=X^(21/25)`, `rho=X^(-3/5)`, `J=X^(1/25)`;
  then `k rho=X^(6/25)`,
  `epsilon=exp(-X^(6/25+o(1)))`, and reconstruction error
  `exp(-X^(6/25+o(1))/2)` up to subleading terms.

## Scope rule

Register the saturation statement only for the block-subspace residual-shift
architecture with arbitrary Hilbert rows and arbitrary separated labels. The
missing hypothesis required to escape is an actual-prime-phase or equivalent
multiplicative-frequency constraint.

Use CPython `3.12.3`, exact `Fraction` finite checks, no RNG/network, and pin
Cycles 19, 23, 27, 28, and 29.
