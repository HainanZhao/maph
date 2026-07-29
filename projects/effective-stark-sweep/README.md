# The Effective-Stark Sweep

This project is a certified census of unconditional archimedean Stark
instances over real quadratic fields.  Its final records have exactly
two possible mathematical outcomes:

- `PROVED`, routed through one frozen proved engine and accompanied by
  a replayable packet certificate; or
- `FRONTIER`, accompanied by the first named obstruction encountered by
  the frozen decision procedure.

No numerical approximation is promoted to a theorem.  The reusable
proof machinery remains in the sibling
[`sic-stark`](../sic-stark/) project; this directory provides the
census definitions, orchestration, records, and certificates.

## Current state

Cycles 001–010 are complete. Publication uploads, identifier recording, and
correspondence are administrative metadata, not research gates.  The
earlier sequencing records are retained only as process history and are
superseded by `data/research-activation-v3.json`.

The exact state can be checked with:

```bash
python3 scripts/audit_activation.py
python3 -m unittest discover -s tests -v
python3 scripts/audit_w1_anchor_screen.py
```

The seven anchor bundles are frozen in
[`data/anchor-battery-v1.json`](data/anchor-battery-v1.json).  They
cover the two Engine-A calibrations, four Engine-B packets, and the
Engine-C primitive packet.

The seven-bundle end-to-end reproduction passed. The maximal-order
ideal backbone contains 8,200 conjugacy-deduplicated cases over 121
certified fields. A preregistered 66-case structural pilot found one
new Engine-B route candidate, five Engine-C route candidates, and one
clean index-four frontier. See
[`docs/cycles-001-010-summary.md`](docs/cycles-001-010-summary.md).

`ROUTE_CANDIDATE` is not a theorem tag. No new case becomes `PROVED`
until its engine-specific packet and identification certificates pass.

## Claim tags

- `VERIFIED`: exact or replay-certified statement.
- `ENCLOSED`: rigorous Arb enclosure.
- `NUMERICAL`: exploratory or cross-check output only.
- `CONJECTURAL`: explicitly conjectural census analysis.
