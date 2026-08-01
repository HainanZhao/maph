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
