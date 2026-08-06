# PROGRAM: Open Conjecture Sweep

## Objective, boundary, and status

- **Objective:** test a tractability-ordered portfolio of open mathematical
  conjectures that have not been officially announced as solved by OpenAI,
  seeking either a complete proof/counterexample or a publishable scoped
  theorem, reduction, obstruction, or certified finite result.
- **Status:** `C001_STOPPED / D001_CLOSED / E001_SELECTED` (legacy cycle `C100`). Earlier closed
  problems, eligibility corrections, and method boundaries are preserved in
  cycle artifacts and the current-gate ledger below. C001's ES(7) anchor
  stopped at its invalid n=25 control criterion. D001's book-Ramsey
  character-sign gate closed at its exact q=7 falsifier. Oracle independently
  selected E001's bounded Hadamard-668 quartic-character completion gate.
- **Claim boundary:** all solve probabilities and tractability rankings below
  are `CONJECTURED` planning estimates. A bounded source search is not proof
  that a problem is open or untouched by OpenAI; eligibility must be checked
  from current primary literature and official OpenAI sources at the start of
  each problem.
- **Project cap:** 400 research cycles across five problems. A cycle is a
  coherent research block under the repository-wide cadence, not a report or
  a single computation.
- **Stop condition:** finish when all five problems have reached their stop
  gates or the 400-cycle pool is exhausted. Stop a problem immediately on a
  complete result, a decisive falsifier, a demonstrated loss of eligibility,
  or a reasoned saturation decision. At project end, seal only results that
  must be relied on and create one handoff if needed.
- **Paper trigger:** a complete proof, certified counterexample, or
  proof-grade scoped theorem/reduction that materially advances its target
  enters a dedicated paper phase. The paper phase turns the result into a
  manuscript and replay archive, performs the required literature and
  hostile-audit work, and either publishes or records why it does not clear
  that bar. Paper work is outside the 400-cycle research budget: it is a
  consequence of a result, never a way to spend research cycles on reporting.
  For Problem 1 specifically, Cycle 49 met its clarity gate by isolating one
  falsifiable deletion-aware packet theorem. Cycle 50 falsified it at the
  inherited pair-fiber stage. LRC(13) is paused with one concise handoff; 30
  unused cycles are banked for Problem 2. Do not add exception patches or
  another local face census without a new project decision.

## Problem-track identifiers

Use a problem prefix plus a three-digit within-problem sequence only for
credit-consuming research state: `A001`, `B001`, `C001`, and so on. The
current ES(7) problem is **C001**; its live legacy preregistration remains
`C100` and must not be renamed. Continue this problem as `C002`, `C003`, …
only for genuinely new research cycles in the same problem. Do not retrofit
the older record registry or artifact filenames.

Every new non-credit selection, source/eligibility screen, postmortem, or
other strategic decision uses a separate global underscore sequence:
`_001`, `_002`, … . These records do not allocate a problem prefix, consume a
cycle credit, or restart a problem's numeric sequence. `_001` and `_002` are
historical non-credit screens; they do not defer the next selection. The next
genuinely selected problem starts **D001**.
Thereafter, a material problem selection advances the letter and restarts at
`001`; a routine continuation, method optimization, or correction retains the
current problem prefix. New program summaries
should lead with the appropriate prefix and give the legacy cycle in
parentheses when one exists, for example `C001 (C100)`.

## Automatic portfolio loop and budget

The program runs itself as a repeating **discovery → Oracle selection →
attack → review/pivot** loop. A non-budgeted **postmortem phase** follows every
closed problem, and a non-budgeted **paper phase** follows a result that meets
the paper trigger. **Oracle** is the named companion for this
program. Problem selection is a critical decision owned by Oracle: it
independently screens the eligible candidates, proposes and ranks targets,
challenges the inherited framing, and selects the next target from a concise
evidence packet. The primary does not pre-propose candidates for ratification;
it executes Oracle's selected attack without waiting for user approval. The
companion is not used for ordinary attack work.

Each selected problem has an 80-cycle envelope, with an automatic strategic
review at 50 cycles since its selection. The 50-cycle review is a *discovery
cycle*: re-check eligibility and literature, generate and compare genuinely
different candidate targets and engines, then select the highest expected
information-gain attack. Continue the present target past 50 only when a
proved high-leverage reduction, a credible closing mechanism, or materially
improved evidence makes it better than the best newly screened alternative.
Otherwise defer it, bank its unused capacity, and immediately select the next
target.

Open an earlier discovery cycle only on a genuine boundary: a proof or
counterexample, loss of eligibility, a durable no-go that removes the viable
route, or a material review showing that the completion chance is low and a
new candidate dominates it. A failed lemma, a resource optimization, a single
negative sample, or ordinary continuation is *not* a pivot trigger; keep the
same research cycle and target while its question and method family remain
coherent. This prevents both rabbit holes and artificial micro-cycles.

### Rolling pivot guard (C100 correction)

The last-100-cycle audit found 16 material target/engine pivots
(`discovery/cycle100_pivot_audit.md`).  This exceeds the program's tolerated
three-pivot rate and activates a stability lock.  For every rolling window of
100 cycles, at most three material pivots are allowed.  A fourth proposed pivot
is rejected unless it is forced by a proved result or counterexample, an
external eligibility loss, or an irreversible status gate.  Minor blocks—one
failed lemma, a bounded negative subtest, an OOM/time/disk cap, a bookkeeping
repair, or a method optimization—must stay in the live cycle and be handled by
an amended preregistration or a genuinely different continuation inside the
same target.

Before any non-exempt pivot, the primary must first document (i) the current
preregistered stop condition, (ii) one continuation attempt that addresses the
block without changing the target, and (iii) an artifact-cited Oracle packet
comparing continuation against the proposed target, including a falsifier and
expected information gain.  After the guard trips, keep the incumbent target
for a ten-cycle stability block; no portfolio reselection is permitted during
that block except for the four exemptions above.  The guard is a cadence rule,
not a new research cycle, and does not authorize retroactive edits to sealed
records.

The discovery cycle must contain a wide primary-source/official-status screen,
creative candidate generation, an adversarial comparison of assumptions and
falsifiers, and Oracle's selected target with a small exact or rigorous
first gate. Its selection packet must state the leading alternatives, the
strongest flaw in the choice, a falsifier, expected information gain, and the
next stop/pivot criterion. It is then followed by an attack cycle (or a
coherent series of attack blocks) until the next boundary. The static portfolio
below is a seed list, not a fixed queue: discovery may reorder, replace, or
retire entries.

Unused capacity is banked for later selected targets; it is never discarded.
The total project cap remains 400 cycles. Budget use is inferred from
`b<ordinal>` preregistration/artifact filenames; do not maintain a duplicate
live counter here. A problem may end before its envelope whenever its expected
value falls below a screened alternative.

## Seed portfolio and current selection

The entries below are starting candidates. Discovery governs their order and
may introduce a better eligible problem.

### Current gate — portfolio discovery after C99

- **C80 closure — OBSERVED engine boundary:** the corrected d=6/m=7 and
  d=7/m=6 compression identities passed exact controls. Balance plus
  zero-shift still admits \(159157855696154\) and \(1394910257088\) ordered
  pairs respectively; three frozen exact searches immediately found
  compressed d=6/m=7 witnesses. This is necessary-condition feasibility, not
  a length-42 pair or a lift theorem. C80 is closed under its failure rule;
  root POSTMORTEMS.md records the reusable screen change.
- **C81 boundary — PROVED / OBSERVED:** the shortest-cycle bypass gives equal
  full/restricted directed girth. Exact finite ranking models rule out
  dominance-only and common-pivot-XYZ-only proofs of spectrum equality; the
  bounded two-chain split screen adds no counterexample. See sealed
  `cycle-81-b081-lem-method-boundary-v1` for the claim boundary.
- **C82 family boundary — PROVED:** the frozen 15-element chain substitution
  has exactly 571,725 linear extensions and no full strict pair-majority
  directed 4-cycle under independent ideal-DP and direct-enumeration routes.
  Thus it cannot be an LEM mismatch realization. Transitive closure adds three
  clone-chain relations in the direct restricted-graph audit; it does not
  affect the no-full-cycle result. See sealed
  `cycle-82-b082-lem-inverse-family-boundary-v1` for the exact boundary.
- **C83 boundary — PROVED:** the exact comparable-tip identity holds on the
  C81/C82 controls, but 30 interval-conditioned reversals and 216 imbalanced
  outside-word fibers refute its two local strengthening attempts.  Oracle's
  one final global-defect inequality has 18 C81 and 768 C82 violations.  See
  sealed `cycle-83-b083-lem-local-defect-boundary-v1` for its exact claim
  boundary; it does not test the full ordered two-triangle configuration.
- **C84 boundary — PROVED:** after source overlap rejected the selected
  1/3--2/3 and Frankl decompositions as prior art, Oracle selected the new
  LRC polynomial route's \(k=13\) composite-modulus gate.  Its direct
  \(\mathbb Z_{14}\) target-box analogue has the exact witness
  \((0,7,0,\ldots,0)\); the complete declared binary fiber has 4,824
  failures.  See sealed
  `cycle-84-b084-lrc-composite-polynomial-boundary-v1`.  This is a source
  theorem-interface boundary, not an eventual-properness or LRC result.
