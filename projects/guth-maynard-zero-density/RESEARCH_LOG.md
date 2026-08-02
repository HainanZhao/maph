# Research log: Beyond Guth--Maynard Zero Density

This is the append-oriented chronological memory for the project. `PLAN.md`
contains only current strategy and status. Material claims retain the tags in
the repository `AGENTS.md`; detailed row registries and proofs live in the
versioned artifacts and documents linked below.

## Cycle 0 — project selection and baseline (2026-08-01)

- `OBSERVED`: T1.1 was selected: improve the Guth--Maynard density exponent
  or delimit saturation, propagate to short intervals, and map other
  L-functions.
- `PROVED` from the cited Guth--Maynard statements: baseline exponents are
  `30/13`, uniform `17/30`, and almost-all `2/15` under the frozen counting
  conventions.
- `OBSERVED`: arXiv:2507.08296 is prior Dirichlet-L work; later source checks
  identified the three-author v2 dated 27 July 2026. P6 must concede it.

## Cycle 1 — arithmetic reconstruction (2026-08-01)

- `PROVED` exact arithmetic: two independent implementations agree on all 24
  labeled baseline, bottleneck, Theorem 1.2, crossover, and short-interval
  formula outputs. Authority:
  `artifacts/cycle-1-route-reconciliation-v3.json` (31-test replay).
- `PROVED` conditional on the published analytic inputs: at
  `sigma=7/10`, the two active large-value terms tie at `2/3`, all three
  energy terms tie at `5/3`, and local aggregation gives `9/13`.
- `OBSERVED` correction: exact assertions rejected two hand-entered spot
  values before certification; the midpoint margin was corrected to `1/54`.
- `OBSERVED`: the original Ingham PDF remained inaccessible and bibliographic
  pagination conflicted; Huxley's published restatement supplies the used
  exponent/range. MP Lemma 24 and several detector/explicit-formula inputs
  remained open at this stage.

## Cycle 2 — complete G0 reconstruction (2026-08-01)

- `PROVED` conditional reconstruction: two routes reconcile all 7 Stream-B
  rows and all 26 Stream-C rows; 15 inherited dependency nodes and 8 source
  gates close. Final authority:
  `artifacts/g0-full-reconstruction-v3.json`, replay
  `proof/run_g0_replay_v4.py`.
- `OBSERVED` six-route resources: wall times
  `0.03/0.16/0.04/0.08/0.14/0.34` seconds and RSS
  `17280/18560/19200/52736/44640/43392` KiB. Evidence:
  `artifacts/g0-six-route-resource-gate-performance-v2.json`.
- Preserved corrections:
  - official Kedlaya DSpace `Publication` bytes replaced an unsupported
    author-copy/license premise;
  - an overbroad Chourasiya--Jha--Kaur range was rejected and replaced by the
    checked Huxley branch;
  - dynamic matrix v2 had been refreshed in place; matrix v3 records the old
    identity as `UNRECOVERABLE_FROM_LOCAL_WORKTREE`;
  - G0 v1 was premature because it omitted two Cycle-1 resource routes;
  - `python3 -O` bypassed G0 v2 bare assertions. V3 explicitly rejects
    `-O/-OO` and is final.
- `PROVED`: G0 PASS reconstructs published `30/13`, `17/30`, and `2/15`; it
  is not a new theorem.

## Cycle 3 — critical atlas and G1 `NO_SELECTION` (2026-08-01)

- `PROVED` exact structural atlas: independent recomputation agrees on 7,744
  local rows, 704 energy rows, and 560 transfer rows. Final authority:
  `artifacts/cycle-3-g1-exact-structural-atlas-v2.json`, SHA-256
  `fd66d17664ca921795617c6bfca76c3be49246ea9351644848a2aadf9e680b08`.
- Preserved exact-atlas correction: v1's preregistration builder allowed
  optimized mode and duplicated grids; v2 imports corrected conventions,
  pins CPython 3.12.3/mpmath 1.2.1, and records convention hash change
  `3d3cef60... -> 642a61fc...`.
- `OBSERVED` empirical atlas: two fresh v4 runs agree byte-for-byte on 588
  rows—429 completed, 159 failed, zero retained, zero validation. Authority
  SHA-256:
  `4e3adc2885a9c441d0006633355b8be87d39599bc93ca68d1270475b27111a88`.
  Engine v1 launch, v2 runtime/checkpoint, and v3 cache/payload defects remain
  preserved.
- `CERTIFIED_NUMERICAL` at `U=2^12`: 434 feasible rows, 154 construction
  failures, zero energy-retention rows, all with positive margins. Authority
  SHA-256:
  `bf050f6186ab2bab247cfb18bc628168149354cc64da8773879e95e56a991fc6`.
  This is not an asymptotic obstruction.
- `PROVED` exact envelope sensitivity: LV3 is the sole zero-residual transfer
  term; right-only or endpoint-only gain does not lower the strict left
  `30/13` supremum. Authority SHA-256:
  `850b825698722d628340b762867c98774dae53443aecde581138c6830993b60e`.
- `OBSERVED` literature audit concedes CGL-v2 overlap for cubic, affine/GCD,
  energy, and Dirichlet-L mechanisms; a Guth-survey sign discrepancy is
  contained. Correction SHA-256:
  `f56529c5919971385cc583b51255636022a5b33fb0cfd4857a587f1d3e099076`.
- Preserved G1 decision correction: v1 had incomplete affirmative predicates
  and no executable binding. Corrected v2 is no-selection-only and returns
  `NO_SELECTION`; no P2 route is selected or refuted. Authority SHA-256:
  `87e697850dea074664227f6be5b187cc12ab4491bad6d2bda0065ee9df1b3872`.

## Cycle 4 — source-anchored recovery and P6 (2026-08-01)

### P1R preregistration correction chain

- `OBSERVED`: v1 failed replay/source/status checks; v2 failed mutable-PLAN
  lifecycle coupling; v3 fixed lifecycle coupling but omitted direct GM
  Theorem 1.1 attribution for `[6,8,8]`.
- Corrected v4 pins the immutable authorization snapshot and source ledger;
  artifact SHA-256
  `e2aeec9ec90e1fea0a9eade53d5ff1e57020df48bd92ae852121a941fbadd7f9`.
  Historical v1-v3 records remain immutable.

### P1R-FS fixed-splice theorem

- `PROVED` conditional on the checked Huxley restatement: retaining
  `I(sigma)=3/(2-sigma)` on `1/2<=sigma<7/10` forces the frozen splice's
  uniform coefficient to be at least `30/13`, regardless of the right branch.
  This is not an actual zero-count lower bound, full-method saturation, a new
  density estimate, or a short-interval theorem.
- Independent routes:
  `artifacts/p1r-fs-route-a-v1.json` and
  `artifacts/p1r-fs-route-b-v1.json`; reconciliation SHA-256
  `2fe46ee076df8b17a93876d76c5b223e1425af831b440dd8f0708f084dbec62b`.

### P1R-CRR formalization and moment reduction

- `OBSERVED`: formalization v1 is `CONTAINED_FAIL`; it suppressed admitted
  finite-`v` slack and incompletely labeled the cubic phase involution.
  Failure artifact SHA-256
  `9cea180d4a649df219d6e8ee9c6a490a279bda7889972e7c9dc70076d584d02f`.
- `PROVED` corrected v2 bookkeeping with
  `delta(v)=1/sqrt(log v)` and `sigma_v=7/10-delta/10`:
  - large-value upper rows: `6+2δ, 8+4δ, 8+4δ`;
  - energy upper rows: `20+5δ, 20+(37/8)δ, 20+5δ`;
  - S3 upper rows: `36+(3/2)δ, 36+3δ, 36+3δ, 36+(45/16)δ`;
  - rational lower moments: `8-3δ, 20-5δ`;
  - exact phase map:
    `conjugate(I_(m1,m2,m3))=I_(-m3,-m2,-m1)`.
- `PROVED` direct Fubini/Cauchy plus the raw-`R` moment arguments yields only
  `integral Rtilde^2=v^(8+o(1))`,
  `integral Rtilde^4=v^(20+o(1))`, and `E(W)=v^(20+o(1))`.
  No incompatibility follows. V2 authority SHA-256:
  `e26be797539eabe53ee765b7067d1c99fe4d440035e27785cf38aa64bc2fc84e`.
- `PROVED` construction-oriented identity:
  `S3_signed=L^3 tr(B_W^3)` for the Hermitian matrix
  `B_W(t,t')=sum_(m!=0) hat(h_(t-t'))(mL)`. Positive cubic size can be sought
  spectrally; individual summands need not be positive.
- `CONJECTURED` bold finite analogue retains all critical balances at
  `H=N^(6/5), R=N^(4/5), Q=N^(2/5), V=N^(7/10)`. Candidate families and the
  proposed 160-row probe are awaiting a separate preregistration; no search
  has run and no negative conclusion is licensed.

### P6 CGL-v2 preregistration and routes

- `OBSERVED` count correction: proposed ranges totaled 47, not 46. Canonical
  L12 now has mandatory `odd_prime` and `two_power` subchecks; L13 is a
  retired alias and no obligation is dropped. Preregistration artifact
  SHA-256:
  `1f9c195fa2dff8a58b754f10a58357384c5e3840839cc48269dd7b595a8ab36a`.
- `OBSERVED` Route A: 46 rows plus both L12 subchecks reconstructed;
  `OPEN_ANALYTIC_INPUT`. Artifact SHA-256
  `f94a7b58f88ccd53ec637349a820bf7df6b86da894a9f9fe48bee58e56d732bd`;
  script SHA-256
  `1ea4dee042050963c55b3b69c06b91a20e766fd9d86ba6efb54a72220d06a1c0`;
  4 tests pass.
- `OBSERVED` Route B: 46 rows plus both L12 subchecks reconstructed;
  `OPEN_ANALYTIC_INPUT`. Artifact SHA-256
  `d107f496c8fd4e52a91eb2637c7edeab0519537fd91d0c3b8c2bf7da7b79f737`;
  script SHA-256
  `28192c7314a46aeca211b8c039e7d02a303e6163f3143aa914d6098fc6e878ca`;
  5 tests pass.
- Both routes preserve the open X/T tail, primitive-to-all transfer,
  undefined `T`-smooth usage, external-input, and multiplicity obligations;
  neither silently repairs the preprint or promotes its `7/3` claim.
- Reconciliation is the next P6 action.

### Workflow correction

- `OBSERVED` user direction: research-stage hostile audits are no longer
  continuation gates. Lightweight source/algebra/replay checks remain; new
  hostile promotion audits are deferred to manuscript/paper stage. Root
  `CLAUDE.md` and `GEMINI.md` symlink to the updated repository `AGENTS.md`.
- `OBSERVED` memory-layout correction: `PLAN.md` is now concise strategic
  state; this file holds chronological cycle summaries, failures, corrections,
  hashes, and replay evidence.

## Preserved failed/deferred/superseded index

- G0 v1 premature; G0 v2 optimized-mode bypass; G0 v3 final.
- Stream-C author-copy/license premise withdrawn; DSpace source chain final.
- CHJ range overstatement withdrawn; checked Huxley route final.
- G1 preregistration draft grid/resource design superseded.
- G1 exact-atlas v1 contained; v2 final.
- G1 probe engines v1-v3 corrected; two fresh v4 runs final.
- G1 route decision v1 contained; v2 `NO_SELECTION` final.
- P2A/P2B/P2C are not selected, not failed, and not refuted.
- P1R preregistrations v1-v3 contained; v4 final historical authority.
- P1R-CRR formalization v1 contained; v2 current research authority.
- Fixed-power and localized `BigN` supplements remain deferred under their
  normalization/localization/endpoint gaps.
- P7's earlier pending state is superseded: the `Q(i)` family is selected and
  P7-1/P7-2 are complete; P7-3 is active. P8 remains deferred pending P7.

## Cycle 5 — CRR limits, P6 repairs, and the selected Hecke family (2026-08-01)

### CRR analytic reductions and finite probe

- `PROVED` conditional on the explicitly `CONJECTURED` Montgomery
  large-values input: an unbounded frozen CRR Base sequence is impossible at
  `sigma=13/20`, and at every fixed `3/5<sigma<7/10`. Saving only one of the
  tied `v^8` terms leaves exponent `8`; fixed savings in both imply CRR-U.
  Artifact SHA-256
  `5d0b5b14df5e6aed5fd28dc1094c36a0b6c6de83da2605a75cbd5d9163154190`.
- `PROVED` scoped no-go: generic spacing, tolerance-one real additive energy,
  and positive `H^-1` smoothing cannot force a fixed power saving for every
  logarithmic alias packet. The construction does not use actual Farey
  `r/s` nodes or a CRR coefficient witness, so those arithmetic routes remain
  open. Artifact SHA-256
  `be9422f9afaa179129f5c46a21ae71220d38545c70ef43c3f293d43e6745b80d`.
- `OBSERVED`: the corrected preregistered finite probe completed all 160 rows
  with `NO_RETAINED_HIT` in 713.816179 seconds and peak RSS 564,809,728 bytes.
  The immutable result has SHA-256
  `41576b9ad21d44435d251a8fefad1cc64bb038384644ce93c1d1a4314c38a0cb`.
  A full semantic replay recomputed every row and matched all deterministic
  fields; replay SHA-256
  `8d4524a43220d067d56d2adb36f33fb8580b732ef9b862d47b582d10e3c35721`.
- `OBSERVED` correction: the result's inherited replay strings named v2 and
  the first results note incorrectly localized misses to cubic agreement.
  The sealed correction records binary64 pass counts: LV `0/160`, energy
  lower `160/160`, upper `147/160`, rational `13/160`, quadrature `10/160`,
  cubic size `160/160`, cubic agreement `0/160`. Non-cubic diagnostics remain
  `OBSERVED`/`EXPLORATORY`; the dual-precision cubic screen is `RECOGNIZED`.
  Correction SHA-256
  `3aedf729001c3d91810035d3d8c30d41540f9c12d077534edcb8a7d4cbbde686`.
  This bounded miss does not refute asymptotic compatibility, and the probe's
  equal-weight phase rounding did not test the proposed leading-eigenvector
  construction.

### P6 reconciliation and repair lemmas

- `OBSERVED`: both 46-row routes and the two L12 subchecks reconcile to
  `OPEN_ANALYTIC_INPUT`. Route B v1's irrelevant arithmetic verifier was
  preserved and corrected. Correction/reconciliation SHA-256 values are
  `42484c02cd9d0defc83224acdc8a6c6763507661c5d0f0875ab934c45b3fa670`
  and `cf59aa63b97d69c672fafa0b0ca49221d9005c3da6ccd61f05d37f4bcbc68e49`.
- `PROVED`: unique primitive induction, finite Euler-quotient zero location,
  conductor partition, and monotone-envelope divisor summation transfer
  primitive bounds to all characters with `tau(q)=q^o(1)`. Artifact SHA-256
  `2edccf46d15229fb8b8ff2c9510d0912f73228da681577ca66d869a8d8acf0d7`.
- `PROVED` conditional on the named external inputs `L_POLY_A`,
  `FOURTH_MOMENT_H`, and `LOW_HEIGHT_MULTIPLICITY_COUNT`: the amended
  `Q=qT` detector cutoff removes the former independent X/T-tail obstruction,
  including fixed-height and compact ranges. V1 SHA-256
  `c672dc559dbbd81b2b30f1a0c8e37354517e43af8da389b89a055504778a118d`;
  canonical-tag correction SHA-256
  `5fef3abecd2f2def93693f2e2c849ac8585b6fe22fb930743df690b359fa34ec`.
- `PROVED` conditional on a multiplicity-inclusive local unit-strip count:
  the multiplicity-weighted count is at most the local factor times the
  distinct-support count, so multiplicity copies never need to enter a
  well-spaced set. This reduces S03 to an S06 source hypothesis. Artifact
  SHA-256
  `6466eabbd5b43bbc5ccd9937e9080bb8dab4ed77b27e4617b675e3546aa71772`.
- `PROVED` under the corrected hypothesis that every prime divisor of `q` is
  at most `T`: the divisor chain covers the full `5/6` interval, including
  prime powers, equality, and compact cases. Later divisors need not remain in
  source Case 2; the valid repair uses the actual fixed-`v` middle
  subdivision. This is not attributed to CGL-v2, whose F08 wording remains
  undefined. Artifact SHA-256
  `5097609783b4e076b268255445e94caeb08bc23f93ad2540703c43e1401ca8af`.
- `OBSERVED` status correction: the immutable smooth-repair v1 used a
  noncanonical compound status. Its deductions are `PROVED` conditional on
  their explicit hypothesis lists; no mathematical or source-boundary change
  was made. Correction SHA-256
  `c8ee4e20a8e96a435e9e2031d5ed126372d8d2a2a9bb0edd4e8e7cf735ebf037`.
- `OBSERVED`: P6 still requires exact S06 primary hypotheses and retains
  conductor-sensitive intermediate formulae. None of these repair lemmas
  promotes the CGL `7/3` claim as a theorem of this project.

### Conditional downstream map

- `PROVED` exact algebra conditional on a genuine global coefficient
  `B_eta=30/13-eta`, `0<eta<4/13`: the uniform endpoint becomes
  `(17-13eta)/(30-13eta)` and the almost-all endpoint becomes
  `(4-13eta)/(30-13eta)`. Artifact SHA-256
  `da4939e8042cb0da64eba2acaee058eafdbebcb8ab90d167ce571dfe83e2170a`.
  No analytic density gain or new prime theorem is claimed.

### P7 finite-order Hecke family over `Q(i)`

- `OBSERVED`: P7 selected primitive finite-order ray-class Hecke characters
  of trivial infinity type with `Q<Nf<=2Q`. The corrected preregistration
  SHA-256 is
  `fa3c98ce481e913f2c8522856114b8cca643d763314e01a36b0aa7cf9110dfc9`.
- `PROVED`: the mod-`(3)` and mod-`(1+i)^4` ray quotients have order two and
  exact conductors; at norm 17 their aggregates are `-2` and `+2`. Also
  `a_Q(i)(n)=sum_(d|n) chi_-4(d)<=tau(n)`. Thus verbatim common-integer-
  coefficient import fails, while character-aware/ideal-indexed routes remain
  open. P7-1 artifact SHA-256
  `200f4328c72e2af2ffe08a9fd3b9901bbbf6b2977c18a34e20a20fb020f033d0`;
  canonical-tag correction SHA-256
  `32d3f2a5ffc8c62e985c7b3c156ddd9c0b00b23908d837b583d806e2c0e05aa8`.
- `PROVED`: exact ray-class orthogonality and the primitive Möbius projector
  hold with the essential coprimality indicator. Thorner 2019, Theorem 2.1,
  restricts to the shell with one common ideal coefficient function and loss
  `(N+4Q^2T^2)(log(2QT))^A`. It does not cover arbitrary character-dependent
  norm-collapsed polynomials. P7-2 artifact SHA-256
  `d4ad1fb81ac2cac49f94fb73616b5134f96fadd86e44f0a94975683b2db0387d`.
- `OBSERVED`: P7-3 must preserve a common ideal sample through the cubic and
  energy steps, handling repeated norms and character coupling. No Hecke
  zero-density or prime-ideal interval theorem has been proved.

## Replay pointers

Run each artifact's recorded `replay` command from the project directory.
Current lightweight checks:

```sh
python3 proof/build_cycle_4_p1r_crr_u_formalization_v2.py --check
python3 discovery/build_cycle_4_p1r_crr_finite_probe_v3_replay_metadata_correction_v1.py --check
python3 discovery/replay_cycle_4_p1r_crr_finite_probe_v3_semantic_v1.py --check
python3 proof/p6_detector_qt_tail_v2_status_correction.py --check
python3 proof/p6_multiplicity_transfer_v1.py --check
python3 proof/p6_tsmooth_corrected_hypothesis_repair_v2_status_correction.py --check
python3 proof/build_p7_ray_orthogonality_v1.py --check
```

## Cycle 6 — actual Farey saturation, P6 closure boundary, and coloured P7-3 (2026-08-01)

### CRR actual-Farey/log-Gram route

- `PROVED` conditional on the frozen RationalMass predicate: the exact
  reduced Farey cells and their true bounded logarithmic jitter force the
  labelled ray bundle at least `(15/8)v^(26-3delta)`. The v1 fixed-jitter
  reduction has SHA-256
  `8f204d56a5609fa9c8a93b152a969a038bc13463d3a36ca746e842bfe21e5f40`.
- `PROVED` conditional on Base cardinality and the checked published raw-R
  L2 lemma: the averaged bundle is at most `v^(26+delta)`. Thus the lower and
  upper central exponents both equal `26`; raw global L2 after discarding the
  coefficient vector cannot supply a fixed saving. This is a saturation
  statement only for that uncoupled step, not for Guth--Maynard as a whole.
  V2 artifact SHA-256:
  `ce59b777ec02769168d9dc330658a0ab1d46b05cdb7ac5dc8115e248d85f8ce8`.
- `CONJECTURED`: AFARI/FARI still requires Base/coefficient coupling or a
  stronger restricted-Farey input. The actual compatible-witness and
  leading-eigenvector routes remain open. V1/v2/formalization replay: 15 tests
  passed; v2 used about 0.04 seconds and 19,072 KiB RSS.

### P6 post-repair reconciliation

- `PROVED`: rerunning the primitive estimate at the exact conductor with
  fresh `q1=d` and only then forming a monotone envelope removes the former
  termwise conductor-domination obligation. Conditional on the primitive
  envelope this gives the all-character divisor-sum transfer. Artifact
  SHA-256:
  `b4c9a30bac20f8b59ecf7e8fdbcb060119d21e29376c3ce6c5ec0cd5335c8d4d`.
