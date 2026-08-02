# Cycle 33 anchor-aware scope correction preregistration v2

## Correction boundary

The v1 actual-prime flat-row counterexample and dimension boundary remain
valid. Its recurrence reformulation omitted two hypotheses: the reconstructed
direction must itself be large on the retained rows, and a multi-anchor
representation needs coefficient control. This v2 may repair only those
hypotheses; it may not prove a recurrence bound.

## Frozen repair

For a unit direction `d`, define its evaluation floor on a row set `C'` by

```text
nu_(C')(d)=min_(t in C') |<x_t,d>|.
```

An anchor representation

```text
||d-sum_(a in A)gamma_a x_a||<=epsilon
```

implies the useful recurrence inequality

```text
|sum_(a in A)gamma_a H(t,a)|>=nu_(C')(d)-epsilon
```

only when `nu_(C')(d)` has a registered lower bound. For `|A|>1`, also
register a stability cap on `||gamma||_1` or `||gamma||_2`; distance alone
does not provide one.

The original rank-one detector `b` satisfies

```text
nu_C(b)>=sqrt(rho)
```

by the source large-value hypothesis, so the anchor recurrence route is valid
for Cycle 26 reconstruction of `b`. An adaptive rank-J direction from Cycle
28 has no such floor without a separate overlap/selection theorem.

Pin Cycle 33 v1 and Cycle 26. Use exact finite checks, CPython `3.12.3`, no
RNG/network.
