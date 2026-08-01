# Cycle 2 — Stream C Route B v4 closure

Claim boundary: `PROVED` conditional only on Guth--Maynard's published
zero-density theorem. This closes the external explicit-formula source gap
identified in Route B v3. It neither improves a density exponent nor proves a
new short-interval theorem. Versions v1--v3 are preserved.

## Outcome

`PROVED`: the MIT OCW-licensed Kedlaya 18.785 formula supplies the previously
unarchived arbitrary-height theorem. It applies for every \(x\ge2\),
\(T>0\), hence covers every Guth--Maynard choice \(2\le T\le x\). The
course proof explicitly counts zero residues with multiplicity. The v2 access
ledger records the CC BY-NC-SA 4.0 provenance, source URLs, frozen hashes, and
the DSpace WAF retrieval limitation.

`PROVED`: with \(u=\lceil x\rceil-1\), \(v=\lfloor x+y\rfloor\), the
half-weighted source formula transfers to Guth--Maynard's integer sum over
\([x,x+y]\), with \(O(\log x)\) endpoint cost and \(v-u=y+O(1)\). At
these integer endpoints \(\langle u\rangle,\langle v\rangle\ge1\), so
the source errors are \(O(x\log^3x/T)\) for \(2\le T\le x\).

`PROVED`: source truncation is by \(|\gamma|<T\); Guth--Maynard prints
\(|\rho|\le T\). The difference, including open/closed boundary points, is
contained in unit strips about \(\pm T\). HSW with Bui--Heath-Brown supplies
a multiplicity-inclusive \(O(\log T)\) local count, so the discrepancy is
\(O(x\log T/T)\), absorbed in the formula error.

`PROVED`: importing only those nodes and the already checked Route-B-v3
Huxley/Ford/Platt--Trudgian/HSW/Bui nodes closes the Route-B chain. The exact
arithmetic remains \(b=30/13\), giving \(\theta=17/30\) in the uniform
branch and \(\theta=2/15\) in the almost-all branch, each with the existing
arbitrary \(\epsilon>0\) slack.

## Replay

```sh
python3 projects/guth-maynard-zero-density/proof/check_cycle_2_stream_c_explicit_formula_sources_v2.py
python3 projects/guth-maynard-zero-density/proof/replay_short_intervals_stream_c_route_b_v4.py --check projects/guth-maynard-zero-density/artifacts/cycle-2-stream-c-route-b-v4.json
python3 -m unittest projects/guth-maynard-zero-density/tests/test_short_intervals_stream_c_route_b_v4.py
```

The deterministic certificate is
[cycle-2-stream-c-route-b-v4.json](../artifacts/cycle-2-stream-c-route-b-v4.json).
