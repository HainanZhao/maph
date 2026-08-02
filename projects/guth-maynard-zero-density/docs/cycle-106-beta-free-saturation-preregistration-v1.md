# Cycle 106 preregistration: beta-free powered-ray saturation boundary

Date frozen: 2026-08-02 UTC.

## Claim boundary

This cycle decides whether the Cycle-105 powered-ray datum alone realizes a
Cycle-67 packet seed. It may prove a non-implication and classify the exact
coefficient-scale orbit in the rational-alias class. It does not rule out a
seed after inspecting the retained stationary payload, prove signed phase
cancellation, or close singleton/large-degree, weak, or simple-root branches.

## Frozen data

- `u,v>0`, `(u,v)=1`, `d=u+v`.
- `N=n0^d`, `R=r0^d`, `(n0,r0)=1`.
- Cycle-102 cross factors obey `R=x*R2`, `N=y*N2`, `(x,y)=1`.
- The rational critical scale number is written `K=A0/S0` in lowest terms.
- Coefficient scales satisfy `1<=lambda<=Lambda`; a hit means
  `|A-lambda*K|<=epsilon` for some integer `A`.
- A genuine transport seed means the Cycle-67 beta-dependent inequality
  `|j0+beta-h0*alpha|<=C0/X` for an original row.

## Gates

1. **Rational scale gate.** Prove exactly
   `K=d*n0^u*r0^v/(x*y)` and compute its reduced denominator `S0`.
2. **Tight-hit gate.** Under `0<=epsilon<1/S0`, prove that a scale is a hit
   iff `S0|lambda`, with unique nearest integer when `epsilon<1/2`. Hence the
   hit set is the exact progression
   `{S0,2S0,...,floor(Lambda/S0)S0}` and has size `floor(Lambda/S0)`.
3. **Saturation gate.** Prove all scales survive exactly when `S0=1` (within
   the frozen tight-hit regime). Preserve an explicit nontrivial integer-`K`
   family.
4. **Seed non-implication gate.** Holding every beta-free powered-ray datum
   fixed, exhibit two beta payloads for one original candidate row: one is an
   exact seed and one misses the strip whenever `C0/X<1/2`. Therefore no
   compiler inspecting only the powered-ray datum can certify a seed.
5. **Payload gate.** State positively that a retained payload which itself
   verifies the seed inequality may invoke Cycle 67; the no-go is scoped to
   beta-free data, not to payload-aware E16.
6. **Replay gate.** Exhaustively compare the simplified `K` with Cycle 104 on
   small perfect-power cores and test exact hit progressions and paired beta
   witnesses with exact arithmetic.

## Outcomes

- Passing the gates banks a sharp unsigned scale-saturation theorem and names
  the missing seed lock as beta/payload coupling.
- A mismatch in the rational formula or hit classification stops the cycle
  and preserves the first counterexample.
- No hostile audit is authorized.

## Replay

```sh
python3 proof/build_cycle_106_beta_free_saturation_v1.py --check
python3 -m unittest tests/test_cycle_106_beta_free_saturation_v1.py
```
