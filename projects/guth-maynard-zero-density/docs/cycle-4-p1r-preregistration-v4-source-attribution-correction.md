# Cycle 4 P1R preregistration v4 source-attribution correction

## Claim boundary

`OBSERVED`: v4 preserves v1--v3 and their hostile failure records.  It repairs
only the direct attribution for the already-sealed large-values exponent
bookkeeping.  It proves no P1R-FS obstruction, large-values, density,
short-interval, compatibility, extremizer, or saturation theorem.  CRR
discovery/search remains prohibited.

The preserved v3 hostile audit found that the vector `[6, 8, 8]` was computed
without an explicit `GM-T1.1` ledger row or machine-checked theorem fragment.
V4 fixes that attribution gap while retaining v3's immutable historical
replay design and its lifecycle correction.

## Direct large-values source record

`PROVED` as source-statement inspection: GM Theorem `thrm:LargeValues`, source
lines 68--79, assumes `|b_n| <= 1`, 1-separated points `t_r` in `[0,T]`, and

\[
\left|\sum_{n=N}^{2N} b_n n^{it_r}\right|\ge V\qquad(r\le R).
\]

It concludes

\[
R\le T^{o(1)}\bigl(N^2V^{-2}+N^{18/5}V^{-4}+TN^{12/5}V^{-4}\bigr).
\]

Under the pinned formal substitution `(N,T,V)=(L,H,v^7)` with
`(L,H)=(v^10,v^12)`, the three monomial exponents are exactly `[6, 8, 8]`.
This is `PROVED` exact algebra for a source upper-bound formula only.  It does
not establish a lower bound, a common coefficient/set family, or saturation.

## Replay and lifecycle

```sh
python3 proof/build_cycle_4_p1r_preregistration_v4.py --check
python3 -m unittest tests/test_cycle_4_p1r_preregistration_v4.py -v
```

Historical replay still reads no mutable current Plan.  The separate v3
operational preflight remains `OBSERVED`, replaceable, and excluded from v4's
historical artifact identity.  `--write` refuses overwrite and `-O`/`-OO`
fail closed under the pinned non-optimized CPython 3.12.3 runtime.
