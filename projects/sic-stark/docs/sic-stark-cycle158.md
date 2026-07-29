# SIC--Stark research cycle 158: dimension-seven publication gate

> **Superseded by Cycle 160.** This gate correctly replayed the
> discriminant-$32$ certificate but incorrectly inferred coverage of
> the independent discriminant-$8$ stratum. Its universal
> dimension-seven scope verdict is withdrawn.

Date: 2026-07-29

## Question

Before shipping the trilogy, does the dimension-seven conductor-two
stratum actually support Paper II's universal Theorem 1, or must the
theorem be rescoped?

## Exact rerun

The canonical dimension-seven form has discriminant \(32\) and order
conductor \(2\). The dedicated closure suite was rerun from the current
tree:

```text
python3 -m unittest tests.test_dimension_seven_closure -v
Ran 8 tests in 28.557s
OK
```

The rerun covers:

- the exact conductor-lowering packet;
- Shintani index \(2\) and safe exponent \(16128\);
- exact one-place ray fields and candidate unit fields;
- phase, Artin, and archimedean labels;
- the complete packet certificate;
- trace one, idempotency, and all \(441\) minors for each formal shift
  \(0\) and \(1\); and
- the exact symbolic orbit reduction.

The form order has one relevant wide class, so unconditional
\(\mathrm{GL}_2(\mathbb Z)\) covariance transports the canonical result
to every admissible dimension-seven tuple.

## Publication archive

The Paper II companion archive was rebuilt twice, compared
byte-for-byte, extracted, checksum-verified, and tested in isolation.
Its clean extraction passed all \(80\) included tests. The archive
contains every dimension-seven lowering, Shintani, root-isolation,
phase, label, packet, and exact-TCC script plus the dedicated closure
test.

```text
dist/sic-stark-paper-II.tar.gz
SHA-256 292ca88e161201898463e20a1a3aa5fcde9d23422e724aee4490ac9fe62df7c1
bytes   415399
```

## Verdict

\[
\boxed{\text{PROVED; NO RESCOPE OF THEOREM 1}}
\]

Paper II's statement that \(0,1\in\mathcal Z_t\) for every admissible
dimension-seven tuple is supported by the exact conductor-two
certificate and archive-local replay. The cycle therefore closes on
the prove branch.

The self-hashed gate record is
`certificates/dimension-seven-cycle158-publication-gate.json`.
