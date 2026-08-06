# Agent instructions: maph

This is the repository-wide instruction file. Root `CLAUDE.md` points here;
edit only this file. Projects live independently under `projects/*/` and may
add a narrower `AGENTS.md`.

## 0. Epistemic ground rules

- Distrust the first answer, including the first trust assessment.
  Favorable or surprising results increase scrutiny.
- Tag every material research claim:
  - `PROVED`: follows from a published theorem whose hypotheses were
    checked exactly in this run;
  - `CERTIFIED_NUMERICAL`: rigorous enclosure, with radius and margin;
  - `RECOGNIZED`: floating-point/lattice identification, never proof;
  - `OBSERVED`: reproducible empirical pattern;
  - `CONJECTURED`: unproved mathematical claim.
  Unlabeled claims are bugs.
- `UNCONDITIONAL` means only: every identity follows from a proved
  theorem under exactly checked hypotheses. It never means “confident.”
- Prefer falsification: state what would refute the working claim and
  treat a surviving counterexample as a headline result.

## 1. Project memory and workflow

Every active research project has a root `PROGRAM.md`; it is the concise,
authoritative strategic state over chat memory. Read the current gate and the
one relevant prior artifact before acting. Do not reread historical material
unless the next question depends on it.

`PROGRAM.md` must contain:

- original objective, claim boundary, status, and stop condition;
- a high-level research-path graph and current gate states;
- short headline theorem, breakthrough, correction, and no-go summaries;
- open questions, next authorized action, and crash recovery commands.

Keep `PROGRAM.md` short enough to reread routinely. Do not store per-cycle row
registries, long correction narratives, exhaustive hashes, test transcripts,
or detailed replay histories there.

Keep a preregistration with its embedded freeze manifest before executable
work that may support a durable claim. Sealing is optional, not a per-cycle
requirement. Seal an immutable `artifacts/cycle-<n>-b<ordinal>-<slug>-v<version>.json`
only when the result must be relied on later: a proof-grade finding, a
later-relevant falsifier, a correction, an irreversible gate or strategy
change, or an external handoff/publication. Otherwise keep the work live in
its one preregistration and `discovery/`; no artifact, status update, or
handover is needed.

Do not seal an intermediate resource-cap result while the same engine,
decision question, and method family are still being pursued with an
optimization or a larger authorized resource tranche. Keep that cycle live
and seal only the resulting strategic boundary. A premature seal remains
immutable and is superseded by a correction in the same cycle; it does not
justify consuming a new cycle.

The `b<ordinal>` filename segment is the campaign-budget ordinal and must
agree with the record payload; it makes budget use discoverable without a
separate live counter. Legacy sealed names remain unchanged.

When a result is sealed, its artifact contains the finding, claim boundary,
frozen hashes, replay, and gate outcome. Create a separate readable decision
document only for paper/publication work, a correction, or when the artifact
cannot state the decision clearly. Preserve a failed, deferred, superseded,
or corrected path only when it materially constrains a later decision; a
correction creates a new record and never mutates a sealed one.

Projects may maintain a local DuckDB index built from those records for
search, dependency queries, and generated status. The database binary is
ignored and never canonical; commit its schema, pinned dependency, rebuild
script, tests, and generated text status only. Do not create or append a
monolithic `RESEARCH_LOG.md`. An existing one is historical archive only.
Use `tools/research_records.py` with a project `research-records.json` profile
to build, validate, and query standard immutable cycle records. Use
`tools/duckdb_tools.py` for schema-agnostic read-only DuckDB inspection.
Once per shell, activate the repository tools from any directory in the
checkout:

```sh
source "$(git rev-parse --show-toplevel)/tools/dev-env.sh"
```

For routine use from inside a profiled project, use the short wrapper:

```sh
research rebuild
research check
research cycle 151
research search negative-tail
research db tables
research db sql "SELECT status, count(*) FROM artifacts GROUP BY status"
```

The wrapper finds `research-records.json`, uses the project `.venv` when
present, and dispatches `db` to the generic read-only DuckDB interface. If a
shell cannot be initialized, `../../tools/research` remains equivalent.
Project-specific code belongs only in its declarative profile or in a proven
new record type; do not create per-project index/query scripts for routine
cycle, claim, gate, dependency, or evidence queries.

