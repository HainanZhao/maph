# Cycle 16: the separable tensor gate

## Claim boundary

`PROVED`: prime-square large values are governed by a separable, rather than
ordinary, spectral norm of an exact tensor-square sampling operator. Failure
of a proposed separable bound has an exact high-spectrum/common-rank-one
overlap certificate. `OBSERVED`: no arithmetic estimate of that certificate
is yet proved.

## Exact tensorization

For prime sampling rows `u_t`, let `S` have row `u_t tensor u_t`. If `a` is
the common prime coefficient vector, then

```text
S(a tensor a)=(Ua)^2,
<a tensor a,S^*S(a tensor a)>=sum_t |(Ua)_t|^4.
```

The row Gram matrix is the Schur square

```text
SS^*=(UU^*) circle (UU^*),
```

where the entries are complex squares of row inner products. This is PSD by
construction. The coefficient vector is not arbitrary in the tensor-square
space: it lies on the Veronese cone `{a tensor a}`.

Define `Sep(H_2)` as the maximum Rayleigh quotient of `H_2=S^*S` over that
cone. If `|P_a(t)|>=V` on `W` and `||a||_2^2=m`, then

```text
|W|V^4 <= Sep(H_2)m^2.
```

At the frozen scales, the desired rank-one semiprime theorem follows from

```text
Sep(H_2) <= X^(56/25+o(1)).
```

The generic fourth-moment exponent is `12/5`, so the missing saving remains
exactly `4/25` in `X`.

## Exact failure certificate

Let `Pi_>L` be the spectral projection of `H_2` above `L`, and let `z` be a
unit tensor of the form `a tensor a`. If
`xi=||Pi_>L z||_2^2`, then

```text
<z,H_2z> <= L+(lambda_max-L)xi.
```

Thus any value at least `A>L` forces

```text
xi >= (A-L)/(lambda_max-L).
```

`PROVED`: within this rank-one semiprime architecture there are exactly two
quantities to control: the high spectral scale and the overlap of its
eigenspace with the same common coefficient tensor. This is deliberately
scoped to the architecture; it is not an exhaustiveness claim about every
possible improvement to zero density.

## Countermodel and live arithmetic input

`PROVED`: if the sampling rows are identical, the top eigentensor is itself
separable and

```text
Sep(H_2)=lambda_max(H_2)=R||u||_2^4.
```

Therefore tensor rank one by itself gives no gain. The live theorem must use
the actual separated rows

```text
u_t=(p^(it))_(p in [X,2X]).
```

It can succeed in either of two ways: prove that the prime Schur-square Gram
has less high spectrum on a large row set, or prove that its high eigentensors
have fixed-power distance from the Veronese cone. The latter is a concrete
coefficient-sensitive inverse theorem and directly connects E3 to E4.

All registered tensor identities, sixteen identical-row countermodels, two
spectral-overlap examples, and the exponent translation are exact rational
calculations.
