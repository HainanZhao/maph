# G0 full reconstruction v3 runtime correction

Claim boundary: `PROVED` optimization-robust replay hardening of corrected G0
v2. It changes no mathematical reconstruction and proves no new theorem.

`OBSERVED`: hostile execution showed that `python3 -O` disables the bare
assertions used by the v1 runtime convention and v2 reconciler. V2's literal
frozen command runs unoptimized and remains a preserved record, but it is not
an optimization-robust final authority.

V3 pins runtime convention v2. It explicitly requires CPython 3.12.3 with
optimization level zero, uses exceptions rather than assertions for its own
gate checks, and invokes v2 in a fresh unoptimized subprocess. The hostile
command below must fail:

```sh
python3 -O projects/guth-maynard-zero-density/proof/reconcile_g0_full_v3.py --check
```

The normal command must pass:

```sh
python3 projects/guth-maynard-zero-density/proof/reconcile_g0_full_v3.py --check
```

`PROVED`: G0 PASS remains the corrected decision; v3 is the authoritative
certificate.