`STATUS.md` is optional, generated only for an intentional handoff. It points
to `PROGRAM.md`, the newest artifact, and recovery commands; it never repeats
strategy or results. Do not regenerate it during ordinary research.

Before work: read only the frozen counts, conventions, and records needed for
the next authorized question; check `git status` and preserve unrelated
changes. Update `PROGRAM.md` only when a strategic boundary
changes strategy, gate, budget/tranche allocation, stop condition, or the
genuinely different next action. A counted cycle, sealed result, failed
subtest, routine checkpoint, or ordinary continuation of the same
research block does **not** by itself authorize a `PROGRAM.md` edit. Never use it
as a progress log. `PROGRAM.md` is a mutable strategic source and must never be
frozen as an artifact input: archive the specific mathematical premise or
prior artifact instead.

### Research-block cadence

A research cycle is a coherent decision block, not a single algebraic
observation, lemma, engine probe, validation run, or required artifact. Its
normal boundary is a material decision point: reuse the live cycle while the
same related question remains active, and open a new one only when the
question or frozen method family genuinely changes. Preregister one decision
question with a real advance condition, then pursue all closely dependent derivations,
counterexamples, alternative formulations, and exact checks needed to answer
it. Reuse the live cycle and its one preregistration for that related work; do
not create a cycle merely to name an intermediate decomposition,
factorization, failed subtest, or bookkeeping repair.

Before opening any new cycle, perform an explicit creative idea-selection pass
in scratch. Generate genuinely different mechanisms—not only variants of the
last tool—including new state spaces, invariants, dualities, inversions,
countermodels, and constructions. Formulate the decision question for each
serious candidate, then question the questioning itself: why this question,
why now, which assumption or inherited framing makes it misleading, what
important question the candidate prevents us from seeing, and what simpler or
more discriminating alternative was rejected. Distrust a familiar formulation
merely because it is easy to execute. Choose one idea only after that
adversarial comparison. Record the chosen question, the main rejected
alternative, and the falsifier in the preregistration; do not turn the scratch
brainstorm into a recurring report or a separate artifact.

Open a new cycle only when a material decision selects a genuinely different
research question or frozen method family, or when an external result or
irreversible gate/status decision changes the research question. A larger
resource tranche, faster implementation, storage-layout change, scheduling or
parallelism change, deterministic replay, additional validation, failed cap,
or bookkeeping correction remains in the same cycle while the engine and
decision question are unchanged. Amend the live preregistration before the
new execution and retain the earlier tranche as a contained result. If a
resource continuation follows a premature seal, issue a same-cycle correction
instead of minting a successor cycle. Never evade the cadence by renaming
routine continuation as a new method family.

Keep scratch in `discovery/` and promote only the conclusion. Replay and commit
only when useful; do not seal, regenerate status, or write a handover after
each subtest. Corrections are only for genuine post-seal defects.

### Closure postmortem

Whenever a problem is solved, refuted, closed for eligibility loss, saturated,
or otherwise stopped, run one lightweight **postmortem cycle** before selecting
the next problem. It is a non-budgeted closure decision block, not an attack
cycle and not a substitute for paper work. Record one concise entry in the
root POSTMORTEMS.md: problem/cycle, stop trigger and evidence, the assumption
or check that failed or succeeded, the reusable rule, and the concrete
next-screen change. Do not repeat the project strategy, reproduce logs, or
write a handover. The postmortem must change a future decision or be omitted;
its purpose is durable repository learning, not ceremony. This requirement
also applies when the whole project closes; no successor problem may be chosen
until its closure entry exists.

### Research delegation

Use subagents when two or more genuinely independent research tracks can run
in parallel with light compute and little shared state—for example literature
checks, proof derivations, or small code reviews. Skip delegation for a small
task. Do not delegate CPU-, memory-, disk-, or runtime-heavy work: subagents
share this machine, so centralize that work and obey the aggregate compute
caps below. The primary agent owns integration and epistemic labeling.

### Critical-decision companion (Oracle)

Name the companion **Oracle** in every program. Use Oracle only for problem
selection, a material fork or seal, a post-result cycle decision, or
publication. Oracle is a co-planner, not a yes/no approver: it and the primary
agent independently propose ideas, review evidence, challenge framing, and
compare falsifiers, cost, and expected information gain.

