# Exact G1 energy no-retention audit v1

`CERTIFIED_NUMERICAL`: at the frozen screen scale `U=2^12`, all 588 rows are
accounted for: 434 finite sets are feasible and 154 fail their declared
construction. Every feasible set fails the energy half of the frozen
retention rule, so no complex finite evaluation can be retained under the
conjunctive rule.

The certificate uses exact integer pair-sum multiplicities for
`#{(a,b,c,d): |a+b-c-d|<=1}` (radius zero). Instead of evaluating logarithms,
it checks the exactly equivalent inequality

```text
max(E/Target, Target/E)^100 > 8,
```

because `U^(1/400)=2^(3/100)`. It records a positive rational margin for each
feasible row. The W5 rational step is independently enclosed as `h=15` by
alternating-series bounds for `log(3/2)` and rational bounds for pi.

This finite-screen result does not establish an asymptotic obstruction,
saturation theorem, density improvement, or G1 route decision. It does show
that the preregistered v1 finite experiment has no energy-eligible candidate
at its first scale.

```sh
python3 projects/guth-maynard-zero-density/proof/audit_g1_energy_no_retention_v1.py --check
```
