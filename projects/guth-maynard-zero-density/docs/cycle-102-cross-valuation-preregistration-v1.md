# Cycle 102 preregistration: cross-valuation inverse atlas

Date frozen: 2026-08-02 UTC.

## Claim boundary

This cycle studies only the exceptional strong-critical fibers left by
Cycles 99--101.  It may prove an exact change of variables and a quantitative
weighted concentration lemma.  It does not claim cancellation from the
stationary phases, a weak-row or simple-root bound, a complete alias moment,
or a density or prime-interval improvement.

## Frozen variables and ranges

- `W=|w|`, `2<=W<=2M`, and `1<=s<W`, `t=W-s`.
- `N/R` is reduced and positive; `B,C<=Q`.
- `g0=(s,t)`, `s1=s/g0`, `t1=t/g0`.
- `x=(s1,R)` and `y=(t1,N)` are the two cross gcds.
- A prime-power colour means the *full* power `p^v` exactly dividing `x` or
  `y`, not an arbitrary subpower.  Side `R` colours come from `x`; side `N`
  colours come from `y`.
- The dyadic index is `floor(log2 z)` for `z>=1`.  The number of possible
  indices for a cross gcd at most `2M` is
  `L_M=1+floor(log2(2M))`.
- All concentration weights are nonnegative.  Signed cancellation is outside
  this lemma and must later use the actual B-process phases/amplitudes.

## Preregistered gates

1. **Exact-core gate.** Prove, not merely test, that writing
   `s1=x*s2`, `R=x*R2`, `t1=y*t2`, `N=y*N2` turns the primitive fiber bases
   into `B0=t2*R2`, `C0=s2*N2`, with
   `W=g0*(x*s2+y*t2)`.  Record all forced coprimalities and prime exclusions.
2. **Replay gate.** Exhaustively compare the original and core formulas for
   every reduced label `N/R`, `2<=W<=18`, and every split.
3. **Concentration gate.** For exceptional atoms of total nonnegative mass
   `E`, with total mass at each distinct `w` at most `A`, prove that some
   side/prime-power colour occurs on at least
   `E/(2*P(2M)*A)` distinct `w`, where `P(H)` counts prime powers at most
   `H`.  With both cross-gcd dyadic indices retained, prove the refined lower
   bound `E/(2*P(2M)*L_M^2*A)`.
4. **Anchor-retention gate.** The computational representation must carry an
   opaque stationary/anchor payload unchanged through colour assignment and
   concentration.  The theorem does not assert that the payloads agree.
5. **Boundary gate.** State explicitly that concentration is useful only once
   a per-`w` cap and an excess above the displayed colour entropy are supplied.
   Do not promote the informal phrase "excess forces many labels" without
   that threshold.

## Outcomes

- Passing all gates banks an exact cross-valuation inverse atlas for E16.
- If exact-core algebra fails, stop this formulation and preserve the first
  counterexample.
- If only the unrefined colour lemma holds, retain it and leave dyadic phase
  reinsertion open.
- No hostile paper-stage audit is authorized by this cycle.

## Replay commands

```sh
python3 proof/build_cycle_102_cross_valuation_inverse_v1.py --check
python3 -m unittest tests/test_cycle_102_cross_valuation_inverse_v1.py
```