- `PROVED`: the S06 source package now supplies polynomial growth with
  exponent `A=3/2`, a multiplicity-inclusive local unit-strip count, and the
  `q>=2` primitive discrete fourth moment in the needed scope. Correction
  chain SHA-256 values:
  `1fbb984c3536c45dedbba36992ef8498cccf21fb7d8e9cab7619b5d2cb14b59a`,
  `a7846345724c5110bc37d14a1ad712182f80f8e56a42ce73309469589df5b3e0`,
  `8566226a67504c91fc2a19e98c7a74c1b805320b825852923b703fb5ce05fb49`,
  and `50330941b45a28e5d248162c5c22a1cb4a0ffe27290c9ae2fd7c6859230ed044`.
- `OBSERVED`: final reconciliation retains all 46 original rows. The exact
  open analytic obligations are the low-value and HMH comparators, S2/AFE,
  character-time energy, the Dirichlet outer Ingham/Huxley inputs, and the
  primitive CGL-style two-term large-value envelope. Therefore no general
  all-character `7/3` theorem is promoted. `q=1` remains covered only by G0's
  zeta `30/13` route. Final artifact SHA-256:
  `e2d10e0ce30c12fb48ce48220ed96f35fe3fa36f6d6d825a68f5e5700b0cd9d0`;
  the root P6 discovery run passed 43 tests.

### P7 common-ideal and fixed-ray coloured cubic

- `PROVED`: the common-ideal Gram, repeated-norm fibre, labelled cubic trace,
  and fixed-modulus coloured Parseval identities are exact. Repeated norms
  cost only a divisor-function factor in one-character L2, but the pair-label
  dependence and varying conductors prevent verbatim import of the integer
  cubic proof. Main/correction SHA-256 values:
  `5363288906df50df18e96afec0760c1fa8bfec912e61bbf05fa60492c77957f2`,
  `fdf5c03927d8c43b67f18eab1e7b6a84bc9cba979861adfa6acc15e16e4482e4`,
  and `caf4055315ccdcb265263c8594f3511108522494793093ef2cbcf0adf290c0dd`.
- `PROVED`: at fixed modulus, complete-character Fourier diagonalization is
  unitary and preserves the cubic normalization. Primitive row selection is
  generally a non-diagonal projection; completion has sharp factor
  `kappa<=|X(f)|<=2Q` and destroys the selected diagonal cancellation.
  Coloured energy can remain at cubic scale under fibrewise separation, with
  `W=X x {0}` an exact extremizer. Direct per-character Guth--Maynard costs
  `F_prim(Q)<=12Q^2`, which is not subpower for `Q=T^theta`.
- `CONJECTURED`: progress now requires a selected-side primitive cubic-excess
  estimate and a cross-conductor bound, not another uncoloured completion.
  Artifact SHA-256:
  `426681db11b09b52dad029a2e0a5931e430a5a5224d55c8f4ca5908b26564027`;
  its isolated replay and six tests passed.
- `OBSERVED`: one predecessor RSS check transiently exceeded its strict cap
  during concurrent file activity and then passed in five isolated repeats.
  Three historical P7 tests have literal-string expectations superseded by
  correction artifacts; the predecessor builders themselves replay. These
  are retained as harness issues, not promoted mathematical disagreements.

## Cycle 7 — coefficient-phase closure and selected-Gram pinching (2026-08-01)

### CRR scalar and coefficient-phase boundary

- `PROVED`: actual-Farey Cauchy plus the checked global fourth-moment/energy
  bound gives only `A_v(W)<<v^(26+o(1))`, while RationalMass forces local
  Farey fourth moment at least a constant times `v^(20-6delta)`. Thus global
  L4/energy is scale-saturated alongside global L2. The scalar profile
  constant on the true Farey union exactly calibrates the Cauchy exponent but
  is not claimed to be Fourier-realizable. Artifact SHA-256:
  `a9b142f8fd22e4fe9ebd4857af4eb7e764aa20ea379170930f6446231e663266`.
- `PROVED`: the same Base coefficient vector supplies the exact phase lower
  bound `a^*G_Wa>=v^(20-4delta)`. A sampled mean-value upper bound gives
  `a^*G_Wa<=v^(20+o(1))`; consequently fixed-power CFARI and AFARI imply one
  another after a constant-factor loss in `eta`. The phase product is not an
  independent power-scale gate. Artifact SHA-256:
  `00ca4e7f794a06d797b24543d174d86ef6d8a3f99a068d14bb693ce894f16dad`.
- `OBSERVED` correction: the immutable AFARI v1 test expected the literal
  words `does not prove`, while the sealed claim says `proves neither`.
  Mathematical replay was unaffected; the failing test is preserved and the
  corrected suite has SHA-256
  `31da90127f321d91bf7b6a2d4373ae1bbff638d7a4fcc4cc9a0fb6ae1c788815`.
- `OBSERVED`: integer-frequency idempotent concentration and classical
  additive Farey large-sieve eigenvalue theorems do not transfer to the
  real-frequency, shrinking log-Farey comb or its all-ones/mixed direction.
  Their missing quantitative degree, gap, energy, and aspect controls are
  recorded in the Cycle-6 notes; no literature theorem was imported.

### Exact capped phase lift and bounded actual-log probe

- `PROVED`: for the actual Dirichlet matrix, the capped all-row value is
  exactly `max_z min_p ||M_W^*(pz)||_1`. Phase rounding a top right singular
  vector gives
  `Gamma(W)^2>=lambda_max N rho phi^2/|W|`, isolating coefficient
  delocalization `rho` and all-row flatness `phi`. Artifact SHA-256:
  `165aff6e15a9c2177b1a69d7a2ce32ff9ba3b2d651aba6683d9f5ecca21403e4`.
- `OBSERVED`: a separately preregistered `v=2` actual-log/Farey prototype
  retained none of three rows. The leading phase had `rho≈0.587` but
  `phi≈5.8e-8`; inverse-row updates raised the minimum to `8.76`, below the
  frozen `128` threshold. This diagnoses finite row flatness only and is not
  asymptotic evidence. Executable preregistration/result SHA-256 values:
  `d0fc1cf67c6b6ebb022cd653259eea2497b5a9b6f82db70842e70783b59ef80e`
  and `0cab222fe49623263fb953ee0d7e863d339774172df5d4843fe40707376a853d`.

### P7 selected-Gram correction and reduction

- `PROVED`: for every selected PSD Gram matrix,
  `G(K)=sum_j(lambda_j-mu)^2(lambda_j+2mu)` and
  `G(K)<=3||K||_op V2(K)`, with sharp general factor three. Exact-conductor
  block pinching corrects the earlier aggregate-sign wording and gives
  `0<=X_cross<=G(K)`; individual expansion summands may still be signed.
- `PROVED`: fixed-ray class averaging preserves the selected trace and its
  diagonal subtraction without the completion factor. Its error is governed
  by a Schatten ray-class discrepancy; the exact Parseval form of `delta_2`
  is a complete-character mean square over the uncoloured time-difference
  multiset. Raw Thorner L2 gives only the diagonal scale, and finite algebraic
  countermodels show coloured energy/local collision data alone do not bound
  the excess.
- `OBSERVED`: the next P7 gate is a conductor-safe difference-sampling bound
  for `delta_2` or a centred-variance estimate of source shape. Artifact
  SHA-256:
  `fac0f8bb8206ce7d0b008363ab9715859e4b5ed2d9932af5f86b684c52c2db5a`;
  builder and five focused tests pass. A brief in-progress local prose edit
  caused one transient mismatch; exact pinned bytes were restored, and no
  sealed artifact was overwritten.

## Cycle 8 — EO-LF4 saturation theorem and stronger-gate boundary (2026-08-01)

### Sharp energy-only actual-log-Farey theorem

- `PROVED`: define EO-LF4 by the actual reduced logarithmic Farey union, the
  frozen height/cardinality/separation scales, and the tolerance-one energy
  band, while omitting the common Base coefficient, RationalMass, and
  PositiveCubic. The checked Guth--Maynard `RL4` lemma gives a uniform
  `v^(20+o(1))` upper bound for its logarithmic local fourth moment.
- `PROVED`: for every sufficiently large even `v`, an actual reduced label
  `(Q+1,5Q/4+1)` supports an equal-weight phase-lattice row set in the same
  EO-LF4 class with logarithmic fourth moment at least `v^20/30`. Hence the
  supremal exponent is exactly `20`, and every fixed-power energy-only F4F
  saving fails. Primary theorem SHA-256:
  `526fdff9ffb1fc63fdf1ee865f36f243963ef1ae0fe11dc0d76c99479ad14c40`.
- `PROVED`: an independent completion audit classifies PLAN Objective 2 as
  `SATISFIED_FOR_EO_LF4_SCOPED_GM_SUBARCHITECTURE`. It explicitly rejects
  promotion to sharp bundle exponent `26`, full CRR, or full Guth--Maynard
  saturation. Main/corrected-test SHA-256 values:
  `e62388fcd1f62460f438d73743920f6209c71fc353254984f45d74e71e416746`
  and
  `966ae131a854b7c2bf1b868ab49f61a4cc9b5379a3bc036601fde5c3832dbb2b`.

### Signed extremizer and exact Base bridge

- `PROVED`: the exact signed pair-sum kernel is a positive Fourier
  projection of norm one on unrestricted `L^2`; finite homogeneous linear
  diagnostics cannot create a spectral gap. More strongly, the actual-label
  phase-lattice construction has `|W|=R`, frozen separation, the full energy
  band, and local fourth moment at least `v^20/20`. It is not Base-admissible
  by any result here. Main/test-correction SHA-256 values:
  `9616ef55eec03f2f11ba2b625fd9e8cbd3c4ad581900a8a441ce9ed130d05796`
  and
  `e7ba78e6f17de27862f69ca6cc61ada2c3724477d0e6757c2f98982719dbf638`.
- `PROVED`: exact rational Dirichlet-phase alias classes on this lattice have
  at most four columns. With
  `Xi=m Gamma^2/((L-1)lambda)`, the common capped Base condition is exactly a
  lower bound on `lambda*Xi`; a compatible lattice must have
  `lambda=v^(12-o(1))` and `Xi=v^(-o(1))`. A fixed-power loss in either
  excludes Base, but neither loss nor a witness is proved. Main/correction
  SHA-256 values:
  `3207a7764470d5512d20778e739e0e0bdc31535c0b2ac68b8366707304678534`
  and
  `9ad5dac78854c26ada7034a87eda981eca4700bdbf1e85dc42761e44fe706843`.
- `PROVED`: the preceding absolute Mellin-bin/Wiener route cannot yield a
  fixed saving; high-frequency mass remains at constant scale. Its artifact
  SHA-256 is
  `18fefc631e63a622cf780c927cd6aad185d5cc310f9e908c09ccb9de1fefc7a4`.

### All-row inverse boundary and correction

- `PROVED`: phase rounding reduces all-row flatness to minimum top leverage
  and coordinatewise phase leakage; actual row deletion gives the sharp
  lower bound `|u_t|^2>=d_t^2/(d_t^2+beta_t^2)`. RationalMass currently
  supplies only average Farey deletion influence. Artifact SHA-256 values:
  `28990f2c703e0f8bfba8e25fb40ecc3d8231392e564653a01fcf5330a52b83ff`
  and
  `9b0d74235c587d8624879626703efc9577020ebb8770defe022108914c35e832`.
- `PROVED` conditional on an explicitly unconstructed surplus core: adding
  one actual late row preserves the scalar Farey/energy predicates but makes
  deletion coverage polynomially small. This blocks a scalar-only RFDI
  implication, not RFDI itself. `OBSERVED` correction: supporting v1 files
  were edited after sealing to add the normalized-bump premise used in
  `J(u)<=2`; the v1 artifact remains immutable and correctly rejects current
  inputs. Replayable v2 records the mutation and re-seals the conditional
  theorem, SHA-256
  `d87bea3ea75dcb84d675b74cc8e214b0daa7438b1b701148878ef49c48ba83f8`.

### P7 detector-side obstruction

- `PROVED`: fixed-conductor primitive induction gives the exact complete-ray
  L2 input, but deterministic sampling leaves the local difference statistic
  `D_Delta`. Fibrewise separation permits `D_Delta=mP`, sharply, and ordinary
  difference energy loses a power. Artifact SHA-256:
  `c943ef3b946c2a1392f226a080711a24b094d9e4cddbb141b2290375afeecc96`.
- `PROVED`: source-checked individual unit-window zero counts are logarithmic,
  but after per-character separation they give no improvement over one row
  per colour. The exact block model still has `D_Delta=mP`; a joint L2 route
  needs one common ideal detector uniformly above a recorded threshold.
  Final correction SHA-256:
  `29e51c44b31ac822431eae0e987d8a8e26168746b3f6e8356e195ce008d7d472`.
  V1/v2 literal-test and rendering defects remain preserved in the correction
  chain; no mathematical source-scale gain is claimed.

### Replay outcome and preserved harness corrections

- `OBSERVED`: the correction-aware root suite replayed 14 current builders
  and 54 focused tests successfully. Historical literal-only failures remain
  preserved for the signed extremizer, phase-lattice Base gate, and Objective
  2 audit; their versioned correction suites are the green checks. The RFDI
  v1 current-input mismatch is intentional and superseded by replayable v2.

## Cycle 9 — creative engine portfolio redesign (2026-08-01)

- `OBSERVED`: the superseded 24-month allocation placed 65% of planned effort
  on the already isolated `lambda*Xi` Base seam. It named higher trace,
  energy refinement, and zero detection as contingencies but did not specify
  new mathematical mechanisms or toy theorems for them.
- `OBSERVED`: no new theorem is claimed in this strategy cycle. The banked
  EO-LF4 theorem licenses moving beyond coefficient-free fourth-moment
  optimization; it does not privilege Base as the unique route forward.
- `CONJECTURED`: `30/13` may be a fixed point of three coupled design choices:
  a single common detector, an uncentred low trace, and scalar energy that
  forgets logarithmic/multiplicative structure. A successful method may need
  to alter two choices together.
- `OBSERVED`: PLAN now incubates six engines: E1 polyphonic zero detection,
  E2 centred nonbacktracking trace, E3 log-Farey curvature/inverse rigidity,
  E4 prime-block entropy amplification, E5 density-feedback renormalization,
  and E6 direct explicit-formula cancellation. E1+E2 and E3+E4 are the first
  planned hybrids.
- `OBSERVED`: research-stage route policy now forbids elimination from a
  failed bounded experiment. Each engine begins with an exact source bridge,
  a toy theorem, and a genuine countermodel; hostile audit remains deferred
  until a concrete manuscript theorem is frozen.

## Cycle 10 — E1 frame detector and E2 two-step centring (2026-08-01)

### Headline outcomes

- `PROVED`: for the weighted detector frame
  `B=sum_j omega_j b_j b_j^*`, `K_B=M B M^*`, and
  `q_t=(K_B)_(t,t)`, every integer `r>=1` satisfies
  `|S|V^(2r)<=sum_t q_t^r<=tr(K_B^r)` when `q_t>=V^2` on
  `S`. If each row is covered by one of `K` uniformly weighted detectors,
  the exact cost is `K^r`.
- `PROVED`: pure colouring by unrelated detectors gives `|S|<=K F` by both
  summation and largest-colour pigeonholing. Since the pinned zero detector
  already has only `O(log T)` dyadic choices, repackaging those choices as
  E1 changes no fixed power exponent. E1 remains live only with additional
  source-derived frame geometry.
- `PROVED`: for a constant-diagonal Hermitian Gram matrix, put
  `A=G-dI`, `r_i=sum_(j!=i)|A_ij|^2`, and
  `C_2=A^2-diag(r_i)`. Then
  `||C_2||_F^2=tr(A^4)-sum_i r_i^2` and
  `lambda_max(G)<=d+sqrt(max_i r_i+||C_2||_op)`.
- `PROVED`: at the frozen Base scales, the preceding inequality forces
  `max_i r_i>=(1/8)v^(24-6delta(v))` or
  `||C_2||_op>=(1/8)v^(24-6delta(v))` for all sufficiently large `v`.
  Neither side is bounded below this scale, so `OBSERVED`: no density or
  short-interval propagation is authorized.
- `PROVED`: the raw length-four nonbacktracking polynomial
  `tr(A^4)-2sum r_i^2+sum_(i!=j)|A_ij|^4` is signed. The preregistered
  exact search checked 125 order-three matrices and found the fifth
  order-four matrix, with edge list `[-2,-2,-2,-2,-2,2]`, giving
  `NB4=-128`. This contains raw-NB4 positivity only; positive two-step
  squares, even dilations, and alias-conditional centring remain live.

### Evidence, replay, and gate effect

- Primary artifact SHA-256:
  `ca1e179cb2b39c2fe8c243aba0d6557b61f4d1dee3a02927bdac528030cb2246`.
- Preregistration:
  `docs/cycle-10-e1-e2-engine-preregistration-v1.md`.
- Theorem note:
  `docs/cycle-10-e1-frame-e2-two-step-v1.md`.
- Exact conventions and deterministic sign search:
  `conventions/e1_e2_engine_v1.py` and
  `discovery/search_cycle_10_nb4_countermodel.py`.
- Replay commands:

  ```sh
  python3 proof/build_cycle_10_e1_frame_e2_two_step_v1.py --check
  python3 -m unittest tests/test_cycle_10_e1_frame_e2_two_step_v1.py
  ```

- `OBSERVED`: builder write/check each used about `0.07` seconds and
  `18,944` KiB peak RSS; four focused tests passed in `0.533` seconds with
  `31,772` KiB peak RSS.
- Gate change: E1 is `FRAME_IDENTITY_COMPLETE_HYBRID_OPEN`; E2 is
  `TWO_STEP_IDENTITY_COMPLETE_HYBRID_OPEN`. The next gate is a source-derived
  E1+E2 frame kernel whose return and coherent-two-step bounds beat the
  explicit colour cost. E3 remains the independent co-primary incubation.

## Cycle 11 — E1+E2 block-variance reduction (2026-08-01)

### Headline outcomes

- `PROVED`: for block value vectors `d_j`, their sum `d`, and raw frame `F`,
  the exact decomposition is
  `F=sum_j d_jd_j^*=dd*/K+Z`, where
  `Z=sum_j(d_j-d/K)(d_j-d/K)^*>=0`. Its diagonal is the pointwise block
  variance. The vector model `d_j=d/K` has `Z=0` despite arbitrary largeness
  of `d`, so detector largeness alone cannot force frame diversity.
- `PROVED`: for every integer `r>=1`,
  `tr(F^r)>=tr((dd*/K)^r)=(||d||_2^2/K)^r`. On `R` rows with
  `|d_t|>=V`, this is at least `(RV^2/K)^r`, a factor `R^(r-1)` above the
  Cycle-10 diagonal threshold. Raw mixed Schatten traces therefore retain
  the original common-detector obstruction at full strength.
- `PROVED`: the rank-one term realizes the coherent E2 branch. If
  `|d_t|^2/K>=a`, then its return-deleted two-step operator satisfies
  `||C_2||_op>=(R-1)(R-2)a^2`. At the frozen bands
  `R>=v^(8-delta)`, `V>=v^(7-delta)`, `K<=v^delta`, this gives
  `lambda>=v^(22-4delta)` and
  `||C_2||_op>=(1/4)v^(44-8delta)` for sufficiently large `v`.
- `PROVED`: independent uniform random colouring of coefficients satisfies
  the exact expectation
  `E F_chi=dd*/K+(1-1/K)G_c`. Random colouring preserves rather than removes
  the forced rank-one detector kernel. All colourings were enumerated exactly
  for coefficient-set sizes 2 through 5 and `K in {2,3}`.
- `OBSERVED`: no analytic saving follows. The E1+E2 gate is now the
  arithmetic size and dispersion of `Z`, or construction of an ensemble
  without the old forced rank-one component. This refines the engine rather
  than terminating it.

### Evidence, replay, and gate effect

- Primary artifact SHA-256:
  `fa6264fc8d040f0e0164b1256ec97f07a6637c7688b94f794096cb6bdef04a8a`.
- Preregistration and theorem note:
  `docs/cycle-11-e1-e2-block-variance-preregistration-v1.md` and
  `docs/cycle-11-e1-e2-block-variance-v1.md`.
- Exact conventions:
  `conventions/e1_e2_block_variance_v1.py`.
- Replay:

  ```sh
  python3 proof/build_cycle_11_e1_e2_block_variance_v1.py --check
  python3 -m unittest tests/test_cycle_11_e1_e2_block_variance_v1.py
  ```

- `OBSERVED`: builder write/check used `0.08` seconds and at most `20,224`
  KiB peak RSS. Four focused tests passed in `0.563` seconds with `31,780`
  KiB peak RSS.
- Gate change: E1+E2 is `RAW_FRAME_SATURATED_VARIANCE_OPEN`. E3/E4 now owns
  the affirmative question whether actual prime/multiplicative blocks force
  variance or entropy after the detector rank-one component is removed.

## Cycle 12 — balanced five-factor fractional tensor (2026-08-01)

### Headline outcomes

- `PROVED` conditional on the frozen balanced-product and coefficient-norm
  hypotheses: if the critical length-`v^5` detector is a product of five
  length-`v` Dirichlet polynomials, then on every row one of ten moments that
  cube two factors and square three is at least the detector to power `12/5`.
  Every such moment has length exactly `v^12=H`.
- `PROVED` conditional local theorem: the discrete mean-value bound for the
  selected moment gives
  `|W|<=v^(36/5+(24/5)delta+o(1))`. The main local exponent `36/5` improves
  the frozen exponent `8` by exactly `4/5`.
- `PROVED`: the uniform ten-moment design is balanced iff all five factor
  length exponents equal one. The sum of all pair exponents forces this
  algebraically. A registered grid checked 306 sorted rational fifths and
  retained only `(1,1,1,1,1)`; the tuple
  `(1/2,1/2,1,3/2,3/2)` has moment lengths from `v^11` to `v^13`.
- `PROVED` conditional anchor algebra: applying the local bound in `v` global
  subintervals would give exponent `41/5` at `sigma=7/10`, anchor density
  coefficient `82/39`, gain `8/39`, and formal interval target `43/82`.
  `OBSERVED`: none is promoted because the source factorization, left
  neighborhood, and full envelope remain open.
