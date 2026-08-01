# Agent instructions: maph

This is the repository-wide instruction file. Root `CLAUDE.md` and
`GEMINI.md` point here; edit only this file. Projects live independently
under `projects/*/` and may add a narrower `AGENTS.md`.

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
the nearest `AGENTS.md`, before acting. Detailed chronological memory lives
in a sibling `RESEARCH_LOG.md`; consult the relevant entries when a task
depends on prior cycles, corrections, or artifact identities.

`PLAN.md` must contain:

- original objective, claim boundary, status, and stop condition;
- a high-level research-path graph and current gate states;
- short headline theorem, breakthrough, correction, and no-go summaries;
- open questions, next authorized action, and crash recovery commands.

Keep `PLAN.md` short enough to reread routinely. Do not store per-cycle row
registries, long correction narratives, exhaustive hashes, test transcripts,
or detailed replay histories there.

`RESEARCH_LOG.md` is append-oriented and must contain:

- one concise finding-and-evidence summary per cycle;
- failed, deferred, superseded, and corrected paths without erasure;
- exact artifact identities/hashes, replay commands, resource observations,
  and detailed gate evidence when material;
- links back to the high-level path or gate affected in `PLAN.md`.

Before work: re-read frozen counts and conventions from artifacts, check
`git status` and recent/fetched history, and preserve unrelated changes.
Update `PLAN.md` only when strategy, status, a headline result, an open
question, or the next authorized action changes. Append cycle-level findings
to `RESEARCH_LOG.md`. Never erase a failed path from the research log.

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
- Every cycle/block entry in `RESEARCH_LOG.md` leads with outcomes and explicitly surfaces
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
