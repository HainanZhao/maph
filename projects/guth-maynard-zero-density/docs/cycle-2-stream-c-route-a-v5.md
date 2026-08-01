# Cycle 2 — Stream C Route A v5 official-source correction

`PROVED` claim boundary: this is a deterministic Route-A replay of the
published Guth--Maynard Section 13.2 deductions, conditional on the published
density theorem. It establishes no new density theorem, prime-interval theorem,
or exponent, and does not promote G0.

V5 preserves Route A v1--v4 and replaces the former author-copy formula path
with official source bytes only. It seals the official MIT DSpace SWORD ZIP,
the two official PDF members, the DSpace item metadata, source-closure v4, and
the v4 source checker. `mutool version 1.23.10` is checked before literal PDF
anchor extraction. No author-hosted/official byte identity is used or asserted.

The historical provenance corrections are precise:

- v2’s CC BY-NC-SA 4.0 and author-byte-license inference is withdrawn;
- v3’s author-copy distribution caveat is superseded by the official archive;
- v4’s Route-A dependence on source-closure v2 is not reused.

All remaining Route-A inputs are separately pinned: GM Section 13.2, Huxley,
Ford, Platt--Trudgian, HSW, and Bui--Heath-Brown. The arithmetic is replayed
from exact fractions. In particular, `1/(30/13)=13/30`,
`2/(30/13)=13/15`, yielding the published endpoints `17/30` and `2/15`.
The Huxley comparison is globally certified by coefficient equality:

\[
30(3s-1)-39=3(30s-23),
\]

so \(30/13-3/(3s-1)\ge0\) for \(4/5\le s<1\), without sample-point
reasoning.

The mathematical artifact is byte-stable and excludes timing. The separately
written performance artifact is `OBSERVED` only.

```sh
python3 projects/guth-maynard-zero-density/proof/replay_cycle2_stream_c_route_a_v5.py --check projects/guth-maynard-zero-density/artifacts/cycle-2-stream-c-route-a-v5.json
python3 -m unittest projects/guth-maynard-zero-density/tests/test_cycle2_stream_c_route_a_v5.py -v
```

Status: **NARROW PASS for Stream C, Route A only**. G0 remains `OBSERVED`
pending the separate full reconciliation.
