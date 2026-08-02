# Cycle 104 preregistration: radical alias separation

Date frozen: 2026-08-02 UTC.

## Boundary

This cycle sharpens the Cycle-103 algebraic number attached to one exact
cross core. It may classify exact rational aliases and prove an elementary
norm separation. It does not claim that the separation closes every radical
degree, aggregate all core splits, or control weak/simple-root branches.

## Frozen notation

- `h=(s,t)`, `u=s/h`, `v=t/h`, `d=u+v=W/h`; hence `(u,v)=(u,d)=1`.
- The Cycle-102 variables obey `u=x*s2`, `v=y*t2`,
  `B0=t2*R2`, and `r=N/R` reduced.
- `K` is the Cycle-103 critical scale number.
- Write the reduced rational `K^d=P/S`, `P,S>0`, `(P,S)=1`.
- Alias denominators satisfy `1<=q<=Lambda`; `m` is a nearest integer to
  `qK`.

## Gates

1. **Single-radical gate.** Prove
   `K=(W/t)B0*r^(s/W)=(d*R2/y)*r^(u/d)` exactly.
2. **Rational-alias classification.** Prove `K` is rational iff both `N` and
   `R` are perfect `d`th powers. Include `d=1` explicitly.
3. **Norm gate.** In the irrational case prove
   `|qK-m|>=1/(S*(qK+|m|)^(d-1))` and the rational safe version
   `>=1/(S*(2*Lambda*U+1/2)^(d-1))`, where
   `U=max(1,P/S)>=K`.
4. **Cycle-103 closure gate.** If twice the frozen critical-value tolerance is
   below the safe norm bound, conclude that no short alias exists and hence
   at most one coefficient scale survives on that core.
5. **Replay gate.** Exhaustively verify the exact simplification and
   perfect-power classification on small cores. Check the norm inequality
   with rigorous interval arithmetic or exact symbolic algebra, recording
   the margin.
6. **Boundary gate.** Large `d` is an open aggregate radical-core branch, not
   evidence that the generic logarithmic-form route should be retried.

## Outcomes

- Passing the gates closes every core satisfying the displayed separation
  criterion to one scale and classifies exact rational saturators.
- Any rational-alias classification counterexample stops the formulation and
  is preserved.
- No hostile audit is authorized.

## Replay

```sh
python3 proof/build_cycle_104_radical_alias_separation_v1.py --check
python3 -m unittest tests/test_cycle_104_radical_alias_separation_v1.py
```
