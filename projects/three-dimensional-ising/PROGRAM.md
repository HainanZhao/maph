# PROGRAM: structural three-dimensional Ising investigation

## Objective, boundary, and gate

- Objective: discover an exact finite-lattice representation of the
  zero-field ferromagnetic simple-cubic Ising partition function that gives a
  demonstrable structural or complexity reduction and can plausibly control
  the thermodynamic limit.
- Current stage: the four-upgrade Lane B campaign in `LANE_B_GOAL.md` is
  complete.  The authoritative records are Cycles 8--11, with the corrected
  Cycle 8 v2 artifact superseding its nondeterministic v1 artifact.
- The user-authorized paper campaign has produced the integrated manuscript
  `paper/canonical-spin-structure-compression/main.tex` and compiled PDF.  It
  includes the abstract separator theorem, grid upper bound, generic
  minimality, sharp `K_(3,3)` obstruction, all-q marginal algorithm,
  robustness boundary, exact validation, and failure ledger.  It has not
  been submitted or published.
- `G1` holds for generic independent nonuniform weights: for every `w>=3`,
  `R_infinity(w)=d_w=2^(w^2-1)`, and `n=11` is uniformly sufficient.  The
  lower bound uses separate normal/opposite one-sided encoders and an
  invertible two-slab buffer, not the falsified direct tree gluing.
- The intrinsic separator theorem, sharp toroidal `K_(3,3)` chain corollary,
  all-q Walsh-marginal algorithm, and embedding-robustness classification are
  sealed as Upgrades 2--4.
- Claim boundary: the complete all-spin-structure tensor has an exact TT/MPS
  of bond at most `d_w` for arbitrary `n,w` and arbitrary nonuniform edge
  weights in the declared embedding, and this carrier is generically minimal
  for every width.  The lower bound does not extend automatically to
  homogeneous anisotropic or isotropic weights or to a specified temperature.
  No compression below the growing transverse carrier, controlled 3D
  thermodynamic limit, exact critical temperature, or critical exponent is
  claimed. The model is not solved.
- No Lane B upgrade gate remains active.  Any new thermodynamic,
  homogeneous-weight, submission, or publication campaign requires an
  explicit user-selected scope.

## Authoritative verification

- Upgrade 1: `artifacts/cycle-8-b11-g1-generic-tightness-v2.json`.
- Upgrade 2: `artifacts/cycle-10-b9-abstract-separator-k33-sharpness-v1.json`.
- Upgrade 3: `artifacts/cycle-9-b8-lane-b-all-q-marginals-v1.json`.
- Upgrade 4: `artifacts/cycle-11-b10-lane-b-embedding-robustness-v2.json`
  extends v1 with an exhaustive same-cubic-grid rotation obstruction.
- Every artifact's immutable `--check` replay passes in the pinned runtime.

## Strategic next action

Human manuscript review or an explicitly requested submission/publication
campaign.  Preserve the exact claim boundary: G1 proves an area-exponential
barrier for this representation; it does not solve the cubic Ising model.