- `CONJECTURED`: the exact next source gate is a decomposition of the
  normalized critical Type-I detector into `v^o(1)` balanced fivefold
  products with coefficient square norms `v^(12+o(1))` after the ten moment
  transforms. Rough/prime-dominated integers and coefficient multiplicity are
  registered adverse cases, not silently discarded.

### Evidence, replay, and gate effect

- Primary artifact SHA-256:
  `2c57bd1f621d7474cea68fd07cd8719c0f8f64c4766cf2cd7fbfcd765921d24d`.
- Preregistration and theorem note:
  `docs/cycle-12-balanced-five-factor-preregistration-v1.md` and
  `docs/cycle-12-balanced-five-factor-v1.md`.
- Exact conventions:
  `conventions/balanced_five_factor_v1.py`.
- Replay:

  ```sh
  python3 proof/build_cycle_12_balanced_five_factor_v1.py --check
  python3 -m unittest tests/test_cycle_12_balanced_five_factor_v1.py
  ```

- `OBSERVED`: builder write/check each used `0.06` seconds and `18,944` KiB
  peak RSS. Four focused tests passed in `0.477` seconds with `31,912` KiB
  peak RSS.
- Gate change: E3+E4 is `CONDITIONAL_LOCAL_GAIN_FACTORIZATION_OPEN`, the
  first portfolio engine with a strict theorem-scale exponent budget. No P3
  density propagation is authorized yet.

## Cycle 13 — source obstruction and weighted fractional tensor (2026-08-01)

### Headline outcomes

- `PROVED`: the Cycle-12 proposed exact source gate is false for the full
  current detector. For every prime above the truncated-Mobius cutoff, its
  coefficient is nonzero; every sum of fivefold Dirichlet convolutions whose
  factors are supported on integers at least two vanishes at primes. This is
  a coefficient-support obstruction, not a large-value theorem about the
  prime remainder.
- `PROVED` conditional on the registered transformed coefficient-square
  norms: for factor exponents `y_i>0` summing to five, a probability design
  on integer increments `k` with `y dot k<=2` and `E k_i=tau` gives exact
  pointwise tensor power `2+tau` and local row exponent `10-7tau`. Strict gain
  is equivalent to `tau>2/7`, while every such design has `tau<=2/5`.
- `PROVED`: when every `y_i<=2`, singleton increments
  `q_i e_i`, `q_i=floor(2/y_i)`, give
  `tau=1/sum_i(1/q_i)`. The former unbalanced countermodel
  `(1/2,1/2,1,3/2,3/2)` now gives `tau=1/3`, local exponent `23/3`, and gain
  `1/3`.
- `PROVED`: the registered exact fifth-grid contains 1,442 sorted cells with
  three through ten factors. The singleton certificate is admissible on 978
  and yields strict gain on 927, equality on 17, and negative formal gain on
  34. The other 464 have a factor exponent above two, which forces zero
  uniform increment in this architecture. The census is sufficient, not an
  optimum linear-program census.
- `OBSERVED`: no density or interval result is promoted. A source-valid
  prime-weighted or logarithmic-derivative detector identity, transformed
  coefficient norms, and control of the rough/non-gain cells remain open.

### Evidence, replay, and gate effect

- Primary artifact SHA-256:
  `c1c057b089ed8626d3d049520eeb1a5ec1709bc55e24db1b0374f09a05588ecf`.
- Preregistration and theorem note:
  `docs/cycle-13-source-obstruction-weighted-tensor-preregistration-v1.md`
  and `docs/cycle-13-source-obstruction-weighted-tensor-v1.md`.
- Exact conventions:
  `conventions/weighted_fractional_tensor_v1.py`.
- Pinned Heath--Brown 1982 primary PDF SHA-256:
  `b32e586d26dac73cb36a4f6dc7c6a7bf08ea5fa88e8ef8b18a8df2d5e849a807`;
  it is reconnaissance only and no theorem from it is imported in Cycle 13.
- Replay:

  ```sh
  python3 proof/build_cycle_13_source_obstruction_weighted_tensor_v1.py --check
  python3 -m unittest tests/test_cycle_13_source_obstruction_weighted_tensor_v1.py
  ```

- `OBSERVED`: builder write/check used about `0.14/0.13` seconds and
  `20,096` KiB peak RSS; four tests passed in `0.106` seconds with `16,512`
  KiB peak RSS.
- Gate change: E3+E4 is `CELLWISE_GAIN_SOURCE_IDENTITY_OPEN`. The false
  exact-factorization conjecture is superseded by a component program:
  source-valid product cells feed the weighted tensor; prime/rough cells feed
  detector redesign or a second analytic engine.

## Cycle 14 — prime-atom integer-moment quantization (2026-08-01)

### Headline outcomes

- `PROVED`: for the length-`v^5` prime atom at local time `v^12` and
  threshold `v^(7/2-delta)`, the standard `2k`-moment model gives local
  exponent `max(12-2k,3k)+2k delta`. Its continuous minimum is `36/5` at
  `k=12/5`, but its integer minimum is exactly `8` at `k=2`; `k=3` gives
  `9`. The integer quantization penalty is `4/5`.
- `PROVED`: ordinary log-convex interpolation between the fourth-moment
  exponent `22` and sixth-moment exponent `30` gives moment exponent `126/5`
  at order `24/5`, hence local exponent `42/5`. Interpolation does not realize
  the lower continuous envelope.
- `PROVED` from the pinned Maynard--Pratt statements: the unconditional
  smooth `Lambda` detector applies to `Y`-half-isolated zeros, and their
  stated consequence already bounds half-isolated zeros by
  `T^(2(1-sigma)+o(1))`. It is not a source-valid replacement detector for
  arbitrary critical Type-I zeros.
- `CONJECTURED`: a prime-specific restricted weak-type estimate or moment
  bound `int_H |P|^(24/5)<=v^(24+o(1))` would give local exponent `36/5` for
  the unfactorable prime component. The target must use prime/logarithmic
  structure; it is not asserted for generic Dirichlet polynomials.
- `OBSERVED`: no density or interval promotion occurs. The new gate is a
  fractional prime restriction theorem plus a bridge from the relevant
  clustered zero class to a prime-supported detector.

### Evidence, replay, and gate effect

- Primary artifact SHA-256:
  `8cd7f58a5972031553708e9efc1f0d8f4a613a232ffbcecc85bb659d085b5152`.
- Preregistration and theorem note:
  `docs/cycle-14-prime-atom-fractional-moment-preregistration-v1.md` and
  `docs/cycle-14-prime-atom-fractional-moment-v1.md`.
- Exact conventions:
  `conventions/prime_atom_fractional_moment_v1.py`.
- Replay:

  ```sh
  python3 proof/build_cycle_14_prime_atom_fractional_moment_v1.py --check
  python3 -m unittest tests/test_cycle_14_prime_atom_fractional_moment_v1.py
  ```

- `OBSERVED`: builder write/check each used about `0.04` seconds and `19,072`
  KiB peak RSS; four tests passed in under `0.05` seconds with `15,872` KiB
  peak RSS.
- Gate change: E3+E4 is
  `CELLWISE_GAIN_FRACTIONAL_PRIME_TARGET_OPEN`. Product cells retain the
  weighted-tensor route; the prime atom now has its own exact target rather
  than being left as an undifferentiated rough remainder.

## Cycle 15 — prime phase transition and rank-one semiprime reduction (2026-08-01)

### Headline outcomes

- `PROVED`: two different coefficient constructions force prime moment lower
  scales `m^p` and `H m^(p/2)`. The first is a coherent spike obtained by
  aligning all prime phases at one ordinate. The second follows from the
  exact Steinhaus identity `E|P(t)|^4=2m^2-m`, deterministic selection, and
  monotonicity of normalized `L^p` norms.
- `PROVED`: at `H=X^(12/5)` these lower exponents meet uniquely at
  `p=24/5`, where both have exponent `X^(24/5-o(1))`. Thus the proposed global
  fractional moment upper is power-sharp against two structurally opposite
  mechanisms.
- `PROVED`: `P_a^2` has diagonal coefficients `a_p^2` and off-diagonal
  coefficients `2a_pa_q`; its coefficient-square norm is exactly `2m^2-m`
  and its semiprime coefficient matrix is symmetric rank one. Two dyadic
  support pieces cost only a constant colour factor.
- `PROVED`: applying the checked generic GM theorem at
  `N=X^2,T=X^(12/5),V=X^(7/5)` gives term exponents
  `6/5,8/5,8/5` in `X`. The desired local count is `X^(36/25)`, so the exact
  restricted rank-one theorem needs saving `4/25` in `X`, equivalently
  `4/5` in `v`.
- `OBSERVED`: a global `L^(24/5)` theorem is sufficient but unnecessarily
  strong. The principal target is the ordinary integer-power GM problem on
  the symmetric rank-one semiprime coefficient class.

### Evidence and replay

- Artifact SHA-256:
  `49a5a573b00f3d56e75b7537dee36792751b877b63bef8d5bfee667fb42b51d1`.
- Preregistration/theorem:
  `docs/cycle-15-prime-phase-transition-rank-one-preregistration-v1.md` and
  `docs/cycle-15-prime-phase-transition-rank-one-v1.md`.
- Replay:

  ```sh
  python3 proof/build_cycle_15_prime_phase_transition_rank_one_v1.py --check
  python3 -m unittest tests/test_cycle_15_prime_phase_transition_rank_one_v1.py
  ```

- `OBSERVED`: builder write/check each used about `0.05` seconds and `18,816`
  KiB peak RSS; four tests passed in `0.015` seconds with `15,872` KiB RSS.

## Cycle 16 — separable tensor gate (2026-08-01)

### Headline outcomes

- `PROVED`: if the tensor-square sampling operator `S` has rows
  `u_t tensor u_t`, then `S(a tensor a)=(Ua)^2`, its row Gram is the Schur
  square `(UU^*) circle (UU^*)`, and the prime fourth moment is the Rayleigh
  quotient of `S^*S` on the Veronese cone `{a tensor a}`.
- `PROVED`: the desired rank-one count follows from separable norm exponent
  `56/25`; the generic fourth-moment exponent is `12/5`, leaving exactly the
  same `4/25` saving in `X`.
- `PROVED`: for a spectral cutoff `L`, a unit rank-one tensor with Rayleigh
  quotient `A>L` has squared overlap at least
  `(A-L)/(lambda_max-L)` with the spectrum above `L`. Within this architecture
  a failed bound therefore has exactly two ingredients: high spectrum and
  overlap of the same common coefficient tensor. This is not a claim about
  every possible method.
- `PROVED`: identical sampling rows satisfy
  `Sep(S^*S)=lambda_max(S^*S)=R||u||^4`. Rank-one coefficients alone force no
  saving; arithmetic separation of actual prime phases is indispensable.
- `OBSERVED`: no prime-phase spectral or overlap loss is yet proved, and no
  density result is promoted.

### Evidence and replay

- Artifact SHA-256:
  `633342875545cf2cb7886356de5dd9beed0a8dcac9b171d1f35a47ce7be9d6ea`.
- Preregistration/theorem:
  `docs/cycle-16-separable-tensor-gate-preregistration-v1.md` and
  `docs/cycle-16-separable-tensor-gate-v1.md`.
- Exact conventions: `conventions/separable_tensor_gate_v1.py`.
- Replay:

  ```sh
  python3 proof/build_cycle_16_separable_tensor_gate_v1.py --check
  python3 -m unittest tests/test_cycle_16_separable_tensor_gate_v1.py
  ```

- `OBSERVED`: builder write/check each used about `0.04` seconds and `18,560`
  KiB peak RSS; four tests passed in `0.008` seconds with `16,128` KiB RSS.
- Gate change: E3+E4 is `RANK_ONE_SEMIPRIME_SEPARABLE_GATE_OPEN`.

## Cycle 17 — finite prime-phase separable search (2026-08-01)

### Headline outcomes

- `OBSERVED`: all 80 preregistered alternating-optimization runs and 35
  deterministic coefficient families completed in 74.492 seconds with
  55,192 KiB peak RSS. The immutable result status is
  `BASELINE_APPROACHED`.
- `OBSERVED`: the best row is the alternating-sign family at `m=16`, with
  count 67 and per-size exponent `1.516522`; this exceeds both the target
  `36/25` and the registered `3/2` baseline marker. Optimized random seed 2
  at `m=24` gives count 101 and exponent `1.452185`, also above the target.
- `OBSERVED`: no registered family crosses `36/25` at `m=32,48,64`; their
  best count exponents are approximately `1.322942,1.214218,1.227720`.
  The largest values in the best rows occur in short consecutive clusters.
- `EXPLORATORY`: post-result log-log slopes for best count versus `m` range
  from roughly `0.47` to `0.72` depending on the fitted suffix. These fits
  were not preregistered and do not weaken the formal adverse outcome.
- `OBSERVED`: no asymptotic countermodel or analytic saving follows. The next
  gate is to isolate coherent clusters analytically before testing diffuse
  high-spectrum/Veronese overlap.

### Evidence and gate effect

- Result SHA-256:
  `8ce4a5592b1ce895b62c659b4568e10992f84f92574db9f2b3f799d1189b89f6`.
- Search/preregistration SHA-256:
  `13d194106631511d69fe71ec28aad7f4ca1ca583763a863d2aa214e292372dfc`
  and
  `e6b46f7dd33f19fd606289a38860a6731b00813ad5bcad823c2ae8c91fbe666f`.
- Result note: `docs/cycle-17-prime-phase-separable-search-v1.md`.
- Integrity/semantic replay:

  ```sh
  python3 proof/check_cycle_17_prime_phase_separable_search_v1.py
  python3 -m unittest tests/test_cycle_17_prime_phase_separable_search_v1.py
  ```

- Gate change: E3+E4 is
  `RANK_ONE_SEMIPRIME_CLUSTER_DECOMPOSITION_OPEN`. The finite crossings are
  retained as adverse cases; they motivate a coherent-cluster/diffuse split
  rather than terminating the rank-one engine.

## Cycle 18 — coherent-cluster skeleton reduction (2026-08-01)

### Headline outcomes

- `PROVED`: the checked classical large-values estimate, localized to an
  interval of length `Y`, gives
  `R(J)<=X^(o(1))(X^(3/5)+Y X^(-2/5))` at threshold `X^(7/10)`.
  Hence every interval of length `2X^(3/5)` contains at most
  `X^(3/5+o(1))` one-separated critical rows.
- `PROVED`: if `C` is a maximal `X^(3/5)`-separated subset of the full row
  set `W`, its radius-`X^(3/5)` intervals cover `W`, and
  `|W|<=X^(3/5+o(1))|C|`.
- `PROVED`: the desired count `|W|<=X^(36/25+o(1))` is therefore reduced to
  the recurrence-skeleton target `|C|<=X^(21/25+o(1))`. The generic
  `X^(8/5)` count gives only skeleton exponent `1`; the required saving is
  still exactly `4/25`.
- `OBSERVED`: cluster removal is a lossless compression, not an analytic
  saving. The open object is a widely separated set of ordinates on which
  one common prime coefficient vector repeatedly has size `X^(7/10)`.

### Evidence and gate effect

- Artifact SHA-256:
  `2aab1890a1e68efc58dcc9ad45dc636766760a610de8299a7f52afb605138936`.
- Preregistration/theorem:
  `docs/cycle-18-coherent-cluster-skeleton-preregistration-v1.md` and
  `docs/cycle-18-coherent-cluster-skeleton-v1.md`.
- Exact conventions: `conventions/coherent_cluster_skeleton_v1.py`.
- Replay:

  ```sh
  python3 proof/build_cycle_18_coherent_cluster_skeleton_v1.py --check
  python3 -m unittest tests/test_cycle_18_coherent_cluster_skeleton_v1.py
  ```

- `OBSERVED`: write/check used about `0.04` seconds and `19,072` KiB peak
  RSS; four focused tests passed.
- Gate change: E3+E4 is `SEPARATED_RECURRENCE_SKELETON_OPEN`. The next
  principal attempts are phase-code entropy and popular-difference inverse
  theorems; determinant rigidity and detector surgery are independent
  high-risk alternatives.

## Cycle 19 — synchronization graph and abstract boundary (2026-08-01)

### Headline outcomes

- `PROVED`: if `R` sampling rows of squared norm `M` have common projections
  at least `V` against a vector of squared norm `A`, phase alignment and
  Cauchy--Schwarz force synchronized Gram mass at least `R^2V^2/A`.
- `PROVED`: writing `w=V^2/A`, if `Rw>=2M`, at least
  `R^2w/(4M)` ordered pairs have phase-aligned real kernel at least `w/4`.
  Their symmetric graph has at least `E^2/R` ordered two-step paths.
- `PROVED`: at `A=M=X`, `V=X^(7/10)`, and the target
  `R=X^(21/25)`, the forced ordered-edge, average-degree, and two-step-path
  exponents are `27/25`, `6/25`, and `33/25`.
- `PROVED`: a positive-definite common-component simplex realizes every
  off-diagonal kernel at exactly `w` for arbitrary `R`; its labels may be
  arbitrarily separated, and all synchronized mass may lie in one coordinate
  block. Consequently scalar coherence, graph density, separation labels,
  and high values alone imply neither the skeleton bound nor positive
  phase-code entropy.
- `OBSERVED`: the exact open seam is arithmetic. For prime rows, a new lemma
  must forbid the forced two-step path count, make popular edges close under
  endpoint differencing, or force multiblock structure usable by E10.

### Evidence and gate effect

- Artifact SHA-256:
  `3c68ee97a31f7a7cb2612769f58c2645b4a58332aeceaa856d7082de635aeb63`.
- Preregistration/theorem:
  `docs/cycle-19-synchronization-graph-preregistration-v1.md` and
  `docs/cycle-19-synchronization-graph-v1.md`.
- Exact conventions: `conventions/synchronization_graph_v1.py`.
- Replay:

  ```sh
  python3 proof/build_cycle_19_synchronization_graph_v1.py --check
  python3 -m unittest tests/test_cycle_19_synchronization_graph_v1.py
  ```

- `OBSERVED`: write/check each used about `0.04` seconds and `18,536` KiB
  peak RSS; five focused tests passed in about `0.04` seconds and `15,872`
  KiB peak RSS.
- Gate change: E7--E10 is `PRIME_LOG_TWO_STEP_CLOSURE_OPEN`. E7 cannot start
  from entropy forced by high values alone; E9 now has an exact graph and
  exponent budget on which a prime-specific closure theorem can act.

## Cycle 20 — sharp exterior-volume collapse (2026-08-01)

### Headline outcomes

- `PROVED`: if `k` rows of squared norm `M` share projections at least `V`
  against a vector of squared norm `A`, then, with
  `w=V^2/A`, `rho=w/M`, and `kw>=M`,
  `det(G)/M^k <= k rho[k(1-rho)/(k-1)]^(k-1)`.
- `PROVED`: the determinant bound is sharp in the abstract Hilbert
  architecture. A two-eigenvalue Gram matrix has diagonal `M`, top
  eigenvalue `kw`, remaining eigenvalue `k(M-w)/(k-1)`, and an exact
  common-projection witness of squared norm `A`.
- `PROVED`: at `k=X^(21/25)` and `rho=X^(-3/5)`, the normalized logarithmic
  volume is at most `-X^(6/25+o(1))`.
- `PROVED` conditional reduction: a uniform lower bound
  `det(G_C/M)>=exp(-X^(theta+o(1)))` for any fixed `theta<6/25` on every
  target-sized, `X^(3/5)`-separated prime-phase row set would contradict the
  forced collapse and prove the skeleton target.
- `PROVED`: Cauchy--Binet rewrites the determinant as the sum of squared
  generalized prime Vandermonde minors. `OBSERVED`: no adequate lower bound
  for that minor sum is yet proved.

### Evidence and gate effect

- Artifact SHA-256:
  `5d647c7ccd850cdae77cb04bb5287d175cb210f1d546ab5f5341b50c4f185b5c`.
- Preregistration/theorem:
  `docs/cycle-20-exterior-volume-preregistration-v1.md` and
  `docs/cycle-20-exterior-volume-v1.md`.
- Exact conventions: `conventions/exterior_volume_v1.py`.
- Replay:

  ```sh
  python3 proof/build_cycle_20_exterior_volume_v1.py --check
  python3 -m unittest tests/test_cycle_20_exterior_volume_v1.py
  ```

- `OBSERVED`: write/check each used about `0.04` seconds and `18,540` KiB
  peak RSS; five tests passed in `0.06` seconds with `16,000` KiB peak RSS.
- Gate change: E7--E10 is `PRIME_LOG_VOLUME_OR_TWO_STEP_OPEN`. E8 now has an
  exact sufficient exponent and a sharp abstract boundary, parallel to E9's
  prime-specific two-step closure gate.

## Cycle 21 — continuum volume and weighted correction (2026-08-01)

### Headline outcomes

- `PROVED`: for the normalized continuous log-frequency frame on a fixed
  interval, `Delta`-separated rows have off-diagonal row sum at most a
  constant times `H_(k-1)/Delta`; Gershgorin gives the corresponding
  determinant lower bound.
- `PROVED` conditional reduction: after cyclic coloring by
  `ceil((log X)^2)`, continuum error is
  `o(X^(-3/5))`. If the normalized prime Gram matrix differs from the
  continuum Gram matrix in operator norm by `o(X^(-3/5))`, its determinant
  is `exp(-o(kX^(-3/5)))`, contradicting Cycle 20.
- `OBSERVED` correction: sealed v1 used uniform measure in
  `y=log(p/X)`. Its pure continuum theorem and explicitly conditional
  implication remain valid, but uniform log measure is not the natural prime
  limit and v1 is superseded as the strategic comparison.
