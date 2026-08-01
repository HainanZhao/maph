# Corrected exact G1 energy no-retention audit v2

`CERTIFIED_NUMERICAL`: this corrected finite certificate accounts for all 588
frozen `U=2^12` screen rows: 434 feasible sets and 154 declared construction
failures. No feasible row satisfies the energy half of the conjunctive
retention rule.

V1 is preserved but superseded for this conclusion. V2 explicitly tests all
prospective Sidon pair sums, including new-versus-new pairs, and reconciles
the exact point list of every feasible independent construction against the
frozen v1 constructor through its SHA-256 hash. It also replaces the cited π
bounds with a rational Machin-formula enclosure from alternating arctangent
series, which certifies the W5 step `h=15` with recorded margins.

The exact rejection test remains
`max(E/Target,Target/E)^100 > 8`; each completed row has a stored positive
rational margin. This is finite numerical evidence only, not an asymptotic
method-saturation or route-selection theorem.

```sh
python3 projects/guth-maynard-zero-density/proof/audit_g1_energy_no_retention_v2.py --check
```