- **C85 boundary — PROVED / OBSERVED:** Oracle's distinct C5
  triple-kernel route for \(K_{5,5}\setminus C_{10}\) passed its complete
  729-row rational two-atom bigraphon control by matching the direct 15-edge
  and reduced kernel routes, with 81 zero rows and least positive defect
  \(7381/14281868906496\).  The exact two-atom CP defect has 8,771 terms.
  The frozen factorization gate produced no checked certificate or rational
  negative before its host-window cap; this is a method boundary, not
  evidence for the global C5-K or Sidorenko inequalities.  See sealed
  `cycle-85-b085-sidorenko-c5-kernel-boundary-v1`.
- **C86 boundary — PROVED:** Oracle's height-four Frankl all-inclusion Hall
  transport passes every declared four-point control (2,034 retained
  dimension-three families, independently matched and Hall-verified), but
  Colbert's named five-point Example 3.20 has all five elements optimal and
  abundant while all five inclusion matchings fail.  This is a direct
  source-control falsifier of the transport, not a Frankl counterexample.
  See sealed `cycle-86-b086-frankl-all-inclusion-hall-boundary-v1`.
- **C88 boundary — PROVED:** the C69 published 13-edge intersecting
  six-partite control has an exact nine-edge residual after deleting \((1,6)\)
  with \(\tau^*=23/8\), but every one-vertex child has \(\tau^*>2\).  The
  complete depth-five packet reconstructs 6,102 rational primal/dual LP
  certificates and has 263 least-applicable FD failures.  See sealed
  `cycle-88-b088-ryser-fractional-drop-boundary-v1`.  This is a greedy
  one-vertex descent boundary only; do not add pair-deletion or threshold
  repairs within it.
- **C89 boundary — PROVED / METHOD_BOUNDARY:** the rank-one stationary
  density-tangent Hessian is nonnegative by the exact 30/30/150 Gram
  decomposition, independently coefficient-replayed on two rational
  three-step controls.  It does not imply a local minimum, higher-order
  control, global Sidorenko, or novelty; do not add grids or regular-graph
  extensions within C89.
- **C90 boundary — PROVED / OBSERVED:** two exact contractions prove strict
  monotonicity on one prescribed S4 T-transform line; the authorized factor
  cap found no reusable character-indexed identity. Do not test another
  transfer, background, group, grid, or graphon variation within C90.
- **C91 boundary — PROVED:** the source-labelled 13-edge Ryser control has
  31 vertices and \(\tau=5\). Its 13 complete four-vertex deletion-cover
  families have counts \((3,5,5,5,5,6,4,6,4,5,6,4,6)\), and two exact CSP
  routes make the frozen reciprocal shared-coordinate trace system UNSAT.
  Do not weaken reciprocity, change the coordinate condition, or test another
  control within C91; return to fresh portfolio discovery.
- **C92 boundary — PROVED:** every one of the 4,223 frozen nontrivial,
  full-universe intersection-closed \([4]\) families has a shared
  \(t=1/3\)/uniform endpoint witness under two exact enumerators. Do not
  extend to \([5]\), change temperature, or invent a post-result monotonicity
  predicate within C92; return to fresh portfolio discovery.
- **C94 interface audit — PROVED / CONJECTURED:** Zhao's decisive condition
  quantifies independently over arbitrary subgroup pairs in every \(S_n\).
  The proposed fixed-diagram, subgroup-free \(n\)-recurrence is therefore
  ill-posed: the unique \(S_1\) input has valid \(S_2\) continuations with
  Möbius densities \(2^{-9}\) and \(1\).  This refutes only that state-only
  schema, not Zhao's comparison.  Do not run an \(S_4\)/\(S_5\) recurrence
  census.  A future bridge must specify an inclusion-compatible subgroup tower
  and state map before executable work; otherwise resume wide discovery.
- **C95 selection — CONJECTURED:** Oracle's artifact-cited C80--C94 exclusion
  map selected the adjusted Bollobás--Meir Boolean four-cube gate: test every
  nontrivial subset of \(\{0,1\}^4\) for a Hamiltonian cycle of fourth-power
  Euclidean cost at most \(32\). A certified excess refutes the adjusted
  \(k=4\) conjecture; a pass proves only that finite class and must stop
  absent an orbit/metric explanation. Do not quotient, enlarge to \(Q_5\),
  or use rational grids/random points.
- **C95 boundary — PROVED:** the exact rooted Held--Karp replay and independent
  witness audit cover all 65,519 labelled nontrivial subsets of \(Q_4\), with
  maximum cost 32 and no excess. See sealed
  `cycle-95-b095-bollobas-meir-q4-boundary-v1`. This proves only the Boolean
  four-cube subclass of the adjusted Bollobás--Meir conjecture. Do not move to
  \(Q_5\), grids, random points, or arbitrary cube points without a new
  orbit/metric mechanism; return to portfolio discovery after the C95
  postmortem.
- **Historical next action before C96:** perform a fresh source/eligibility screen, then invoke
  Oracle only with an artifact-cited historical exclusion map and a genuinely
  new exact or rigorous first gate.
- **C96 screen — NO_SELECTION:** the post-C95 primary-source search found no
  new bounded verifier. Bollobás--Meir continuations are blocked by C95;
  Kakeya, finite-cyclic Fuglede, Nivat's remaining |F|=6 case, the remaining
  all-rank Littlewood--Richardson frontier, and the newly screened
  book-Ramsey/Steiner/Hadamard leads have no source-cleared finite method
  family. Oracle returned `NO_SELECTION`; full exclusions and the decision
  packet are in `discovery/cycle96_portfolio_no_selection.md`. Do not invoke
  another attack until a genuinely new gate is source-defined.
- **C97 screen — NO_SELECTION:** the size-22 Diophantine equation is a
  source-defined residual with exact witness checking, but Oracle found no
  bounded, source-cleared polynomial/norm-form ansatz. Do not run the
  `|x|>10^50` benchmark search or open C97 as an attack; fixed degrees,
  coefficient bounds, and an overlap audit are required first. See
  `discovery/cycle97_diophantine_candidate_screen.md`.
- **C98 boundary — PROVED:** the exact normalized degree-(4,3,6) family in
  coefficient box `[-648,648]` has no identity for
  `z^2+y^2 z+x^3-2`. The replay exhausted 67,288,360 bounded branches in
  25.99 seconds, with the published adjacent-family control passing an
  independent generic expansion. This closes only that degree/height family;
  do not enlarge the box. See sealed
  `cycle-98-b098-diophantine-fixed-ansatz-boundary-v1`; pivot to an
  elliptic-surface or norm-form engine after a fresh source/idea screen.
- **C99 screen — NO_SELECTION:** the primary quadratic-form source confirms
  that `z^2+y^2 z+x^3-2=0` remains open, but its tangent algorithm does not
  transfer directly: completing the square leaves an additional square-
  coordinate constraint. Oracle ranked a square-preserving tangent lift,
  elliptic multisection, and cubic norm-form orbit as future designs, but none
  has a finite state, verifier, and falsifier. Do not open C99 as an attack,
  enlarge C98, or run the `|x|>10^50` benchmark search. See
  `discovery/cycle99_quadratic_form_screen.md`.
- **C001 (C100) closure — OBSERVED control defect:** Oracle selected the
  source-defined (ES(7)=33) reduced orientation-SAT anchor. The canonical
  attempt hit a host OOM. The amended n=25, k=7 lower-memory control then
  returned SAT; its complete 179,400-variable model independently satisfies
  all 3,504,438 generated clauses. Requiring this sub-threshold instance to
  be UNSAT was an invalid scalability criterion, so it cannot authorize a
  canonical retry. This is neither an ES(7) result nor a SAT-model
  realizability claim. See `discovery/cycle100_control_outcome.md`.
- **_001 historical screen:** Oracle independently reconstructed the
  C80--C001 decisions and found no candidate with an explicit state,
  invariant/transition, direct verifier, falsifier, bounded stop, and a
  nonduplicating historical delta. The closest design is C99's
  square-preserving tangent lift. Its two evident tangent-plane curves have
  only their base integral points, and no non-tangent-plane self-map or
  integrality invariant is known. This is an exclusion record, not permission
  to leave D001 unselected. See
  `discovery/_001_portfolio_no_selection.md`.
- **_002 historical screen:** the 2026 near-Williamson source gives a
  genuine structured order-167 Hadamard-668 state and exact autocorrelation
  verifier, unlike the C96 record. But it ends at exhaustive generation and
  has no lift, constructor, or informative negative cap at 167. Do not run a
  SAT/local-search/enumeration census. This is an exclusion record, not an
  allowable selection outcome; Oracle must now choose D001 independently. See
  `discovery/_002_hadamard_near_williamson_screen.md`.
