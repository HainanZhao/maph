# Cycle 33 v2 correction: anchor recurrence needs evaluation and stability

## Correction

`OBSERVED` scope error in v1: closeness of a reconstructed direction `d` to
an anchor span does not by itself translate the original detector's large
values into kernel recurrence. The direction `d` must be known large on the
retained rows. For multiple anchors, the representation coefficients must
also be controlled.

Define

```text
nu_(C')(d)=min_(t in C')|<x_t,d>|.
```

If

```text
||d-sum_(a in A)gamma_a x_a||<=epsilon,
```

then and only with a registered evaluation floor does the triangle inequality
give the useful statement

```text
|sum_(a in A)gamma_a H(t,a)|
 >=nu_(C')(d)-epsilon.                                 (1)
```

For `|A|>1`, distance to the span does not bound `gamma`: nearly cancelling
anchors permit arbitrarily large coefficient norms. A stable multi-anchor
gate must therefore include an `l1`/`l2` cap or a lower Gram bound.

## Valid rank-one route

The original normalized detector `b` satisfies

```text
nu_C(b)>=sqrt(rho)
```

by the source large-value hypothesis. Cycle 26 reconstructs this same `b`,
so (1) is valid for its anchor analysis. In particular, a one-anchor
approximation has coefficient magnitude `1+O(epsilon)` and forces the
normalized prime kernel at every retained row to have magnitude at least
`sqrt(rho)-O(epsilon)`.

## Adaptive rank-J route

Cycle 28's reconstructed direction `Ey` is selected by residual leverage; no
lower bound for `nu_C(Ey)` has been proved. Its flat-support reductions remain
valid as reconstruction statements, but they cannot be fed into recurrence
without a separate evaluation-overlap or row-selection theorem.

The v1 flat-row witness and universal-distance no-go are unchanged. The live
anchor recurrence theorem is first restricted to the original rank-one
detector; adaptive directions carry an additional evaluation-floor gate.
