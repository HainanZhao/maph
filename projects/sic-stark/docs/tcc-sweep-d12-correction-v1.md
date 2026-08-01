# Correction D12-C1 — fixed point versus stabilizer eigenunit

**Date:** 2026-08-01 UTC
**Status:** `CORRECTION_CONTAINED`
**Affected claims:** only exploratory D12 bridge artifacts; no published
certificate or proved TCC statement is affected.

## Error and cause

The first D12 ray-label experiments used
\(\lambda=(11+3\sqrt{13})/2=4+3y\), the expanding eigenvalue of
\(L_z=\left(\begin{smallmatrix}10&3\\3&1\end{smallmatrix}\right)\),
in the principal element \(q\lambda-\widetilde p\).  This conflated
the stabilizer eigenvalue with the fixed point required by the
AFK/Kopp ray correspondence.

For \(Q=\langle1,-3,-1\rangle\), the correct RM fixed point is
\[
 \rho=\frac{3+\sqrt{13}}2=y+1,
 \qquad L_z\cdot\rho=\rho,
 \qquad 3\rho+1=\lambda.
\]
With \(\mathfrak b=\mathcal O_K\) and
\(\mathfrak m=12\mathcal O_K\), Kopp's correspondence gives
\(\alpha=12\), hence the characteristic representative is
\[
 \alpha\left(\frac q{12}\rho-\frac{\widetilde p}{12}\right)
 =q\rho-\widetilde p,
\]
not \(q\lambda-\widetilde p\).

## Containment

The following outputs are retained for audit but **invalidated as
AFK/Kopp label evidence**:

- `tcc-sweep-d12-fixed-ray-shortcut-audit-v1.json`;
- `tcc-sweep-d12-conductor-lowering-v1.json` and its script;
- `tcc-sweep-d12-lowered-engine-a-packets-v1.json` and its script.

Their counts (71 lowered rows, six scalar moduli) must not be cited.
The v1 multiplier ledger's all-character phase identity remains an
algebraic identity because its theta character is invariant under
integral changes to the first characteristic coordinate, but its
reported positive lifts are not the AFK/Kopp lifts; it is superseded
for bridge use.

## Corrected replay

`audit_tcc_sweep_d12_conductor_lowering_corrected_v2.py` uses the exact
fixed-point positivity condition and verifies
\[N(q\rho-\widetilde p)=\widetilde p^2-3\widetilde p q-q^2.\]
It produces 48 full-modulus and 95 lowered rows across eleven HNF
moduli.  The dependent corrected packet replay is
`certify_tcc_sweep_d12_lowered_engine_a_packets_corrected_v2.py`.
The corrected fixed-point multiplier replay is
`audit_tcc_sweep_d12_multiplier_ledger_corrected_v2.py`.
Both remain `EXPLORATORY`: no sign table, AFK value identification,
minor certificate, or TCC conclusion follows.