- `PROVED` corrected v2: normalized prime mass has reference measure
  `dnu=e^y dy` on `[0,log 2]`. Its kernel is
  `(2^(1-ih)-1)/(1-ih)`, bounded by `3/|h|`; the row-sum constant becomes
  `6H_(k-1)/Delta`, while the sufficient discrepancy scale remains exactly
  `o(X^(-3/5))`.
- `OBSERVED`: the weighted prime operator discrepancy is open; no skeleton,
  density, or interval result is promoted.

### Evidence and gate effect

- V1 artifact SHA-256:
  `ed5f391adb5d767ec5c769043ea884633d09d65192057af8995104032dfdd391`.
- V2 correction artifact SHA-256:
  `2d326ad019096f23c9a15c3bf1a9d4b1f860fe5d3241a1dbbc78b9bb8c462971`.
- V1 theorem and v2 correction:
  `docs/cycle-21-continuum-volume-v1.md` and
  `docs/cycle-21-continuum-volume-correction-v2.md`.
- Replay:

  ```sh
  python3 proof/build_cycle_21_continuum_volume_v1.py --check
  python3 proof/build_cycle_21_continuum_volume_correction_v2.py --check
  python3 -m unittest tests/test_cycle_21_continuum_volume_v1.py
  python3 -m unittest tests/test_cycle_21_continuum_volume_correction_v2.py
  ```

- `OBSERVED`: v1 write/check used about `0.05/0.04` seconds and `18,524` KiB
  peak RSS; v2 correction write/check used about `0.05/0.04` seconds and
  `18,560` KiB peak RSS. Five tests passed for each version.
- Gate change: E7--E10 is
  `WEIGHTED_PRIME_QUADRATURE_OR_TWO_STEP_OPEN`. The natural E8 analytic input
  is now one operator-norm discrepancy, while E9 remains an independent
  arithmetic closure route.

## Cycle 22 — square-root volume noise and E8 renormalization (2026-08-01)

### Headline outcomes

- `PROVED`: for `k=2n`, a flat unitary `U` gives the exact positive Gram
  model `H=I+sqrt(n/m)[[0,U],[U*,0]]`. It has diagonal one,
  off-diagonal entries of modulus `m^(-1/2)`, operator deviation
  `sqrt(k/(2m))`, and determinant `(1-k/(2m))^(k/2)`.
- `PROVED`: at `m=X`, `k=X^(21/25)`, square-root entry noise produces
  operator scale `X^(-2/25)` and negative log-volume scale `X^(17/25)`.
  The former exceeds Cycle 21's sufficient gate by `13/25` powers; the latter
  exceeds Cycle 20's common-vector signature by `11/25` powers.
- `PROVED` scoped no-go: square-root entry cancellation alone cannot supply
  the full operator comparison or absolute determinant lower bound used in
  the raw E8 formulation. This does not prove actual prime rows realize the
  model and does not refute determinant methods with a bulk subtraction.
- `CONJECTURED`: the viable E8 object is a bulk-renormalized log determinant
  or spectral-shift statistic that removes ordinary `k^2/X` loss and retains
  the additional common-vector scale `kX^(-3/5)=X^(6/25)`.

### Evidence and gate effect

- Artifact SHA-256:
  `e75e69e9d8b770de14aa4c567a598ae60779b31c790b5714745c03068ce8f9cc`.
- Preregistration/theorem:
  `docs/cycle-22-volume-noise-preregistration-v1.md` and
  `docs/cycle-22-volume-noise-v1.md`.
- Exact conventions: `conventions/volume_noise_v1.py`.
- Replay:

  ```sh
  python3 proof/build_cycle_22_volume_noise_v1.py --check
  python3 -m unittest tests/test_cycle_22_volume_noise_v1.py
  ```

- `OBSERVED`: write/check used about `0.05/0.04` seconds with about
  `18,560` KiB peak RSS; five tests passed in `0.05` seconds with `15,972`
  KiB peak RSS.
- Gate change: E7--E10 is
  `RENORMALIZED_SPECTRAL_SHIFT_OR_TWO_STEP_OPEN`. The raw weighted-continuum
  comparison is retained as a conditional theorem but is no longer the
  principal E8 research target.

## Cycle 23 — residual spectral shift and inverse leverage (2026-08-01)

### Headline outcomes

- `PROVED`: for normalized Gram `H=UU*/M` and normalized common projection
  `q=Ua/sqrt(AM)`, the common-direction residual is exactly
  `Z=H-qq*=U(I-aa*/A)U*/M>=0`.
- `PROVED`: writing `rho_t=|q_t|^2`,
  `D=diag(sqrt(1-rho_t))`, `B=D^(-1)ZD^(-1)`, and `s=D^(-1)q`, a positive
  definite residual satisfies
  `det(H)/det(B)=product_t(1-rho_t)[1+s*B^(-1)s]`.
- `PROVED`: if every `rho_t>=rho` and inverse leverage
  `L=s*B^(-1)s<=exp(epsilon k rho)`, the bulk-renormalized shift is at most
  `-(1-epsilon)k rho+log 2`. Conversely, avoiding shift below `-c k rho`
  forces `L>=exp((1-c)k rho)-1`.
- `PROVED`: at the skeleton scales, `k rho=X^(6/25)`. Hence ordinary
  square-root spectral bulk cancels inside `det(B)`; the exact remaining
  alternatives are a detectable negative shift, exponentially large residual
  inverse leverage, or the separately retained `RESIDUAL_SINGULAR` branch.
- `OBSERVED`: no prime-specific leverage bound or singular-branch structure
  theorem is yet proved, so no skeleton, density, or interval promotion
  occurs.

### Evidence and gate effect

- Artifact SHA-256:
  `605e7a3eb5ac5b4e342b512e4465762d43b1b919051e4dafd01058e7ae14121b`.
- Preregistration/theorem:
  `docs/cycle-23-residual-spectral-shift-preregistration-v1.md` and
  `docs/cycle-23-residual-spectral-shift-v1.md`.
- Exact conventions: `conventions/residual_spectral_shift_v1.py`.
- Replay:

  ```sh
  python3 proof/build_cycle_23_residual_spectral_shift_v1.py --check
  python3 -m unittest tests/test_cycle_23_residual_spectral_shift_v1.py
  ```

- `OBSERVED`: write/check each used about `0.04` seconds with about
  `18,532` KiB peak RSS; five tests passed in `0.05` seconds with `15,872`
  KiB peak RSS.
- Gate change: E7--E10 is `RESIDUAL_LEVERAGE_OR_TWO_STEP_OPEN`. E8 now has a
  canonical bulk subtraction and one exact lock; E9 remains a genuinely
  independent recurrence route.

## Cycle 24 — leverage pruning and residual ill-conditioning (2026-08-01)

### Headline outcomes

- `PROVED`: freeze `delta=exp(-k rho/8)`. If at least half the rows have
  common-direction mass `rho_t>=1-delta`, those rows form a complete
  near-Cauchy recurrence packet: every normalized prime kernel has modulus at
  least `1-2delta` after phase alignment.
- `PROVED`: otherwise a subsystem of `n>=k/2` regular rows remains. It has
  either residual shift at most `-n rho/2`, a singular residual, or
  `lambda_min(B)<=2k exp(-k rho/8)`.
- `PROVED`: at the critical skeleton scale, every non-shift alternative is
  stretched exponential in `k rho=X^(6/25)`. This replaces an unstructured
  “large inverse leverage” condition by two explicit prime-arithmetic
  structures.
- `OBSERVED`: Cycle 24 itself excludes neither structure and promotes no
  skeleton, density, or interval result.

### Evidence and gate effect

- Artifact SHA-256:
  `939b0d39d4976be5b3dfbbef4e5797b3130504945825eb43cc9b5ed7516f5531`.
- Preregistration/theorem:
  `docs/cycle-24-leverage-pruning-preregistration-v1.md` and
  `docs/cycle-24-leverage-pruning-v1.md`.
- Exact conventions: `conventions/leverage_pruning_v1.py`.
- Replay:

  ```sh
  python3 proof/build_cycle_24_leverage_pruning_v1.py --check
  python3 -m unittest tests/test_cycle_24_leverage_pruning_v1.py
  ```

- `OBSERVED`: check and five focused tests each used about `0.04` seconds;
  peak RSS was `18,544` and `15,872` KiB respectively.
- Gate change: E8 is
  `NEAR_CAUCHY_OR_RESIDUAL_ILL_CONDITIONING_PRIME_EXCLUSION_OPEN`.

## Cycle 25 — near-Cauchy prime recurrence excluded (2026-08-01)

### Headline outcomes

- `PROVED`: if the normalized dyadic prime kernel at a difference `h` has
  modulus at least `1-2delta`, every prime-ratio phase is within
  `4 sqrt(M delta)` of one.
- `PROVED`: choose three primes in fixed separated proportional subintervals
  of `[X,2X]`. Eliminating `h` between two phase congruences produces a
  nonzero form `n log(p/q)-m log(r/q)` with `m,n<<X^(12/5+o(1))`.
- `PROVED`: Theorem 5.4 in the pinned Evertse notes (the explicit rational
  Matveev theorem) bounds that form below by `exp(-O((log X)^3))`, whereas
  Cycle 24 would bound it above by
  `exp(-X^(6/25-o(1))/16)`. Thus the near-Cauchy alternative is impossible
  for sufficiently large `X`.
- `OBSERVED`: collective residual singularity or
  `lambda_min(B)<=2k exp(-k rho/8)` remains open, as does detection of the
  negative shift. No skeleton, density, or interval result is promoted.

### Evidence and gate effect

- Artifact SHA-256:
  `a550a56484243f2e3b3cc4b237d41f91e794618a79630afdaac21c6426fa4392`.
- Source SHA-256:
  `artifacts/sources/evertse-linear-forms-logarithms-ch5.pdf` is
  `1f7f41e3b3292e380651baf4b30ed8717c3411909202dc0409a0d41ed4f149f0`.
- Preregistration/theorem:
  `docs/cycle-25-near-cauchy-exclusion-preregistration-v1.md` and
  `docs/cycle-25-near-cauchy-exclusion-v1.md`.
- Exact conventions: `conventions/near_cauchy_exclusion_v1.py`.
- Replay:

  ```sh
  python3 proof/build_cycle_25_near_cauchy_exclusion_v1.py --check
  python3 -m unittest tests/test_cycle_25_near_cauchy_exclusion_v1.py
  ```

- `OBSERVED`: write/check each used about `0.04` seconds and `18,688` KiB
  peak RSS; five tests used `0.04` seconds and `15,872` KiB peak RSS.
- Gate change: E7--E10 is `RESIDUAL_NEAR_DEPENDENCE_OR_SHIFT_OPEN`. The
  principal E8 object is now a generalized prime-Vandermonde lower bound for
  the normalized residual, not raw operator pseudorandomness.

## Cycle 26 — inverse leverage as detector reconstruction (2026-08-01)

### Headline outcomes

- `PROVED`: with normalized row matrix `X`, common unit vector `b`, residual
  row matrix `W`, `B=WW*`, and scaled common projection `s`, one has the
  exact decomposition `D^(-1)X=s b*+W`.
- `PROVED`: when `B>0`, set `c=B^(-1)s` and `L=s*B^(-1)s`. Then
  `c*s=L`, `||c*W||^2=L`, and
  `||(c*/L)D^(-1)X-b*||=L^(-1/2)`.
- `PROVED`: Cycle 24's large-leverage branch therefore reconstructs the
  normalized detector coefficient vector from scaled prime-phase rows with
  error at most `sqrt(2)exp(-k rho/8)`, stretched exponential in
  `X^(6/25-o(1))`.
- `PROVED`: if `B` is singular, every residual null vector gives either exact
  detector reconstruction (`c*s!=0`) or exact linear dependence among the
  scaled prime rows (`c*s=0`).
- `OBSERVED`: reconstruction has not yet been converted into a source-valid
  complementary detector, and exact row dependence is not excluded. No
  skeleton, density, or interval result is promoted.

### Evidence and gate effect

- Artifact SHA-256:
  `6082d255ea07383913f30ceb5d9835e5f902245972d208af66b95acd27dcc64e`.
- Preregistration/theorem:
  `docs/cycle-26-detector-reconstruction-preregistration-v1.md` and
  `docs/cycle-26-detector-reconstruction-v1.md`.
- Exact conventions: `conventions/detector_reconstruction_v1.py`.
- Replay:

  ```sh
  python3 proof/build_cycle_26_detector_reconstruction_v1.py --check
  python3 -m unittest tests/test_cycle_26_detector_reconstruction_v1.py
  ```

- `OBSERVED`: write/check each used about `0.04` seconds and `18,688` KiB
  peak RSS; five tests used `0.04` seconds and `15,872` KiB peak RSS.
- Gate change: E7--E10 is
  `DETECTOR_RECONSTRUCTION_OR_EXACT_DEPENDENCE_OPEN`. E10 becomes the largest
  active allocation: exploit reconstruction rather than first trying to
  contradict it. Exact dependence and shift detection remain parallel E8/E9
  branches.

## Cycle 27 — Hadamard detector surgery (2026-08-01)

### Headline outcomes

- `PROVED`: partition the prime atom into `J` equal-mass coordinate blocks
  and sign them by a Sylvester Hadamard system. The resulting `J` detector
  coefficient vectors are orthogonal, have equal norm, and preserve every
  coefficient magnitude.
- `PROVED`: for block contributions `z_j` and signed detector values `S_ell`,
  `sum_ell|S_ell|^2=J sum_j|z_j|^2` and
  `sum_(ell>=1)|S_ell|^2=J sum_j|z_j-S_0/J|^2`.
- `PROVED`: if `|S_0|>=V`, either a non-original detector orthogonal to the
  original resonance has value at least `V/(4J)`, or, after aligning `S_0`,
  every block contribution has real part greater than `3V/(4J)`.
- `PROVED`: for `J=X^o(1)`, both alternatives lose only a subpower. Thus
  complementary detector conservation fails only on a simultaneously
  aligned multiblock family, which is a concrete E7 input.
- `OBSERVED`: neither the orthogonal signed frame nor the multiblock family
  has yet been bounded with a fixed-power saving. No skeleton, density, or
  interval result is promoted.

### Evidence and gate effect

- Artifact SHA-256:
  `4a62765a22c0a2ca7a70d5917925859029faad155827a031efee90918c703c53`.
- Preregistration/theorem:
  `docs/cycle-27-hadamard-detector-surgery-preregistration-v1.md` and
  `docs/cycle-27-hadamard-detector-surgery-v1.md`.
- Exact conventions: `conventions/hadamard_detector_surgery_v1.py`.
- Replay:

  ```sh
  python3 proof/build_cycle_27_hadamard_detector_surgery_v1.py --check
  python3 -m unittest tests/test_cycle_27_hadamard_detector_surgery_v1.py
  ```

- `OBSERVED`: write/check each used about `0.04` seconds and `18,688` KiB
  peak RSS; five tests used `0.04` seconds and `15,872` KiB peak RSS.
- Gate change: E7--E10 is `ORTHOGONAL_SURGERY_OR_MULTIBLOCK_SYNC_OPEN`.
  Research priority shifts to a prime-log bound for simultaneous aligned
  block values and an exact mixed-trace ledger for iterated orthogonal
  signings.

### Cycle 27 v2 correction — prime-count remainder (2026-08-01)

- `OBSERVED` correction: v1's application prose treated equal-cardinality
  prime blocks as automatic, but the dyadic prime count `M` need not be
  divisible by `J`. The conditional equal-mass theorem itself is unchanged.
- `PROVED`: retain `J floor(M/J)` coordinates and discard `r<J`. Every
  detector value changes by at most `r`, so v1 applies with `V'=V-O(J)`.
  For `J=X^o(1)`, the relative detector and mass losses are respectively
  `X^(-7/10+o(1))` and `X^(-1+o(1))`.
- Correction artifact SHA-256:
  `3010bb6b8f32fad2d10630c8ce9fc15682393ecc54d0567bfa82597582d7c4e5`.
- Correction documents:
  `docs/cycle-27-hadamard-detector-surgery-correction-preregistration-v2.md`
  and `docs/cycle-27-hadamard-detector-surgery-correction-v2.md`.
- Replay:

  ```sh
  python3 proof/build_cycle_27_hadamard_detector_surgery_correction_v2.py --check
  python3 -m unittest tests/test_cycle_27_hadamard_detector_surgery_correction_v2.py
  ```

- `OBSERVED`: write/check used `0.04` seconds and about `18,420/18,492` KiB
  peak RSS; four tests used `0.04` seconds and `15,872` KiB peak RSS.

## Cycle 28 — rank-J spectral shift and reconstruction (2026-08-01)

### Headline outcomes

- `PROVED`: for an orthonormal `J`-dimensional detector subspace,
  `det(XX*)/det(B)=product_t(1-rho_t)det(I_J+S*B^(-1)S)`.
- `PROVED`: if `K=sum rho_t` and the shift exceeds `-K/2`, then
  `lambda_max(S*B^(-1)S)>=exp(K/(2J))-1`. Its top eigenvector identifies an
  adaptive detector-subspace direction reconstructed with error
  `lambda_max^(-1/2)`.
- `PROVED`: the Cycle 27 threshold ledger retains shift magnitude
  `k rho/(32J^2)` or reconstruction error
  `sqrt(2)exp(-k rho/(64J^3))`; for `J=X^o(1)` both remain on the
  `X^(6/25-o(1))` stretched-exponential scale.
- `PROVED`: a singular residual gives exact detector-subspace reconstruction
  or exact scaled-row dependence.
- `OBSERVED`: no prime-specific contradiction or density promotion follows.

### Evidence and gate effect

- Artifact SHA-256:
  `53d2c7eca302b3fd02ff499578657c533a1747077f4e21439587ecc56614a576`.
- Theorem: `docs/cycle-28-rank-j-spectral-shift-v1.md`.
- Replay:

  ```sh
  python3 proof/build_cycle_28_rank_j_spectral_shift_v1.py --check
  python3 -m unittest tests/test_cycle_28_rank_j_spectral_shift_v1.py
  ```

- `OBSERVED`: write/check used about `0.04/0.05` seconds and `18,688` KiB
  peak RSS; five tests used `0.04` seconds and `15,984` KiB peak RSS.
- Gate effect: replace detector colors by one common detector subspace.

## Cycle 29 — polynomial block-subspace amplification (2026-08-01)

### Headline outcomes

- `PROVED`: take `J=X^(1/25+o(1))` consecutive prime intervals and the
  normalized restrictions of the original coefficient vector. Their span
  contains the original detector, so every row retains projection at least
  `rho=X^(-3/5-o(1))` with no `J` loss.
- `PROVED`: a half-sized packet within squared distance
  `delta=exp(-k rho/8)` of this block subspace is impossible. Two rows and
  three good primes inside one block produce a nonzero logarithmic form with
  upper `exp(-k rho/32+O(log X))`, contradicting Matveev's
  `exp(-O((log X)^3))` lower bound.
- `PROVED`: on the regular half-system, the alternatives are shift at most
  `-k rho/4`, approximate or exact reconstruction of a block-modulated
  detector direction, or exact scaled-row dependence. Approximate
  reconstruction error is `exp(-X^(1/5-o(1)))`.
- `OBSERVED`: the entropy/profile of the block modulation has not been
  exploited; no skeleton, density, or interval result is promoted.

### Evidence and gate effect

- Artifact SHA-256:
  `bec07567ef2855c27f67bcb05f21268873fdaa7b1f87a540e38047820029aed8`.
- Theorem: `docs/cycle-29-polynomial-block-subspace-v1.md`.
- Pinned source inputs include the checked G0 uniform PNT dependency graph
  and the Cycle 25 Evertse/Matveev source.
- Replay:

  ```sh
  python3 proof/build_cycle_29_polynomial_block_subspace_v1.py --check
  python3 -m unittest tests/test_cycle_29_polynomial_block_subspace_v1.py
  ```

- `OBSERVED`: write/check each used `0.04` seconds and `18,688` KiB peak RSS;
  five tests used `0.05` seconds and `15,872` KiB peak RSS.
- Gate effect: the live inverse object is a polynomial-dimensional scalar
  modulation of the original prime coefficients.

## Cycle 30 — abstract block-subspace saturation (2026-08-01)

### Headline outcomes

- `PROVED`: a block-flat detector and tuned simplex residual simultaneously
  realize arbitrary row count, arbitrary separated labels, perfect aligned
  block contributions, zero nontrivial Hadamard detector values, and common
  projection squared `rho`.
- `PROVED`: choosing
  `L_target=(1-rho)^(-k)-1` and
  `epsilon=k rho/((1-rho)L_target)` makes inverse leverage exactly
  `L_target` and the multiplicative determinant shift exactly one. The common
  detector is reconstructed with error `L_target^(-1/2)`.
- `PROVED`: at the critical scales the residual small eigenvalue and
  reconstruction error are stretched exponential on `X^(6/25)`.
- `PROVED` scoped saturation: projection size, label separation, block-flat
  synchronization, Hadamard surgery, residual normalization, determinant
  shift, and reconstruction do not bound the row count for unrestricted
  Hilbert rows. This is not asserted for actual prime phases.
- `OBSERVED`: further linear-algebra-only refinements cannot close the live
  gate; actual logarithmic/multiplicative structure is mandatory.

### Evidence and gate effect

- Artifact SHA-256:
  `36517f5e75a2c951034f1722c9427d207c28d082cf7dd4cece3e1cb1077308f2`.
- Theorem: `docs/cycle-30-block-subspace-extremizer-v1.md`.
- Replay:

  ```sh
  python3 proof/build_cycle_30_block_subspace_extremizer_v1.py --check
  python3 -m unittest tests/test_cycle_30_block_subspace_extremizer_v1.py
  ```

- `OBSERVED`: write/check used about `0.04/0.05` seconds and about
  `18,560/18,688` KiB peak RSS; five tests used `0.05` seconds and `15,872`
  KiB peak RSS.
