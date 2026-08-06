# C100 source and gate screen: the 33-point Erdős–Szekeres case

This is a discovery and selection packet, not an attack preregistration. It
authorizes no solver run.

## Eligibility and source status

`OBSERVED`: Dumitru, *Notes on the 33-point Erdős–Szekeres problem*,
arXiv:2512.24061v1 (30 December 2025), states that the first unresolved
planar case is whether every 33-point general-position set contains a convex
7-gon, equivalently whether `ES(7)=33`. A current search found no later
primary-source resolution. The official OpenAI search found only an unrelated
Ramsey-number paper mentioning the classical Erdős–Szekeres bound, not a
resolution of the planar `ES(7)` case.

## Source-defined exact interface

The source supplies a finite Boolean state:

* one orientation variable for each of the `C(33,3)=5456` triples;
* realizable 4-point orientation selectors;
* reduced CC-style 5-point clauses;
* exact 4-set convexity criterion: a set is convex iff every 4-subset is
  convex;
* one no-convex-7-set clause for each of the `C(33,7)=4,272,048` 7-sets;
* convex-layer templates and a finite anchoring/sub-cubing parameter.

The source reports UNSAT certificates for several anchored subfamilies and
publishes the generator/replay repository. This is a source-cleared exact
verifier: an UNSAT certificate for a sound relaxation is a valid obstruction;
a SAT assignment is only a candidate until full realizability is certified.
The reduced CC clause set is explicitly a relaxation, so it must not be
described as a complete proof of `ES(7)=33`.

## Candidate gate

Candidate state: one frozen convex-layer composition and its finite anchor
subcube, with the published orientation-SAT encoding regenerated from pinned
code. Exact verifier: deterministic CNF hash, solver proof certificate, and
independent proof checking. Falsifier: a checked SAT model that survives a
complete chirotope/realizability audit, or a soundness defect in the claimed
UNSAT reduction. A no-hit/timeout is only a resource result. Stop/pivot:
close only the frozen anchored family; select a complete layer-family cover
only after a source-backed completeness proof and aggregate resource cap.

The first gate should use a short published configuration, not the paper's
multi-week hard instances. No execution is authorized before preregistration,
proof-checker pinning, disk measurement, and Oracle selection.

## Alternatives and adversarial comparison

* **Spectral join comparison:** Liu--Ning, arXiv:2605.05048, records an open
  classification of pairs `(G1,G2)` for which joining `K1` preserves a spectral
  comparison, but gives no finite canonical family or exact first gate.
* **C99 Diophantine engines:** the square-preserving tangent, elliptic
  multisection, and cubic norm-form designs remain uninstantiated; reopening
  them would violate the C99 boundary.
* **C96 deferred portfolio:** Kakeya, finite-cyclic Fuglede, Nivat `|F|=6`,
  all-rank LR, and book-Ramsey/Steiner/Hadamard still lack a comparable
  source-cleared finite interface in the current exclusion map.

Strongest flaw in selecting `ES(7)`: an anchored UNSAT result may close only a
small geometric subfamily while consuming substantial CPU, and the reduced
order-type encoding is not complete for SAT outcomes. Its advantage is that
the state, exact verifier, falsifier, and finite method family are already
published, so a carefully bounded gate can produce a durable method boundary
without pretending to solve the global conjecture.

Sources: <https://arxiv.org/abs/2512.24061>,
<https://arxiv.org/abs/2605.05048>.

## First execution tranche (`OBSERVED` CAP)

The frozen CNF was generated with the declared counts and hash
`5f5eccbf03707c6ab4ae821a7df441260a1e75d27674520aff69da0f38c91b23`.
The disposable `n=17,k=6` control passed twice: default and
`--plain --elim=false --probe=false` CaDiCaL runs both returned UNSAT, and
independent `drat-trim` returned `s VERIFIED` in each case.

The canonical default CaDiCaL run was then OOM-killed by the host at roughly
15.35 GiB RSS while writing a 12.15-GB partial DRAT file. It produced no
terminal status, timing footer, or checkable proof. Kernel logs identify the
OOM killer; this is `OBSERVED` resource failure, not evidence about `ES(7)` or
the anchored CNF. The partial proof and CNF are preserved. The live
preregistration was amended only to authorize the disposable lower-memory
benchmark; no canonical retry is yet authorized.
