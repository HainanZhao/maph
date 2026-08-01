# G1 energy no-retention audit v3: Machin identity closure

`CERTIFIED_NUMERICAL`: v3 preserves the v2 finite energy certificate and
closes the remaining π-bound provenance. It proves with `Fraction` arithmetic
that `tan(4 atan(1/5))=120/119` and that subtracting `atan(1/239)` has tangent
one. The recorded rational Machin interval gives the principal branch, so the
identity `π/4=4 atan(1/5)-atan(1/239)` follows before the alternating series
is used to certify the W5 step `h=15`.

The outcome is unchanged: all 588 frozen screen rows are accounted for, 434
are feasible, 154 are declared construction failures, and zero feasible row
passes the exact energy retention test. This remains finite evidence only.

```sh
python3 projects/guth-maynard-zero-density/proof/audit_g1_energy_no_retention_v3.py --check
```
