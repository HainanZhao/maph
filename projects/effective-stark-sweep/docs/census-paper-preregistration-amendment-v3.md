# Census-paper preregistration amendment v3: effective orbit anchor

Frozen: 2026-07-31 UTC, after checking RQ-000089 only against the
already-banked Euler-degeneracy artifact and before extracting any
new relative unit, trace, exponent, or polynomial for a
four-character row.

## Preserved anchor-selection failure

Amendment v2 selected RQ-000089 as the first row with four supported
quadratic characters.  The frozen exact Euler audit shows that one of
its four character terms has \(E_\chi=0\).  Its effective unit product
therefore has only three factors, whose eight formal sign patterns can
already match the eight Artin classes.  RQ-000089 cannot exercise the
proper-image factor gate that amendment v2 intended.

No unit or polynomial was extracted before this finding.  The v2
selection remains preserved as a failed anchor choice.

## Corrected frozen anchor

The replacement selection rule uses only
`artifacts/engine-a-euler-degeneracy-v1.json`, SHA-256
`f4ead3438d3b305fa42e73e1d979530a04104ce8d642db0b1c9ac85929bac033`:

> choose the lexicographically first stable RQ id with four supported
> quadratic characters and zero vanishing Euler terms.

The resulting anchor is RQ-000245.  The exact orbit-factor gates from
amendment v2 are unchanged.
