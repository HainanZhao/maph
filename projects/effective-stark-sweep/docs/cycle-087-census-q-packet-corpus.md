# Cycle 087 — exhaustive Q-stratum packet-polynomial corpus

## Outcome

`PROVED`: Every one of the 1,560 rows in the frozen quadratic stratum
has an exact packet polynomial over its base real quadratic field.
Every row passes exact conductor/Euler data, certified quartic-field
unit data, Artin-image cardinality, identity-factor selection,
reciprocity up to the monic constant, squarefreeness, irreducibility
over \(K\), positivity provenance, and the frozen coefficient cap.

The row files are hash-chained in stable RQ order.  The verified final
root is
`7c04242b1d4c11293af96f83f4915dbed25f6125c60d82965e533df5c9d81855`.

## Height calibration

`OBSERVED`: The preregistered height-only pass covered all 1,560 Q
rows and all 2,232 supported quadratic-character occurrences without
constructing a packet polynomial or opening an analytic packet target.
There are 1,560 nonzero effective character occurrences after the 672
zero Euler products are removed.  The maximum coefficient-digit
predictor is 89 at RQ-005284, so the frozen rule selected a 256-digit
runtime cap.

The exact corpus maximum is 62 coordinate digits, at RQ-007171.

## Exact distributions

| invariant | exact counts |
|---|---|
| packet degree over \(K\) | 1: 346; 2: 930; 4: 242; 8: 42 |
| common exponent denominator | 1: 1,491; 2: 69 |
| all-Euler-zero packet \(X-1\) | 346 |

The 346 degree-one rows agree exactly with the already-banked all-zero
Euler sub-stratum.

## Preserved failures and correction

The initial general script had three tooling defects, all found before
the corpus run: GP block syntax, a variable-collision bug in the exact
polynomial evaluator, and a missing factor of two in the Fourier
multiplier.  The last defect selected a factor that failed the frozen
positivity gate, so it could not pass silently.

The first population attempt used a full-field unit-lattice
calculation to extract denominator-two roots.  RQ-001090 and
RQ-001697 each hit the preregistered 300-second cap.  That 397-row
partial chain is preserved at
`artifacts/census-q-packets-unit-lattice-partial-v0/`.

The exact identity power is already an element of the degree-at-most-16
full ray field.  Replacing the unit-lattice calculation by PARI's exact
`nfeltissquare` test extracts its square root directly.  The two timeout
rows then passed in approximately 0.10 seconds each, and RQ-000245
reproduced its independently banked anchor polynomial byte-for-byte as
mathematical text.  This is the implemented memory/time synthesis
improvement; it does not change the registered mathematical route.

The clean run then passed 1,560/1,560 rows in 43.458666 seconds.  Its
slowest row took 0.214415 seconds.

## Evidence and replay

- `artifacts/census-packet-height-calibration-v1.json`
- `artifacts/census-q-packets-v1/manifest.json`
- `artifacts/census-q-packet-corpus-audit-v1.json`
- `scripts/certify_census_q_packet.gp`
- `scripts/run_census_q_packet_synthesis.py`
- `scripts/audit_census_q_packet_corpus.py`

Quick audit:

```sh
python3 scripts/audit_census_q_packet_corpus.py
```

Full clean replay:

```sh
census_replay_dir=$(mktemp -d)
python3 scripts/run_census_q_packet_synthesis.py \
  --output-dir "$census_replay_dir/census-q-packets-v1"
```

The next active gate is the preregistered deterministic 50-row
independent Arb audit.  Until it passes, the analytic cross-check table
remains open even though the exact finite Q corpus is banked.
