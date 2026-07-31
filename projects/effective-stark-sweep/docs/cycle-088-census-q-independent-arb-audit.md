# Cycle 088 — independent 50-row Arb audit

## Outcome

`CERTIFIED_NUMERICAL`: The preregistered deterministic sample of 50 Q
rows passes an independent Arb audit.  The sample contains 43 nonzero
effective quadratic-character occurrences and 13 all-Euler-zero rows.
After Fourier transport, 101 distinct Artin sign rows pass.

The independent route constructs each primitive quartic field and uses

\[
 L'_K(0,\chi_{\rm prim})
 = (h_LR_L/w_L)/(h_KR_K/w_K).
\]

Arb encloses the full regulators from complete fundamental-unit
systems.  This stage completes before the comparison code opens the
corpus powered traces.  It never opens the relative-unit norm kernel,
selected packet factor, or packet roots.

The exact comparison route reconstructs each character value from the
denominator-cleared trace and applies the exact Artin sign rows.  Every
inflated independent character ball contains the corresponding
trace-derived interval.  Every Artin-row difference contains zero with
radius below \(10^{-38}\).

## Preserved precision failure

The frozen initial precision of 192 bits reached RQ-006617 with a
difference ball containing zero but radius approximately
\(5.43825\times10^{-27}\), so it failed the preregistered radius gate.
This is preserved in
`artifacts/census-q-arb-audit-192bit-failure-v0.json`.

The route, sample, and acceptance rule were unchanged.  At 384 bits the
full 50-row audit passes.  This is a precision escalation, not a method
substitution.

## Evidence

- `data/census-paper-q-arb-sample-v1.json`
- `data/census-paper-preregistration-amendment-v6.json`
- `artifacts/census-q-arb-audit-v1.json`
- `scripts/export_census_q_regulator_route.gp`
- `scripts/audit_census_q_arb_sample.py`

Replay:

```sh
python3 scripts/audit_census_q_arb_sample.py
```