- Gate change: E7--E10 is `PRIME_CURVE_BLOCK_MODULATION_OPEN`. The next
  theorem must use the actual values `p^(-it)`, unique factorization, or an
  equivalent source constraint.

## Cycle 31 — variable-rank amplification and self-dual scale (2026-08-01)

### Headline outcomes

- `PROVED`: Cycle 29 extends from `kappa=1/25` to every fixed
  `0<kappa<6/25`. The blockwise Matveev exclusion remains valid because
  block length stays inside the checked PNT range and
  `|h|/J>=X^(3/5-kappa+o(1))` tends to infinity.
- `PROVED`: the regular reconstruction error is
  `exp(-X^(6/25-kappa-o(1)))`; the exponent is positive precisely throughout
  the registered range.
- `PROVED`: `kappa=4/25` is self-dual. Block count has exponent `4/25`, one
  block and the target skeleton each have exponent `21/25`, and the
  reconstruction error has exponent `2/25`.
- `OBSERVED`: this identifies a square generalized-prime-Vandermonde scale
  but proves no determinant lower bound, skeleton gain, density gain, or
  interval gain.

### Evidence and gate effect

- Artifact SHA-256:
  `7c6f3a75cbe0d16ebe729260cbc7ac42fee4b86e00b80fb832926317e8f11784`.
- Theorem: `docs/cycle-31-variable-rank-self-dual-v1.md`.
- Replay:

  ```sh
  python3 proof/build_cycle_31_variable_rank_self_dual_v1.py --check
  python3 -m unittest tests/test_cycle_31_variable_rank_self_dual_v1.py
  ```

- `OBSERVED`: write/check each used `0.05` seconds and `18,688` KiB peak RSS;
  five tests used `0.04` seconds and `15,872` KiB peak RSS.
- Gate effect: use the `4/25 : 21/25` block decomposition as the principal
  arithmetic scale.

## Cycle 32 — flat-support modulation ladder (2026-08-01)

### Headline outcomes

- `PROVED`: discard modulation coordinates below `1/(2sqrt(J))`; they carry
  at most one quarter of the squared mass. One of `O(log X)` dyadic amplitude
  bins then carries squared mass at least `3/(4L)`.
- `PROVED`: after projection and normalization, the selected `s` block
  coefficients have magnitudes between `1/(2sqrt(s))` and `2/sqrt(s)`, while
  reconstruction error remains `exp(-X^(2/25-o(1)))`.
- `PROVED`: writing `s=X^(lambda+o(1))`, the prime-coordinate exponent is
  `21/25+lambda`, the row exponent is `21/25`, and coordinate excess is
  exactly `lambda`, for `0<=lambda<=4/25`.
- `PROVED`: `lambda=0` is square in exponent; the other rungs have quantified
  positive coordinate excess.
- `OBSERVED`: no ladder rung is yet excluded, so no skeleton, density, or
  interval promotion occurs.

### Evidence and gate effect

- Artifact SHA-256:
  `be844d4e3967573eb7e00464e6be3a85a10d37c943c3a6e3e8607734b04bfa22`.
- Theorem: `docs/cycle-32-flat-support-modulation-v1.md`.
- Replay:

  ```sh
  python3 proof/build_cycle_32_flat_support_modulation_v1.py --check
  python3 -m unittest tests/test_cycle_32_flat_support_modulation_v1.py
  ```

- `OBSERVED`: write/check each used `0.04` seconds and `18,688` KiB peak RSS;
  five tests used `0.04` seconds and `16,000` KiB peak RSS.
- Gate change: E7--E10 is `SELF_DUAL_FLAT_SUPPORT_PRIME_CURVE_OPEN`. The
  immediate theorem target is the square `lambda=0` prime-Vandermonde rung;
  positive rungs go to support pruning or multiplicative energy.

## Cycle 33 — anchor-aware correction (2026-08-01)

### Headline outcomes

- `PROVED` actual-prime counterexample: for any prime support and real
  `t_0`, the normalized restricted row `p^(-it_0)` is exactly flat and lies
  exactly in any phase-row span containing `t_0`. Its augmented Gram
  determinant is zero.
- `PROVED` dimension boundary: when a `k by N` row matrix has full column rank
  and `k>=N`, every detector lies in the row span. On an exponent-square
  rung, invertibility confirms reconstruction rather than excluding it.
- `OBSERVED` correction: Cycle 32's flat-support theorem remains valid, but
  the proposed universal `lambda=0` distance/determinant lower bound is too
  broad.
- `PROVED` reduction: define `alpha_r(d)` as distance to the closest span of
  at most `r=X^o(1)` anchor rows. Small `alpha_r` converts detector values
  into weighted restricted prime kernels `K_S(t-t_a)`; positive `alpha_r`
  isolates genuinely many-row transverse reconstruction.
- `OBSERVED`: neither branch is yet bounded, so no skeleton, density, or
  interval result is promoted.

### Evidence and gate effect

- Artifact SHA-256:
  `6594393b00ff39f98b85d8eb1027dbf85187c6772ef97d9616d14a3a580b654d`.
- Theorem/correction: `docs/cycle-33-anchor-aware-correction-v1.md`.
- Replay:

  ```sh
  python3 proof/build_cycle_33_anchor_aware_correction_v1.py --check
  python3 -m unittest tests/test_cycle_33_anchor_aware_correction_v1.py
  ```

- `OBSERVED`: write/check used `0.04` seconds and about `18,560/18,432` KiB
  peak RSS; five tests used `0.05` seconds and `15,872` KiB peak RSS.
- Gate change: E7--E10 is
  `ANCHOR_RECURRENCE_OR_TRANSVERSE_RECONSTRUCTION_OPEN`. The one-anchor
  restricted-kernel exponent ledger is the immediate next action.

## Cycle 33 v2 correction — anchor evaluation and stability scope (2026-08-01)

### Headline correction

- `PROVED`: distance of a reconstructed direction to an anchor span does not
  by itself transfer the original large detector values. The direction must
  also have a quantitative evaluation floor on the row set.
- `PROVED`: a many-anchor transfer additionally requires a coefficient norm
  bound; a small approximation error with arbitrarily unstable coefficients
  gives no useful pigeonhole threshold.
- `PROVED`: the original normalized detector has evaluation floor
  `sqrt(rho)` on the retained rows, so Cycle 26's original-detector anchor
  branch remains valid. No such floor has been proved for the adaptive
  rank-`J` directions from Cycles 28--32.
- `OBSERVED` correction: Cycle 33 v1's proposed anchor-versus-transverse
  taxonomy was too broad. The flat-support ladder remains a reconstruction
  theorem only until evaluation and stability are separately established.

### Evidence and gate effect

- Correction artifact SHA-256:
  `dbe25f01bdf8a49aa4f6cace91dcce773a8c76ebc2f9a3879ca185028274ef75`.
- Correction theorem:
  `docs/cycle-33-anchor-aware-scope-correction-v2.md`.
- Replay:

  ```sh
  python3 proof/build_cycle_33_anchor_aware_scope_correction_v2.py --check
  python3 -m unittest tests/test_cycle_33_anchor_aware_scope_correction_v2.py
  ```

- Gate effect: retain the original-detector anchor branch; quarantine the
  adaptive-direction recurrence implication until both an evaluation floor
  and stable coefficients are proved.

## Cycle 34 — stable anchors reduce to the unweighted prime kernel (2026-08-01)

### Headline outcomes

- `PROVED`: if the normalized original detector is
  `epsilon=o(sqrt(rho))`-close to one normalized phase row, then every
  translated skeleton row satisfies
  `|sum_(X<p<=2X)p^(-ih)|>=X^(7/10-o(1))`.
- `PROVED`: translation preserves the `X^(3/5)` separation and polynomial
  height bound. Hence the one-anchor branch is exactly an unweighted
  prime-kernel large-values problem.
- `PROVED`: an approximation by `X^o(1)` anchors with coefficient `l1` norm
  `X^o(1)` reduces by witness colouring to the one-anchor problem without a
  fixed-power loss.
- `PROVED` reduction: it is sufficient to prove that the number of
  `X^(3/5)`-separated `h`, `|h|<=X^(12/5)`, with unweighted kernel at least
  `X^(7/10-o(1))` is `X^(21/25+o(1))`. The checked generic skeleton exponent
  is `1`, so the exact missing saving is `4/25`.
- `OBSERVED`: the kernel theorem, stability of Cycle 26/28 reconstruction
  coefficients, adaptive evaluation floors, and transverse reconstruction
  remain open. No density or interval result is promoted.

### Evidence and gate effect

- Artifact SHA-256:
  `0390c0f9ce57deccfee89e2fa3632c9a0e217818f9d7b94ddbe5960ead63c4a1`.
- Theorem: `docs/cycle-34-stable-anchor-kernel-v1.md`.
- Replay:

  ```sh
  python3 proof/build_cycle_34_stable_anchor_kernel_v1.py --check
  python3 -m unittest tests/test_cycle_34_stable_anchor_kernel_v1.py
  ```

- `OBSERVED`: write/check used `0.05/0.04` seconds and
  `18,688/18,560` KiB peak RSS; five tests used `0.05` seconds and
  `15,872` KiB peak RSS.
- Gate change: E7--E10 is
  `UNWEIGHTED_KERNEL_OR_TRANSVERSE_RECONSTRUCTION_OPEN`. The unweighted
  kernel theorem is the lead arithmetic target; unstable and transverse
  reconstructions are separate branches.

### Current-chain replay

- `PROVED`: all 27 available proof builders for Cycles 10--34 replayed with
  `--check`, including both correction versions where present.
- `PROVED`: the 28 Cycle 10--34 test modules ran 128 tests with no failures.
- `OBSERVED`: repository-wide discovery ran 282 tests and retained 12 legacy
  Cycle 4--8 failures. Six are errors, chiefly old preregistration/audit
  scripts intentionally bound to a historical `PLAN.md`; six are stale
  wording or superseded-artifact assertions. They predate Cycles 10--34 and
  are not evidence against the current theorem chain. They remain visible
  for a future versioned legacy-test correction and were not edited during
  this research-stage update.

## Cycle 35 — kernel-engine ledger and entropy--volume match (2026-08-01)

### Headline outcomes

- `PROVED`: after removing the coherent point `h=0`, a separated
  `24/5` estimate
  `sum_(h in C)|K(h)|^(24/5)<=X^(21/5+o(1))` implies the target
  `|C|<=X^(21/25+o(1))`. Relative to the Cycle 14 global moment scale, the
  exact required saving is `X^(3/5)`, equal to the skeleton spacing.
- `PROVED`: finite van der Corput differencing reduces low-time pointwise
  control to aggregate shifted-prime correlations `C_r(t)`. The estimate
  `sum_r|C_r(t)|<=X^(2+o(1))/|t|` would give
  `|K(t)|<=X^(7/10-eta/2+o(1))` for
  `|t|>=X^(3/5+eta)`.
- `PROVED`: for the unrestricted integer correlations, the monotone
  first-derivative estimate gives
  `|I_r(t)|<<min(X,X^2/(|t|r))` and aggregate
  `X^2 log X/|t|` at low time. `OBSERVED`: this cancellation does not
  transfer merely by deleting composite indices; a sifted oscillatory
  estimate is the new prime-specific gate, and high times remain separate.
- `PROVED`: discretizing prime phases into
  `L>=2pi/delta` arcs and applying Pinsker gives histogram divergence at
  least `delta^2/8=X^(-3/5-o(1))` for every threshold row.
- `PROVED` cross-engine match: a target-sized skeleton therefore carries
  total phase information on exponent `21/25-3/5=6/25`, exactly the
  independently sealed exterior-volume and residual spectral-shift scale.
  An entropy accumulation upper bound at that exponent would close the
  kernel theorem.
- `OBSERVED`: hollow restriction, sifted curvature, and entropy accumulation
  are all open. No kernel-count, density, or interval result is promoted.

### Evidence and gate effect

- Artifact SHA-256:
  `cedc4cce7699fa02db9cabe2346286aac3eabd4f82e4559d4f0263c268cdce3e`.
- Theorem: `docs/cycle-35-kernel-engine-ledger-v1.md`.
- Replay:

  ```sh
  python3 proof/build_cycle_35_kernel_engine_ledger_v1.py --check
  python3 -m unittest tests/test_cycle_35_kernel_engine_ledger_v1.py
  ```

- `OBSERVED`: write/check used `0.05/0.04` seconds and `18,688` KiB peak
  RSS; six tests used `0.05` seconds and `16,000` KiB peak RSS.
- Gate change: E7--E10 is `ENTROPY_VOLUME_OR_SIFTED_CURVATURE_OPEN`.
  First test the information-projection/determinant seam; pursue a
  phase-retaining Selberg/Vaughan decomposition if the higher-harmonic
  remainder cannot be controlled.

## Cycle 36 — information projection and first-harmonic saturation (2026-08-01)

### Headline outcomes

- `PROVED`: for a phase histogram with fixed rotated first moment `r`, the
  von Mises exponential family is its KL information projection. The exact
  Pythagorean identity is
  `D(q||u)=J(r)+E(q)`, where `E(q)=D(q||qstar)>=0`.
- `PROVED`: exact formal-series arithmetic gives
  `J(r)=r^2+r^4/4+5r^6/36+O(r^8)` and
  `kappa(r)=2r+r^3+(5/6)r^5+O(r^7)`.
- `PROVED`: at `r^2=rho=X^(-3/5)` and `k=X^(21/25)`, both
  `kJ(r)` and the sharp Cycle 20 common-projection negative log determinant
  equal `(1+o(1))k rho`, with leading constant one and exponent `6/25`.
  First-harmonic entropy is therefore the determinant collapse in
  information coordinates, not an independent saving.
- `PROVED`: if the entropy excess is quadratically tiny,
  `E(q)=o(r^4)`, Pinsker preserves the von Mises second harmonic
  `r^2/2+o(r^2)`. Its unnormalized prime-kernel scale is `X^(2/5)`, exactly
  the Cycle 19 popular-edge threshold.
- `PROVED` scoped saturation: minimal first-harmonic information plus the
  sharp determinant/graph mechanisms cannot supply the missing `4/25`.
  The only new E7 objects are excess entropy and joint von Mises rigidity
  across separated rows.
- `OBSERVED`: neither object is bounded for actual prime rows. No
  prime-kernel count, density gain, or interval gain is promoted.

### Evidence and gate effect

- Artifact SHA-256:
  `a80600191a8dd58642b6bf9bc72a40c6946c4503b36db213cdee5ec0037b027d`.
- Theorem: `docs/cycle-36-information-projection-v1.md`.
- Replay:

  ```sh
  python3 proof/build_cycle_36_information_projection_v1.py --check
  python3 -m unittest tests/test_cycle_36_information_projection_v1.py
  ```

- `OBSERVED`: write/check used `0.04/0.04` seconds and about
  `18,560/18,432` KiB peak RSS; six tests used `0.05` seconds and
  `16,128` KiB peak RSS.
- Gate change: E7--E10 is `EXCESS_ENTROPY_OR_SIFTED_CURVATURE_OPEN`.
  Decompose entropy excess by harmonic scale or prove joint von Mises
  incompatibility; retain sifted curvature as the independent lead.

## Cycle 37 — entropy-excess harmonic-routing boundary (2026-08-01)

### Headline outcomes

- `PROVED`: on `L` equal arcs, Parseval identifies chi-square divergence with
  total nonzero Fourier mass; when the von Mises projection is uniformly
  comparable to the uniform histogram, KL excess is comparable to the
  squared full harmonic vector above that projection.
- `PROVED` exact hiding model: for any `2<=m<=L-2`, the positive
  perturbation
  `q_j=qstar_j+(2a/L)cos(2pi m j/L)` preserves total mass and the first
  Fourier coefficient exactly while adding Fourier coefficients `a` only at
  `m` and `L-m`. Its excess is comparable to `a^2`, uniformly in `m`.
- `PROVED` scoped no-go: raw entropy excess does not select bounded harmonic
  order. With `L=X^(3/10)`, scalar pigeonholing loses `X^(3/10)`, exceeding
  the entire missing saving `X^(4/25)`.
- `PROVED` routing ledger: excess at the `r^4=X^(-6/5)` and
  `r^2=X^(-3/5)` scales forces, by scalar selection alone, only unnormalized
  kernel exponents `1/4` and `11/20`. These are respectively below the
  Cycle 19 popular-kernel scale `2/5` and the original threshold `7/10`.
- `OBSERVED`: the hiding model is an abstract histogram, not an actual-prime
  row family. E7 remains open through a vector-valued all-harmonic estimate
  or a theorem forbidding high-order hiding jointly across actual prime
  rows. No kernel-count, density, or interval result is promoted.

### Evidence and gate effect

- Artifact SHA-256:
  `4877fa4480dd6834253be58be82f981f2600002f9c385079acbccd288fc7dd43`.
- Theorem: `docs/cycle-37-excess-harmonic-routing-v1.md`.
- Replay:

  ```sh
  python3 proof/build_cycle_37_excess_harmonic_routing_v1.py --check
  python3 -m unittest tests/test_cycle_37_excess_harmonic_routing_v1.py
  ```

- `OBSERVED`: write/check used `0.04/0.04` seconds and about
  `18,560/18,540` KiB peak RSS; five tests used `0.04` seconds and
  `15,872` KiB peak RSS.
- Gate change: E7--E10 is `VECTOR_HARMONIC_OR_SIFTED_CURVATURE_OPEN`.
  Do not spend the `L` colour loss; retain the harmonic vector or use common
  prime-row coupling. Sifted curvature remains equal priority.

### Current-chain replay

- `PROVED`: all 30 available proof builders for Cycles 10--37 replayed with
  `--check`, including every retained correction version.
- `PROVED`: the 31 Cycle 10--37 test modules ran 145 tests with no failures.
- `OBSERVED`: `git diff --check` passed. The previously logged legacy Cycle
  4--8 failures were not rerun or altered in this cycle.

## Cycle 38 — vector rescaling boundary and two-scale lift (2026-08-01)

### Headline outcomes

- `PROVED`: the fan `t_m=4A^2 Delta/m`, `A<=m<2A`, is
  `Delta`-separated and has the common rescaled ordinate `mt_m=4A^2 Delta`.
  Thus flattening the harmonic vector has sharp collision multiplicity `A`;
  at `A=X^(3/10)` this exceeds the missing `X^(4/25)` saving.
- `PROVED`: retaining the original large value gives
  `D_m(t)=K(t)K(mt)=sum_(p,q)(pq^m)^(-it)`. Unique factorization makes the
  ordered labels injective for every `m>=2`, including `p=q`, so the exact
  cardinality and coefficient-square norm are both `M^2`.
- `PROVED` ledger: harmonic energy `X^(-e)` forces per-row two-scale energy
  exponent `17/5-e`; the registered vector targets are `91/25` for `e=3/5`
  and `76/25` for `e=6/5`.
- `OBSERVED`: no estimate at either target is proved. Ambient support near
  `X^(m+1)` cannot be replaced by the sparse cardinality without a new
  theorem, and excess relative to the von Mises vector need not transfer at
  the transition scale because of cancellation.

### Evidence and gate effect

- Artifact SHA-256:
  `0da5a1791b7228a19651db15ecf3bce1909bbc2c57b985bee107e8787010de52`.
- Theorem: `docs/cycle-38-vector-harmonic-two-scale-v1.md`.
- Replay:

  ```sh
  python3 proof/build_cycle_38_vector_harmonic_two_scale_v1.py --check
  python3 -m unittest tests/test_cycle_38_vector_harmonic_two_scale_v1.py
  ```

- `OBSERVED`: write/check used `0.05/0.04` seconds and
  `18,548/18,544` KiB peak RSS; six tests used `0.05` seconds and
  `16,000` KiB peak RSS.
- Gate change: E7 becomes a two-scale sparse prime-monomial problem; scalar
  flattening is closed as a route.

## Cycle 39 — moment-amplified prime-monomial reduction (2026-08-01)

### Headline outcomes

- `PROVED`: for fixed `s`, every coefficient of
  `K(t)^sK(mt)` is at most `(1+floor(s/2))s!`, uniformly for `m>=2`, and its
  coefficient-square norm lies between `M^(s+1)` and that constant times
  `M^(s+1)`. The proof counts possible exponent-`m` primes and residual
  ordered prime multisets.
- `PROVED` conditional reduction: the hollow separated estimate
  `AMPR_s: sum_t sum_m|K(t)^sK(mt)|^2<=X^(s+31/10+o(1))` gives row-count
  exponent `11/10+e-2s/5` on harmonic-energy branch `X^(-e)`.
- `PROVED`: `s=3` is the least integer moment closing `e=3/5`; it gives
  count exponent `1/2` and margin `17/50`. `s=4` is least for `e=6/5`; it
  gives exponent `7/10` and margin `7/50`.
- `PROVED` scoped obstruction: `s=1`, even granted the same idealized
  cardinality-scale restriction, yields exponents `13/10` and `19/10` and
  closes neither branch. Amplification is necessary inside this reduction.
- `CONJECTURED`: `AMPR_3` and `AMPR_4` hold for actual prime phases. The
  estimates must be hollow, separated, fixed in `s`, and uniform over
  `2<=m<=X^(3/10)`. No kernel-count, density, or interval result is promoted.

### Evidence and gate effect

- Artifact SHA-256:
  `3b83385d1d7e7ed447cafe0f7e42be1badb1bb26ba42cc458cf3fa3b8f204826`.
- Theorem: `docs/cycle-39-moment-amplified-prime-monomial-v1.md`.
- Replay:

  ```sh
  python3 proof/build_cycle_39_moment_amplified_prime_monomial_v1.py --check
  python3 -m unittest tests/test_cycle_39_moment_amplified_prime_monomial_v1.py
  ```

- `OBSERVED`: write/check used `0.04/0.04` seconds and
  `18,432/18,556` KiB peak RSS; six tests used `0.05` seconds and
  `16,000` KiB peak RSS.
