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

## Master plan

The authoritative current roadmap, dependency map, paper status, and
research queue are maintained in [`PLAN.md`](PLAN.md). Historical
cycle notes are evidence and process history; they do not supersede
the master plan.

## Current state

The proxy-free routing census v5 covers all 8,200 frozen
representatives. Its current occurrence counts are 3,899 exact
trivial identities, 1,560 Engine-A eligible rows, 232 Engine-B
eligible rows, 881 Engine-C eligible rows, and 1,628 named
frontiers. Eligibility is a routing statement, not a case-level packet
theorem.

The current selected-results manuscript is
[`paper/effective-stark-results.tex`](paper/effective-stark-results.tex).
It contains the uniform Engine-A theorem, eight selected Engine-B
packets, five selected cyclic-quartic CM packets, and two structural
lemmas. The paper, supplement, and companion archive are public at
[Zenodo DOI 10.5281/zenodo.21703306](https://doi.org/10.5281/zenodo.21703306);
the top-level PDF and TeX files are directly previewable there.

The census paper has a substantial Markdown draft at
[`paper/effective-stark-sweep-draft.md`](paper/effective-stark-sweep-draft.md).
Its final W4 analysis remains gated on the v5 Engine-B
occurrence-transport ledger.

Compact verification of the selected-results surface is:

```bash
python3 scripts/verify_results_companion.py all
python3 scripts/audit_results_paper_full.py
python3 -m unittest discover -s tests -v
```

## Claim tags

- `VERIFIED`: exact or replay-certified statement.
- `ENCLOSED`: rigorous Arb enclosure.
- `NUMERICAL`: exploratory or cross-check output only.
- `CONJECTURAL`: explicitly conjectural census analysis.
