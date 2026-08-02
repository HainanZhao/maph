# Cycle 173 preregistration: positive forward balance obstruction

## Question and boundary

Test whether a reduced-rational **forward** Cycle-167 cross edge can satisfy
all of its frozen conservative requirements on the actual positive
exponential branch `alpha_ell=exp(2pi ell/Delta)-1>0`. The permitted result
is an exact obstruction to the conservative balance gate. It does not rule
out reverse orientation, a transport using more strip-constant slack, a
different map, or any global transport construction.

## Frozen forward data

Let `ell>0`, so `y=1+alpha_ell>1`, and retain a bound `Y>=y`. Let positive
coprime `a,q`, a depth `K`, and a forward affine edge satisfy

```text
h_plus=q h/a,
h,h_plus in [H,2H],
qK<=H,
2H Y C_*/(aK)<=1,       C_*>=1.                    (1)
```

The final condition is the Cycle-167 conservative balance gate, allowing a
registered multiplicative slack `C_*` but no post-result relaxation.

## Gate

1. Prove from the two row ranges that `a/q=h/h_plus<=2`.
2. Prove from balance and admissibility that `a/q>=2YC_*`.
3. Since `Y>1` and `C_*>=1`, conclude that no such forward edge exists.
4. Record the exact scope: this contains the positive forward conservative
   direct-map branch only. It neither prohibits reverse orientation nor
   asserts that every beta-preserving transport must use this balance ledger.

## Falsifier and advance condition

The falsifier is a complete positive-branch forward row satisfying every
line of (1), or any proof that the actual Cycle-167 balance budget has a
slack smaller than the registered `C_*>=1`. Advance if the contradiction is
exactly replayed and its orientation/slack/positive-branch limits are kept
visible.
