# Cycle 13: source obstruction and weighted fractional tensor

## Claim boundary

`PROVED`: the full Guth--Maynard Type-I detector cannot be an exact sum of
balanced fivefold Dirichlet convolutions whose factors are supported on
integers at least two. `PROVED` conditional on transformed coefficient-square
norms: a cellwise fractional design with parameter `tau` gives local row
exponent `10-7tau`.

`OBSERVED`: this does not prove a new zero-density estimate. It replaces a
false source gate by a component architecture: factorable cells are handled
by fractional tensors, while prime/rough cells require a different detector
identity or a separate estimate.

## 1. The prime-support obstruction

For a prime `p>2T^(1/100)`, the truncated Möbius sum in the pinned detector
has only the divisor `d=1`. Thus

```text
b_p=exp(-p/T^(1/2)) != 0,
tilde b_p=(N/p)^sigma b_p != 0.
```

On the other hand, the Dirichlet convolution of five sequences supported on
integers at least two has support in the composite integers (indeed its
indices are at least `2^5`). Its coefficient at every prime is zero, and a
sum of such convolutions still vanishes there. Therefore the proposed exact
full-detector decomposition in Cycle 12 is impossible on any relevant dyadic
interval containing such a prime.

The theorem is deliberately narrow: it does not show that prime-supported
coefficients create large values on the selected zero rows, and it does not
exclude factors containing the unit, approximate decompositions, or a new
prime-weighted zero detector.

## 2. Cellwise fractional designs

Write a product cell as `A=product_i A_i`, with factor-length exponents
`y_i>0` summing to five. For an integer vector `k>=0` satisfying
`sum_i y_i k_i<=2`, the moment

```text
B_k=product_i A_i^(2+k_i)
```

has length at most `v^12`, the local time scale. Suppose rational weights
`pi_k` satisfy

```text
sum pi_k=1,                 sum pi_k k_i=tau  for every i.
```

Then, pointwise and without assuming any factor has modulus at least one,

```text
product_k |B_k|^pi_k = |A|^(2+tau).
```

Hence some supported moment is at least the right-hand side. Colouring rows
by such a moment and applying the same length-`v^12` mean-value input as in
Cycle 12 gives, conditional on its coefficient-square norm,

```text
|W| <= v^(10-7tau + 2(2+tau)delta + o(1)).
```

Thus `tau>2/7` gives a strict improvement over exponent eight. Moreover,

```text
5tau=sum_i y_i E(k_i)=E(sum_i y_i k_i)<=2,
```

so `tau<=2/5`. The balanced Cycle-12 design is optimal in this abstract
length budget, although unbalanced cells may still attain or approach the
same value through other designs.

## 3. A constructive unbalanced theorem

Assume `y_i<=2` and set `q_i=floor(2/y_i)`. Each singleton pattern `q_i e_i`
is admissible. Giving it weight

```text
pi_i=(1/q_i)/sum_j(1/q_j)
```

makes every expected coordinate equal to

```text
tau_single=1/sum_i(1/q_i).
```

This is an explicit certificate, not a claim of optimality. It recovers
`tau=2/5` for `(1,1,1,1,1)`. More importantly, the Cycle-12 unbalanced
countermodel `(1/2,1/2,1,3/2,3/2)` has
`q=(4,4,2,1,1)`, `tau=1/3`, and local exponent `23/3`; it therefore retains
a gain `1/3` even though the uniform ten-moment construction exceeds the
time length.

If some `y_i>2`, every admissible pattern has `k_i=0`, so no positive uniform
`tau` exists in this architecture. Such cells, together with the prime
support, form the precise rough remainder now assigned to detector redesign.

## 4. Exact grid outcome

`PROVED`: among all 1,442 sorted positive fifth-grid cells with total
exponent five and between three and ten factors, 978 admit the singleton
design. It gives a strict saving on 927 cells, equality on 17, and a negative
formal gain on 34. The remaining 464 contain a factor exponent exceeding
two and cannot have positive uniform `tau` under any admissible design.

The best registered gain is `4/5`, attained for example at `(1,2,2)`. The
smallest positive registered gain is `1/52`, at
`(1/5,2/5,3/5,3/5,4/5,6/5,6/5)`. No failed cell is interpreted as a failure
of a different detector decomposition or a non-product engine.

## 5. Consequence for the research architecture

`PROVED`: exact balanced factorization of the full current detector is the
wrong source gate. `CONJECTURED`: a generalized Vaughan/Heath--Brown
decomposition of a prime-weighted or logarithmic-derivative detector can
produce finitely many product cells; the cellwise theorem would handle those
with `tau>2/7`, leaving a now-explicit rough-cell problem.

The next proof obligation is therefore not “factor everything evenly.” It is
to derive a source-valid detector identity, attach an exact `y`-vector and
coefficient-square norm to every cell, and show that the total contribution
of cells outside the strict-gain region is subcritical or is absorbed by a
second engine.
