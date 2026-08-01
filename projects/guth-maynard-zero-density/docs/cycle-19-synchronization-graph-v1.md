# Cycle 19: synchronization graph and the prime-log closure gap

## Claim boundary

`PROVED`: common large projections force a quantitatively dense graph of
phase-aligned row correlations and many two-step paths. `PROVED`: these facts,
even with arbitrarily separated row labels, do not bound the number of rows
in an abstract Hilbert system and do not force positive phase-code entropy.
`OBSERVED`: the corresponding prime-log closure theorem is open.

## Synchronization theorem

Let `||a||^2=A`, let `||u_t||^2=M`, and suppose
`|<a,u_t>|>=V` for `R` rows. Align the projections with phases `z_t` and set
`K(t,s)=<u_t,u_s>` and `w=V^2/A`. Cauchy--Schwarz gives

```text
sum_(t,s) z_t conjugate(z_s)K(t,s) >= R^2 w.
```

If `Rw>=2M`, deleting the diagonal leaves real mass at least `R^2w/2`.
Since every real kernel entry is at most `M`, at least

```text
R^2 w/(4M)
```

ordered off-diagonal pairs have phase-aligned real kernel at least `w/4`.
The graph is symmetric. If `E` is its ordered edge count, Cauchy--Schwarz on
the degrees gives at least `E^2/R` ordered two-step paths, allowing the two
endpoints to coincide.

At `A=M=X`, `V=X^(7/10)`, and `R=X^(21/25)`, the correlation scale is
`X^(2/5)`. The forced ordered-edge, average-degree, and two-step-path
exponents are respectively

```text
27/25,  6/25,  33/25.
```

Thus a hypothetical target-sized skeleton is far from a set of isolated
accidents: it carries a growing recurrence graph.

## Sharp abstract obstruction

For arbitrary `R`, use orthonormal vectors `e_0,...,e_R`, set

```text
a=sqrt(A)e_0,
u_t=sqrt(M)(sqrt(w/M)e_0+sqrt(1-w/M)e_t).
```

Then every projection has size `sqrt(Aw)` and every distinct row pair has
kernel exactly `w`. All pairs are popular, for any `R`, and external labels
can be assigned any separation. The Gram eigenvalues are `M-w` and
`M+(R-1)w`, so the construction is genuine whenever `0<w<=M`.

Putting the common component and `a` in one declared coordinate block also
makes the phase-code block entropy zero. Therefore neither separation labels,
common projection, scalar coherence, graph density, nor high-value data alone
can produce the skeleton saving or an entropy increment.

## The exact open seam

For prime rows `u_t=(p^(-it))`, two popular edges sharing a vertex correspond
to two large values of the prime kernel at separated differences. Abstract
Gram positivity does not make the endpoint difference popular. A useful
prime-log closure lemma must add one genuinely arithmetic statement, for
example:

- too many two-step paths are impossible for the prime kernel;
- many two-step paths force many popular endpoint differences and hence an
  iterating recurrence tree; or
- the paths force synchronized mass in several genuine prime blocks, which
  can be routed into E10 detector surgery.

This replaces the vague instruction “use entropy” with a precise missing
implication and its required exponent budget.
