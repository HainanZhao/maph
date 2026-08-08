# PROGRAM: structural three-dimensional Ising investigation

## Objective, boundary, and gate

- Objective: discover an exact finite-lattice representation of the
  zero-field ferromagnetic simple-cubic Ising partition function that gives a
  demonstrable structural or complexity reduction and can plausibly control
  the thermodynamic limit.
- Current stage: the four-upgrade Lane B research campaign is sealed, but the
  paper is in an active self-contained-proof revision cycle.  The manuscript
  is not submission-ready and has not been submitted or published.  Zenodo
  version DOI `10.5281/zenodo.21845273` is reserved in an unsubmitted,
  zero-file draft; it is not yet registered or public.
- Active gate: a referee must be able to verify the grid upper bound and
  arbitrary-width generic saturation from the manuscript and its readable
  appendices, without treating scripts or JSON artifacts as proofs.  The
  required proof chains are the checkerboard ribbon geometry, explicit
  H1--H3 representatives, complete normal/opposite encoder inductions, the
  printed `K_(3,3)` minors, and the human-readable width-three
  specialization.  The grid theorem has been explicitly weakened to a
  fraction-field TT; a denominator-free polynomial-ring TT is quarantined as
  a separate unproved refinement rather than a submission gate.
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
- No new thermodynamic or homogeneous-weight claim is authorized in this
  revision.  Lemmas 4.2, 5.1, and 6.1 remain manuscript-level open gates
  until their self-contained arguments are complete; finite-width replays
  are audits only.

## Authoritative verification

- Upgrade 1: `artifacts/cycle-8-b11-g1-generic-tightness-v2.json`.
- Upgrade 2: `artifacts/cycle-10-b9-abstract-separator-k33-sharpness-v1.json`.
- Upgrade 3: `artifacts/cycle-9-b8-lane-b-all-q-marginals-v1.json`.
- Upgrade 4: `artifacts/cycle-11-b10-lane-b-embedding-robustness-v2.json`
  extends v1 with an exhaustive same-cubic-grid rotation obstruction.
- Publication reservation only:
  `artifacts/zenodo-canonical-spin-structure-compression-draft-reservation-v1.json`.
  This is not a proof or publication artifact.
- Every artifact's immutable `--check` replay passes in the pinned runtime.

## Strategic next action

Finish the two explicit boundary-incidence tables for the normal islands and
opposite cut, then return to the still-pending co-core/collar topology and
H1--H3 triangular-correction proof.  After those mathematical gates, perform
the final claim/dependency audit and build the deterministic DOI-bearing
archive for the reserved Zenodo draft.  Preserve the exact claim boundary:
the proposed G1 theorem concerns generic independent weights in this
representation and does not solve the cubic Ising model.
