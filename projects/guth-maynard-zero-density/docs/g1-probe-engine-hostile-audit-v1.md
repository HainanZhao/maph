# Hostile audit of the G1 finite-probe engine v1

`OBSERVED`: the preserved v1 engine is contained and cannot be used as the
G1 empirical authority. This audit evaluates no finite complex row and proves
no analytic statement. It records three protocol defects against the frozen
v1 executable:

- Its CPython/mpmath identities are written into an observation record but
  never enforced before execution.
- A retained candidate whose two larger-scale synthetic validation scores are
  both strictly worse remains `COMPLETED`; v1 has no mechanical score-loss
  disposition for the preregistered falsifier.
- An unexpected row exception escapes `compute_full`, so it is not retained
  as a distinct failed row and can prevent creation of a complete observation
  artifact.

The v1 executable and any abandoned first launch remain preserved. A
separately versioned correction and a fresh run from the unchanged
preregistration are required before G1 route selection.

```sh
python3 projects/guth-maynard-zero-density/proof/audit_g1_probe_engine_hostile_v1.py --check
```
