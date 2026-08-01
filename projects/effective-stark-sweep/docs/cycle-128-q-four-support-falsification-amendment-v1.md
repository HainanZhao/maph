# Cycle 128 — four-support falsification amendment v1

## Timing and correction record

This amendment was frozen after the enriched frozen-range export
revealed that none of its 57 four-support rows is all-zero, and before
the expanded-range search was run. The pattern is therefore
`EXPLORATORY_POST_RESULT`.

The amendment was initially appended to the original Cycle-128
preregistration file. The first proof audit correctly rejected that
mutation because it invalidated the source hash frozen by the earlier
feature export. The original preregistration has been restored; this
successor amendment preserves the expanded-search rule separately.
The initial discovery search artifact is preserved as v1 but is
superseded for provenance by a clean v2 replay against this file. No
mathematical output from v1 is promoted.

## Frozen search

Before any attempt to state four-support nondegeneracy generally, run
a lexicographically ordered counterexample search over squarefree
radicands (2\le D\le500) and finite-ideal norms
(101\le N\le300), using the same finite-ideal conjugacy
canonicalization and pinned-place ray conventions. Stop at the first
exact four-support row for which every supported character has a
deleted prime of primitive-character value (+1), or at 20 minutes
wall time / 2 GiB resident memory.

The first surviving counterexample refutes the universal four-support
nondegeneracy claim and is the headline outcome. Failure to find one
is only a bounded negative over the actually completed prefix; it is
never a theorem. The search has no RNG and may not skip a failed row.

## Required successor records

- `discovery/q-euler-pattern-analysis-v2.json` must supersede the v1
  analysis after validating the restored original preregistration.
- `discovery/q-four-support-counterexample-search-v2.json` must rerun
  the complete search against this amendment.
- The theorem audit must reject v1 as proof input and use only the two
  v2 successor records.