Invoke Oracle with `gpt-5.6-sol` and `high` reasoning effort or higher. Do
not downshift Oracle for convenience: its role is reserved for the decisions
where the best available conceptual review is worth the added deliberation.

Oracle's standing philosophy is **question → question the questioning →
brainstorm**. First question the inherited target, evidence, assumptions,
state space, success criterion, and reason it is being asked now. Next question
that critique itself: identify which familiarity, computability, prestige,
recent failure, or inherited vocabulary may be biasing what Oracle treats as
the problem, and name the important question the critique could still hide.
Only after those two adversarial passes may Oracle brainstorm. That brainstorm
must include genuinely different problems or mechanisms—not variants of the
incumbent—and then rank them by falsifier, exact or rigorous verifier, cost,
expected information gain, and credible path to closure. Oracle's packet must
briefly expose this reasoning, not merely output a choice.

For problem selection, the primary supplies its independent analysis; Oracle
selects and records alternatives, strongest flaw, falsifier, information gain,
and stop/pivot criterion. The primary executes the choice. At other forks,
Oracle advises and the primary decides. Use one concise evidence packet and do
not invoke, poll, or wait for Oracle during ordinary research.

### One live specification per cycle

Keep one preregistration while a cycle is live. Amend it in place; Git history
preserves intermediate states. Do not create ledgers, addenda, or same-cycle
versions unless needed for a correction or publication decision.

### Executable preregistration preflight

For every new cycle, the canonical preregistration must contain exactly one
embedded `research-freeze-v1` JSON manifest before executable discovery,
proof, test, or replay code is created or run. It is the machine-readable
freeze layer *inside that same preregistration*, not a second specification.
It declares typed parameters and resource caps (or explicitly justified
`not_applicable` entries), formula families, selection and failure rules,
the pre-execution UTC/Git boundary, and all frozen input paths. Run the shared
preflight first:

```sh
research prereg check docs/cycle-<n>-b<ordinal>-<slug>-preregistration-v1.md \
  --expected-cycle <n>
```

The builder freezes both the preregistration and validator hashes and records
the checked manifest hash. A manifest-head mismatch blocks initial execution;
only deterministic replay after a later commit may use `--allow-head-drift`.
Do not retrofit a sealed record: legacy pre-manifest cycles are explicitly
unprotected, not silently repaired. A prose rule, placeholder value,
post-result cap, or executable input that disagrees with the manifest fails
preflight and halts that unsealed branch until corrected.

### Missing-bridge research rule

An absent theorem, constructor, or interface is not a terminal research
answer. Treat it as a named design problem. Before promoting a scoped
interface cut or saturation barrier, attempt at least one genuinely new
engine: a new invariant, lift, duality, completion, local-to-global
principle, inverse theorem, or a discriminating countermodel. State what the
new engine would have to preserve and what evidence would falsify it. Existing
artifacts are constraints and launch points, not a ceiling on invention.
The purpose of exploration is not merely to recombine available theorems.
When the decisive bridge is absent, give the proposed construction equal
standing with any literature route: formulate its state space and invariant,
build the smallest falsifiable prototype, and seek a new proof mechanism
before declaring the program saturated. A negative result may constrain that
engine, but must not be recast as evidence that only existing building blocks
are legitimate.

## 2. Discovery and proof are separate

- Use `discovery/` for heuristics, floats, recognition, conjectural
  solvers, pattern searches, and AI-proposed identities.
- Use `proof/` for exact arithmetic, certified enclosures, and pinned
  proof pipelines. Legacy projects must maintain an explicit equivalent
  separation until migrated.
- Discovery may select a candidate; it never closes an identity.
  Closure requires exact algebra or a rigorous enclosure satisfying a
  preregistered criterion with explicit margin.
- Every proof-grade result must be version-pinned, hash-recorded,
  scripted, and one-command replayable. If it cannot be replayed, it
  does not exist.
- Regression tests must not invoke a mode that overwrites a sealed canonical
  artifact. Test deterministic payload construction in-process or direct a
  replay at a disposable target; use the immutable builder's `--check` mode
  for the canonical artifact.
- Reuse a project-local, versioned sealing scaffold for routine artifact
  mechanics: runtime checks, frozen-input hashes, prior-status validation,
  deterministic JSON rendering, and immutable `--write`/`--check` behavior.
  Cycle builders should contain only cycle-specific inputs, theorem checks,
  claim boundaries, and payload fields. Freeze the scaffold and its tests as
  artifact inputs. Never rewrite a scaffold used by an existing artifact;
  create the next version instead. Do not mechanically refactor already
  sealed builders, because their recorded hashes are part of the replay.

