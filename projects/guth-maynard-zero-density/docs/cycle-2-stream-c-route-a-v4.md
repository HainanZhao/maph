# Cycle 2 — Stream C Route A v4 correction

`PROVED` claim boundary: this is a source-sealed replay of the published
Guth--Maynard Section 13.2 deductions, conditional on the published density
theorem. It proves neither a new density result nor a new prime-interval
exponent, and it does not promote G0.

Route A v4 retains v1--v3 unchanged and corrects the source-authority gap in
v3. The v3 output was deterministic on its tested runtime, but its replay did
not seal access-ledger v2, the v2 source-closure artifact, or Kedlaya's
von-Mangoldt proof unit. Accordingly, v4 does not reuse v3's broader source
authority claim. This is not an allegation that v3's output bytes were
nondeterministic. The older v1/v2 reports carry timing fields and are therefore
identified here by their stable semantic replay hashes rather than raw bytes.

The v4 artifact pins:

- the access ledger v2 and explicit-formula source closure v2;
- both Kedlaya course PDFs, including the arbitrary-height formula and the
  multiplicity residue proof;
- GM Section 13.2, Huxley, Ford, Platt--Trudgian, HSW, and
  Bui--Heath-Brown source hypotheses.

The arithmetic is a fresh Route-A `Fraction` replay. It checks
`1/(30/13)=13/30`, `2/(30/13)=13/15`, and the uniform/almost-all endpoints
`17/30` and `2/15`. The Huxley comparison is universal: exact polynomial
coefficient equality gives

\[
\frac{30}{13}-\frac{3}{3s-1}
=\frac{3(30s-23)}{13(3s-1)}\ge0
\qquad(4/5\le s<1),
\]

with no finite sample-point promotion.

The deterministic mathematical artifact contains no timing. An optional,
separate `OBSERVED` performance artifact records wall time.

```sh
python3 projects/guth-maynard-zero-density/proof/replay_cycle2_stream_c_route_a_v4.py --check projects/guth-maynard-zero-density/artifacts/cycle-2-stream-c-route-a-v4.json
python3 -m unittest projects/guth-maynard-zero-density/tests/test_cycle2_stream_c_route_a_v4.py -v
```
