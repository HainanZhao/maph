# Cycle 177 preregistration: actual-curve primitive-ray census engine

## Amendment log

- 2026-08-02: Cycle 64 was re-read before computation.  It already proves the
  primitive-ray compression proposed in the initial draft.  The active
  question is therefore narrowed in place to the exact rational-root
  saturator below; no new same-cycle document is created.

## Question

For the Cycle-63 beta-free actual exponential pair census

```text
P = sum_(1<=d<=H) (H-d) #{1<=ell<=c Delta:
    ||d(exp(2pi ell/Delta)-1)|| <= 2C/X},
```

does the positive exponential curve admit a legal rational-root family that
violates the raw uniform target `P<X^(17/25+o(1))`?  If so, does that family
realize the already required seeded deep-packet branch rather than a genuine
large total census?  The purpose is to determine whether the pair census can
remain a uniform analytic target at all.

## Frozen symbolic regime

- `Delta=X^(3/5)`, `H=X^(11/25)`, fixed `0<c<1`, and fixed `C>0`.
- Use the Cycle-64 primitive-ray and Cycle-65--67 depth/seed ledgers as
  frozen inputs; they are not re-proved here.
- Fix `0<c<1`, choose an integer `r>=1` with
  `log(1+1/r)<2pi c`, and for a positive integer `L` set
  `Delta_L=2pi L/log(1+1/r)` and `X_L=Delta_L^(5/3)`.
- The designated label is `ell=L`, so
  `alpha_L=exp(2pi L/Delta_L)-1=1/r`.  Retain every
  `d=kr<=H_L` and its exact integer `n=k`.
- For the seed check set `beta=0`, `q=r`, `a=1`, and retain a central source
  row `h_0=r m` with `j_0=m`; freeze `K=floor(H_L/(4r))`.
- The only admissible proof engines are the exact rational-root identity,
  the explicit weighted-pair sum, and the existing seeded-packet propagation
  identity.  A finite affine, signed-local, beta-free, or terminal-web
  classifier alone is declared non-progress.
- A finite affine, signed-local, beta-free, or terminal-web classifier alone
  is declared non-progress.

## Frozen discovery protocol

The main family is symbolic and exact.  The only numerical work is a
non-proof sanity check of the finitely instantiated formulas at
`r in {1,2,3,5,8}`, `L in {10,100,1000}`, and `c=1/4`, using 100 decimal
digits and recording any apparent failure without retry.  It may not select
parameters or alter the exact proof.

## Advance and failure rules

Advance only on one of the following.

1. `PROVED`: the exact family has `P>>X_L^(22/25)`, so the raw uniform
   Cycle-63 pair target is false by `X_L^(1/5)` within the stated continuous
   scale formulation; and
2. `PROVED`: its central beta-zero row is a Cycle-67 seeded packet of depth
   `K>>X_L^(11/25)`, while its direct triple-census contribution is only
   `asymp X_L^(11/25)`.  Thus it does not by itself refute the direct
   `T<X^(16/25)` target.

The next target must be a diagonal-aware direct triple census or a theorem
that routes every heavy actual packet into a usable seeded recurrence.  A
uniform raw pair-census bound is no longer admissible.

## Falsifiers

- `ell=L` is outside `1<=ell<=c Delta_L`.
- `alpha_L` is not exactly `1/r`, or a listed `d=kr` fails the pair condition.
- The weighted sum has exponent below `22/25`, or its beta-zero packet lacks
  a source seed, depth, or in-range progression.
- The construction uses an additional arithmetic restriction on `Delta` not
  present in the frozen Cycle-63 formulation.  Such a restriction would
  narrow this result's scope rather than be silently ignored.
