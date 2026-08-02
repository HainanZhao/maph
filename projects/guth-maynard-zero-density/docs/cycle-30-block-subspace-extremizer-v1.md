# Cycle 30: a sharp block-subspace residual-shift extremizer

## Claim boundary

`PROVED`: an explicit abstract Hilbert-space family simultaneously saturates
block synchronization, polynomial detector-subspace projection, detector
reconstruction, and the bulk-renormalized determinant shift. Labels may be
arbitrarily separated. This is a saturation theorem only for the architecture
that does not impose the actual prime phase curve; it is not a prime
counterexample and proves no density or interval result.

## Construction

Let `f_1,...,f_J` be orthonormal and define the block-flat detector

```text
b=J^(-1/2)sum_j f_j.
```

For `k>=2` and `0<rho<1`, let `B_epsilon` be the correlation matrix with
eigenvalue `epsilon` on the all-ones direction and eigenvalue
`(k-epsilon)/(k-1)` on its orthogonal complement. Thus every off-diagonal
entry is `(epsilon-1)/(k-1)`. Realize it as the Gram matrix of unit residual
vectors `r_t`, orthogonal to the detector subspace, and set

```text
x_t=sqrt(rho)b+sqrt(1-rho)r_t.                         (1)
```

Every row has norm one and detector projection squared `rho`. Its contribution
against the `j`th detector block `f_j/sqrt(J)` is exactly `sqrt(rho)/J`.
Consequently all blocks are perfectly aligned and every nontrivial Hadamard
signed detector vanishes.

## Exact shift cancellation

For the rank-one common direction in (1), the normalized residual is
`B_epsilon` and

```text
s=sqrt(rho/(1-rho)) 1.
```

Choose

```text
L_target=(1-rho)^(-k)-1,
epsilon=k rho/((1-rho)L_target).                       (2)
```

Because the all-ones eigenvalue of `B_epsilon` is `epsilon`, its inverse
leverage is

```text
s*B_epsilon^(-1)s
 =k rho/((1-rho)epsilon)
 =L_target.                                             (3)
```

The multiplicative determinant shift is therefore exactly

```text
(1-rho)^k(1+L_target)=1.                               (4)
```

Equivalently, the logarithmic shift is zero: exponentially large inverse
leverage cancels the entire common-direction volume collapse. Cycle 26's
dual vector reconstructs `b` with exact error `L_target^(-1/2)`.

## Finite and critical instances

For `k=4`, `rho=1/4`, exact arithmetic gives

```text
L_target=175/81,
epsilon=108/175,
residual off-diagonal=-67/525,
full Gram off-diagonal=27/175.
```

Both Gram matrices are positive definite, and (4) holds exactly.

At the critical skeleton scales

```text
k=X^(21/25), rho=X^(-3/5), J=X^(1/25),
```

one has `k rho=X^(6/25)` and `k rho^2=o(1)`. Hence

```text
epsilon=exp(-X^(6/25+o(1))),
L_target^(-1/2)=exp(-X^(6/25+o(1))/2).
```

The abstract labels do not enter (1), so they may be assigned any prescribed
separation, including `X^(3/5)`.

## Saturation statement and gate effect

`PROVED`: projection size, label separation, block-flat synchronization,
Hadamard surgery, PSD residual normalization, determinant shift, and detector
reconstruction do not jointly bound the row count in the abstract
block-subspace residual-shift architecture. The tuned simplex residual is a
sharp extremizer for that package.

Therefore any strict skeleton saving must use a constraint absent here: the
actual curve `t -> (p^(-it))_p`, unique factorization/logarithmic curvature,
or a source identity tying detector coefficients to that curve. This scoped
saturation result does not quantify over methods carrying such arithmetic
information.
