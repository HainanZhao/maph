# Agent instructions: maph

This is the repository-wide instruction file. Root `CLAUDE.md` points here;
edit only this file. Projects live independently under `projects/*/` and may
add a narrower `AGENTS.md`.

The author's name is **Hainan Zhao**. Use that full name in manuscripts,
archives, and publication metadata; do not abbreviate it to a username.

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

`GOAL.md` is user-owned. Never create, edit, rename, or delete it without an
explicit user instruction for that specific change.

An instruction to **finish**, **complete**, or **follow** `GOAL.md` is a
terminal research directive, not a document-editing task. It means carry out
and resolve every in-scope research topic according to the completion criteria
written in `GOAL.md`. Reading or reorganizing the file, improving plans,
running bounded experiments, reaching a resource cap, proving a narrower
method boundary, or preparing partial results does not finish the goal. Do not
report `GOAL.md` complete or mark its goal achieved until every required topic
has its stated proof, verified counterexample, or other explicitly permitted
terminal outcome. This directive authorizes the research work described by
the file; it does not by itself authorize changing the user-owned file.

Keep `PROGRAM.md` short and strategic: current objective, claim boundary,
active gate, meaningful constraints, and the next action. Do not use it as a
progress log or duplicate replay evidence.

Preregistration is not required. Sealing is optional, not a per-cycle
requirement. Seal an immutable `artifacts/cycle-<n>-b<ordinal>-<slug>-v<version>.json`
only when the result must be relied on later: a proof-grade finding, a
later-relevant falsifier, a correction, an irreversible gate or strategy
change, or an external handoff/publication. Otherwise keep the work live in
`discovery/`; no artifact, status update, or
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

Projects may use a local index or the shared research tools for artifact
search and validation. The immutable artifacts and their replay commands are
canonical; a database, status file, or research log is never required.

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
question or frozen method family genuinely changes. State one decision question
with a real advance condition, then pursue all closely dependent derivations,
counterexamples, alternative formulations, and exact checks needed to answer
it. Reuse the live cycle for that related work; do
not create a cycle merely to name an intermediate decomposition,
factorization, failed subtest, or bookkeeping repair.

Before a genuinely new engine, consider at least one materially different
mechanism and state what would falsify the chosen one. Do this in scratch; do
not create a planning record unless it materially aids a later decision.

Open a new cycle only when a material decision selects a genuinely different
research question or frozen method family, or when an external result or
irreversible gate/status decision changes the research question. A larger
resource tranche, faster implementation, storage-layout change, scheduling or
parallelism change, deterministic replay, additional validation, failed cap,
or bookkeeping correction remains in the same cycle while the engine and
decision question are unchanged. Update the live decision note when useful
before the new execution and retain the earlier tranche as a contained result. If a
resource continuation follows a premature seal, issue a same-cycle correction
instead of minting a successor cycle. Never evade the cadence by renaming
routine continuation as a new method family.

Keep scratch in `discovery/` and promote only the conclusion. Replay and commit
only when useful; do not seal, regenerate status, or write a handover after
each subtest. Corrections are only for genuine post-seal defects.

### No autonomous project or problem switching

Agents must not autonomously search for, screen, select, reselect, pivot to,
or switch projects or problems. Only an explicit user instruction may
authorize portfolio discovery, problem selection, or a project switch. A
bounded method-family result is never authorization to close the broader
problem or begin another one.

Problem selection is exclusively human. Within that human-authorized problem,
the primary agent selects and executes every research cycle. Before a material
new cycle, the primary independently reads the current `PROGRAM.md` and the
relevant recent records, performs **question → question the questioning →
brainstorm**, and records an exclusion map: former question, outcome/falsifier,
and the exact state, invariant, or claim-boundary delta. The selected cycle
must name an input state, invariant/map/transition, smallest direct verifier,
resource-bounded stop criterion, and falsifier. Do not substitute a finite
census for an unspecified design question.

### Missing-bridge research rule

An absent theorem, constructor, or interface is not by itself a terminal
answer. Before claiming saturation, identify the missing bridge and decide
whether a genuinely new invariant, lift, duality, completion, inverse theorem,
or countermodel has enough expected information to justify work. Existing
artifacts constrain future claims; they do not prohibit invention.

## 2. Discovery and proof are separate

- Use `discovery/` for heuristics, floats, recognition, conjectural
  solvers, pattern searches, and AI-proposed identities.
- Use `proof/` for exact arithmetic, certified enclosures, and pinned
  proof pipelines. Legacy projects must maintain an explicit equivalent
  separation until migrated.
- Discovery may select a candidate; it never closes an identity.
  Closure requires exact algebra or a rigorous enclosure satisfying an
  explicit criterion with margin.
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

## 4. Corrections and declared controls

- Never silently edit a certified record. Issue a versioned correction
  artifact stating the error, cause, affected claims, and reruns.
- A convention change requires regeneration or explicit re-audit of
  every downstream certificate.
- Before relying on a result, record the actual ranges, thresholds, margins,
  samples, RNG seeds, degree/resource caps, formula families, and rule for
  failed rows in its replay or artifact. Post-result choices are
  `EXPLORATORY` unless independently justified.
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
- a declared audit fails;
- a candidate counterexample survives initial rigorous checks;
- documents assign incompatible conventions/claims to one certificate;
- a novelty claim depends on an unread reachable paper;
- a resource cap would force an undeclared method substitution;
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
- Treat runtime as the scarce resource in compute-heavy research. Before a
  long run, optimize the hot path, compile with appropriate production
  optimizations, and benchmark a representative exact control. Do not spend
  hours on an avoidably slow implementation merely because code changes are
  cheap.
- Parallelize only when it materially shortens an independent, deterministic
  computation. Keep one CPU free and apply resource limits in aggregate.
- Before a disk-heavy run, check available space and leave a practical system
  reserve.
- Record wall time and peak memory for principal replays.
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
