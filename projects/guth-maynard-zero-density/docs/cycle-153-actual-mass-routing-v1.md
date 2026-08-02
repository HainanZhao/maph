# Cycle 153: every forced negative divisor-comb correlation routes to strict halo or labelled escape

## Claim boundary

`PROVED`: if the post-error residual correlation satisfies
`-Re<H,w_h>/W_h>=mu_*>0` and is partitioned exactly as `H=S+E`, then either
the licensed strict smooth halo has labelled negative-part mass at least
`mu_*/2`, or the labelled escape component has normalized negative correlation
at least `mu_*/2`.  This is an exact routing compiler.

It does not prove the actual weight normalization or uniform per-mode bound
needed to invoke Cycle 152, bound either routed class, prove a full moment,
density improvement, or prime-interval theorem.

## Exact post-error split

Normalize by the Cycle-149 one-witness scale

```text
W_h=KQ^2/h.
```

Cycle 150 supplies the residual anti-aligner only after its strict-positive
error has been removed.  Freeze the surviving statement as

```text
-Re <H,w_h>/W_h >= mu_*.                           (1)
```

Let `S` contain exactly the smooth positive-chart halo modes satisfying the
literal strict denominator, lcm, and bounded-tail conditions of Cycle 151.
Write `H=S+E`, where `E` is the disjoint exhaustive complement.  Its labels
record one reason from the frozen list: boundary denominator, phase-changing
chart, nonsmooth payload, unbounded tail, failed rational label, inadmissible
lcm, or registered truncation.

For `S=sum_b S_b`, retain every exact correlation

```text
gamma_b=<S_b,w_h>/W_h,
N_S=sum_b (-Re gamma_b)_+.                         (2)
```

## Routing inequality

From `H=S+E` and (1),

```text
-Re <E,w_h>/W_h
 =-Re <H,w_h>/W_h + Re <S,w_h>/W_h
 >=mu_* - N_S.                                    (3)
```

Indeed `-Re sum_b gamma_b<=sum_b(-Re gamma_b)_+=N_S`.
If `N_S>=mu_*/2`, the strict branch has the claimed labelled negative mass.
Otherwise (3) gives

```text
-Re <E,w_h>/W_h >=mu_*/2.                          (4)
```

Thus no forced negative correlation remains unclassified.

## Cycle 152 interface

The strict output becomes a Cycle-152 antecedent only after establishing

```text
sum_b w_b<=1,
0<=(-Re gamma_b)_+<=Cw_b/m_b
```

with fixed `C`, positive chart weights, and the retained labels
`(b,w_b,r_b,h_b,d_b,m_b,L_b,tau_b,gamma_b)`.  Until then it is only an actual
mass branch, not an actual bounded-multiplier fan.  The escape output likewise
is an obligation to analyze, not an exclusion theorem.

## Gate effect

The next task is to prove the strict branch's normalization/per-mode bound or
to use the labelled escape obligation to improve the phase, payload, boundary,
or unbounded-tail decomposition.
