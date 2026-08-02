# Cycle 107 preregistration: actual-scale geometric phase

Date frozen: 2026-08-02 UTC.

## Claim boundary

This cycle restores the actual anchor divisibilities and traces the complete
Cycle-94/95 stationary phase along the Cycle-106 rational scale progression.
It may prove an exact geometric-phase reduction and a bounded-variation sum
bound. It does not assert that the actual amplitudes already satisfy the
required variation budget or that base-phase resonance is a packet seed.

## Frozen data

- Reduced anchor `c0=p0/q0`, `p0,q0>0`.
- `K=A0/S0` is reduced; `B=lambda*B0`, `C=lambda*C0`.
- Actual indices require
  `A=p0*n=lambda*K`, `B=p0*n'`, and `C=q0*m`.
- The entropy phase is
  `F(H,Delta;m,n,n')=Delta log(c0 Delta/m)-H log(H/n)
  +(H-Delta)log((H-Delta)/n')`.
- The full projective Poisson phase is
  `Phi=c*F-mu*H-nu*Delta`, with fixed Poisson modes `mu,nu` and
  `c=D/(2pi)`.
- `e(z)=exp(2pi i z)` and `||z||` is distance to the nearest integer.

## Gates

1. **Actual-scale lattice.** Prove the least positive admissible scale is
   `lambda0=lcm(S0*p0/(p0,A0), p0/(p0,B0), q0/(q0,C0))`, and every actual
   scale is `lambda0*ell`. Derive the integral base indices `(n0,n0',m0)`.
2. **Stationary scaling.** Prove that if `(H0,Delta0)` solves the stationary
   equations for the base indices, then `(ell H0,ell Delta0)` solves them for
   `(ell n0,ell n0',ell m0)`.
3. **Phase homogeneity.** Prove exactly
   `F(ell H0,ell Delta0;ell m0,ell n0,ell n0')=ell F0` and hence
   `Phi_ell=ell Phi0` for fixed `mu,nu,c`.
4. **Geometric cancellation.** Prove
   `|sum_{ell<=L}e(ell Phi0)|<=min(L,1/(2||Phi0||))`, with the resonant
   convention that the second term is infinite when `||Phi0||=0`.
5. **Weighted BV gate.** For complex amplitudes `a_ell`, prove the same phase
   factor times `|a_L|+sum|a_ell-a_(ell+1)|`. No amplitude regularity is
   inferred without tracing the actual B-process weights.
6. **Inverse output.** Failure to save must retain `c0`, beta-bearing payload,
   `mu,nu`, base indices, base stationary coordinates, and `Phi0` with an
   explicit near-integer threshold. Do not call it a seed without checking
   Cycle 67.
7. **Replay gate.** Verify divisibility lattices exhaustively and phase
   homogeneity symbolically; test geometric and BV inequalities with rigorous
   enclosures or exact root-of-unity cases.

## Outcomes

- Passing the gates converts the unsigned all-scale saturator into exact
  phase cancellation unless one base phase is resonant.
- A resonant base phase is payload-bearing E16 output, not automatic
  realization.
- No hostile audit is authorized.

## Replay

```sh
python3 proof/build_cycle_107_actual_scale_phase_v1.py --check
python3 -m unittest tests/test_cycle_107_actual_scale_phase_v1.py
```
