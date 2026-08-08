# PROGRAM: structural three-dimensional Ising investigation

## Objective, boundary, and gate

- Objective: discover an exact finite-lattice representation of the
  zero-field ferromagnetic simple-cubic Ising partition function that gives a
  demonstrable structural or complexity reduction and can plausibly control
  the thermodynamic limit.
- Current stage: the Lane B paper's Phase 0 proofs and Phase 1 upgrades have
  reached their prescribed terminal outcomes, and the deterministic release
  is public at version DOI `10.5281/zenodo.21845273` (concept DOI
  `10.5281/zenodo.21845272`).
- Active gate: closed.  The archive was built twice byte-identically, checked
  after extraction, replayed through the authoritative Cycle 7--17 records,
  uploaded with verified checksums, and published with the main PDF as the
  public default preview.
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
  for every width.  At width three, one frozen minor remains generically
  nonzero on the homogeneous anisotropic locus and on the isotropic line
  outside a finite algebraic exceptional set.  This does not extend
  automatically to arbitrary homogeneous width or a specified temperature.
  No compression below the growing transverse carrier, controlled 3D
  thermodynamic limit, exact critical temperature, or critical exponent is
  claimed. The model is not solved.
- The symbolic encoder-incidence proof and independently generated
  width firewall close Lemma 6.1 in Cycle 12 v2.  The label audit now
  separates completed geometry, lower bounds, and the K_(3,3) obstruction.
  The planar-arc coboundary lemma closes the former exposed-longitude support
  gap uniformly, without a width-by-width table.  Finite-width replays are
  audits only.

## Authoritative verification

- Upgrade 1: `artifacts/cycle-8-b11-g1-generic-tightness-v2.json`.
- Upgrade 2: `artifacts/cycle-10-b9-abstract-separator-k33-sharpness-v1.json`.
- Upgrade 3: `artifacts/cycle-9-b8-lane-b-all-q-marginals-v1.json`.
- Upgrade 4: `artifacts/cycle-11-b10-lane-b-embedding-robustness-v2.json`
  extends v1 with an exhaustive same-cubic-grid rotation obstruction.
- Encoder incidence proof:
  `artifacts/cycle-12-b12-encoder-incidence-proof-v2.json` supersedes v1's
  over-broad sealing scope and closes the normal/opposite boundary tables.
- Polynomial-ring all-sector cores and Phase 0 closure:
  `artifacts/cycle-13-b13-polynomial-tt-grid-cores-v1.json`.
- Width-three homogeneous locus:
  `artifacts/cycle-14-b14-homogeneous-w3-v2.json` supersedes v1's volatile
  benchmark payload.
- Paired-cycle probe terminal negative:
  `artifacts/cycle-15-b15-paired-cycle-probe-v1.json`.
- Tensor-network translation:
  `artifacts/cycle-16-b16-tensor-network-translation-v2.json` supersedes v1's
  corrected dependency.
- Optional second-application stop:
  `artifacts/cycle-17-b17-second-application-probe-v1.json`.
- Publication:
  `artifacts/zenodo-canonical-spin-structure-compression-published-v1.json`;
  the earlier draft-reservation artifact remains historical only.
- Every authoritative artifact's immutable `--check` replay passed in the
  pinned runtime from the extracted public archive.

## Strategic next action

No in-scope work remains for the paper goal.  Any post-publication manuscript
or archive change requires a new Zenodo version.  Preserve the limitation
that the homogeneous result is width three only, the cubic carrier is still
`2^(L^2-1)`, and the three-dimensional Ising model is not solved.
