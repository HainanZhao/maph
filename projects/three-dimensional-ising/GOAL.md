# Goal: finish the Lane B separator-compression paper

Revise *Separator Compression of the Complete Spin-Structure Family for
Cubic-Lattice Ising Strips* into a self-contained, reproducible manuscript.
This is the remaining project goal. It does not authorize a claim that the
three-dimensional Ising model is solved, a thermodynamic limit, or an exact
critical temperature.

## Claim and verification discipline

- Use `\proved` only when the manuscript itself contains the complete
  argument. Every `\proofpending` environment must state in one sentence the
  exact missing step; if only a dependency is missing, name that dependency.
- When computation enters a promoted claim, require an independent exact
  replay over both primes `1,000,000,007` and `1,000,000,009`. Finite
  computation is an audit firewall, never an arbitrary-width proof.
- Before each task, freeze its acceptance criterion, kill/escalation
  criterion, conventions, ranges, and replay command in `discovery/`.
- Record a failed path by naming the false step, not merely its correction.
  Do not silently patch a failed symbolic family.
- Phase 1 is blocked until all three Phase 0 obligations are green.

## Phase 0: blocking obligations

### T1. Symbolic boundary-incidence proof for the encoder lemma

The incidence tables now printed in the manuscript are provisional. Replace
manual transcription by a symbolic generator, parametric in width and split
by parity, which:

1. enumerates every boundary edge of the normal sets `I_3`, `I_5`, and
   `I_{2,r}`, and of the opposite-phase set `C_W`;
2. classifies every edge into the appropriate gauge/exceptional/retained,
   internal-face, or large/old-component class;
3. emits the finite period-two parity-pattern table used by the proof; and
4. agrees with brute-force face-dual calculations for widths `4..8`.

The opposite phase is the translated restriction of the single global
checkerboard rotation to longitudinal layers `1..5`; the normal phase is its
restriction to layers `0..4`.

Acceptance: the generated Appendix C table is exhaustive in every parity
case, the width `4..8` firewall agrees, both relevant prime replays pass when
arithmetic enters, and the complete symbolic induction justifies promoting
`lem:encoders`.

Kill/escalate: any edge outside the declared trichotomy invalidates the
island/cut decomposition. Report that edge family and re-examine the encoder
recurrence; do not repair one row locally.

### T2. Denominator-free polynomial-ring tensor train

Construct the all-sector tensor train over `Z[t_e]`, not merely over its
fraction field:

1. fix one global cochain gauge and a filtration-compatible completion-tree
   system;
2. define every edge block `E_j` and its local phases `Q_j,H_j` as
   restrictions of that global data;
3. prove coefficientwise telescoping for every even subgraph and mask
   sequence, including the absence or explicit absorption of all junction
   cross terms; and
4. compare dense core contractions with literal pre-Arf enumeration at
   `(n,w)=(6,3),(7,3),(4,4)`, using exact polynomial comparison where
   practical and otherwise two independent evaluations over each prime.

Acceptance: a written telescoping lemma proves that the cores reproduce every
term exactly once over `Z[t_e]`; `thm:grid-upper` is correctly restated over
that ring; the marginal theorem is unconditional on core existence; and the
two-prime replay is green.

Kill/escalate: localize any failed junction as either an incompatible
completion-tree choice or a genuine residual junction phase. A genuine
residual phase is a reportable separation between fraction-field and
polynomial-ring bonds and must not be hidden.

### T3. Complete label and dependency audit

Audit `prop:genus`, `lem:canonical`, `lem:grid-exact`, `lem:encoders`,
`thm:grid-upper`, `lem:XYfull`, `thm:grid-tight`, and `thm:k33`.

For each statement, either supply a complete self-contained proof and promote
it, or attach an exact one-sentence gap statement at the environment. Print
an acyclic dependency graph and the propagation rule in the revision-status
box. Conservative dependency cascades must be explicit rather than silent.

Acceptance: every label is locally justified, every pending dependency is
named, and no theorem is promoted solely from a finite-field certificate.

## Phase 1: upgrades after Phase 0 closes

### T4. Homogeneous anisotropic and isotropic width-three locus

Restrict the existing `G_{10,3}` paired-cycle minor first to
`Z[t_x,t_y,t_z]` and then to `Z[t]`. Use preregistered random nonvanishing
gates over both primes, followed by exact interpolation or symbolic
elimination if all gates vanish.

Either prove generic rank `256` on a nonempty open anisotropic/isotropic
locus, with isolated univariate exceptions stated precisely, or exhibit the
restriction's vanishing ideal as a structural separation. Do not generalize
from width three without a proof for the encoder minor.

### T5. Short paired-cycle generalization probe

Decode the geometry of the width-three chord set
`{44,52,103,110,112,118,120,162}` and look for a width-parametric family.
Continue only if an explicit pattern gives the target rank at width four over
both primes. Otherwise record the negative working result and stop this
probe; the encoder route remains primary.

### T6. Tensor-network translation

Add an approximately two-page MPO/MPS interpretation containing only
cross-referenced proved results: the pre-Arf tensor as a disorder-parameter
MPO, separator masks as virtual indices, the TT-rank/minimal-bond dictionary,
H1--H3 as virtual gauge conditions, and the Walsh-marginal environment sweep.
State the actual marginal cost consistently with the proved theorem.

### T7. Optional second application

Only if T4 closes quickly, test one genuinely non-grid strip family, such as
a honeycomb or triangular-lattice tube, against H1--H3. Stop if verifying the
relative-chain hypotheses becomes comparable in difficulty to the grid
proof; this task must not delay T4 or T6.

## Completion criteria

The goal is complete only when Phase 0 is fully discharged, the manuscript
and independently compiling source bundle pass their replay and claim audits,
and Phase 1 has reached its specified theorem, structural-negative, or
timeboxed terminal outcomes. Then build the deterministic DOI-bearing
archive, verify extracted replay/checksums/preview ordering, and publish a new
Zenodo version under the repository's standing publication authorization.

Preserve the final limitation: for cubic boxes the transverse carrier remains
`2^(L^2-1)`. The work removes genus-sector redundancy; it does not remove the
physical area-law barrier or solve the cubic Ising model.
