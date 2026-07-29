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

Phase 0 is prepared but not activated.  The sequencing gate in the
charter requires Papers I and II to be posted to arXiv, their immutable
artifact DOIs to exist, and the Kopp correspondence to be sent.  Those
external actions require the author's accounts and review.

Local Phase-0 preparation can be checked with:

```bash
python3 -m unittest discover -s tests -v
python3 scripts/run_anchor_reproduction.py --list
python3 scripts/run_anchor_reproduction.py --dry-run
```

The seven anchor bundles are frozen in
[`data/anchor-battery-v1.json`](data/anchor-battery-v1.json).  They
cover the two Engine-A calibrations, four Engine-B packets, and the
Engine-C primitive packet.

## Claim tags

- `VERIFIED`: exact or replay-certified statement.
- `ENCLOSED`: rigorous Arb enclosure.
- `NUMERICAL`: exploratory or cross-check output only.
- `CONJECTURAL`: explicitly conjectural census analysis.