- Gate change: E7--E10 is
  `MOMENT_AMPLIFIED_PRIME_MONOMIAL_RESTRICTION_OPEN`. The next cycle expands
  `AMPR_s` into exact near-collision kernels and measures the permissible
  loss against margins `17/50` and `7/50`.

### Current-chain replay

- `PROVED`: all 32 available proof builders for Cycles 10--39 replayed with
  `--check`, including every retained correction version.
- `PROVED`: the 33 Cycle 10--39 test modules ran 157 tests with no failures.
- `OBSERVED`: `git diff --check` passed. The previously logged legacy Cycle
  4--8 failures were not rerun or altered.

## Cycle 40 — coherent global floor and hollow-notch correction (2026-08-01)

### Headline outcomes

- `PROVED`: after removing its harmless carrier phase, `K(t)^sK(mt)` has
  frequency bandwidth at most `(s+m)log 2` and total nonnegative coefficient
  mass `M^(s+1)`.
- `PROVED`: the triangular-kernel identity, a `1/H` frequency partition,
  positivity, and Cauchy--Schwarz give the uniform lower bound
  `integral_(|t|<=H)(1-|t|/H)|K(t)^sK(mt)|^2 dt
  >=M^(2s+2)/(12(s+m))`.
- `PROVED`: summing this floor over `m<=X^(3/10)` has exponent `2s+2`, which
  exceeds `AMPR_3` by `19/10` and `AMPR_4` by `29/10`. An unmodified global
  positive-kernel mean or raw near-collision count is therefore mis-scaled.
- `PROVED` scope boundary: the floor may be supplied entirely by the
  coherent `O(1/m)` neighborhood of zero, whereas `AMPR_s` uses
  `|t|>=X^(3/5)`. It does not refute the hollow discrete estimates.
- `CONJECTURED`: a notched restriction operator, centred Gram residual, or
  finite difference removes the zero packet while preserving enough of the
  large row values. No kernel-count, density, or interval gain is promoted.

### Evidence and gate effect

- Artifact SHA-256:
  `d8a2c9cabc9834dc26ec7850e1f9268e136b2e2b13d1ddc6690195553b646254`.
- Theorem: `docs/cycle-40-hollow-notch-v1.md`.
- Replay:

  ```sh
  python3 proof/build_cycle_40_hollow_notch_v1.py --check
  python3 -m unittest tests/test_cycle_40_hollow_notch_v1.py
  ```

- `OBSERVED`: write/check used `0.04/0.04` seconds and
  `18,516/18,520` KiB peak RSS; four tests used `0.05` seconds and
  `15,872` KiB peak RSS.
- Gate change: E7--E10 is `HOLLOW_NOTCHED_AMPLIFIED_RESTRICTION_OPEN`.
  Global collision counting is removed from the lead actions; differencing
  and centred residual operators become the constructive next steps.

## Cycle 41 — smooth annular sampling and signed collision form (2026-08-01)

### Headline outcomes

- `PROVED`: a smooth reproducing kernel at centered bandwidth `B` gives a
  sampling inequality for any hollow `Delta`-separated set: the sample sum
  is bounded by `B` times the mean square on
  `Delta/2<=|u|<=H+Delta/2`, plus Schwartz tail leakage.
- `PROVED`: for `F_(m,s)` and decay order nine, summing the leakage over
  `m<=X^(3/10)` gives exponents `47/10` for `s=3` and `67/10` for `s=4`.
  These lie below the corresponding targets by `7/5` and `2/5`.
- `PROVED`: the annular mean is exactly the prime-monomial collision form
  with signed kernel `2(sin(bu)-sin(au))/u`. Replacing it by its absolute
  value restores the Cycle 40 coherent floor and is not a valid route.
- `PROVED` reduction: the weighted annular estimates
  `ASAM_s: sum_m(s+m) integral_W|K(u)^sK(mu)|^2du
  <=X^(s+31/10+o(1))` imply `AMPR_s` and inherit its closure margins.
- `CONJECTURED`: `ASAM_3` or `ASAM_4` follows from signed shifted-prime
  curvature, a finite difference, or an annular kernel spectral estimate.
  No kernel-count, density, or interval gain is promoted.

### Evidence and gate effect

- Artifact SHA-256:
  `b10715ee78b090b432b0b2f928eb20153967b162ace7c9323df9e42e290de343`.
- Theorem: `docs/cycle-41-annular-sampling-v1.md`.
- Replay:

  ```sh
  python3 proof/build_cycle_41_annular_sampling_v1.py --check
  python3 -m unittest tests/test_cycle_41_annular_sampling_v1.py
  ```

- `OBSERVED`: write/check used `0.04/0.04` seconds and `18,432` KiB peak
  RSS; four tests used `0.04` seconds and `15,872` KiB peak RSS.
- Gate change: E7--E10 is
  `SIGNED_ANNULAR_PRIME_MONOMIAL_CANCELLATION_OPEN`. The next theorem must
  exploit signed annular cancellation, beginning with the wider-margin
  `s=3` branch.

### Current-chain replay

- `PROVED`: all 34 available proof builders for Cycles 10--41 replayed with
  `--check`, including every retained correction version.
- `PROVED`: the 35 Cycle 10--41 test modules ran 165 tests with no failures.
- `OBSERVED`: `git diff --check` passed. The previously logged legacy Cycle
  4--8 failures were not rerun or altered.

## Cycle 42 — localized comb and row-resonance target (2026-08-01)

### Headline outcomes

- `PROVED`: the exact sampling comb has total mass `|C| ||phi||_1` and
  pointwise overlap `O(B)` on `Delta`-separated rows.
- `PROVED`: replacing it by `B` times the full annulus loses
  `BH/|C|=B Delta=X^(9/10)` at maximal occupancy, more than both Cycle 39
  closure margins. `ASAM_s` remains sufficient but is overstrong.
- `PROVED`: the localized form factors into prime-monomial coefficient
  pairs, the smooth cutoff `hat(|phi|)(log(n/n')/B_m)`, and the actual row
  Fourier sum `R_C(log(n/n'))`.
- `PROVED`: its diagonal exponent is
  `s+1+9/5+3/10=s+31/10`, exactly the target. `LCAM_s` is therefore the
  diagonal-sharp lead theorem.
- `CONJECTURED`: a dual row large sieve, differencing of `R_C`, or
  shifted-prime curvature controls the off-diagonal. No kernel-count,
  density, or interval gain is promoted.

### Evidence and gate effect

- Artifact SHA-256:
  `c109b790a235080fc0b6130a78e4f647fc54951217fe37c7f84e0b8b94090369`.
- Theorem: `docs/cycle-42-localized-comb-v1.md`.
- Replay:

  ```sh
  python3 proof/build_cycle_42_localized_comb_v1.py --check
  python3 -m unittest tests/test_cycle_42_localized_comb_v1.py
  ```

- `OBSERVED`: write/check used `0.04/0.05` seconds and `18,432` KiB peak
  RSS; four tests used `0.05` seconds and `15,872` KiB peak RSS.
- Gate change: E7--E10 is `LOCALIZED_COMB_ROW_RESONANCE_OPEN`.

## Cycle 43 — AP-row resonance and curved Beatty prime pairs (2026-08-01)

### Headline outcomes

- `PROVED`: for `C_R={jDelta:1<=j<=R}`, the row Fourier sum is an exact
  Dirichlet kernel and has size `>=cR` when
  `|xi-2pi k/Delta|<=1/(RDelta)`.
- `PROVED`: for a one-prime replacement `xi=log((p+r)/p)`, this resonance is
  equivalent up to constants to the curved strip
  `|r-p(exp(2pi k/Delta)-1)|<<p/(RDelta)`.
- `PROVED`: at `R=X^(21/25)` the log window is `X^(-36/25)` and the integer
  shift width is `X^(-11/25)`, hence at most one integer shift occurs for
  fixed `(p,k)`.
- `PROVED`: for fixed small `k`, the shift has scale `X^(2/5)` but the error
  in the linear center `2pi kp/Delta` is `X^(-1/5)`, larger than the strip.
  The exact exponential center is mandatory.
- `CONJECTURED`: weighted curved Beatty-prime-pair cancellation handles
  lattice-like rows, while nonlattice rows have Fourier decay on enough
  prime-monomial ratios. Neither branch is closed; no density or interval
  gain is promoted.

### Evidence and gate effect

- Artifact SHA-256:
  `96af26c677f43d4998cd25190456202d6c61d1297c9a493259048337ab7144b9`.
- Theorem: `docs/cycle-43-row-lattice-beatty-v1.md`.
- Replay:

  ```sh
  python3 proof/build_cycle_43_row_lattice_beatty_v1.py --check
  python3 -m unittest tests/test_cycle_43_row_lattice_beatty_v1.py
  ```

- `OBSERVED`: write/check used `0.04/0.04` seconds and
  `18,516/18,652` KiB peak RSS; four tests used `0.04` seconds and
  `15,872` KiB peak RSS.
- Gate change: E7--E10 is
  `CURVED_BEATTY_PRIME_PAIR_OR_NONLATTICE_ROW_OPEN`.

### Current-chain replay

- `PROVED`: all 36 available proof builders for Cycles 10--43 replayed with
  `--check`, including every retained correction version.
- `PROVED`: the 37 Cycle 10--43 test modules ran 173 tests with no failures.
- `OBSERVED`: `git diff --check` passed. The previously logged legacy Cycle
  4--8 failures were not rerun or altered.

## Cycle 44 — Beatty literature and derivative-test boundary (2026-08-01)

### Headline outcomes

- `PROVED` from checked hypotheses: Banks--Shparlinski Theorem 5.1 fixes an
  irrational finite-type Beatty slope and permits constants depending on the
  fixed slope. It does not provide uniformity for
  `alpha_k(X)=exp(2pi k/X^(3/5))-1` tending to zero.
- `PROVED` from checked hypotheses: Banks--Guo Theorem 1.1 treats fixed
  finite-type slopes and assumes a strong Hardy--Littlewood conjecture for
  every finite shift set. It is not the required unconditional prime-pair
  input.
- `PROVED`: applying the explicit Arias de Reyna `d`-th derivative theorem
  to `h p(exp(2pi x/Delta)-1)` gives three exact saving terms. At Fourier
  resolution `nu=11/25`, `d=3` saves `3/50`, `d=4` saves `12/175`, and all
  `d>=5` have first-term ceiling at most `3/80`.
- `PROVED` scoped boundary: `12/175<7/50<17/50`, so this checked
  one-variable derivative family cannot close either branch. This does not
  delimit joint `(p,k)` averaging, stronger exponent pairs, or sieve input.
- `CONJECTURED`: a two-variable curvature/sieve estimate or nonlattice row
  decay supplies the missing gain. No density or interval result is promoted.

### Evidence and gate effect

- Artifact SHA-256:
  `8271c9f5a84cc576a3ab088247697d341de67795f2bf04d7665e40e3b55177a7`.
- Theorem/source ledger: `docs/cycle-44-beatty-derivative-v1.md`.
- Replay:

  ```sh
  python3 proof/build_cycle_44_beatty_derivative_v1.py --check
  python3 -m unittest tests/test_cycle_44_beatty_derivative_v1.py
  ```

- `OBSERVED`: write/check used `0.04/0.04` seconds and
  `18,532/18,656` KiB peak RSS; four tests used `0.05` seconds and
  `15,872` KiB peak RSS.
- Gate change: E7--E10 is `JOINT_PK_CURVATURE_OR_NONLATTICE_ROW_OPEN`.

### Current-chain replay

- `PROVED`: all 37 available proof builders for Cycles 10--44 replayed with
  `--check`, including every retained correction version.
- `PROVED`: the 38 Cycle 10--44 test modules ran 177 tests with no failures.
- `OBSERVED`: `git diff --check` passed. The previously logged legacy Cycle
  4--8 failures were not rerun or altered.

## Cycle 45 — joint `(p,k)` large sieve and wrap lock (2026-08-01)

- `PROVED`: for `theta_k=h(exp(2pi k/Delta)-1) mod 1`, the lifted spacing is
  `h/Delta` and `O(h)` wrap colours suffice. The classical large sieve gives
  energy `(hX+Delta)X^(1+o(1))` and joint first-moment exponent
  `13/10+nu/2` when `h=X^nu`.
- `PROVED`: at `nu=11/25` this saves `2/25`. If the effective wrap loss is
  `h^mu`, the saving is `3/10-mu nu/2`; full `4/25` saving requires
  `mu<=7/11`, while the narrow `7/50` margin requires `mu<=8/11`.
- `OBSERVED`: this is an auxiliary joint-sum gain, not `LCAM_s` or a density
  gain. Artifact SHA-256:
  `7927eab818a98871417d94ef595310de4cb0c3ef1eb9eea5293328a1f5edeabf`.

## Cycle 46 — inverse-log wrap count (2026-08-01)

- `PROVED`: multiplicity in a `1/X` arc is equivalent, up to absolute window
  constants, to counting `j=O(h)` for which
  `||(Delta/(2pi))log(1+(j+beta)/h)||<<Delta/(hX)`.
- `PROVED`: at `h=X^(11/25)`, the horizontal length, vertical height, graph
  slope, graph second derivative, and vertical tube exponents are
  `11/25,15/25,4/25,-7/25,-21/25`. The required count is `X^(7/25)`.
- `OBSERVED` terminology correction deferred to Cycle 47: the sealed note
  called `y''` curvature. Its inverse-wrap equivalence and exact graph-
  derivative ledger remain valid, but Euclidean curvature has a different
  exponent.
- Artifact SHA-256:
  `1917dc4886fc65333e4a7933b582a80344c208a8e7ff13b34493f98d9d512d64`.

## Cycle 47 — checked near-curve input and exact `1/25` gap (2026-08-01)

- `PROVED` correction: `|y''|=X^(-7/25)` is graph second derivative;
  Euclidean curvature is `X^(-19/25)`, radius is `X^(19/25)`, Euclidean
  arclength is `X^(15/25)`, and the normal tube width is `X^(-1)`.
- `PROVED` from the checked Huxley--Sargos hypotheses: order three gives term
  exponents `8/25,4/25,-1/25,0`, hence count `X^(8/25+o(1))`. Exact
  enumeration of orders `3<=k<=20` confirms order three is best. The
  derivative/major-arc term misses the desired `7/25` by exactly `1/25`.
- `PROVED`: Howard--Trifonov Theorem 7.7 has satisfied thin-tube hypotheses
  after normal conversion and gives the weaker exponent `26/75`, equal to
  the affine-arclength exponent. Huxley's unrelated `7/11` discrepancy
  exponent is not imported by numerical coincidence.
- `CONJECTURED`: a logarithm-specific major-arc theorem saves the remaining
  `X^(1/25)`, perhaps through the differential identity
  `y'y'''=2(y'')^2`, exponentiation, or averaging over `h` before maximizing
  in the phase shift.
- Artifact SHA-256:
  `209dd38186cefbfad2f286b1fbc6400745425fb6fc8555bd8e06ac5547174a55`.
- Gate change: E7--E10 is
  `LOG_MAJOR_ARC_SAVING_1_25_OR_NONLATTICE_ROW_OPEN`.

## Cycle 48 — Huxley--Sargos reaches the `s=4` auxiliary margin (2026-08-01)

- `PROVED`: uniformly for `h=X^nu`, the order-three wrap count is
  `A(h)<=min(h,X^(1/10)h^(1/2))X^o(1)`. Retaining both large-sieve terms and
  setting `nu=11/25` gives energy exponents `58/25` and `37/25`, joint
  exponent `73/50`, and saving exactly `7/50`.
- `PROVED`: this gains `3/50` over Cycle 45 and matches the registered `s=4`
  auxiliary margin, while remaining `1/50` short of the full `4/25` saving.
- `OBSERVED`: the full localized-comb bridge and nonlattice branch remain
  open; no density promotion occurs. Artifact SHA-256:
  `2c0522bee7f7d287dbadfc3d6268316a5f87a0c67725379ea399cfa1583d580f`.

## Cycle 49 — row-Fourier exceptional sets and absolute-pairing boundary (2026-08-01)

- `PROVED`: for target-sized `Delta`-separated rows,
  `int_(-B)^B|R_C|^2=2BR+O(R log R/Delta)`. At the frozen scales the diagonal
  and off-diagonal exponents are `57/50` and `6/25`.
- `PROVED`: the set where `|R_C|>R X^(-7/50)` has measure at most
  `X^(-13/50+o(1))`; the analogous `4/25` threshold has measure exponent
  `-11/50`.
- `PROVED` scoped boundary: absolute prime-monomial coefficient pairing still
  exceeds `LCAM_4` by `39/10`. The required theorem must retain signed or
  `L2` coupling at coefficient-energy scale. Artifact SHA-256:
  `ea00b6ff9791a4d389e9e2431e3bdec7cc185538e07ffd86f9873c7e90899f5a`.

## Cycle 50 — stable-range support-kernel factorization (2026-08-01)

- `PROVED`: for `m>s`, unique factorization identifies the harmonic prime
  and unordered ordinary-prime multiset. The distinct support has size
  `M binomial(M+s-1,s)` and correlation
  `K(mh)H_s(h)`, with `H_s` complete homogeneous symmetric.
- `PROVED`: exact Newton formulas are
  `H_3=(P1^3+3P1P2+2P3)/6` and
  `H_4=(P1^4+6P1^2P2+3P2^2+8P1P3+6P4)/24`.
- `PROVED`: phase-aligned Halász--Montgomery reduces large `F_(m,s)` values
  to row sums of this factored difference kernel. Small `m` was still open
  at this cycle. Artifact SHA-256:
  `ed68a75b1e6d191e23528fb23b1e7e41e7919e1e16bbc09d178a2ed71c72aaab`.

## Cycle 51 — all-harmonic support partitions (2026-08-01)

- `PROVED`: a prime-exponent partition `lambda` occurs in the support iff
  `lambda` partitions `s+m` and `max(lambda)>=m`. Set-partition Möbius
  inversion converts every resulting monomial symmetric function into an
  explicit polynomial in `K(jh)`, `j<=s+m`.
- `PROVED`: exact expansions for `(3,2),(3,3),(4,2),(4,3),(4,4)` agree with
  direct rational-alphabet evaluations, and the general formula reconciles
  symbolically with Cycle 50 when `m>s`. The small-harmonic exception is
  closed algebraically. Artifact SHA-256:
  `3608f1e6048d13dfbd8a8e619127518c4355bcc5dd80e578498014e8e0a20304`.

## Cycle 52 — support-kernel self-duality (2026-08-01)

- `PROVED`: uniformly for fixed `s` and all `m>=2`,
  `G_(m,s)(h)=K(mh)K(h)^s/s!+O_s(M^s)`. Every collision/lower-support
  stratum loses a full prime-coordinate power.
- `PROVED`: if the correlation deficit is `eta<1`, and the kernel deficits
  at `h,mh` are `alpha,beta`, then `s alpha+beta<=eta+o(1)`. At
  `(s,eta)=(4,7/50)`, this forces deficits at most `7/200` and `7/50`.
- `CONJECTURED`: a popular-difference trigger plus additive-structure
  extraction routes these near-full recurrences into Cycle 48. Artifact
  SHA-256:
  `bec97f88a9d9602d28cb5ee528dab803c854022c35f8c3fd9187c302bc793cc6`.

## Cycle 53 — one-shot trigger boundary (2026-08-01)

- `PROVED`: after selecting one of `X^(3/10)` harmonics, `AMPR_s` failure
  guarantees only `r+2v>=s+14/5`. One-shot support-space
  Halász--Montgomery forces an off-diagonal only above `2s+2`.
- `PROVED`: the trigger gaps are `11/5` for `s=3` and `16/5` for `s=4`.
  This is scoped to the one-shot inequality; it does not obstruct
  coordinatewise Bessel or a centred higher trace.
- Gate change: E7--E10 is
  `MULTILINEAR_TRIGGER_THEN_TWO_SCALE_INVERSE_OPEN`. Artifact SHA-256:
  `fefe66bf2b3d65835d0b187afc4fc7ea3e53f9953d701f7dcd29943ed921484e`.

## Cycle 54 — coordinatewise-Bessel design boundary (2026-08-01)

- `PROVED` conditional design theorem: if each exposed ordinary prime
  coordinate removes one full support power, then after assigning the
  Cycle-48 `7/50` saving to `q^m`, `s-1` contractions still miss the strict
  `AMPR_s` off-diagonal trigger by `3/50`, while all `s` contractions cross
  it with margin `47/50`, for `s=3,4`.
- `CONJECTURED`: a source-valid sequential Bessel/duality inequality realizes
  every ordinary-coordinate contraction and retains the powered-coordinate
  saving. The ledger proves the requirement, not this analytic contract.
- Creative pivot: E11 targets the full all-coordinate contraction; E12
  subtracts Cycle-51 collision partitions in a centered cube trace; E13
  treats the logarithmic differential identity as an averaged transport law.
  E12/E13 have the exact smaller target `3/50` if they replace the final
  ordinary contraction.
- Gate change: E7--E13 is
  `ALL_COORDINATE_CONTRACTION_OR_3_50_HYBRID_OPEN`. Artifact SHA-256:
  `566e0c651c7fc95cf91719094702fe35a7156821fedac688cb96a6cf1f6362e0`.

## Cycle 55 — scalar centered traces are exactly sharp (2026-08-01)

- `PROVED`: for every `R rho<=1`, unit rows can have common projection
  squared `rho` and Gram matrix exactly `I_R`. Hence subtracting the scalar
  diagonal leaves zero and every centered even Schatten trace vanishes.
- `PROVED`: Cycle 54's penultimate stage has
  `R rho=X^(-3/50+o(1))`, inside this sharp abstract range. Raising the trace
  order alone cannot replace the final ordinary contraction.
- `CONJECTURED`: center actual prime coordinates before tensorization; the
  abstract result does not cover such a prime-partition cumulant. Artifact
  SHA-256:
  `50a66a5d1aea0e9173e4c23bc8bf262e0c937b162a86942e957065635c6c53ab`.

