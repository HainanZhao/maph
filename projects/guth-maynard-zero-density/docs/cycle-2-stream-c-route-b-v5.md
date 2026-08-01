# Cycle 2 — Stream C Route B v5

**Claim boundary — PROVED narrow Route-B pass.** Conditional on Guth--Maynard's
published zero-density theorem, v5 independently replays the already-published
Route-B short-interval deductions and seals their official formula-source
chain. It does not re-prove that density theorem, improve either exponent,
close a two-route Stream-C result, or declare G0 PASS.

Run:

```sh
python3 proof/replay_short_intervals_stream_c_route_b_v5.py --check
```

V5 preserves v1--v4. It expressly corrects v4's use of the old
source-closure-v2/CC-BY-NC-SA-4.0 premise: it seals source-closure v4 and its
checker, the independent official SWORD audit, official SWORD ZIP, both
official PDFs, and frozen DSpace item metadata. The official chain records the
course's CC BY-NC-SA 3.0 field; no rights assertion is made about author copies.

The standalone replay imports no Route-A artifact or script. It retains Route
B's non-formula nodes from v3/v4 (Huxley, Ford, Platt--Trudgian, and HSW/Bui)
and independently checks the exact invariants `b=30/13`,
`theta_uniform=17/30`, and `theta_almost_all=2/15`.

`mutool version 1.23.10` is pinned. The mathematical artifact contains no
runtime field. A separate `--write-performance` command writes the intentionally
non-deterministic host-time observation.
