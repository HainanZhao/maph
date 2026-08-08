# PROGRAM: structural three-dimensional Ising investigation

## Objective, boundary, and gate

- Objective: discover an exact finite-lattice representation of the
  zero-field ferromagnetic simple-cubic Ising partition function that gives a
  demonstrable structural or complexity reduction and can plausibly control
  the thermodynamic limit.
- Current stage: the post-review character-duality correction is closed and
  publicly released at version DOI `10.5281/zenodo.21848792` (concept DOI
  `10.5281/zenodo.21845272`).  The unsupported original version DOI
  `10.5281/zenodo.21845273` was retracted and now resolves only to a Zenodo
  tombstone.
- Closed gate: the arbitrary-width internal-cut proof now uses the correct
  crossed character table `lambda_a <-> PD(b)`, `lambda_b <-> PD(a)`, and a
  pushed-off meridian proof for H3.  The affected exact rank and
  denominator-free-core certificates were replayed independently before the
  corrected release.
- `G1` holds for generic independent nonuniform weights: for every `w>=3`,
  `R_infinity(w)=d_w=2^(w^2-1)`, and `n=11` is uniformly sufficient.  The
  lower bound uses separate normal/opposite one-sided encoders and an
  invertible two-slab buffer, not the falsified direct tree gluing.
- The intrinsic separator theorem, sharp toroidal `K_(3,3)` chain corollary,
  all-q Walsh-marginal algorithm, and embedding-robustness classification are
  sealed as Upgrades 2--4.
- Target claim boundary after correction: the complete all-spin-structure tensor has an exact TT/MPS
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
- Character-duality correction:
  `artifacts/cycle-18-b18-character-duality-correction-v3.json` supersedes its
  two same-cycle sealing corrections.
- Corrected publication:
  `artifacts/zenodo-canonical-spin-structure-compression-published-v3.json`.
  It supersedes the v2 publication after adding the explicit exposed-longitude
  H1 proof and telescoping endpoint normalization.  The v1 publication
  artifact and retracted DOI are unsupported historical records, not replay
  obligations.

## Strategic next action

No further correction action is open.  Preserve the limitation that the
homogeneous result is width three only, the cubic carrier is still
`2^(L^2-1)`, and the three-dimensional Ising model is not solved.  The next
research question requires an explicit user direction.