## Cycle 56 — actual-prime edge cumulant (2026-08-01)

- `PROVED`: coordinatewise centering gives the PSD kernel
  `E_(m,s)(h,g)=C_m(h,g)C(h,g)^s`, where
  `C(h,g)=k(h-g)-k(h)conj(k(g))`.
- `PROVED`: the kernel annihilates a diagonal edge, has diagonal
  `(1-|k(mh)|^2)(1-|k(h)|^2)^s`, and its signed expansions have respectively
  8 and 10 terms with coefficient `l1` norms 16 and 32 for `s=3,4`.
- `CONJECTURED`: a spectral restriction bound or failure inverse theorem
  converts this retained prime-phase information into a strict hybrid gain.
  Artifact SHA-256:
  `3e38876a10cf4c5696b40eb69a77825569ec225566b6799f029f337cb4879d23`.

## Cycle 57 — Hilbert-valued support collapse (2026-08-01)

- `PROVED`: the coordinate-centred tensor is a Hilbert-valued Dirichlet
  polynomial on the actual labels `q^m p_1...p_s`. Cycle-39 fiber
  multiplicity and fiberwise Cauchy--Schwarz bound collapse cost by
  `D_s=(1+floor(s/2))s!`, uniformly for every `m>=2`.
- `PROVED`: `D_3=12`, `D_4=72`, and pre-collapse raw coefficient energy is
  exactly `(M-1)^(s+1)`. Thus integer-frequency collisions cost no exponent.
- Gate change: E12 is a Hilbert-valued sparse edge-cumulant restriction or
  approximate-multiplicativity problem. Artifact SHA-256:
  `c2af9b4aa7c467c6e9d795eb0c7665b9769aa9e4c6187b3c0e9a7d5d94174e8d`.

## Cycle 58 — strict hybrid-margin correction (2026-08-01)

- `PROVED` correction: a hybrid saving exactly `3/50` reduces the
  penultimate trigger to equality; it does not meet the strict off-diagonal
  condition. Closure requires `>3/50`, or exact `3/50` plus a separately
  proved logarithmic or constant strict margin.
- `PROVED` correction: replacing the complete powered-coordinate input
  similarly requires saving `>1/5`; exact `1/5=7/50+3/50` ties.
- The proved Cycle-54 gaps and Cycle-55--57 algebra are unaffected. Their
  conjectural analytic target wording is superseded by this correction.
- Gate change: E7--E13 is
  `HILBERT_EDGE_CUMULANT_GT_3_50_OR_FULL_CONTRACTION_OPEN`. Artifact SHA-256:
  `0bde0caa82cda62b8a61af9902e6eecc00d89442d41779826bb52a59e6a3dcef`.

## Cycle 59 — trigger surplus versus recurrence strength (2026-08-01)

- `PROVED` conditional ledger: if an adjusted trigger is crossed by surplus
  `mu`, generic phase-aligned counting forces correlations at deficit `eta`
  only for `eta>r-mu`. It then gives at least `X^(r+mu-o(1))` ordered popular
  edges and average-degree exponent `mu`.
- `PROVED`: at `r=21/25`, Cycle-48 deficit `eta=7/50` requires
  `mu>7/10`; uniformly for `r<=1`, it requires `mu>43/50`. Total
  penultimate hybrid savings are respectively `>19/25` and `>23/25`.
- `PROVED`: the full final-coordinate surplus `47/50` reaches the strong
  recurrence uniformly. A hybrid barely above `3/50` does not do so by
  generic counting alone.
- Strategic fork: E12 must prove its complete Hilbert quadratic-form
  restriction directly, or supply a prime-specific graph amplifier before
  Cycle 52. Artifact SHA-256:
  `f01cc7fa5fdf066f3c461b6db6227cfe7c4050ab6230fe58bd9ade8a45ad96fa`.

## Cycle 60 — coordinate-ANOVA identity (2026-08-01)

- `PROVED`: for phase-aligned tuple polynomial `S`, the energy density
  `|S|^2` decomposes orthogonally under coordinate averages `A_j` and
  differences `D_j=I-A_j`. Centered coordinates contribute
  `p^(-ih)-k(h)`; averaged coordinates contribute `k(h)`.
- `PROVED`: there are 16 subset components for `s=3` and 32 for `s=4`, in 8
  and 10 symmetry types. The fully centered component has exactly the
  Cycle-56/57 Hilbert edge-cumulant quadratic norm.
- Analytic routing: large tuple-energy variance selects a nonconstant
  component at constant cost; small variance is a flat-energy inverse branch,
  not a discard. Artifact SHA-256:
  `69f032ddd9d6d22fdca9c55a2078f274baca900a98b281046d694ba77c1c2d8a`.

## Cycle 61 — coefficient-projection annihilator form (2026-08-01)

- `PROVED`: on ordered tuples, Hilbert synthesis factors as `A=C B`, where
  `B` lifts a distinct-label vector to fibers and
  `C=P_q tensor P_p1 tensor...tensor P_ps` centers every coordinate.
- `PROVED`: `A*A<=D_s I`, with `D_3=12,D_4=72`. The exact loss
  `||B beta||^2-||A beta||^2` is the sum of proper coordinate-ANOVA energies;
  near saturation forces every powered and ordinary coordinate marginal
  small for the same edge weights.
- `PROVED` source-scope check: pinned Guth--Maynard Theorem 1.1 is scalar and
  assumes one fixed `l-infinity` coefficient vector; their introductory
  remark emphasizes that even replacing this by an `l2` hypothesis is not
  available in their proof. It does not automatically supply a
  dimension-free Hilbert large-value theorem with row-dependent directions.
- Gate: capture a fixed-power marginal for the actual Fourier vector, or turn
  simultaneous small marginals into a prime-log annihilator/recurrence
  theorem. Artifact SHA-256:
  `d44a5144f06d51336c0be81e89bf24d4007939d1cacdaab498251adc708164ff`.

## Cycle 62 — single-edge projection boundary (2026-08-01)

- `PROVED`: for `beta_n=n^(-ih)`, full coordinate centering retains exactly
  `(1-|k(mh)|^2)(1-|k(h)|^2)^s`; when both normalized kernels are
  polynomially small, the retained fraction is `1-o(1)`.
- `PROVED` scoped boundary: no universal pointwise operator power saving is
  possible. The valid phase-aligned vector has the additional identity
  `beta_n=|sum_t z_t n^(-it)|^2>=0`, coupling all `R^2` differences. The
  single-edge stress vector does not refute a theorem using this structure
  and target-violating row cardinality.
- Gate change: E7--E13 is
  `NONNEGATIVE_AUTOCORRELATION_ANOVA_OR_RECURRENCE_OPEN`. Artifact SHA-256:
  `059fb1b05d9f4c8e6df046d46b900916a1e27ffb2f348cb0d40d8727b467993f`.

## Cycle 63 — logarithmic transport census (2026-08-01)

- `PROVED`: the inverse-log wrap condition reduces to triples satisfying
  `|j+beta-h alpha_ell|<=C/X`, with
  `alpha_ell=exp(2pi ell/Delta)-1`. The transport surface has Hessian
  determinant exponent `-6/5`.
- `PROVED`: the summed pointwise Hilbert--Schmidt exponent is `19/25`.
  Powered-coordinate saving `>1/5` follows if the weighted beta-free pair
  census has exponent strictly below `17/25`; equivalently, more than
  `3/25` of averaging saving is needed beyond pointwise control.
- Gate: `LOG_TRANSPORT_PAIR_CENSUS_LT_17_25_OPEN`. Artifact SHA-256:
  `d5dc9dd9ff3f5636c98980d35f6f973d72f9e62c04644fe510b4f0de06d4f153`.

## Cycle 64 — primitive Farey-packet transport (2026-08-01)

- `PROVED`: Farey separation `X^(-22/25)` exceeds the approximation windows
  `X^(-1)`, and curve spacing `X^(-3/5)` does likewise. Each curve index and
  reduced rational therefore belongs to at most one primitive packet.
- `PROVED`: the maximal weighted packet cost is `H^2/(2q)`, reducing the
  strict pair target to harmonic packet mass below `X^(-1/5)`. Random-volume
  mass has exponent `-2/5`, leaving heuristic margin `1/5`.
- Gate: `LOG_FAREY_PACKET_MASS_OR_LOW_DENOMINATOR_RECURRENCE_OPEN`. Artifact
  SHA-256:
  `60a78bc81f2916e594221a1258a35024b96e67ecf5d2af6bc9a53731d1cdc76f`.

## Cycle 65 — depth-refined packet ledger (2026-08-01)

- `PROVED`: for packet error `epsilon=|q alpha_ell-a|`, retain depth
  `K=min(H/q,C/(X epsilon))`. Its exact weight is
  `KH-qK(K+1)/2`. At `q=X^(theta+o(1)),K=X^(kappa+o(1))`, the sufficient
  packet-count target is strictly below `X^(6/25-kappa)`.
- `PROVED`: one packet reaches the pair target only for
  `kappa>=6/25`; admissibility then forces `theta<=1/5`. This matches the
  independently derived critical synchronization average-degree exponent.
- Correction: low denominator alone does not force many differences; the
  Cycle-64 conjectural wording is superseded by joint denominator and depth.
- Gate: `LOG_DEPTH_PACKET_DISCREPANCY_OR_X6_25_AP_RECURRENCE_OPEN`. Artifact
  SHA-256:
  `f86cecfa996a7583990a24a6060167a700fa8cca54c199ec92cdf2f3c8637a2d`.

## Cycle 66 — primitive Möbius--Poisson contract (2026-08-01)

- `PROVED`: a nonnegative band-limited majorant, exact coprimality inversion,
  and Poisson summation preserve primitive numerator-denominator labels. The
  diagonal exponent is `theta-kappa-2/5`, with margin
  `16/25-theta>=1/5` to the packet target.
- `PROVED`: after the `(KX)^(-1)` prefactor, the strict raw off-diagonal
  target is `X^(31/25)` on every admissible `(theta,kappa)` scale. Composite
  frequencies are at most `X^(36/25+o(1))`.
- Gate: `PRIMITIVE_POISSON_X31_25_OR_DEEP_PACKET_RECURRENCE_OPEN`. Artifact
  SHA-256:
  `5d096b9f64a2dc82657d798d7fcd911812d8a6b8a7a326368330b532e16ef5bd`.

## Cycle 67 — seeded packet recurrence (2026-08-01)

- `PROVED`: if one genuine strip hit accompanies a packet of depth `K`, the
  identity along `h0+kq,j0+ka` produces at least `1+floor(K/2)` realized
  hits at enlarged strip constant `C0+C1`, with no exponent loss.
- `PROVED` scope correction: without the beta-dependent seed, packet depth
  supplies allowable differences only. The structured branch becomes an
  E7/E9/E10 recurrence handoff only after a seed is supplied or extracted.
- Gate: `SEEDED_X6_25_AP_RECURRENCE_OPEN`. Artifact SHA-256:
  `85bd999fca3e1d675c0b3096a6cd287866d9e1aef227239b42b94b39ff585d02`.

## Cycle 68 — folded-frequency large-sieve boundary (2026-08-01)

- `PROVED`: folding by `m=rq'` gives
  `A_m=sum_(q'|m)sum_(b:bq'~Q)mu(b)b^-1 fhat(m/(q'bKX))`, with
  `|A_m|<<tau(|m|)`, support `|m|<<KXQ`, and square-norm exponent at most
  `1+theta+kappa`.
- `PROVED` scoped boundary: Cauchy plus the generic separated-point large
  sieve gives raw exponent `13/10+theta+kappa`, missing `31/25` by
  `3/50+theta+kappa`. This does not cover Möbius- or phase-sensitive bounds.
- Gate unchanged: retain the signed divisor sum, exponential transport phase,
  or seeded major arcs. Artifact SHA-256:
  `4c179b10dfb15ec20a9189001ca2c2b81dd3aac09ab56c0b1da9d224ae85d4b8`.

## Cycle 69 — stationary transport dual (2026-08-01)

- `PROVED`: Poisson summation in `ell` gives stationary phase
  `Psi(m,k)=u-m-u log(u/m)`, `u=kDelta/(2pi)`. It is homogeneous of degree
  one, and its full `(m,k)` Hessian determinant vanishes identically.
- `PROVED` scoped boundary: complete frequency folding loses Cycle 63's
  nonzero transport Hessian, so a generic two-dimensional Hessian estimate
  cannot repair Cycle 68. An unfurled variable or projective ratio curvature
  is required.
- `PROVED` scale identity: `m<=X^(36/25)` gives stationary
  `k<=X^(21/25)`, exactly the critical skeleton exponent. No identification
  of stationary aliases with zero rows is claimed.
- Gate: `UNFURLED_TRANSPORT_OR_PROJECTIVE_X21_25_DUAL_OPEN`. Artifact
  SHA-256:
  `4f868a07381d89ccfafe72f80553a63b9457447a848408d22cb4493d4726a04c`.

## Cycle 70 — unfurled stationary curvature (2026-08-01)

- `PROVED`: for fixed stationary `k`, restoring `m=rq'` gives
  `det Hess_(r,q')Psi(rq',k)=(u/(rq'))^2-1=exp(4pi ell/Delta)-1`.
  Thus the curvature lost in Cycle 69 is restored off the zero endpoint.
- `PROVED`: an `ell=X^(lambda)` block is automatically subcritical by
  packet uniqueness when `lambda<6/25-kappa`. On the surviving range the
  determinant exponent is at least `-9/25-kappa`.
- Gate: prove a two-variable estimate on the unbalanced
  `r<<bKX,q'~Q/b` box which absorbs this endpoint loss. Artifact SHA-256:
  `2218be784434352a97037a865a40acd43969562f3430df22944b23adbbde6acc`.

## Cycle 71 — primitive-fraction wedge (2026-08-01)

- `PROVED`: a denominator block contains at most `X^(2theta+o(1))`
  available reduced fractions. Packet injectivity therefore closes every
  cell with `2theta+kappa<6/25`, both for packet count and weighted pair
  census. Equality ties.
- `OBSERVED` source boundary: Huang, arXiv:1403.7388, definition (1.1) and
  Theorem 1, use two rational coordinates with a common denominator; they do
  not directly cover the mixed `ell/Delta,a/q` grid here.
- Artifact SHA-256:
  `f6711801f4f6b521a801933d6cfe596f2953821a56daa6baab206cb27557ef35`.

## Cycle 72 — primitive positive-numerator cutoff (2026-08-01)

- `PROVED`: for `q>1`, primitivity excludes `a=0`; packet accuracy gives
  `ell>>Delta/q`. Hence the Cycle-70 Hessian is at least
  `X^(-theta-o(1))`, improving its nonsharp loss `X^(-9/25-kappa)`.
- `PROVED`: the exceptional reduced zero numerator occurs only at `q=1`, a
  constant-size denominator branch.
- Artifact SHA-256:
  `547bb719c76df324c2dfda63f12c6a2a3c83ace3bbfd4d8eb5b941895296a7ef`.

## Cycle 73 — numerator-resolved packet atlas (2026-08-01)

- `PROVED`: on `a=X^(alpha+o(1))`, packet count is at most
  `X^(theta+alpha+o(1))`. Thus every cell with
  `theta+alpha+kappa<6/25` closes strictly in both packet and weighted pair
  formulations; equality ties.
- `PROVED`: `alpha=theta+lambda-3/5`, and the factored Hessian loss is exactly
  `theta-alpha`. The residual analytic atlas is
  `theta+alpha+kappa>=6/25`, `0<=alpha<=theta`,
  `theta+kappa<=11/25`.
- Gate: `NUMERATOR_RESOLVED_RESIDUAL_CURVATURE_OPEN`. Artifact SHA-256:
  `fdad9eae285d61f8782b8e6e18809d559fee87ffcf2fddeca53a002b807b6685`.

### Current-chain replay

- `PROVED`: all 66 available proof builders for Cycles 10--73 replayed with
  `--check`, including every retained correction version.
- `PROVED`: the 67 Cycle 10--73 test modules ran 310 tests with no failures.
- `OBSERVED`: `git diff --check` passed. An accidental broad replay reached
  the preserved Cycle-4 mutable-PLAN failure before the corrected current-
  chain filter was applied; this is the already logged legacy lifecycle
  mismatch, not evidence against Cycles 10--73.

## Cycle 74 — fixed-denominator Huxley--Sargos wedge (2026-08-01)

- `PROVED`: applying the checked order-three Huxley--Sargos near-integer
  estimate to `y_q(a)=(Delta/(2pi))log(1+a/q)` and then taking the minimum
  with the trivial numerator count gives
  `w(theta,alpha)=min(alpha,max(0,alpha+1/10-theta/2))` for each fixed `q`.
  Summing denominators gives packet-count exponent `theta+w`.
- `PROVED`: this closes a nonempty region beyond Cycle 73. The registered
  witness `(theta,kappa,alpha)=(11/50,0,1/50)` ties the raw budget at
  `6/25` but has Huxley--Sargos exponent `23/100`, a strict margin `1/100`.
  For `theta>1/5`, the lower piece closes when
  `theta+kappa<6/25`; the upper piece closes when
  `alpha+theta/2+kappa<7/50`. The endpoint tie is not promoted.
- Strategic implication: pointwise numerator curvature has a proof-grade but
  limited role. The live residual requires cancellation across `q`; the
  high-level plan now makes the E14 Monge--Ampere, E15 shifted-correlation,
  and E16 seed-extraction engines the principal forge.
- Gate: `HS_NUMERATOR_WEDGE_CLOSED_Q_AVERAGE_RESIDUAL_OPEN`.
- Artifact SHA-256:
  `57869f9a6506076198b54bb877417eecaf96682ff8ada606ab8d39ab4cc9e1ae`.
- Replay:
  `python3 proof/build_cycle_74_hs_numerator_wedge_v1.py --check` and
  `python3 -m unittest tests/test_cycle_74_hs_numerator_wedge_v1.py`.

### Current-chain replay through Cycle 74

- `PROVED`: all 67 retained proof builders for Cycles 10--74 replayed with
  `--check`, including correction versions.
- `PROVED`: all 68 retained Cycle 10--74 test modules ran 315 tests with no
  failures.
- `OBSERVED`: `git diff --check` passed.

## Cycle 75 — affine-normalized denominator geometry (2026-08-01)

- `PROVED`: in `(a,q)` coordinates,
  `det Hess Y=-C^2/[q^2(a+q)^2]`; in shifted coordinates `n=q+a`, the
  Hessian is `C diag(-1/n^2,1/q^2)`. After scaling `a=Ax,q=Qy`, both
  Hessian singular values are between `(CA/Q)/832` and `13CA/Q`.
- `PROVED`: the intrinsic curvature scale is therefore
  `Delta A/Q=X^(lambda+o(1))`, not the unnormalized loss
  `X^(alpha-theta)`. The tube relative to this scale is
  `X^(-1-alpha-kappa+o(1))`, independent of `theta`.
- `PROVED`: `e(kY)=(n/q)^(ikDelta)` and
  `gcd(n,q)=gcd(a,q)`. Primitive pairs have no nontrivial repeated exact
  ray, so only approximate rational webs remain as E16 inverse objects.
- `PROVED`: combining Cycle 70 and Cycle 74 gives banked packet exponent
  `B=min(lambda,theta+w)` and exact live residual `B+kappa>=6/25`. The
  maximal additional saving deficit is `7/15`, uniquely at
  `(theta,alpha,kappa)=(1/3,1/3,8/75)`, where both banked bounds equal `3/5`.
- Gate: `AFFINE_CURVATURE_CONTRACT_EXACT_E14_E15_ANALYTIC_GAIN_OPEN`.
- Artifact SHA-256:
  `3dbe955aaea7dffece0b06e1e30fd9d46a7023d1d3ce438991a1dbd57c4576dd`.
- Replay:
  `python3 proof/build_cycle_75_denominator_geometry_v1.py --check` and
  `python3 -m unittest tests/test_cycle_75_denominator_geometry_v1.py`.

## Cycle 76 — Huxley--Sargos across denominators (2026-08-01)

- `PROVED`: for fixed numerator, the checked order-three theorem gives
  `u=min(theta,1/10+alpha/6+theta/3)` denominators; after summing numerators,
  the count exponent is `alpha+u`. The derivative term uniformly dominates
  the theorem's tube and ratio terms on the registered atlas.
- `PROVED`: the estimate is nontrivial when
  `theta>3/20`, `alpha<4theta-3/5`, and closes strictly when
  `7alpha/6+theta/3+kappa<7/50`.
- `PROVED`: `(theta,kappa,alpha)=(6/25,0,0)` is live after Cycle 75 and ties
  the old target at `6/25`, but the denominator estimate gives `9/50`, a
  strict margin `3/50`. Equality at `(6/25,0,9/175)` is not promoted.
- `OBSERVED`: the preregistered rational-grid search located the witness; it
  is quarantined from the exact symbolic proof.
- Gate: `DENOMINATOR_HS_WEDGE_CLOSED_TWOD_OR_SHIFTED_RESIDUAL_OPEN`.
- Artifact SHA-256:
  `4f4c2c3a1829dd829f991147a41c22d8a75dc499c8c43e2d7ae0bed45b1a4219`.
- Replay:
  `python3 proof/build_cycle_76_hs_denominator_wedge_v1.py --check` and
  `python3 -m unittest tests/test_cycle_76_hs_denominator_wedge_v1.py`.

### Current-chain replay through Cycle 76

- `PROVED`: all 69 retained proof builders for Cycles 10--76 replayed with
  `--check`, including correction versions.
- `PROVED`: all 70 retained Cycle 10--76 test modules ran 326 tests with no
  failures.
- `OBSERVED`: `git diff --check` passed.

## Cycle 77 — critical anchored saddle (2026-08-01)