## 3. Conventions are code

- Pin every sign, orientation, normalization, ordering, transform
  direction, generator, embedding/place label, special-function
  convention, and host-system ordering once in a conventions module.
  Derive scripts and manuscript displays from it.
- Certified replay code is the source of truth. If a display disagrees,
  fix the manuscript and record the discrepancy—never patch proof code
  merely to match prose.
- Independently derive every phase/sign/label identity from the pinned
  conventions.
- Audit circularity: an “after aligning” step may inspect only the side
  frozen before the target was computed. Record the audit.

## 4. Corrections and preregistration

- Never silently edit a certified record. Issue a versioned correction
  artifact stating the error, cause, affected claims, and reruns.
- A convention change requires regeneration or explicit re-audit of
  every downstream certificate.
- Before computing, freeze: ranges, thresholds, margins, samples, RNG
  seeds, degree/resource caps, formula families, and the rule for failed
  rows. Post-result choices are `EXPLORATORY`.
- During research, a failed lightweight check contains the affected
  claim/table and is logged, but it does not automatically terminate a broader
  speculative branch. Never drop the row silently.
- Do not initiate hostile audits during research. Hostile audits begin only
  when concrete claims enter manuscript/paper-stage promotion. During
  discovery and theorem development, use lightweight source, algebra, replay,
  and consistency checks so bold ideas are not killed prematurely. Preserve
  contrary evidence for the later paper-stage audit.

## 5. Redundancy and coverage

- Promote results through two genuinely independent routes when the
  mechanism permits. Agreement must include labels, not only unlabeled
  invariants.
- Map every theorem case split to a certified anchor. Unexercised
  branches remain open actions.
- Reconcile every repeated count across papers, supplements, and README
  from one frozen dataset in a table built before writing.
- Running the same pipeline twice is replay, not independent
  verification.

## 6. Literature and novelty

- Read reachable primary papers—theorems and hypotheses, not abstracts—
  and check this program’s companion papers before claiming novelty.
- Record exact overlap, theorem numbers, applicable cases, and
  structural limits of prior methods. Concede overlap explicitly.
- First try to derive a proposed phenomenon from existing results.
  Reclassify automatic consequences as consistency checks.
- Scope priority claims to the reviewed evidence; never convert a
  bounded search into a universal negative.

## 7. Stop and escalate

The following findings do **not** automatically require stopping the
active goal or escalating to the user immediately. Record and contain
the affected claim, preserve the evidence, withhold invalid promotion,
and continue safe independent work toward the user's request. Highlight
the issue clearly once the current request, ask, or goal has been
cleared:

- an independent route disagrees with a certified record;
- a preregistered audit fails;
- a candidate counterexample survives initial rigorous checks;
- documents assign incompatible conventions/claims to one certificate;
- a novelty claim depends on an unread reachable paper;
- a resource cap would force an unregistered method substitution;
- a surprising favorable result has not completed heightened checks.

Use judgment to decide whether the evidence warrants stopping the
affected branch, opening a separate branch, or formulating a new
thesis. Surface the issue earlier only when continuing would corrupt
evidence, create an irreversible or unauthorized change, compromise
safety, or make meaningful progress on the user's goal impossible.
Never conceal, erase, or silently work around a listed finding.

## 8. Writing and reporting

- Put the claim boundary first and state what is not proved precisely.
- Support every theorem row in text with route, candidate, and labels;
  corpus IDs alone are insufficient.
- Label non-proof cross-checks as quarantined and explain why.
- Verify bibliography metadata and cite theorem/page numbers. Uncited
  entries and dangling references are bugs.
- Every cycle record leads with outcomes and explicitly surfaces
  newly banked major theorems, breakthroughs, corrections, containment
  events, and structural no-go results. State tags, gate changes, and
  implications.
- Cold outreach: lead with the recipient’s problem, include one result
  about their work, ask at most three falsifiable questions, disclose AI
  assistance, and attach the replay archive.
- Agents never send email, Slack, direct messages, or any other
  outbound communication. Agents may prepare and verify drafts,
  recipients, attachments, and handoff instructions; a human performs
  every send action.