- **D001 (C101) selection — CONJECTURED planning decision:** Oracle selected
  the book-Ramsey all-\(n\) construction problem, beginning with a uniform
  signed six-block character completion for prime powers \(q\equiv7\pmod8\),
  \(n=(q+1)/2\). The frozen first gate is symbolic: retain the public
  \(n=70\) block-type placement and exhaust only its 19 sign choices against
  the character-matrix relations, with direct \(q=7,23\) checks. A pass is a
  candidate arithmetic family; a no-hit is a rigidity boundary for this
  completion, not a graph census or a claim about the general conjecture. See
  `discovery/_003_d001_book_ramsey_selection.md`.
- **D001 (C101/B101) closure — PROVED method boundary:** both exact-integer
  evaluators exhausted all \(2^{19}=524{,}288\) fixed sign assignments at
  \(q=7\), with zero satisfying the frozen Seidel conditions. Since a uniform
  \(q\equiv7\pmod8\) identity would specialize to \(q=7\), this exactly
  falsifies the selected completion. It does not constrain a new block type,
  another character architecture, individual graph constructions, or the
  all-\(n\) conjecture. Do not enlarge signs or perform a graph census; D001
  closes because no residual bounded block type is identified. See sealed
  `cycle-101-b101-book-ramsey-character-sign-rigidity-v1`.
- **E001 (C102) selection — CONJECTURED planning decision:** Oracle selected
  a reciprocal-even quartic-character near-Williamson constructor at order
  167: form \(A(i)=\chi(i)\) off zero and \(B_b(i)=\chi(i^4+bi^2+1)\), then
  exactly complete three \(B_b\) autocorrelation vectors against \(A\). This
  is at most 167 algebraically generated sequences and 14,028 pair sums, not
  an arbitrary sequence census. A hit is checked by all-shift PAF and a
  668-by-668 block product; a no-hit closes only this quartic mechanism. See
  `discovery/_004_e001_hadamard_quartic_selection.md`.

### Closed gate — C80 quaternary Legendre pairs, length 42

- **Banked result:** C72 `PROVED` the generalized five-blocker theorem and the
  consequence \(\tau(H)=6\Rightarrow D(H)\ge6\); corrected artifact v2 is the
  canonical record.
- **Eligibility correction — OBSERVED:** Haonan Zhang, *Proof of the
  Holevo-Utkin conjecture on sharp \(\ell_p\) norms for zero-sum vectors*,
  arXiv:2605.05243v1 (4 May 2026), Theorem 2, proves the full conjecture for
  every \(d\ge4\). C74's bounded primary-source screen missed it. C75 is
  consequently contained as an overlapping reconstruction; do not seal it or
  begin a paper phase.
- **Selection — CONJECTURED planning decision:** after the corrected
  exact-statement, arXiv-ID/title, current-primary/citation, and official
  OpenAI screens (`discovery/cycle76_source_screen.md`), Oracle selected
  Song--Chen Conjecture 2 for three qubits, uniform two-body weights, and
  \(Q=\operatorname{diag}(q,1-q)\).  Its first gate is an exact rational
  Ky Fan falsifier search, followed only by exact certification of any hit.
  The LEM 4-cycle question is the immediate reserve; Ryser needs a genuinely
  new global dual mechanism.
- **Finite packet — OBSERVED:** C77's 10,136 canonical low-support rational
  states at the seven frozen \(q>1/2\) values produced no numerical Ky Fan
  candidate; the full \(Q=I/2\) control had maximum floating residual
  \(7.8\times10^{-16}\).  This is not a theorem or evidence beyond the
  named packet.
- **Diagonal-slice correction — PROVED prior overlap:** C77 independently
  replayed the diagonal three-qubit slice, but Alhejji--Knill, Proposition
  IV.5, already proves the stronger classical state-tuple statement.  Retain
  the table only as a convention cross-check; do not seal or paper-promote it.
- **C79 endpoint foundation — PROVED:** sealed
  `cycle-79-b079-compatible-endpoint-foundation-v1` proves the weighted,
  compatible three-qubit pair-support endpoint at \(Q=I/2\), independently
  of Song--Chen. Its exact replay checks 64 spin-flip matrix-unit identities,
  all eight target rows, and 736 polygon-domain scalar rows. It does not
  itself prove arbitrary \(Q\).
- **C78 interpolation theorem — PROVED:** correction v3
  `cycle-78-b078-compatible-spin-endpoint-correction-v3` supersedes the
  withdrawal and reinstatement metadata record. C79 supplies the \(Q=I/2\)
  endpoint; positivity gives the pure endpoint; common local-unitary
  diagonalization and the common ordered target spectrum make the interpolation
  rigorous. This proves Conjecture 2 in the scoped case of
  all compatible three-qubit states, arbitrary weights supported on
  \(AB,AC,BC\), and every qubit \(Q\).  It remains strictly narrower than
  Conjecture 2.
- **Certification correction — PROVED:** the source endpoint is currently an
  arXiv preprint, so C78 v1 did not meet the repository definition of
  `PROVED`; its sealed v1 correction records the withdrawal. C79 and the
  audited v2/v3 correction chain resolve the dependency without mutating any
  historical record.
- **Paper phase — OBSERVED non-release:** the self-contained draft, literature
  audit, replay instructions, and hostile review are in
  `paper/c78-compatible-spin-endpoint/`. It is not publishable without
  authorship/venue, a tracked release boundary, deterministic extracted replay
  archive, DOI, and Zenodo release gates; PAPER_AUDIT.md records the boundary.
- **Closure postmortem — PROVED workflow decision:** root POSTMORTEMS.md
  records the source-authority lesson required before next-target selection.
- **Selection correction — PROVED source correction:** Wilf multiplicity 19
  is already proved (Kliem--Stump, Proposition 6.9), while 42 remains the
  smallest unresolved quaternary Legendre-pair length. The earlier screen
  made both calls incorrectly; discovery records the correction.
- **C80 selection — CONJECTURED planning decision:** exact 6/7 compression,
  balance, PSD/Parseval, and symmetry-signature gate for length 42; SAT lift
  only from compatible exact signatures. LEM 4-cycles is the immediate pivot
  if this gate does not yield a pair or a proof-producing decomposition.
- **Next action:** preregister and execute the bounded C80 compression gate.
  Do not resume C76--C79 or paper work unless external release authority
  changes.

### Problem 1 — Lonely Runner for 14 total runners, \(LRC(13)\)

- **Target:** prove \(LRC(13)\) or produce a rigorous counterexample.
- **Why first:** `CONJECTURED` 15–35% chance of resolving the selected finite
  case and 35–60% chance of publishable progress. It has an exact finite
  interface and the highest estimated short-horizon tractability.
- **Risk:** `OBSERVED` the first exact \(I(13,199,1)\) census has 4,748,938
  canonical representatives. Initial-sieve generation and subsequent lifting
  are both materially harder than the original planning estimate.