- `PROVED`: at `(theta,alpha,kappa)=(1/3,1/3,8/75)`, choosing one packet
  anchor converts every other packet, up to absolute tube constants, into
  `|n-c0*q*exp(2pi*d/Delta)|<<X^(-83/75)`. After normalization the mesh is
  `(Delta^-1,Q^-1,Q^-1)`, the tube is `X^(-36/25)`, and the saddle Hessian
  determinant is uniformly nonzero. The exact count target is `X^(2/15)`.
- `PROVED`: an anchor-free pair reduction gives product-supported
  `|U-exp(2pi*d/Delta)V|<<X^(-58/75)`. Its formal volume exponent is
  `37/75` against pair target `4/15`, quantifying an anchor loss `17/75`.
- `OBSERVED` source boundary: checked planar/hypersurface rational-point
  theorems use a common denominator. Even granting integer `Delta`, the
  isotropic embedding has height `X^(14/15)` and leaves a `4/5` gap to the
  anchored target. This does not rule out a sublattice-aware adaptation.
- Gate: `CRITICAL_ANCHORED_SADDLE_ACSI_OR_PHASE_WEB_OPEN`.
- Artifact SHA-256:
  `c68cc89eb163d81d85374a61986c62c4004f1b5c195a5088a7063fb9ed670dbd`.
- Replay:
  `python3 proof/build_cycle_77_critical_saddle_v1.py --check` and
  `python3 -m unittest tests/test_cycle_77_critical_saddle_v1.py`.

### Current-chain replay through Cycle 77

- `PROVED`: all 70 retained proof builders for Cycles 10--77 replayed with
  `--check`, including correction versions.
- `PROVED`: all 71 retained Cycle 10--77 test modules ran 331 tests with no
  failures.
- `OBSERVED`: `git diff --check` passed.

## Cycle 78 — exact Freiman phase web (2026-08-01)

- `PROVED`: if four critical packet indices satisfy
  `ell_1+ell_2=ell_3+ell_4`, their reduced labels satisfy the exact identity
  `r_1r_2=r_3r_4`. Clearing four denominators leaves error
  `Q^3*eta=X^(-8/75+o(1))`, so the relation is integer-forced.
- `PROVED`: prime valuations therefore define an exact Freiman homomorphism
  on every relation present in the hit set. A complete arithmetic progression
  maps to `r_j=r_0g^j`; rational height bounds its length by `O(log Q)`.
- `PROVED` scope boundary: the target cardinality `X^(2/15)` lies below the
  generic `Delta^(1/2)=X^(3/10)` Sidon threshold. Additive-energy
  pigeonholing need not produce any relation, so sparse relation-poor sets
  remain the ACSI minor-arc branch.
- Gate: `EXACT_FREIMAN_WEB_OR_SPARSE_ACSI_OPEN`.
- Artifact SHA-256:
  `bbff3b63005b7ef468ee23289e9e3f4b7d0f30cfe79374dcb3df0622aec23d5a`.
- Replay:
  `python3 proof/build_cycle_78_freiman_phase_web_v1.py --check` and
  `python3 -m unittest tests/test_cycle_78_freiman_phase_web_v1.py`.

### Current-chain replay through Cycle 78

- `PROVED`: all 71 retained proof builders for Cycles 10--78 replayed with
  `--check`, including correction versions.
- `PROVED`: all 72 retained Cycle 10--78 test modules ran 335 tests with no
  failures.
- `OBSERVED`: `git diff --check` passed.

## Cycle 79 — double B-process and logarithmic saddle (2026-08-01)

- `PROVED`: a band-limited tube majorant reduces the Cycle-77 critical count
  to the exact raw Fourier requirement
  `sum_(k<=X^(83/75)) |S_k| < X^(31/25+o(1))`, where
  `S_k=sum_(d~Delta,q~Q)e(k c0 q exp(2pi d/Delta))`.
- `PROVED`: double Poisson has stationary map
  `r=k c0 exp(2pi d/Delta)`, `h=2pi q r/Delta`, inverse
  `d=(Delta/(2pi))log(r/(kc0))`, `q=hDelta/(2pi r)`, and leading
  amplitude `Delta/(2pi r)`. The dual phase is
  `(hDelta/(2pi))log(kc0/r)` and has nonzero saddle determinant in `(k,r)`.
- `PROVED`: `r~k`, `h~kQ/Delta`, and the maximum `h` exponent is `21/25`,
  exactly the frozen prime-skeleton scale. Frequencies
  `k<Delta/Q=X^(4/15)` contribute at most `X^(6/5+o(1))`, a strict
  `1/25` margin to the raw target.
- Claim boundary: no uniform stationary remainder or high-frequency dual
  cancellation is yet proved.
- Gate: `DOUBLE_B_HIGH_FREQUENCY_LOG_SADDLE_OPEN`.
- Artifact SHA-256:
  `855bd15a08f78433e09edf2b3e66ef67abea109d69d55a763132ef3a8c084eb2`.
- Replay:
  `python3 proof/build_cycle_79_double_b_process_v1.py --check` and
  `python3 -m unittest tests/test_cycle_79_double_b_process_v1.py`.

## Cycle 80 — primal phase occupancy (2026-08-01)

- `PROVED`: uniformly for `k=X^(xi+o(1))` through the Fourier support, every
  circular interval of length `O(1/Q)` contains at most
  `A_k<=X^(22/45+o(1))` phases
  `k c0 exp(2pi d/Delta) mod 1`. The checked order-three theorem's tube term
  dominates its derivative and ratio terms on the entire range.
- `PROVED`: a clustered circle large sieve gives
  `|S_k|<=Q(A_k Delta)^(1/2)<=X^(79/90+o(1))`.
- `PROVED`: the dyadic Fourier block exponent is `xi+79/90`, so every block
  `4/15<=xi<163/450` is strictly below `31/25`. This adds width `43/450`
  beyond Cycle 79. The endpoint `xi=163/450` ties and is not promoted.
- Strategic implication: the unresolved problem is now confined to
  `163/450<=xi<=83/75`; primal multiscale occupancy and the dual logarithmic
  saddle can be developed as independent, competing engines.
- Gate: `PRIMAL_OCCUPANCY_BAND_CLOSED_DUAL_HIGH_FREQUENCY_OPEN`.
- Artifact SHA-256:
  `751e8edde6469dabe637a17d8bc2cad491a9ed2caa49f099ce60020ef0a069d7`.
- Replay:
  `python3 proof/build_cycle_80_phase_occupancy_v1.py --check` and
  `python3 -m unittest tests/test_cycle_80_phase_occupancy_v1.py`.

### Current-chain replay through Cycle 80

- `PROVED`: all 73 retained proof builders for Cycles 10--80 replayed with
  `--check`, including correction versions.
- `PROVED`: all 74 retained Cycle 10--80 test modules ran 344 tests with no
  failures.
- `OBSERVED`: `git diff --check` passed.
- `OBSERVED`: an initial broad glob again reached the preserved Cycle-4
  mutable-PLAN hash mismatch. The replay was immediately restricted to the
  authoritative Cycle 10--80 chain; this is the logged legacy lifecycle
  mismatch, not evidence against the current results.

## Cycle 81 — exact q-transform (2026-08-01)

- `PROVED`: because the Cycle-79 phase is exactly linear in `q`, Fourier
  inversion gives an exact one-variable kernel.  Its leading term is
  `D/(beta r) W(x_r)V(hD/(beta Qr))
  e((hD/beta)log(kc0/r))`; the frozen sign gives `V(a)`, not `V(-a)`.
- `PROVED`: Taylor expansion only in the Schwartz-localized variable gives
  central error `O_(W,V)(D/(Qr^2))`.  Summing `r~k` and `h~kQ/D` costs
  `X^o(1)` per `k`; smooth nonstationary charts are power-negligible.
- `PROVED`: accumulation through `k<=X^(83/75+o(1))` has exponent `83/75`,
  a strict `2/15` margin to the raw `31/25` target.  The stationary-remainder
  problem is removed; cancellation in the exact logarithmic sum remains.
- Gate: `EXACT_Q_TRANSFORM_SEALED_LOG_RESONANCE_PROJECTOR_OPEN`.
- Artifact SHA-256:
  `0753d455a2e9428b28f1b9dac59b04fd57008db562370202a300a38a818631a4`.
- Replay:
  `python3 proof/build_cycle_81_exact_q_transform_v1.py --check` and
  `python3 -m unittest tests/test_cycle_81_exact_q_transform_v1.py`.

## Cycle 82 — smooth phase projector (2026-08-01)

- `PROVED`: smooth Poisson summation gives
  `|Theta_Q(x)|<<Q(1+Q||x||)^(-A)`.  Summing occupancy annuli directly,
  without Cauchy--Schwarz, yields `|S_k|<<Q A_k`.
- `PROVED`: Cycle 80's `A_k<=X^(22/45+o(1))` therefore gives per-frequency
  exponent `37/45`.  All blocks `xi<94/225` close strictly, adding
  `163/450<=xi<94/225` of width `1/18`; the endpoint ties.
- Gate: `SMOOTH_PROJECTOR_BAND_CLOSED_FIXED_CENTER_RESONANCE_OPEN`.
- Artifact SHA-256:
  `5faff9b1b6a94da3df33e0b68423d0b9a0663a62c480d5713e2cea8a21ec4b11`.
- Replay:
  `python3 proof/build_cycle_82_smooth_phase_projector_v1.py --check` and
  `python3 -m unittest tests/test_cycle_82_smooth_phase_projector_v1.py`.

## Cycle 83 — Fejer--VdC fixed-center resonance (2026-08-01)

- `PROVED`: Fejer majorization and the classical second-derivative estimate
  give
  `R_k<<D/Q+sqrt(kQ)+D/sqrt(kQ)`.  On the active range the middle term
  dominates, so `R_k<=X^(xi/2+1/6+o(1))`.
- `PROVED`: dyadic projector annuli use bandwidth `Q/L`; fixed Schwartz
  decay absorbs every resulting power of `L`, preserving the central
  exponent.
- `PROVED`: the Fourier block exponent is `3xi/2+1/2`, closing
  `94/225<=xi<37/75`, a new width `17/225`.  The endpoint ties.  The largest
  second-derivative parameter at that endpoint has exponent `-28/75`, so the
  checked small-derivative regime is uniform.
- `OBSERVED` source context: the frozen Guth--Maynard primary source
  `arXiv:2405.20552v2` explicitly invokes the classical first/second
  derivative bounds in its Poisson functional-equation argument; Cycle 83
  derives the normalization from the registered phase derivatives.
- Gate: `FEJER_VDC_BAND_CLOSED_HIGH_FREQUENCY_EXPONENT_PAIR_OPEN`.
- Artifact SHA-256:
  `e946bcc64e4601a0822e81dfc6c0e5ee8296f46187af743716b8bd2cfde8fafe`.
- Replay:
  `python3 proof/build_cycle_83_fejer_vdc_resonance_v1.py --check` and
  `python3 -m unittest tests/test_cycle_83_fejer_vdc_resonance_v1.py`.

## Cycle 84 — averaged resonance incidence (2026-08-01)

- `PROVED`: joint Fejer majorization in a dyadic `k` block reduces the
  radius-`L/Q` incidence to
  `I_L<<KDL/Q+(L/Q)sum_(j<=Q/L)|B_j|`.
- `PROVED`: summing smoothly in `k` first, the monotone function
  `j c0 exp(2pi d/D)` crosses `O(j)` integers and has derivative `asymp j/D`.
  One discretization point per crossing plus total interval length gives
  `|B_j|<<D+jK`, including exact rational-anchor multiples.
- `PROVED`: hence `I_L<<KDL/Q+D+KQ/L`.  After the outer projector and
  Schwartz annuli, the Fourier-`L1` exponent is
  `max(xi+3/5,14/15,xi+2/3)`.  This closes
  `37/75<=xi<43/75`, a strict new width `2/25`; the endpoint ties.
- `PROVED` structural lock: the one-point-per-crossing term stops unsigned
  incidence at `43/75`, exactly `1/15` before its volume-only cutoff
  `16/25`.  Above `16/25`, even volume-optimal unsigned incidence cannot
  meet the raw target, so signed cancellation is necessary.
- Gate: `AVERAGED_RESONANCE_BAND_CLOSED_CROSSING_INVERSE_OPEN`.
- Artifact SHA-256:
  `b7f67aa9613891c0de006711fc07475085aab0114fd44808a701cf57fe79ca9b`.
- Replay:
  `python3 proof/build_cycle_84_averaged_resonance_v1.py --check` and
  `python3 -m unittest tests/test_cycle_84_averaged_resonance_v1.py`.

### Current-chain replay through Cycle 84

- `PROVED`: all 77 retained proof builders for Cycles 10--84 replayed with
  `--check`, including correction versions.
- `PROVED`: all 78 retained Cycle 10--84 test modules ran 366 tests with no
  failures.
- `OBSERVED`: `git diff --check` passed.

## Cycle 85 — logarithmic crossing occupancy (2026-08-01)

- `PROVED`: an occupied `j`-crossing implies the inverse-log near-integer
  condition
  `||(D/(2pi))log(r/(jc0))||<<D/(jK)` with `r~j`.
- `PROVED`: the checked order-three theorem has derivative, tube, ratio, and
  constant exponents
  `1/10+nu/2`, `1/5+2nu/3-xi/3`, `(2nu-xi)/3`, and `0`.  The derivative term
  dominates throughout `43/75<=xi<=16/25`, `0<=nu<=1/3`; its minimum margin
  over the tube term is `8/225`.
- `PROVED`: after the trivial minimum, the occupied-crossing exponent is
  `min(nu,1/10+nu/2)`.  Dyadic `j` summation and the frozen annular decay give
  Fourier-`L1` exponent `xi+3/5`, closing
  `43/75<=xi<16/25`, width `1/15`; the endpoint ties.
- `PROVED` structural boundary: unsigned smooth incidence has now reached its
  formal volume limit.  On `16/25<=xi<=83/75`, signed cancellation or a
  structured inverse output is necessary.
- Gate: `UNSIGNED_INCIDENCE_VOLUME_LIMIT_SIGNED_RESONANCE_OPEN`.
- Artifact SHA-256:
  `c35f1fb2425f9e54497225907e66b69d0176fdc4f4030c8c721bf82d66d3c2e9`.
- Replay:
  `python3 proof/build_cycle_85_log_crossing_occupancy_v1.py --check` and
  `python3 -m unittest tests/test_cycle_85_log_crossing_occupancy_v1.py`.

### Current-chain replay through Cycle 85

- `PROVED`: all 78 retained proof builders for Cycles 10--85 replayed with
  `--check`, including correction versions.
- `PROVED`: all 79 retained Cycle 10--85 test modules ran 371 tests with no
  failures.
- `OBSERVED`: `git diff --check` passed.

## Cycle 86 — signed zero mode and regime split (2026-08-01)

- `PROVED`: the smooth projector satisfies
  `int_(R/Z)Theta_Q(x)dx=V(0)=0` exactly because its frozen dyadic weight is
  supported inside `(0,infinity)`.  The continuous unsigned volume mode is
  absent from the signed architecture.
- `PROVED`: one `S_k` has atom exponent `14/15`; square-root size is `7/15`,
  a `2/15` saving over unsigned size `3/5`.  A diagonal-strength second
  moment would give block exponent `xi+7/15`, closing strictly through
  `xi<58/75`; the endpoint ties.
- `PROVED` target split: on `16/25<=xi<58/75`, the exact target is
  `sum_(k~K)|S_k|^2<=X^(xi+14/15+o(1))`.  On
  `58/75<=xi<=83/75`, pointwise square-root cancellation is insufficient;
  every dyadic large-value level must satisfy
  `s+log_X M_xi(s)<31/25` or output inverse structure.  The ceiling average
  allowance is `2/15`.
- Claim boundary: no signed moment, large-value estimate, or new band is
  proved in this cycle.
- Gate: `SIGNED_DIAGONAL_MOMENT_OPEN` and
  `SIGNED_LARGE_VALUE_SPARSITY_OPEN`.
- Artifact SHA-256:
  `4d6f78f433b052c6d3497d46d67b015d6963fe67f862e0d6c52124c6d26a3dd4`.
- Replay:
  `python3 proof/build_cycle_86_signed_regime_split_v1.py --check` and
  `python3 -m unittest tests/test_cycle_86_signed_regime_split_v1.py`.

### Current-chain replay through Cycle 86

- `PROVED`: all 79 retained proof builders for Cycles 10--86 replayed with
  `--check`, including correction versions.
- `PROVED`: all 80 retained Cycle 10--86 test modules ran 376 tests with no
  failures.
- `OBSERVED`: `git diff --check` passed.

## Cycle 87 — Mellin-alias atlas for the signed second moment (2026-08-01)

- `PROVED`: the primal second moment has exact pair kernel
  `K sum_m hat U(K(m-(z_u-z_v)))`; its atom diagonal has exponent
  `xi+14/15`, exactly the Cycle-86 target, and the continuous pair-kernel
  zero mode is absent because `U(0)=0`.
- `PROVED`: in the exact dual coordinates, crossing heights `h,h'` and
  Poisson summing in `k` gives phase `t log k-mk`,
  `t=D(h-h')/(2pi)`, stationary inverse `k=t/m`, Hessian `-m^2/t`, and
  amplitude `sqrt(|t|)/|m|`.
- `PROVED`: all off-diagonal interactions split into equal height, the
  nonstationary range `0<|h-h'|<<K/D`, and stationary aliases
  `K/D<<|h-h'|<<KQ/D` with `1<<|m|<<Q`.
- Claim boundary: no moment estimate, band closure, large-value theorem,
  density gain, or interval gain was proved.
- Gate: `MELLIN_ALIAS_TRICHOTOMY_BOUND_OR_WEB_OPEN`.
- Artifact SHA-256:
  `68b88ccd4ce3e5371906e3b0da3c254056b79bad9504880ebbff04b9cebce8ca`.
- Builder SHA-256:
  `40c5ee246dea06bed2cc5acd44c764df50ddcd483323d4d5b6ac64a1d689d4ff`.
- Replay:
  `python3 proof/build_cycle_87_mellin_alias_atlas_v1.py --check` and
  `python3 -m unittest tests/test_cycle_87_mellin_alias_atlas_v1.py`.

## Cycle 88 — finite signed-moment profiler (2026-08-01)

- `OBSERVED`: all 15 preregistered `(anchor,xi)` slopes of `M2/(KN)` were
  classified `OBSERVED_FLAT` across the six frozen scales. The slopes range
  from `-0.05421016655749921` to `0.038564744733388855`.
- `OBSERVED`: across all 90 rows, `M2/(KN)` ranges from
  `0.8967634990993699` to `1.1461450611790376`, normalized `L1` from
  `0.8241735234093808` to `0.9420261250726057`, and normalized maximum from
  `2.1901198120269596` to `4.3090601471255505`.
- `OBSERVED`: this supports the lower diagonal-moment conjecture but is
  adverse evidence for unstructured upper-band cancellation: square-root
  average size persists through `xi=83/75`. This finite computation proves
  neither asymptotics nor a moment bound.
- Frozen output SHA-256:
  `c5ef4b34d9d7483d04cf87231786acf1bca15ba6d52771fc8297b811b7211c1b`.
  Script SHA-256:
  `19e686dea38c8f5777cec7d664730c31b4fdb7809b4ddf1b997ac3fedfd1d54e`.
- Runtime: CPython `3.12.3`, NumPy `1.26.4`; write replay wall time `7.12s`,
  peak RSS `69712 KiB`; check replay wall time `7.12s`, peak RSS `69732 KiB`.
- Replay:
  `python3 discovery/run_cycle_88_signed_moment_profiler_v1.py --check`.

## Cycle 89 — moment-concentration inverse gate (2026-08-01)

- `PROVED`: for `L1=sum a_k`, `M2=sum a_k^2`, and `M4=sum a_k^4`, Hölder
  gives `M2<=L1^(2/3)M4^(1/3)`, hence `M4>=M2^3/L1^2`.
- `PROVED`: conditional on diagonal-size
  `M2>=X^(xi+14/15-o(1))` and raw target
  `L1<=X^(31/25-delta+o(1))`, the fourth moment must have exponent at least
  `3xi+8/25+2delta`. Relative to the diagonal/random exponent
  `xi+28/15`, the forced excess is `2xi-116/75+2delta`; it is zero at
  `xi=58/75,delta=0` and `2/3` at the Fourier ceiling.
- `PROVED` strategic reduction: under the stated second-moment hypothesis,
  upper-band success requires fourth-moment concentration. Concentration is
  necessary, not sufficient; no fourth-moment estimate is proved.
- Containment event: the first exact unit test rejected two auxiliary
  transcription constants (`37/150` and `37/75`). Direct rational
  recalculation corrected them to `19/75` and `34/75`; the preregistered
  governing formula and endpoint values were unchanged. The failed test was
  preserved here rather than omitted.
- Gate: `MOMENT_CONCENTRATION_OR_SATURATION_INVERSE_OPEN`.
- Artifact SHA-256:
  `93e22952845f8e5b21ad841d79604a09eccc26ca9ca083bf1f65ac0a60de5dc8`.
  Builder SHA-256:
  `5e075c015c6e9d16797614086aec640a2323d86e0fe1a34a6fd4436ebcf815e0`.
- Builder runtime: CPython `3.12.3`, wall time `0.04s`, peak RSS
  `18516 KiB`.
- Replay:
  `python3 proof/build_cycle_89_moment_concentration_gate_v1.py --check` and
  `python3 -m unittest tests/test_cycle_89_moment_concentration_gate_v1.py`.

### Current-chain replay through Cycle 89

- `PROVED`: all 81 retained proof builders for Cycles 10--89 replayed with
  `--check`, including correction versions and excluding discovery-only
  Cycle 88.
- `PROVED`: all 82 retained Cycle 10--89 test modules ran 386 tests with no
  failures.
- `OBSERVED`: the deterministic Cycle-88 discovery output replay matched.
- `OBSERVED`: combined replay wall time was `12.52s` with peak RSS
  `69764 KiB`; `git diff --check` passed.