## 9. Session and compute hygiene

- Re-read a file immediately before editing it.
- Timebox exploration and preserve negative results as artifacts.
- Treat runtime as the scarce resource in compute-heavy research. Before a
  long run, optimize the hot path, compile with appropriate production
  optimizations, and benchmark a representative exact control. Do not spend
  hours on an avoidably slow implementation merely because code changes are
  cheap.
- Parallelize independent deterministic search work by default. On a shared
  machine with `N` available CPUs, use at most `N-1` CPUs unless the user says
  otherwise, leaving one CPU for the system and other work. Prefer balanced
  or dynamic sharding, verify that shard union equals the unsharded search on
  a small exact control, and enforce preregistered time, node, leaf, and memory
  caps in aggregate rather than once per worker.
- For future authorized disk-heavy runs, measure free space immediately before
  preregistration and set the aggregate temporary-disk cap to at most that
  free space minus 5 GiB, reserving the 5 GiB for the system and other work.
  Log the byte-level measurement and cap, recheck free space at launch, and
  stop naturally if concurrent use erodes the reserve. Do not reinterpret
  total filesystem capacity as available space or alter an already-running
  process merely because this default was added later.
- Record wall time and peak memory for principal replays.
- **Persistent-goal continuation guard:** a continuation turn must take one
  concrete, state-advancing action (for example inspect evidence, run a
  replay, edit a preregistration, obtain a companion decision, or commit a
  verified result). Never end such a turn with a status-only final such as
  "continuing" or "still active": that can retrigger the same goal without
  progress. If no safe concrete action remains, perform the ordinary blocked
  audit and mark the goal blocked only when its threshold is met; otherwise
  wait silently for an actual user or external-state event. Treat repeated
  identical continuation notices as an orchestration defect, not research
  progress, and stop emitting them.
- Treat a transient slow-server, spinner, or dismissible wait notice as
  already dismissed: continue safe local work or wait/retry silently. Surface
  it only after it has become a real blocker under the ordinary escalation
  rules, not merely because the interface is slow.
- Never ask the user to respond to, approve, or interpret the notice “Our
  systems are thinking a bit more about this request before responding.” It is
  a transient wait state: wait or continue safe work silently, retry when
  appropriate, and surface it only if it becomes a genuine blocker.
- Pin tool/library versions. Different PARI versions may emit different
  but equivalent generators; prove equivalence before changing expected
  outputs. Use the pinned Linux/container pipeline when exact byte-level
  reproduction matters.
- Check for concurrent commits before release:
  `git fetch && git log HEAD..origin/main --oneline`.

## 10. Publishing and Zenodo

- Use `ZENODO_TOKEN` only in an `Authorization: Bearer` header; never
  expose it in URLs, output, or files.
- Reserve the DOI first, insert it into paper/source metadata, compile
  twice, and verify rendered text.
- Build deterministic archives twice and compare bytes. Test the
  extracted archive, not only the live tree.
- Upload metadata, archive, then standalone PDF and source at the
  deposit root so the main paper previews directly. Verify local and
  remote checksums.
- Zenodo's visible file/preview order may follow lexical filename
  sorting. Name the main-paper upload so it sorts before every
  supplement, addendum, archive, and other previewable file; record and
  verify the ordered remote inventory and the public default preview.
- Merge an addendum into the main manuscript in the next version when
  it belongs to that paper. Do not leave a competing standalone
  addendum PDF at the deposit root if it can displace the main-paper
  preview; preserve the historical addendum inside the versioned
  archive instead.
- The preceding Zenodo ordering and addendum-integration rules are
  persistent repository knowledge. Never delete or weaken them without
  the user's explicit instruction.
- A timeout may hide a successful write; inspect deposition state before
  retrying mutations.
- Publishing is irreversible, but the user has granted standing
  authorization for agents to publish repository releases to Zenodo
  without a separate per-release approval. Before publishing, complete
  every DOI, deterministic-build, extracted-replay, metadata,
  inventory, checksum, and preview gate; after publishing, report the
  exact public files, metadata, and verified checksums.
- This standing Zenodo authorization is persistent repository
  knowledge. Never delete or narrow it without the user's explicit
  instruction.
- After publication, changes require a new Zenodo version.
- No manuscript circulates as final before its proof archive has an
  immutable DOI.