- **Initial source:** the finite-checking framework in
  [Forum of Mathematics, Sigma](https://www.cambridge.org/core/journals/forum-of-mathematics-sigma/article/linearly-exponential-checking-is-enough-for-the-lonely-runner-conjecture-and-some-of-its-variants/A51A991DE89B8C9C2E2FF13FBD4501DA).
- **Advance condition:** a reproducible exact model of the verified first-open
  case plus either a new structural reduction, a smaller certified checking
  region, or a proof/counterexample candidate surviving independent checks.

### Problem 2 — Sidorenko for \(K_{5,5}\setminus C_{10}\)

- **Target:** prove or disprove
  \[
  t(K_{5,5}\setminus C_{10},W)\ge t(K_2,W)^{15}
  \]
  for every graphon \(W\).
- **Why second:** `CONJECTURED` 8–15% chance of complete resolution and 35–60%
  chance of publishable progress. The target is one concrete graph with a
  clean analytic verifier.
- **Known boundary:** published work identifies this graph as a smallest open
  Sidorenko case and supplies an obstruction to ordinary sums-of-squares
  proofs; recheck the exact theorem and hypotheses before relying on it.
  [Source](https://par.nsf.gov/servlets/purl/10277018)
- **Advance condition:** a certified extremizer reduction, entropy or
  conditional-expectation inequality beyond the known SOS barrier, or a
  certified violating graphon.

### Problem 3 — intersecting Ryser at \(r=6\)

- **Target:** prove or disprove \(\tau(H)\le 5\nu(H)\) for intersecting
  6-partite 6-uniform hypergraphs, with the exact convention fixed during the
  eligibility audit.
- **Why third:** `CONJECTURED` 4–9% chance of complete resolution and 25–45%
  chance of publishable progress. The first unresolved parameter supports
  structural classification and exact SAT/ILP certificates.
- **Known boundary:** recent literature reports the intersecting case proved
  through \(r=5\) and open from \(r=6\); verify this status before execution.
  [Source](https://people.maths.ox.ac.uk/~scott/Papers/ryser.pdf)
- **Advance condition:** a certified reduction of minimal counterexamples, a
  new cover/matching inequality, or exhaustive closure of a nontrivial class.

### Problem 4 — the \(1/3\)–\(2/3\) poset conjecture

- **Target:** prove that every finite non-chain poset has an incomparable pair
  \((x,y)\) for which the probability that \(x<y\) in a uniformly random
  linear extension lies in \([1/3,2/3]\), or find a counterexample.
- **Why fourth:** `CONJECTURED` 3–7% chance of full resolution and 25–45%
  chance of publishable progress. Exact linear-extension counting provides a
  strong finite experimental interface, but the general structural bridge is
  difficult.
- **Initial source:** recent work on special classes is an entry point, not
  evidence for the full conjecture.
  [Source](https://ieeexplore.ieee.org/abstract/document/10900886/)
- **Advance condition:** a new reducible class, minimal-counterexample
  restriction, or an inequality that survives exhaustive finite testing and
  exact proof checks.

### Problem 5 — Frankl's union-closed sets conjecture

- **Target:** prove that every finite nonempty union-closed family other than
  \(\{\varnothing\}\) contains an element appearing in at least half its
  member sets, or find a counterexample.
- **Why last:** `CONJECTURED` 2–5% chance of full resolution and 20–40% chance
  of publishable progress. It is exceptionally clean and computable but has
  resisted many local averaging arguments.
- **Initial source:** [2023 JCTA work on special
  classes](https://www.sciencedirect.com/science/article/pii/S0097316523000869).
- **Advance condition:** a genuinely new invariant, a strict
  minimal-counterexample reduction, or certified closure of a meaningful new
  family.

## Research path and gates

```text
Automatic loop [C73 COMPLETE: ORACLE RESELECTED C72 RYSER]
  -> discovery: eligibility screen + adversarial candidate comparison
  -> Oracle selects one target with an exact/rigorous first gate
  -> attack while the decision question and method family stay coherent
  -> durable result/no-go/eligibility loss, or 50-cycle review
  -> discovery and reselection (bank unused capacity) -> repeat

Problem 1: LRC(13), 14 total runners [PAUSED: HANDOFF AT C50]
  -> eligibility and exact frontier audit [COMPLETE]
  -> reproduce exact ansatz checker [COMPLETE]
  -> largest-entry orbit quotient [CLOSED: STRATEGICALLY INSUFFICIENT]
  -> in-memory coverage-directed quotient [CLOSED: MEMORY GATE]
  -> disk-partitioned coverage quotient, 64/128-GiB tranches [CLOSED: EDGE GATE]
  -> pairwise packing cut before child emission [CLOSED: STRUCTURAL NO-GO]
  -> three-way non-co-cover hypergraph cut [CLOSED: DISCOVERY RESULT]
  -> direct exact r-translate feasibility before child emission [CLOSED: PERFORMANCE GATE]
  -> fused first-lift interface and multi-choice CSP [CLOSED: CONTROLS PASS, P199 PERFORMANCE GATE]
  -> exact weighted-time dual certificate [CLOSED: H11 STRUCTURAL NO-GO]
  -> gcd-pattern cover engine [CLOSED: CONTROLS PASS, P199 PERFORMANCE GATE]
  -> proof-producing SAT/PB encoding [CLOSED: 100/100 SAMPLE CERTIFIED UNSAT]
  -> syntactic checked-core permutation template [CLOSED: EXACT STRUCTURAL NO-GO]
  -> selected-core typed semantic instantiation [CLOSED: COLLAPSES TO PRIOR FAMILY]
  -> alternate-proof / MUS diversification [CLOSED: CERTIFIED CORES, SHRINK GATE FAILED]
  -> resolution-graph backward / dominator slicing [CLOSED: SIX SAT SLICES, NO DOMINATOR]
  -> gcd-conditioned learned-certificate decision tree [CLOSED: COMPLETE BASE-7 TREE, SPARSE TEMPLATE]
  -> analytic typed time-deficit signature family [CLOSED: 6044/6084 ON EACH OF TWO BASES]
  -> conditional pair-choice Hall lift [CLOSED: FOUR NEW BASE-3 LEAVES]
  -> symbolic first-seven-coordinate case split [CLOSED: AGGREGATE WALL GATE]
  -> exact CRT bad-time interface [COMPLETE: PROVED TWO-DIAGONAL THEOREM]
  -> coupled diagonal-incidence / width-three reduction [COMPLETE: 15 LEAVES]
  -> targeted width-four block deficiency [COMPLETE: ONE LEAF]
  -> adaptive width-four partition oracle [COMPLETE: 60 OBSERVED UNRESOLVED]
  -> eight-class CRT/Ramanujan dual [COMPLETE: 60 OBSERVED UNRESOLVED]
  -> twelve-class quadratic-residue CRT dual [COMPLETE: 60 OBSERVED UNRESOLVED]
  -> compact width-five transferred-weight control [COMPLETE: 60 OBSERVED UNRESOLVED]
  -> fresh width-five time-weight LP [COMPLETE: 60 OBSERVED UNRESOLVED]
  -> capacity-selected cyclic width-five geometry [CONTAINED: INCOMPLETE AUDIT]
  -> semantic-primal lift equivalence control [COMPLETE: EXACT LABELED RANK-THREE INTERFACE]
  -> CRT-conjugacy synchronization invariant [COMPLETE: EXACT PARTIAL ACTION]
  -> additive atom-pair convolution quotient [CLOSED: EXACT SPLITTING WITNESS]
  -> degree-zero GF(2) uncovered tensor [CLOSED: EXACT FIELD BOUNDARY]
  -> degree-zero GF(3)/GF(5) uncovered tensors [CLOSED: EXACT FIELD BOUNDARIES]
  -> exact rational degree-zero certificate [CLOSED: INTEGER LEFT-NULL WITNESS]
  -> rank-one coordinate-local signed measure [CLOSED: FULL-GRID OBSTRUCTION]
  -> degree-one signed product-functional lift [CLOSED: FULL RAW REPLAY]
  -> degree-two product-functional prototype [CLOSED: FULL 16,170,400-LABEL REPLAY]
  -> rooted ownership/blocker functional extension [CLOSED: EXACT DIAGONAL SPAN NO-GO]
  -> full priority/fallback signed ownership routing [CLOSED: 13 EXACT BLOCK NO-GOS]
  -> pair-correlated signed ownership moments [CLOSED: EXACT DEGREE-THREE COUNTERMODEL]
  -> ownership-literal multiples of rank-two blockers [CLOSED: EXACT SIGNED DEGREE-THREE CONSTRUCTION]
  -> four-partite H2 / horn filling under rank-one/two/three deletions [CLOSED: EXACT AMBIENT HOMOLOGY, FIRST MOMENT FILLS]
  -> full selected moment-H2 coupling and coherent face-choice lift [CLOSED: 3954/3954 EXACT INTEGRAL FILLS]
  -> stratified non-anchor coupling and cone-mechanism holdout [CLOSED: 2000/2000 CONE OR ACYCLIC]
  -> global defect-supported chain homotopy / countermodel [CLOSED: EXACT PROJECTION, LOCAL AXIOMS INSUFFICIENT]
  -> relative-chain/Cech quotient by global p199 closure relations [CLOSED: EXACT COORDINATE REFORMULATION]
  -> affine sheaf/syzygy descent over shared labeled faces [CLOSED: EXACT 256-ROW GLOBAL SECTION]
  -> canonical-face rewrite / critical-pair confluence [CLOSED: REPAIR PASSES, LITERAL CONFLUENCE REFUTED]
  -> relative diagonal-stratum contraction / terminal homology [CLOSED: 382,453,314/382,453,319; FIVE BUFFER-SURROGATE EXCEPTIONS]
  -> deletion-aware relative cube packet theorem [CLOSED: 29,048/29,050; TWO PAIR-FIBER FAILURES]
  -> lift-aware reduction / prime-product closure [BLOCKED BY ALGEBRAIC GATE]
  -> close, stop, or saturate
  -> bank unused allocation

Problem 2: Sidorenko single graph [CLOSED: C68 SCOPED FIXED-S3 THEOREM]
  -> current eligibility/literature audit [COMPLETE: PROVISIONALLY ELIGIBLE]
  -> exact finite-group conjugacy-averaging comparator [CLOSED: 840 EXACT NONNEGATIVE ROWS]
  -> bounded equal-block local graphon variation [CLOSED: 512 EXACT POSITIVE-FIRST-DIRECTION ROWS]
  -> symmetric arbitrary-kernel directional local stability [CLOSED: PROVED AT p=1/2]
  -> nonsymmetric bipartite directional local extension [CLOSED: PROVED FOR EVERY FIXED p]
  -> symbolic S3 Zhao-deficit packet [CLOSED: 1,360 EXACT FINITE POINTS]
  -> S3 ternary one-orbit smoothing packet [CLOSED: 1,458 EXACT ROWS]
  -> positive-monomial conditional-variance cone [CLOSED: EXACT 756-COLUMN NO-GO]
  -> Pólya multiplier certificate [CLOSED: NO COEFFICIENTWISE PASS THROUGH K=24]
  -> S3 flat-stratum local comparison [COMPLETE: PROVED FOUR-BASE LOCAL THEOREM]
  -> representation/Gram conditional-variance identity [DEFERRED: NO PINNED SDP ROUTE]
  -> conjugacy-orbit KKT/exchange minimizer lemma [CLOSED: FINITE PACKET; CONTINUOUS GAP]
  -> continuous S3 orbit-invariant minimizer reduction [COMPLETE: EXACT SIX-COORDINATE QUOTIENT]
  -> fiberwise invariant minimization [COMPLETE: UNIFORM DEGREE-26 FIBER REDUCTION]
  -> fixed unequal-weight 2x2 bipartite step graphons [CLOSED: NO EXACT NEGATIVE OR REUSABLE REDUCTION]
  -> larger-group and step-graphon ladders [PAUSED: HARD STOP AT C65]
  -> cross-conjecture leverage/novelty audit [COMPLETE: C66 PIVOT GATE PASSED]
  -> fixed-S3 fiber-boundary positivity [COMPLETE: C67 EXACT FOUR-FAMILY THEOREM]
  -> exact chord-remainder / interior-fiber sign [COMPLETE: C68 FULL FIXED-S3 THEOREM]
  -> resultant-defined interior branches [NOT NEEDED]
  -> transferability or scoped closure decision [COMPLETE: PUBLISHABLE SCOPED THEOREM]
  -> Problem 3: intersecting Ryser r=6 [DEFERRED: C71 BOUND; C72 BROAD CLASSIFICATION BRANCH]
     -> eligibility and primary-literature audit [COMPLETE: OPEN FOR r>=6]
     -> local deletion-cover exchange [CLOSED: C69 NON-DISCRIMINATING]
     -> minimal-counterexample deletion-witness incidence design [DEFERRED: C70 LOCAL CONTROLS NON-DISCRIMINATING]
     -> six-color complete-graph component cover [NEXT: EXACT EQUIVALENT STATE SPACE]
     -> high-star nonlinearity defect [COMPLETE: C71 PROVED D>=5; LOCAL EQUALITY SATURATED]
     -> global defect-to-cover invariant [RETURN ONLY THROUGH DISCOVERY]
  -> C73 discovery [COMPLETE: Q7 WITHDRAWN; C72 RYSER RESELECTED]
  -> Resumed C72: D=5 universal core blocker [ACTIVE]
  -> all further targets [DISCOVERY-SELECTED, NOT QUEUED]
  -> final proof package or handoff [AT PORTFOLIO STOP]
```

For each problem, use the same four substantive gates within its available
allocation:

1. **Eligibility:** current open status, exact statement, official-OpenAI
   exclusion, closest primary results, and smallest exact verifier.
2. **Reproduction:** replay the strongest applicable theorem or computational
   baseline and identify its precise obstruction.
3. **New engine:** attempt at least one new invariant, lift, duality,
   completion, inverse theorem, or discriminating countermodel; state what it
   preserves and what falsifies it.
4. **Closure:** independently check the decisive argument, hypotheses,
   computation, and novelty, or record the strongest later-relevant no-go and
   move forward.

Do not reserve fixed numbers of cycles for administration. Research continues
while a gate has a credible advance path; it stops early when preserving the
balance has higher expected value.

## OpenAI eligibility screen

`OBSERVED` in a bounded 2026-08-03 official-source search: OpenAI publicly
announced a disproof of the planar unit-distance conjecture, published its ten
First Proof submissions, and described additional GPT-5 mathematical work.
Those announced targets are excluded. Repeat the official-source search for
each shortlisted problem immediately before starting it.

- [Planar unit-distance announcement](https://openai.com/index/model-disproves-discrete-geometry-conjecture/)
- [First Proof submissions](https://openai.com/index/first-proof-submissions/)
- [GPT-5 science experiments](https://openai.com/index/accelerating-science-gpt-5/)

## Headline findings and corrections

- `OBSERVED` Cycle 1 reproduced the published \(I(6,47,1)\) and
  \(I(7,47,1)\) counts by independent exact routes, then completed the first
  \(I(13,199,1)\) census: 4,748,938 representatives after 5,869,850,724 DFS
  nodes. Every emitted row passed an independent modular-cover recheck. The
  count does not imply \(J(13,199)=\varnothing\) or \(LRC(13)\); see the sealed
  Cycle-1 artifact for the exact boundary.
- `OBSERVED` Cycle 2's canonical-parent quotient reproduced both baseline
  tuple sets exactly, but the \((13,199)\) run exhausted its aggregate
  586,985,072-node budget without reaching a leaf. The sealed artifact records
  an algorithmic performance failure only; it is not a mathematical no-go.
- `OBSERVED` Cycle 3's coverage-directed level quotient reproduced a naive
  oracle and both baseline tuple sets, then exceeded the logged 8 GiB virtual-
  memory limit while constructing depth 8. Its retained-path argument remains
  available to a partitioned storage engine; see the sealed artifact.
- `OBSERVED` Cycle 4's exact 64-partition engine completed depth 8 with
  33,193,860 states and used only 375,140 KiB peak RSS, then stopped exactly
  at its configured 64 GiB logical serialized-byte cap while expanding depth
  9. The physical filesystem did not fail.
- `OBSERVED` corrected Cycle 4 combined both storage tranches, completed depth
  9 with 354,931,861 states, and then stopped at 5,869,850,727 generated edges
  before reaching a leaf. The v2 artifact supersedes the intermediate v1
  conclusion without consuming another cycle.
- `PROVED` Cycle 5 found that the 14 frozen bad exponents for ((13,199))
  satisfy (B-B=H_{199}): all 99 differences occur, so the pairwise
  incompatibility graph has no edges and its clique cut is vacuous for every
  state. `OBSERVED` the exact frontier made 416,007,772 packing checks, zero
  prunes, and reproduced the Cycle-4 edge gate. This does not constrain
  higher-order non-co-cover relations or fused cover/lifting.
- `PROVED` Cycle 6 established the forbidden-triple weak-colorability
  necessary condition and found its (H_{199}) relation nontrivial. `OBSERVED`
  exact direct five-translate feasibility rejected 85,594 of the fixed
  100,000-state depth-8 prefix, while agreeing with triple colorability on
  the first 1,000 states. Direct feasibility is stronger than the triple cut;
  the agreement is not an equivalence proof.
- `OBSERVED` Cycle 7 integrated direct feasibility without changing either p47
  tuple set, but its stratified p199 benchmark had a 31 ms p99 and roughly
  1 GiB peak RSS for only 1,000 rows—over 300 times the frozen 100 microsecond
  frontier gate. This is a host-specific implementation limit, not a lower
  bound on future exact representations.
- `PROVED` Cycle 8 established the parent-intersected first-lift retained path
  and closed both exact controls: raw `(3,11,4)` and all 53 canonical
  `(6,47,7)` base orbits leave no survivor, implying `J(6,47)=empty` under the
  checked lifting proposition. `OBSERVED` both exact capped `(13,199,14)` CSP
  formulations returned CAP for every one of 100 stratified completed base
  orbits; this is a method-performance outcome only, not a p199 survivor or
  emptiness claim.
- `PROVED` Cycle 9 found a structural no-go for the nonnegative weighted-mask
  dual on its complete raw H11 prototype: each of its 240 l=1-improper bases
  has an explicit lifted mask cover, making the strict dual inequality
  impossible. The gcd clause, rather than mask-cover impossibility, closes
  that prototype.
- `PROVED` Cycle 10's exact gcd-pattern predicate closed the complete H11 and
  p47 controls. `OBSERVED` every row in the fixed 100-orbit p199 sample reached
  the two-million-node cap without SAT or UNSAT; the all-CAP result is a
  bounded implementation-performance failure, not mathematical evidence about
  p199 feasibility.
- `PROVED` Cycle 11 reconstructed and checked the exact first-lift CNF and
  independently verified all 393 DRAT certificates: 240 H11 controls, 53 p47
  controls, and all 100 fixed stratified p199 bases are UNSAT. Hence those 100
  named p199 bases are absent from `F_1(13,199,14)`. This is a finite exclusion,
  not full `F_1` emptiness, a density estimate, `J` emptiness, or `LRC(13)`.
- `PROVED` Cycle 12 certified 100 extracted UNSAT cores and closed the frozen
  syntactic template family: all 80 cores had no residue-preserving coordinate-
  permutation embedding across 20 held-out validation CNFs, and the selected
  core and its 293-clause deletion-minimal subcore had no embedding in 100
  external CNFs. This is a no-go for that literal mapping family only; it does
  not constrain other cores, semantic substitutions, interpolation, or
  `LRC(13)`.
- `PROVED` Cycle 13 partitioned every clause of the selected 293-clause core:
  281 map into universal exactly-one or gcd-channel schemas, while its 12
  target-dependent coverage clauses are unions of complete 2/7 divisor-color
  classes. Thus every permitted within-color choice bijection adds no image
  beyond Cycle 12's coordinate permutations, which already had no match in
  the 20 validation and 100 external targets. Other cores and semantic
  families remain open.
- `PROVED` Cycle 14's exact 80-core census found 1,179, 1,174, and 1,169
  color-splitting coverage clauses in the three selected bases, and 16 of 27
  diversified extraction rows received fresh checked UNSAT certificates; 11
  rows were resource-capped. `OBSERVED` the selected 2,329-clause core retained
  1,180 discriminating clauses but yielded zero certified single deletions
  under 2,328 capped attempts, and each of four whole-role deletion formulas
  returned solver SAT. This fails the at-most-500 advance gate but does not
  show that a small discriminating core is impossible.
- `PROVED` Cycle 15's checked LRAT derivation uses 2,294 of 2,329 input
  clauses. Its empty clause has 31 immediate branches and no derived node
  reachable from every branch, ruling out a strict derived dominator. All six
  protected distance/frequency prefixes of sizes 128, 256, and 500 are SAT by
  preserved, directly checked models. This closes only those graph slices,
  not arbitrary clause subsets or branch-community unions.
- `PROVED` Cycle 16 partitioned the gcd-admissible assignments for frozen base
  7 into 6,084 canonical mod-2/mod-7 witness leaves and independently replayed
  a checked UNSAT proof for every residual. Its selected 27-clause direct
  cover-deficit core maps exactly to held-out leaves of bases 4 and 3.
  `PROVED` the exact template census found 34,398 matches among 608,400 frozen
  base/leaf tests, but zero complete bases; this certifies only those named
  residuals, not any further full base, `F_1`, `J`, or `LRC(13)`.
- `PROVED` Cycle 17 established the exact weighted time-deficit inequality and
  independently reconstructed certificates for 6,044 of 6,084 canonical
  leaves of frozen base 4 and the same count for base 3: 12,088 named leaf
  exclusions total. Forty leaves per base remain unresolved. `OBSERVED` the
  unrestricted floating LP optimum was one on all 80 survivors; this is not
  an exact dual-optimality or saturation claim.
- `PROVED` Cycle 18 established the pair-choice Hall inequality and
  independently reconstructed strict deficits for base-3 leaf ordinals 83,
  121, 952, and 979. Combined coverage is now 6,048/6,084 leaves for base 3
  and 6,044/6,084 for base 4. `OBSERVED` the frozen pair search produced no
  candidate for the other 76 rows; this does not rule out other partitions or
  larger coupled states.
- `PROVED` Cycle 19 established that inclusion-maximal coverage antichains
  preserve full-cover feasibility. `OBSERVED` its optimized 3,500-second
  prototype certified no leaf and produced no full-cover candidate: three
  rows partially executed and 73 never started. All 76 rows are aggregate-
  wall caps after correction of three deadline-sentinel labels. This is a
  performance boundary, not a mathematical no-go.
- `PROVED` Cycle 20 established that for coprime positive (p,c), writing
  (x=x_p+pj) with canonical residues gives
  (c\min(x,pc-x)<pc) exactly when (j=0), or when (j=c-1) and
  (x_p\ne0); moreover (j=p^{-1}(x_c-x_p)\bmod c). Independent complete
  C++ and Python controls agreed on all 7,871,973 frozen ordered pairs for
  H11, p47, and p199. This factorizes one bad-time predicate only: the two
  diagonals remain coupled and no global cover or leaf is closed.
- `PROVED` Cycle 21 established the exact coupled row-fiber incidence model
  and independently replayed width-three integer deficits for 15 previously
  unresolved leaves: nine for base 4 and six for base 3. Exact margins range
  from 1 to 126. `OBSERVED` 11,895 direct cyclic transfer trials closed no
  further leaf. Sixty-one leaves remain; neither base is complete.
- `PROVED` Cycle 22 independently replayed a width-four deficit for base-4
  leaf 952 with exact margin 88. Its ten-partition LP family completed 602
  trials without caps and left 60 leaves unresolved. `OBSERVED` the attempted
  all-four-subset transfer reached the aggregate wall after partially testing
  three leaves and never starting 57; this is a performance boundary only.
- `OBSERVED` Cycle 23 exhaustively selected one-four-plus-three-triples
  partitions from exact pair-overlap scores (200,200 candidates for each of
  60 leaves), then completed all 60 initial and all 60 distinct reselected
  width-four LPs. No integer deficit emerged. Independent replay recomputed
  every initial and adaptive tie from the direct CNFs. This confines only the
  frozen pairwise selector and one-reselection method; it is not a width-four
  or LRC no-go theorem.
- `OBSERVED` Cycle 24 completed the frozen eight-class CRT/Ramanujan dual
  across all 60 survivors without a deficit; every class-LP objective was
  above one. Most optima collapsed to one class, motivating a distinct
  quadratic-residue refinement rather than more partitions in the same cycle.
- `OBSERVED` Cycle 25 completed the frozen twelve-class quadratic CRT dual
  across the same 60 survivors. Its exact class basis is nonsingular, yet the
  objective range and near-total single-class collapse persist. This closes
  that finite refinement, not Fourier or width-four capacity arguments.
- `OBSERVED` Cycle 26 exactly recovered the Cycle-22 width-four witness, then
  transferred it through a complete restriction-selected 5+4+4 family. All
  60 targets were nondeficits, with direct replay gaps from 20,681 to 49,231.
  This closes one sparse-weight/fixed-geometry transfer, not width five.
- `OBSERVED` Cycle 27 completed a fresh direct time-weight LP with exhaustive
  finite separation on the same fixed 5+4+4 geometry for all 60 survivors.
  It took 21--69 rounds and 58--149 cuts per target; every printed objective
  was within floating tolerance of one and no frozen integerization produced
  a direct deficit. An independently written streamed replay matched all 60
  target identities, objectives within `1e-8`, rounds, and cut counts. This
  closes the fixed-geometry LP family only, not a width-five or LRC claim.
- `OBSERVED` Cycle 28's exact four-witness selector chose nonbaseline cyclic
  5+4+4 geometries for all 60 survivors, and its primary floating LP promoted
  none. The closure audit failed: 35 LP traces matched exactly, while base-3
  leaf 91 gave the same objective `1` but a 28-round/80-cut primary path and a
  26-round/74-cut unpinned independent path. A one-thread control reproduced
  28/80, classifying thread-sensitive numerical behavior, but 24 traces remain
  independently unconfirmed. The sealed record is an incomplete-audit
  containment boundary, not closure of the cyclic family.
- `PROVED` Cycle 29 gives an exact equivalence between finite direct-cover
  feasibility and a labeled ownership partition avoiding all coordinate-local
  blockers. Two independent implementations agree on 327,680 complete
  synthetic interfaces, all 64,000 H11 lifts, and the p199 base-4/leaf-78
  census: 12,264 signature patterns represent 190,867,444 concrete blockers,
  all of rank at most three. This is an exact asymmetric interface, not a leaf
  exclusion; forgetting the labels or applying generic hypergraph coloring
  would collapse toward Cycle 6's necessary-only relaxation.
- `PROVED` Cycle 30 classifies the gcd-stratified unit-transport algebra on
  p199 base 4 / leaf 78: 1,386 masks generate 1,390 pointwise atoms—only four
  fewer than the 1,394 negation orbits. The two exceptional six-point CRT
  atoms nevertheless convolve atom-constantly with every mask generator in
  all 2,772 tested profiles, independently reproduced with 2,079 distinct
  compressed profiles. This is a partial module action, not full atom-pair
  convolution closure, a Schur ring, or a leaf exclusion.
- `PROVED` Cycle 31 refutes that specific 1,390-atom partition as an additive
  convolution quotient. Both singleton translations pass, but the first pair
  witness \(A=\{\pm1\}\), \(B=\{\pm198\}\) has sums
  \(\{\pm197,\pm199\}\), splitting the six-point atom containing
  \(199\) and \(597\) with values one and zero. This is a structural no-go
  for the four mergers beyond negation, not for refined partitions or other
  algebraic engines.
- `PROVED` Cycle 32 finds the exact H11 identity \(F_{12}=1\) on the first
  infeasible base, then closes the analogous degree-zero GF(2) family on p199
  base 4 / leaf 78. Among 4,243 frozen evaluation rows, a 577-row subsystem
  XORs to zero on all 1,394 predicate columns and to one on the right-hand
  side; independent reversed-pivot elimination agrees. This rules out only
  degree zero in characteristic two, not odd fields or positive degree.
- `PROVED` Cycle 33 closes the same degree-zero family over both
  \(\mathbb F_3\) and \(\mathbb F_5\). On the identical 4,243-row,
  1,394-column interface, normalized left-null certificates of size 802 and
  985 respectively recombine every predicate column to zero and the RHS to
  one; independent set-based and reversed highest-pivot replays agree. These
  are field-specific no-gos, not a rational conclusion.
- `PROVED` Cycle 34 closes characteristic zero on the same restriction. A
  primitive 1,229-term integer left-null vector of maximum height 2,807 bits
  annihilates all 1,394 predicate columns and has nonzero coefficient sum.
  An independent route rebuilt the evaluation matrix as direct sets and
  verified every big-integer sum. Hence no degree-zero rational identity
  exists for this leaf/interface; positive degree remains open.
- `PROVED` Cycle 35 replaces that large sampled witness by thirteen short
  integer local normals of mass one. Their tensor product has global mass one
  and annihilates every direct predicate on the complete digit grid because
  each predicate has a zero local contraction in at least one coordinate.
  Independent direct-mask replay verifies all 1,394 predicates; coefficients
  have magnitude at most five. Exactly 181 predicates have only one killing
  coordinate, locating the degree-one boundary.
- `PROVED` Cycle 36 constructs a new mass-one product functional annihilating
  all 1,394 predicates and all 221,646 one-hot coordinate-indicator multiples.
  The exact compression theorem says a predicate's complete degree-one family
  vanishes iff it has two ordinary zero contractions or one strong pointwise
  zero coordinate. Independent direct-set replay checks every raw label;
  coefficients have magnitude at most six. Thus the frozen direct-predicate
  calculus has no degree-\(\le1\) rational identity for this leaf.
- `PROVED` Cycle 37 constructs a mass-one product functional annihilating all
  1,394 predicates, 221,646 degree-one generators, and 16,170,400 labeled
  distinct-coordinate degree-two generators. Same-coordinate products reduce
  by the one-hot relations. The exact compression condition is three ordinary
  zero contractions or one strong pointwise-zero coordinate, and an
  independent direct-set replay checks every raw label. Thus the named
  direct-predicate calculus has no degree-\(\le2\) identity; this does not
  constrain ownership auxiliaries or justify an automatic degree-three step.
- `PROVED` Cycle 38 evaluates all 12,264 symbolic ownership-blocker patterns,
  representing 190,867,444 concrete blockers through 26,348,103 complete
  global-type tuples. Every cyclic rooted first-cover/fallback pushforward has
  a nonzero rank-two blocker moment. Independent enumeration of the 14,406
  nonzero signed-support assignments verifies one blocker per root, and an
  integer augmented left-null certificate with nonzero right side 300 rules
  out mass-one cancellation in their thirteen-measure span. This is a no-go
  only for that deterministic rooted span at the unmultiplied generator layer.
- `PROVED` Cycle 39 expands those thirteen maps to the complete 53,248-section
  span of all deterministic priority orders with one fallback. Exact rank-two
  CEGAR closes every fallback block using 573 selected rows; independent
  replay checks all integer left-null products across every section column and
  331,338 direct signed-support assignments. This proves no mass-one
  combination exists in that priority span, but does not constrain pair-
  correlated or nonlocal routing.
- `PROVED` Cycle 40 constructs a mass-one rational signed ownership-moment
  family through degree three on p199 base 4 / leaf 78. It satisfies one-hot
  totality, lifted rank-one support, all 6,684,938 rank-two and 19,661,454
  rank-three type tuples, and exact lower-marginal compatibility. Independent
  replay reconstructs 694,912 pair classes and all 693 triple-mask classes;
  36 singleton exceptions induce 228,252 pair-diagonal deletions, with none
  unresolved. This is a local signed countermodel, not a positive/global
  ownership distribution, a leaf certificate, or LRC(13), and it omits
  arbitrary multiples of rank-two and rank-three generators.
- `PROVED` Cycle 41 extends that signed functional through every Boolean-
  reduced ownership-literal multiple of every rank-two blocker. The new
  mechanism is tripartite chain filling: an exact sparse-boundary census and
  a dense Cech/Mayer--Vietoris argument jointly close every interface, with an
  independent reconstruction. This is not positivity, a global ownership
  distribution, the full blocker ideal, a leaf certificate, or LRC(13);
  rank-three multiples remain open, and nontrivial pair-intersection homology
  prevents an automatic recursive extension.
- `PROVED` Cycle 42 classifies the preregistered four-partite prototype:
  3,893 of 3,954 raw interfaces (354 of 409 distinct structural complexes)
  have nonzero rational \(H_2\), with dimension at most 40 and identical
  GF(2) dimensions. On the first such interface `(2,5,14,5)`, an eight-term
  ambient cycle has a dual cochain pairing `-1`, but the globally canonical,
  repeated-type-symmetric Cycle 41 moment cycle is the boundary of one allowed
  tetrahedron. Ambient homology alone is therefore not a functional
  obstruction; only that first actual moment class was tested.
- `PROVED` Cycle 43 constructs one shared repeated-type-symmetric face tensor
  for each of 11,852 selected unordered triples and fills every resulting
  four-face moment cycle: 3,954/3,954 exact integral boundaries, even though
  3,893 ambient complexes have nonzero rational \(H_2\). Independent direct-
  signature replay checks every face, pair marginal, cycle, and fill. The
  3,942 ordinary cases use one tetrahedron; twelve exceptional signed-cube
  cases use seven-term cone fills. This is a finite three-anchor theorem, not
  a natural contraction or full degree-four functional.
- `PROVED` Cycle 44 independently reproduces an outcome-blind non-anchor
  selection from 103,289 candidates and fills all 2,000 canonical moment
  cycles. Exactly 1,528 are explicit distinguished-vertex cones; the other
  472 have exact GF(2) H2 zero and hence are rational boundaries. Every one of
  the 29 positive-H2 interfaces is a cone. Direct-sum decomposition by
  four-type multiset and stabilizer averaging make the selected local fills
  mutually coherent. This is a finite holdout theorem, not a universal
  cone-or-acyclic result or natural contraction.
- `PROVED` Cycle 45 constructs a generic stagewise discrete-Morse operator
  with exact chain homotopy (dh+hd=I-\pi). On all 5,954 frozen Cycle 43/44
  interfaces, the initial and extended schedules leave respectively 470 and
  457 nonzero projections, all known rational boundaries. Exact searches find
  2,647 arbitrary and 649 locally signature-realizable models with genuinely
  nonboundary projections, proving that local blocker/signature geometry is
  insufficient. The missing discriminator must use global p199 type and
  marginal closure; this is not a degree-four functional or LRC(13).
- `PROVED` Cycle 46 constructs the exact owner-star Čech total complex and
  fills all 457 frozen Cycle 45 residuals over the rationals. Witness supports
  range from 6 to 178, and an independently written reversed-pivot replay
  checks all three solver classes. The augmentation is a chain resolution and
  homology isomorphism, proving that this localization adds no global
  relation: it is a coordinate reformulation of ordinary boundary membership.
  The missing mechanism must enforce compatibility among repeated labeled
  faces, not perform another local fill.
- `PROVED` Cycle 47 gives an exact equivalence between raw occurrence-labeled
  and compressed unordered-face affine descent. On an outcome-blind connected
  patch of 256 previously untested p199 quadruples, one canonical lower-
  transport face rule fills every row across a face-incidence graph of cycle
  rank 447. A full independent audit reconstructs all 185 face classes, 1,024
  occurrences, 839 gluing identifications, and 256 fills with zero residuals.
  This is a finite global-section theorem, not universal sheaf acyclicity or
  a new universal construction; the section itself reuses the Cycle 43/44
  canonical rule.
- `PROVED` Cycle 48 gives a closed Möbius formula for three compatible pair
  transports, a universal zero-pair-marginal signed-cube move, and a
  terminating triangular repair criterion. An outcome-blind 512-face corpus
  repairs completely (12 strong and 500 targeted), with full independent
  selector and reverse-order replay. All 314 starts having an initial
  forbidden defect exhibit a literal nonjoinable reached diamond. This
  refutes confluence as the universal gate without refuting deterministic
  repair; the finite corpus is not a universal p199 constructor.
- `PROVED` Cycle 49 proves the relative diagonal-fiber packet theorem under
  its frozen buffers and audits all 382,453,319 raw-valid unordered p199 type
  triples independently. It closes 382,453,314 exactly; five interfaces fail
  only the pairwise-distinct surrogate. Exact cube-kernel elimination fills
  the first `(4,4,5)` exception with an allowed repeated-owner alternative,
  so it is `BUFFER_INCOMPLETE`, not terminal homology. The remaining labels
  are `(4,4,6)`, `(4,4,64)`, `(4,5,35)`, and `(4,6,35)`. This authorizes one
  deletion-aware pattern theorem, not five repairs or a claimed universal
  contraction.
- `PROVED` Cycle 50 tests the sole allowed deletion-aware triple-packet
  relaxation on every 29,050 raw-valid `(2,2,2)`/`(2,2,4)` p199 interface.
  It contracts 29,048, including three C49 residuals, but independently
  reproduces two `PAIR_01` buffer failures at `(4,5,35)` and `(4,6,35)`.
  This falsifies the frozen triple-only theorem. The remaining idea would be
  a distinct pair-fiber method, but the C50 stop rule bars adding it here;
  Problem 1 is paused rather than patched.
- `PROVED` Cycle 51 completes an exact 840-row test of Zhao's
  conjugacy-averaging comparison for the Möbius graph: all indicators on
  (S_3,D_8,Q_8) and all distinct subgroup-product indicators in (S_3,S_4)
  are nondecreasing under class averaging, with independent reverse-order
  replay and direct (S_3) controls. This finite result does not approach a
  proof of the universal comparison, so the group census is closed rather
  than enlarged. The next distinct engine is exact fixed-density variation.
- `PROVED` Cycle 52 completes the frozen exact p=1/2 local-variation census:
  all 512 primitive symmetric zero-mean equal-block 2/3-step directions have
  a positive first nonzero coefficient (489 at degree two, 23 at degree four),
  with complete independent reverse-edge replay. This excludes no unequal,
  nonsymmetric, higher-rank, other-density, or global competitor. C53 is the
  analytic arbitrary-finite-rank quadratic/Hessian-kernel question, not a
  larger step-matrix census.
- `PROVED` Cycle 53 proves directional local stability at \(W\equiv1/2\) for
  every nonzero bounded **symmetric** zero-mean kernel: the exact quadratic
  form is \(30\,2^{-13}\|d_U\|_2^2\), while its zero-degree kernel has zero
  cubic coefficient and positive quartic coefficient
  \(5\,2^{-11}\operatorname{tr}(T_U^4)\). This is not uniform, not at other
  densities, and not Sidorenko. C54 tests the genuinely bipartite,
  nonsymmetric tangent space rather than treating symmetry as harmless.
- `PROVED` Cycle 54 extends the local theorem to every bounded nonzero
  mean-zero **bipartite** kernel at every fixed \(p\in(0,1)\): the quadratic
  form is \(15p^{13}(\|a\|_2^2+\|b\|_2^2)\), and on the two-sided degree
  kernel the five-cycle quartic term is
  \(5p^{11}\operatorname{tr}((T_UT_U^*)^2)>0\). It is direction-dependent,
  not a uniform neighborhood or global theorem. The next gate is Zhao's
  genuinely nonlocal conjugacy-averaging bridge, not further local analysis.
- `PROVED` Cycle 55 checks 1,360 exact finite points in a frozen S3
  class-zero symbolic packet, with no negative Zhao deficit. A pre-promotion
  missing dyadic denominator briefly created six false rows; independent
  cleared-value replay contained and removed them before sealing. This does
  not give positivity between sampled points or beyond the packet. C56 asks
  the sharper universal one-orbit smoothing question.
- `PROVED` Cycle 56 checks all 729 ternary S3 functions under smoothing each
  nontrivial conjugacy class (1,458 exact comparisons). Both exact evaluators
  find no reversal. This is a finite falsifier packet only; it does not give
  orbitwise Schur-convexity. C57 seeks a group-uniform conditional-variance
  identity, where a single rational reversal remains decisive.
- `PROVED` Cycle 57 computes the full exact S3 3-cycle symbolic smoothing
  deficit and refutes one frozen 756-column positive-monomial Handelman cone:
  the coefficient functional \([c_e^3c_T^6c_C^4t^2]\) is \(-35,400\) on
  the target and nonnegative on every basis term. This is a cone-specific
  no-go, not a smoothing counterexample. C58 permits Gram squares, whose
  cancellations are outside that cone.
- `PROVED` Cycle 59 excludes the frozen Pólya coefficientwise certificate
  through multiplier degree 24: 928 of 9,857 coefficients remain negative at
  the cap. The result is a bounded multiplier-family no-go, not a Zhao
  counterexample.
- `PROVED` Cycle 61 gives strict local endpoint comparison near the four
  positive central S3 bases `(1,1,1)`, `(1,2,1)`, `(2,1,2)`, and `(2,2,2)`.
  The full kernel quartic is positive, the central-transverse Hessians factor
  by `(c_C-c_e)^2` with positive quotient, and the only allowed cubic has a
  fourth-order central-displacement zero. This is local S3 evidence only;
  it does not prove Zhao's comparison or Sidorenko.
- `PROVED` Cycle 62 finds no negative deficit among all 118,755 height-24 S3
  simplex rows, and all 61 exact full-KKT grid rows are central. The exact
  exchange derivatives factor by class differences, but their quotients have
  mixed coefficients and fail the frozen Pólya ladder through degree 24.
  `OBSERVED` 300,000 exact denominator-1000 samples also have no negative row.
  None of this classifies the continuous KKT system.
- `PROVED` Cycle 63 gives an exact continuous S3 quotient.  The deficit is a
  weighted-degree-15 polynomial in `(e,t,c,r2,u,s2)` on an explicitly proved
  semialgebraic realizability region; an independently verified enlarged
  `S3 x C2` symmetry removes the anticipated orientation invariant.  The
  equivalent elementary-invariant form yields exact multiplicity-stratified
  stationary equations.  A 300-second modular Groebner tranche reached its
  wall cap before a basis, and 300,000 deterministic exchange probes found no
  reversal.  The latter are `OBSERVED`; positivity, zero-dimensionality,
  Zhao comparison, and Sidorenko remain unproved.
- `PROVED` Cycle 64 classifies every fixed outer S3 invariant fiber.  Its
  minima lie on four explicit endpoint families or among at most 156 isolated
  algebraic pairs.  The `12 x 12` derivative Sylvester determinant has exact
  `u` degree 26 because its leading coefficient is a nonzero rational
  constant, so the reduction has no genericity exception.  This count is per
  fiber: the branches still vary over a three-dimensional outer continuum,
  and no sign, Zhao, or Sidorenko conclusion follows.
- `PROVED` Cycle 65's exact normalized denominator-4 `2 x 2` step-kernel grid
  has 0 negative, 809 constant-on-effective-support zero, and 2,316 positive
  rows; all 96 retained candidates rounded to denominator `10^9` are strictly
  positive. `OBSERVED` three deterministic searches totaling 3,072,000 trials
  found no exact counterexample or reusable extremal reduction. This is not
  continuous `2 x 2` positivity or a Sidorenko theorem. The frozen hard stop
  therefore pauses those engines and rolls 95 unused cycles into the shared
  project bank.
- `PROVED` Cycle 66 traces C63--C64 to the exact fixed-`S3` instance of Zhao's
  Theorem 1.3 comparison for the Möbius graph. Completing that sign would be a
  full continuous nonabelian case, but would not imply the all-group hypothesis
  or Sidorenko. `OBSERVED` a bounded primary-source search found no prior
  fixed-`S3` theorem or semialgebraic reduction; novelty remains `CONJECTURED`.
  The user-directed pivot targets boundary positivity with a new domain-aware
  exact engine, not another census or coefficientwise ladder.
- `PROVED` Cycle 67 proves (N(a)-N(a^{cl})\geq0) on all four C64 endpoint
  families. Nine exact radial charts reduce the equality geometry to the
  squared curves `1-y-3x+xy=0` and `3x-1=0`; 31 exact tensor-Bernstein charts
  cover every exceptional divisor. A clean replay independently expands the
  frozen source and invariant polynomials and matches all nine charts
  coefficient-for-coefficient. This is a boundary theorem only: interior
  fiber critical points, the full fixed-`S3` comparison, Zhao's universal
  hypothesis, and Sidorenko remain open.
- `PROVED` Cycle 68 closes the full fixed-`S3` comparison: for every
  nonnegative \(a:S_3\to\mathbb R\), \(N(a)\geq N(a^{cl})\).  The exact
  identity \(P=P_0+s_2G\), C67's complete \(s_2=0\) face, and an exact
  18-chart primary/secondary equality-blow-up certificate prove the result.
  A replay reconstructs the degree-15 six-value source and verifies the
  terminal charts independently. This is a publishable scoped theorem, not
  Zhao's all-group hypothesis or a Sidorenko proof.
- `PROVED` Cycle 69 verifies the published 13-edge intersecting 6-partite
  equality control and proves that every minimum cover after each edge deletion
  admits no equal-size replacement from the deleted edge. This shuts the raw
  local-exchange mechanism: its failure is forced already by \(\tau=5\), so it
  provides no discrimination for a hypothetical \(\tau\ge6\) counterexample.
- `PROVED` C70's exact equality control realizes 64 distinct deletion-cover
  part profiles, so part occupancy is not a usable witness invariant. The
  primary literature confirms the exact Gyárfás equivalence with covering a
  six-edge-colored complete graph by five monochromatic components. The
  witness-design branch is deferred rather than overfit; the next state space
  is equivalent, not a relaxation.
- `PROVED` C71 proves that a hypothetical \(r=6,\tau=6\) counterexample has
  at least five excess pair intersections. Its exact 11-edge \(D=5\)
  high-star equality core is satisfiable, so local defect incidence cannot
  upgrade the bound or prove a cover; any continuation needs a genuinely
  global invariant.
- `CONJECTURED`: the tractability order above maximizes the probability that
  early closure creates rollover capacity for the harder problems.

## Open questions

1. Can the C68 secant certificate be compressed into a representation-
   theoretic or conditional-expectation identity that applies to the
   subgroup-product hosts Zhao requires?
2. Does the complete family of deletion witnesses \((e,C_e)\) in an
   edge-minimal hypothetical \(r=6,\tau\ge6\) system satisfy a forced
   incidence, Hall, or double-counting inequality incompatible with six parts?
3. Can a global invariant couple the high-star defect core to the rest of a
   hypothetical counterexample strongly enough to yield a five-block cover?
3. Does any successful `S3` argument expose an invariant that survives on the
   decisive `(S_n,1_(T1 T2))` subgroup-product family?

## Next authorized action

Open E001 (legacy Cycle 102 / B102) only under a preregistration freezing the
reciprocal-even quartic-character map on \(\mathbb F_{167}\), its 84-coordinate
PAF/row-sum vector, and exact pair-sum completion. Run no arbitrary-sequence
search, SAT, local search, or new character family. A no-hit closes only this
constructor; a hit requires independent all-shift, block-product, eligibility,
and overlap checks before any Hadamard claim.

## Crash recovery

From the repository root:

```sh
git status --short
sed -n '1,260p' projects/open-conjecture-sweep/PROGRAM.md
find projects/open-conjecture-sweep -maxdepth 3 -type f | sort
```

Then read only the live preregistration and newest durable artifact, if one
exists. `PROGRAM.md` is strategic state, not evidence. Keep exploratory work
in `discovery/`, proof-grade work in `proof/`, and generate `STATUS.md` only
for an intentional handoff.
