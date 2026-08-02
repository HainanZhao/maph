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

Every active research project has a root `PLAN.md`; it is the concise,
authoritative strategic state over chat memory. Read it completely, then
the nearest `AGENTS.md`, before acting. Detailed cycle memory lives in
committed, individually named cycle records; consult the relevant artifact
and linked documents when a task depends on prior cycles, corrections, or
artifact identities.

`PLAN.md` must contain:

- original objective, claim boundary, status, and stop condition;
- a high-level research-path graph and current gate states;
- short headline theorem, breakthrough, correction, and no-go summaries;
- open questions, next authorized action, and crash recovery commands.

Keep `PLAN.md` short enough to reread routinely. Do not store per-cycle row
registries, long correction narratives, exhaustive hashes, test transcripts,
or detailed replay histories there.

Each sealed cycle must instead have a committed, immutable record:

- `artifacts/cycle-<n>-<slug>-v<version>.json` is the canonical
  machine-readable finding, claim boundary, tags, frozen hashes, replay, and
  gate outcome;
- `docs/cycle-<n>-<slug>-v<version>.md` and its preregistration document are
  the readable derivation and decision record;
- failed, deferred, superseded, and corrected paths remain as records; a
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

`STATUS.md` is the cold-start operational handoff, not merely an index
summary. A code-start agent must be able to begin the next authorized cycle
without reading a historical aggregate log. Its generated profile content
must state, with epistemic tags: the present project-level outcome and claim
boundary; why the active gate is now the bottleneck; the exact criterion that
would advance it (including disallowed pseudo-progress); explicitly deferred
work; and the ordered first commands/record to inspect. Keep this compact and
link to canonical records rather than duplicating their derivations. Update
the profile and regenerate `STATUS.md` whenever any of those handoff facts
change.

Before work: re-read frozen counts and conventions from artifacts, check
`git status` and recent/fetched history, and preserve unrelated changes.
Update `PLAN.md` only when strategy, status, a headline result, an open
question, or the next authorized action changes. Seal cycle-level findings in
their individual record and regenerate the compact status view. Never erase a
failed path from the cycle record set.

### Research-block cadence

A research cycle is a substantive block, not a single algebraic observation.
Preregister one question with a real advance condition, then pursue all
closely dependent derivations, counterexamples, and exact checks needed to
answer it before sealing. A normal cycle should contain multiple lemmas or a
genuine bound-or-obstruction decision; do not create a new cycle merely to
name an intermediate decomposition, factorization, or bookkeeping repair.

Keep intermediate work in a short `discovery/` or readable working-decision
ledger, tagged `CONJECTURED`/`OBSERVED` as appropriate. Promote it only with
the enclosing cycle's immutable record. Run replay, profile/status rebuild,
and commit once per completed research block—not after each lemma. An early
seal is justified only by a correction, falsifier, externally useful result,
or an irreversible strategy/gate decision. Batch routine checks locally.

### One live document set per cycle

While a cycle is in progress, keep exactly one canonical preregistration and
one compact working-decision ledger for that cycle. Amend the canonical files
in place under a short dated/amendment log; do not create `v2`, `v3`, or other
same-cycle addendum documents merely because an engine, formula, or gate
evolves. Git history preserves intermediate states. Create a new correction
or versioned document only after a cycle has sealed, or when an immutable
certificate actually needs correction. The working ledger records rejected
routes and compact reasons, not full derivational scratch.

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

## 1a. Critical-decision companion

Every research session in this repository starts one companion at the same
time as the primary worker, before exploration begins. The companion belongs
to the session, not to a cycle, branch, or individual decision: it remains
the mentor/checkpoint tracker across every cycle and project decision made in
that session. Use a more capable available model for this companion when the
platform permits. Otherwise use an independent agent with a fresh brief and
no responsibility for the primary derivation.

The companion is a mentor/checkpoint tracker, not a duplicate implementer or
a hostile auditor. It maintains a short decision ledger: the frozen premise,
alternatives considered, decisive evidence and tags, the recommended next
action, and any unexamined assumption. It operates asynchronously by default:
start it and send one compact session brief without waiting, then batch
material deltas into one checkpoint packet. Routine deltas are notification
only and request no reply. A decision packet is normally under 150 words (and
never over 250) and uses one fixed interface: decision sought; frozen
claim/gate and tag; at most three decisive evidence or change bullets; known
flaw; and requested disposition. Link a changed excerpt, artifact, or hash
instead of asking for a project reread. Ask for exactly four short items in
reply: recommendation, flaw, falsifier, and next action. The companion must
not re-derive the live work or inspect unrelated files unless that packet asks
it to. Do not poll or wait during reversible derivations, candidate engines,
routine computations, or amendments within an already active cycle; notify
the companion and continue.

Blocking consultation is reserved for an irreversible or strategic decision:
changing the strategic status, claim boundary, gate, or advance condition in
`PLAN.md`; starting or abandoning a path not already authorized by the plan;
sealing/committing a material claim; promoting/containing a material theorem;
or external publication. A routine cycle start already authorized by the
current plan is notify-only, not a blocking checkpoint. Use one fast
checkpoint flow for every blocking decision:

1. Send one batched packet to the stable identity as soon as the decision is
   foreseeable, then continue all reversible work.
2. At the actual decision point, consume its concise reply. Do not first
   inspect status, run a liveness rehearsal, or solicit an acknowledgement.
3. If no reply is available, reactivate that *same* identity once with the
   unchanged packet and a short response request. Continue reversible work
   while it responds. If it still fails, defer only that critical decision;
   record the timeout and do not substitute a new, unbriefed companion.

Do not iterate after a reply unless its stated falsifier or flaw is triggered.
Record only the final recommendation and adopt/reject reason in the relevant
decision record. The primary keeps the companion task identity and latest
compact packet there. A completed companion is an idle mentor, not a failure:
`followup_task` reactivates that stable identity when its next packet is ready.
This protocol complements the paper-stage hostile audit; it does not start
one early.

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
- Record wall time and peak memory for principal replays.
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
