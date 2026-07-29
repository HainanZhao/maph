# Artifact-emphasis amendment

Timestamp: 2026-07-29T08:15:52Z

Status: interpretive amendment; no production parameter changed

## Decision

The engine is the project's primary artifact.  The main data artifact
is a curated, structurally diverse oracle/conformance set containing a
few hundred exact entries.  The complete 79,200-entry fidelity grid is
supplementary archival data.

This amendment changes neither the authorized Cycles 016–018 compute
nor any frozen kernel, source, grid, threshold, hash, evaluation order,
overflow predicate, or replay gate.  The exhaustive run continues
because:

- its 1.58-node-day pilot projection was already accepted;
- the additional coverage has archival value; and
- the C2 unit-lattice comparison needs certified CBC-side anchors for
  a certified-versus-certified benchmark.

## Corrected motivation

The weak reading of the source audit was that production vector sites
publish no merit tables.  That absence is rational: the vector is the
reusable object, while the numerical merit depends on convention,
weights, normalization, and evaluator.

The stronger, supportable finding is one layer lower.  Across the
named, hash-frozen LatNet Builder and QMCPy revisions and the frozen
public-distribution perimeter, the audit found no independently
replayable exact or enclosed evaluation path.  A merit produced within
that frozen toolchain cannot be falsified from its supplied artifacts
alone.  This is a bounded claim about the audited toolchain, not a
universal negative about all QMC software or unpublished historical
code.

The methods paper therefore leads with:

1. the exact evaluator and its normalization discipline;
2. the independent verifier and replay contract;
3. the preregistered conformance/oracle suite; and
4. the exhaustive grid as supplementary reference data.

## Oracle-set role

The oracle set is selected from structure, never from observed merit
values.  It covers:

- the full tractable prefix range needed for embedded-construction
  regression;
- low, intermediate, and maximal values on the frozen \(N\) and \(d\)
  axes;
- all three frozen product-weight profiles;
- source-family variation; and
- adversarial comparison cases: sign symmetry, exact ties, zero and
  tiny weights, and large rational denominators.

It is a software-conformance suite, not a representative sample of
lattice quality and not evidence about a merit-value distribution.

## Methods-paper meta-lesson

The original selling point inferred a substantive gap from an absence
before asking whether the absence was rational.  It was.  Applying the
project's own claim discipline relocated the contribution from
“publish the missing numbers” to “supply the independently replayable
path by which any such number can be challenged.”  The correction is
part of the method: interrogate the reason for missing evidence before
turning its absence into a novelty claim.
