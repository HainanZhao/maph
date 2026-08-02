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

## Cycle 90 — equal-height B-process and saddle contract (2026-08-01)

- `PROVED`: the equal-height branch is
  `sum_k U(k/K) sum_h |sum_r A_(k,h,r)|^2`; its same-`r` diagonal has the
  exact target exponent `xi+14/15`.
- `PROVED`: the smooth B-process sends the length-`K` logarithmic `r` sum to
  a length-`Q` sum with stationary point `r=t/n`, phase
  `t(1-log(t/n))`, and amplitude `sqrt(t)/n`. The remainder has exponent
  `xi+3/5`, a strict `1/3` margin below the diagonal target.
- `PROVED`: the dual off-diagonal localizes to
  `|n'-n exp(2pi a/D)|<<1/K`, `a~D`, `n,n'~Q`. Its volume exponent is
  `14/15-xi`, below the target `1/3` by `xi-3/5>=1/25`; the surface Hessian
  determinant is `-(beta^2/D^2)exp(2beta a/D)`.
- Claim boundary: no collision bound, equal-height closure, full moment,
  density gain, or interval gain was proved.
- Gate: `EQUAL_HEIGHT_BPROCESS_SADDLE_DISCREPANCY_OR_WEB_OPEN`.
- Artifact SHA-256:
  `a24a63110e26fff4672c8b8e2cca27569a00885dec7b8c934f8ca3971967c3de`.
  Builder SHA-256:
  `5adf4552231150e17de894e13470895a1c5e8480e4150b5cd2e995c81d123758`.
- Builder runtime: wall time `0.04s`, peak RSS `18560 KiB`.
- Replay:
  `python3 proof/build_cycle_90_equal_height_bprocess_v1.py --check` and
  `python3 -m unittest tests/test_cycle_90_equal_height_bprocess_v1.py`.

## Cycle 91 — finite saddle-collision profiler and correction (2026-08-01)

- Containment event: v1 used `max(C/scale,1e-300)` for normalized slope
  regressions, contrary to the preregistered `max(C,1)/scale`. This produced
  meaningless slopes `106.124...` and `35.127...`. The v1 script and output
  are preserved; correction v2 changes only those regression inputs.
- `OBSERVED` corrected result: `C/Q` is `OBSERVED_FLAT` at `xi=16/25` and
  `xi=7/10`, with slopes `0.0147526` and `-0.116128`, and
  `OBSERVED_DECAYING` at `xi=3/4`, slope `-0.484186`.
- `OBSERVED`: across all frozen rows, `C/Q<=0.116`, `C/(DQ/K)<=0.482`,
  maximum per `a` is two, and maximum per `n` is two. These finite data
  support the volume-scale collision conjecture but prove no asymptotic.
- Corrected output SHA-256:
  `340c14afa18183920c7437493b448bd09caa3e9a72a59c3dee34f63e69b805e8`.
  Corrected script SHA-256:
  `74746b9c8cd799e5ba948267a927955976322514894ea025c9d5d7429bf31bd0`.
  Correction document SHA-256:
  `b28934ce9bf63943df288a5b6c29f8ddc5cbe33a7fb1a27a44dc4f0a1360a72c`.
- Corrected write/check runtimes: `1.18s`/`1.41s`; peak RSS
  `263020`/`262712 KiB`.
- Replay:
  `python3 discovery/run_cycle_91_saddle_collision_profiler_correction_v2.py --check`.

## Cycle 92 — collision-ray inverse lemma (2026-08-01)

- `PROVED`: Farey spacing and the margin `K/Q>=X^(23/75+o(1))` force all
  collisions at one `a` onto one primitive rational ray.
- `PROVED`: monotone exponential spacing and
  `KQ/D>=X^(28/75+o(1))` make primitive labels injective across distinct
  `a` values. No transcendence lower bound is used.
- `PROVED`: a class of multiplicity `M` has primitive denominator
  `q<<Q/M`; `C_tot` collisions yield a dyadic class with
  `>>C_tot/(M log Q)` distinct `a` values and injective labels. Thus excess
  over `QX^epsilon` is an explicit rational-ray web, not an anonymous error.
- Claim boundary: the web is not yet a transport seed and no analytic
  collision bound, moment, density gain, or interval gain is proved.
- Artifact SHA-256:
  `e4d20db8df77672cd8622abd891b0bc97cbb0914c538e95682c19cf98e48f43e`.
  Builder SHA-256:
  `af4d4debd0ea13755e64193cdd3992f6825c429f4191e538b65d75cb748906c9`.
- Builder runtime: wall time `0.04s`, peak RSS `18432 KiB`.
- Replay:
  `python3 proof/build_cycle_92_collision_ray_inverse_v1.py --check` and
  `python3 -m unittest tests/test_cycle_92_collision_ray_inverse_v1.py`.

## Cycle 93 — strict sub-alias nonstationary closure (2026-08-01)

- `PROVED`: for nonzero integer `Delta h` in a fixed buffered range
  `|Delta h|<=c_*K/D`, the `m=0` rescaled derivative is `>>D`, while every
  `m!=0` derivative is `>>(1+|m|)K`.
- `PROVED`: repeated smooth integration by parts gives kernel
  `O_A(KD^-A)` for arbitrary `A`; after every polynomial support sum the
  complete strict branch is `O_B(X^-B)` for arbitrary fixed `B`.
- Claim boundary: the transition `|Delta h|~K/D`, stationary integer
  aliases, equal-height analytic bound, full moment, density gain, and
  interval gain remain open.
- Artifact SHA-256:
  `5dd299f0a0c67774f65b30cffd1e2ee48aace17b07eb6c3c6e1700b1e306cd3d`.
  Builder SHA-256:
  `ba9968ad53b3839d7d2f41c3a474ff970dcaceb76b2bd35b3b0e42ed5f1a03b6`.
- Builder runtime: wall time `0.04s`, peak RSS `18432 KiB`.
- Replay:
  `python3 proof/build_cycle_93_nonstationary_mellin_branch_v1.py --check`
  and `python3 -m unittest tests/test_cycle_93_nonstationary_mellin_branch_v1.py`.

## Cycle 94 — triple-B entropy and central anchor difference (2026-08-01)

- `PROVED`: the stationary values from the `k,r,r'` B-processes combine to
  `F=Delta log(c0 Delta/m)-h log(h/n)+(h-Delta)log((h-Delta)/n')`; all linear
  and `log(D/(2pi))` terms cancel exactly.
- `PROVED`: central stationarity gives `(h-Delta)/h=n'/n` and
  `m=c0(n-n')`; for `c0=p0/q0`, this is the integer relation
  `q0 m=p0(n-n')`.
- `PROVED` structural boundary: `F` is degree-one homogeneous in
  `(h,Delta)` and its Hessian determinant is identically zero. Nonzero
  Poisson modes are projective entropy aliases, not covered by the central
  relation.
- Containment event: two initial SymPy checks rejected equivalent logarithm
  forms because simplification preserved a difference of logs. The check was
  changed to compare forced log expansions; the registered phase,
  derivatives, and determinant were unchanged.
- Artifact SHA-256:
  `9b6fc5021af3622821729f72966fcb15a4c9b74d0ef668d14ccc6f32349266a5`.
  Builder SHA-256:
  `8813d0667bbd6a630dd54d312be82342d55892f24a330033cf952c5f4366dc6a`.
- Builder runtime: wall time `0.45s`, peak RSS `56180 KiB`.
- Gate: `CENTRAL_ANCHOR_DIFFERENCE_WEB_BANKED_PROJECTIVE_ENTROPY_ALIASES_OPEN`.
- Replay:
  `python3 proof/build_cycle_94_triple_b_entropy_v1.py --check` and
  `python3 -m unittest tests/test_cycle_94_triple_b_entropy_v1.py`.

### Current-chain replay through Cycle 94

- `PROVED`: all 85 retained proof builders for Cycles 10--94 replayed with
  `--check`, including correction versions and excluding discovery-only
  Cycles 88 and 91.
- `PROVED`: all 86 retained Cycle 10--94 test modules ran 406 tests with no
  failures.
- `OBSERVED`: the deterministic Cycle-88 and corrected Cycle-91 discovery
  outputs replayed exactly.
- `OBSERVED`: combined replay wall time was `14.79s`, peak RSS
  `262584 KiB`, and `git diff --check` passed.

## Cycle 95 — exact projective entropy modes (2026-08-01)

- `PROVED`: after Poisson summation in the two projective height variables,
  exact stationarity is equivalent to
  `p0 n-p0 n'g^u-q0m g^(u+v)=0`, with `g=exp(2pi/D)` and integer modes
  `(u,v)`.
- `PROVED`: Gelfond--Schneider applies with algebraic
  `alpha=-1`, algebraic irrational `beta=-2i/D`, and the branch
  `Log(-1)=i*pi`; hence the corresponding value `g=exp(2pi/D)` is
  transcendental. The source and checked hypotheses are recorded in
  `docs/cycle-95-gelfond-schneider-source-v1.md`.
- `PROVED`: separating all coincidences among the exponents `0,u,u+v`
  excludes every exact noncentral mode. The only solution is `u=v=0`, when
  the equation is the central anchor difference `p0(n-n')=q0m`.
- Claim boundary: transcendence is qualitative. No uniform lower bound for a
  near-zero Laurent trinomial, complete alias estimate, moment theorem,
  density gain, or interval gain was proved.
- Containment event: an auxiliary nonzero-polynomial test initially asserted
  `15-12-6=3`; the value is `-3`. The frozen convention was corrected before
  sealing. This did not affect the stationary equation or classification.
- Artifact SHA-256:
  `73c1a220bd5bbacd2c813a7cbb36611c88bcc4e9e0e84bc8de97c95d6364128f`.
  Builder SHA-256:
  `13f878a5282607352bef273951c4c4a714837fa32a17886fffa20e656dbca049`.
- Builder runtime: wall time `0.05s`, peak RSS `19452 KiB`.
- Gate:
  `EXACT_ALIASES_CENTRAL_NEAR_PROJECTIVE_MODES_QUANTITATIVE_OPEN`.
- Replay:
  `python3 proof/build_cycle_95_projective_entropy_modes_v1.py --check` and
  `python3 -m unittest tests/test_cycle_95_projective_entropy_modes_v1.py`.

## Cycle 96 — projective integer-jet separation (2026-08-01)

- `PROVED`: for
  `f(x)=A-B exp(ax)-C exp(bx)`, with positive integer coefficients and a
  noncentral integer mode, the constant and linear jets
  `J0=A-B-C`, `J1=Ba+Cb` are integers and
  `f''(t)=-Ba^2exp(at)-Cb^2exp(bt)<0`.
- `PROVED`: if `J0!=0` and `x exp(xM)S1<=1/2`, then `|f(x)|>=1/2`.
  If `J0=0,J1>0`, then `|f(x)|>=x`. If `J0=0,J1<0` and
  `x exp(xM)S2<=1/2`, then `|f(x)|>=x/2`. If `J0=J1=0`, then
  `|f(x)|>=exp(-xM)x^2S2/2`.
- `PROVED`: under
  `(A,B,C,a,b,x)=(p0n,p0n',q0m,u,u+v,2pi/D)`, these inequalities give
  quantitative separation in the registered small-mode sectors. The only
  uncovered jet geometries are large displacement and negative-linear
  derivative turnover.
- Claim boundary: the registered sectors are not proved to exhaust the
  projective Poisson support. No complete alias estimate, moment theorem,
  density gain, or interval gain was proved.
- Containment event: the first seal attempt failed before artifact creation
  because the dynamic loader did not place the conventions module in
  `sys.modules` before evaluating its dataclass. The loader alone was fixed;
  the theorem, frozen inputs, and tests were unchanged.
- Artifact SHA-256:
  `4ab624c4d2edd837ca4c70ce7ae6067982e5c846798a855f89931340d3485683`.
  Builder SHA-256:
  `cbf28e70147a19293c5b64d70fa9e424d0da296b6b999f0e421b0724689fab7e`.
- Successful builder runtime: wall time `0.06s`, peak RSS `19456 KiB`.
- Gate: `INTEGER_JET_SMALL_MODES_BANKED_TURNOVER_SECTORS_OPEN`.
- Replay:
  `python3 proof/build_cycle_96_projective_integer_jet_v1.py --check` and
  `python3 -m unittest tests/test_cycle_96_projective_integer_jet_v1.py`.

### Current-chain replay through Cycle 96

- `PROVED`: all 87 retained proof builders for Cycles 10--96 replayed with
  `--check`, including correction versions and excluding discovery-only
  Cycles 88 and 91.
- `PROVED`: all 88 retained Cycle 10--96 test modules ran 418 tests with no
  failures.
- `OBSERVED`: the deterministic Cycle-88 and corrected Cycle-91 discovery
  outputs replayed exactly.
- Containment event: the first aggregate replay command passed a complete
  newline-separated filename list as one shell argument and therefore ran no
  builder. A process-orchestrated replay then passed each path separately.
- `OBSERVED`: successful combined replay wall time was `15.25s`, peak RSS
  `262724 KiB`; `git diff --check` passed and `HEAD..origin/main` was empty.

## Cycle 97 — algebraic-root inverse atlas (2026-08-02)

- `PROVED`: clearing negative powers from
  `f(t)=A-Bexp(at)-Cexp(bt)` produces a nonzero integer polynomial `P` with
  degree at most `2M` and coefficient `l1` norm at most `A+B+C`; every real
  residual root has a positive algebraic exponential coordinate.
- `PROVED`: strict concavity gives at most two real roots and one critical
  point. With `delta=|f(x)|`, `eta=|f'(x)|`, and the registered curvature
  envelope, `eta>=max(2delta,2sqrt(Ldelta))` forces an algebraic root within
  `2delta/eta`; otherwise the row has simultaneous small value and derivative.
- `PROVED`: under stronger localization `eta<=ell/2`, the modes have opposite
  signs and the row lies within `2eta/ell` of the explicit critical point
  `exp((a-b)t*)=-Cb/(Ba)`.
- Claim boundary: no effective entropy linear-form separation, support
  exhaustion, alias moment, density gain, or interval gain was proved.
- Containment event: the first near-double test chose data with `t*=0`,
  outside the preregistered `x>0` domain. It was replaced by a positive
  critical-point anchor; theorem constants and formulas were unchanged.
- Artifact SHA-256:
  `5af4394e8a8f48b70cff4f1b32e9a213640df499f273f701bc0ffe5ffd0d2644`.
  Builder SHA-256:
  `5d3256397ab6f6fc72b8b3b79c45ab082d2235f4c15eab7a51a138004e4158b1`.
- Builder runtime: wall time `0.06s`, peak RSS `19840 KiB`.
- Replay:
  `python3 proof/build_cycle_97_projective_algebraic_root_v1.py --check` and
  `python3 -m unittest tests/test_cycle_97_projective_algebraic_root_v1.py`.

## Cycle 98 — direct pointwise logarithmic-form ledger (2026-08-02)

- `PROVED`: the actual stationary equations and fixed dyadic supports give
  `M=max(|u|,|u+v|)<<D=X^(3/5+o(1))`; Cycle 97 gives
  `[Q(i,alpha):Q]<=4M`.
- `PROVED` source insertion: Gaudron, arXiv:1004.3652, Theorem 1.1, applies
  to `Dlog(alpha)+2i log(-1)=Dlog(alpha)-2pi` with `n=2,t=1`; the field,
  independence, logarithm, and coefficient-height hypotheses were checked.
- `PROVED` scoped no-go: the direct worst-case cost is
  `3/5+3/5+6/5=12/5`, so the theorem guarantees only
  `exp(-X^(12/5+o(1)))`, asymptotically too weak to certify a fixed power.
  This is not a no-go for sparse, averaged, low-degree, or critical methods.
- Claim boundary: no complete alias moment, density gain, or interval gain
  was proved.
- Artifact SHA-256:
  `9ac5bba45e11798b592b94250ee52d3b89d632125f116754188580ff8f55c160`.
  Builder SHA-256:
  `d9d6adc0c9a2e2a3156754b4e3cd19e27fc3bae42161e324d3610a59877ffb9a`.
- Builder runtime: wall time `0.04s`, peak RSS `18644 KiB`.
- Replay:
  `python3 proof/build_cycle_98_gaudron_direct_ledger_v1.py --check` and
  `python3 -m unittest tests/test_cycle_98_gaudron_direct_ledger_v1.py`.

## Cycle 99 — critical rational-ray compiler (2026-08-02)

- `PROVED`: every opposite-sign critical row has reduced rational label
  `r=C|b|/(B|a|)=exp(wt*)`, `w=a-b`, of numerator and denominator at most
  `H=QM`; `1<=|w|<=2M`.
- `PROVED`: if `rho=|t*-x|` and
  `L>=max(|wx|,|wt*|)`, then
  `|r-exp(wx)|<=exp(L)|w|rho`. Farey spacing makes the label unique when
  this is below `1/(2H^2)`; exponential spacing makes labels injective across
  distinct `w` below `exp(-L)(exp(x)-1)/2`.
- `PROVED`: substituting Cycle 97's `rho<=2eta/ell` gives an explicit strong-
  localization threshold. All surviving multiplicity lies in the oriented
  factorization fiber `C|b|R=B|a|N`, `a-b=w`.
- Claim boundary: no bound for that fiber, weak near-double rows, full alias
  moment, density gain, or interval gain was proved.
- Artifact SHA-256:
  `69e453fea12a404c17078169ac605c17b05109b99c74e0dd82f830e1ecdf2ee6`.
  Builder SHA-256:
  `d7357a33c2a4416665dd86d9b9c9c3745d166941a2a261671d681bea32b209c5`.
- Builder runtime: wall time `0.05s`, peak RSS `19900 KiB`.
- Gate:
  `STRONG_CRITICAL_RAYS_BANKED_SIMPLE_ROOT_AVERAGE_WEAK_ROWS_AND_FIBER_OPEN`.
- Replay:
  `python3 proof/build_cycle_99_critical_rational_ray_v1.py --check` and
  `python3 -m unittest tests/test_cycle_99_critical_rational_ray_v1.py`.

### Current-chain replay through Cycle 99

- `PROVED`: all 90 retained proof builders for Cycles 10--99 replayed with
  `--check`, including correction versions and excluding discovery-only
  Cycles 88 and 91.
- `PROVED`: all 91 retained Cycle 10--99 test modules ran 433 tests with no
  failures.
- `OBSERVED`: the deterministic Cycle-88 and corrected Cycle-91 discovery
  outputs replayed exactly.
- `OBSERVED`: combined replay wall time was `15.19s`, peak RSS
  `262592 KiB`; `git diff --check` passed and `HEAD..origin/main` was empty.

## Cycle 100 — exact critical-fiber atlas (2026-08-02)

- `PROVED`: for fixed signed `w`, reduced label `N/R`, and
  `s=|a|`, `t=|b|`, `s+t=|w|`, every positive solution of
  `CtR=BsN`, `B,C<=Q`, is uniquely
  `B=lambda*tR/g`, `C=lambda*sN/g`, where `g=gcd(sN,tR)` and
  `lambda<=Qg/max(sN,tR)`.
- `PROVED`: the exact fiber count is the sum of those lambda ranges, and
  `g=g0*gcd(s/g0,R)*gcd(t/g0,N)`, `g0=gcd(s,t)`. Thus every nongeneric row
  has an explicit side-labelled cross-valuation prime-power web.
- `PROVED`: when both cross gcds are one,
  `F_generic<=2Q tau(|w|)/min(N,R)`.
- Sign-provenance correction: Cycle 66's Möbius sign belongs to its primitive
  packet representation. No proved bridge carries it to the Cycle-87
  stationary variables `(B,C,s,t)`, whose available signs are oscillatory
  phases/B-process amplitudes. The plan was corrected before Cycle 100 was
  sealed; no Möbius cancellation is claimed here.
- Claim boundary: no exceptional-web, weak-row, alias-moment, density, or
  interval bound was proved.
- Artifact SHA-256:
  `2b5de8802840ce6411ef9b1eef887d4619ecb04d1c71fe520491db4cb01b2da1`.
  Builder SHA-256:
  `ae6855b521cf4bf5ff182d63281e7fa2457b3d65374821549d93517971e5f1e7`.
- Builder runtime: wall time `0.04s`, peak RSS `19328 KiB`.
- Replay:
  `python3 proof/build_cycle_100_critical_fiber_atlas_v1.py --check` and
  `python3 -m unittest tests/test_cycle_100_critical_fiber_atlas_v1.py`.

## Cycle 101 — aggregate generic critical packing (2026-08-02)

- `PROVED`: for `J` distinct reduced labels in a fixed compact ratio
  interval, putting `z_j=min(N_j,R_j)` gives
  `#{j:z_j<=Y}<<Y^2` and `sum_j 1/z_j<<sqrt(J)`.
- `PROVED`: Cycle-99 injectivity gives `J<=4M`; inserting the Cycle-100
  labelwise bound yields total generic strong-critical multiplicity
  `<=8K_L Q T_M sqrt(M)=Q M^(1/2+o(1))`.
- `PROVED`: at `Q=X^(1/3+o(1))`, `M<=X^(3/5+o(1))`, the aggregate exponent
  is `19/30`, a square-root saving in the mode range over the naive `QM`.
- Claim boundary: cross-valuations, weak near-double rows, simple-root rows,
  the alias moment, density gain, and interval gain remain open.
- Containment event: the first seal attempt failed before artifact creation
  because the dynamic conventions loader could not resolve its imported
  Cycle-100 module. Adding the project root to the sealer import path fixed
  only packaging; formulas, hashes of theorem inputs, and tests were
  unchanged.
- Artifact SHA-256:
  `3c4e6a34b839df06028233e127a01001e094dc16665c833f43ec370642d3c4d1`.
  Builder SHA-256:
  `db82d0019df52f89b388e198cb70e12c7fa441a6db8b19f2a7493aebe018a243`.
- Successful builder runtime: wall time `0.05s`, peak RSS `19908 KiB`.
- Gate:
  `GENERIC_STRONG_CRITICAL_X19_30_BANKED_CROSS_VALUATION_WEAK_SIMPLE_OPEN`.
- Replay:
  `python3 proof/build_cycle_101_generic_critical_packing_v1.py --check` and
  `python3 -m unittest tests/test_cycle_101_generic_critical_packing_v1.py`.

### Current-chain replay through Cycle 101

- `PROVED`: all 92 retained proof builders for Cycles 10--101 replayed with
  `--check`, including correction versions and excluding discovery-only
  Cycles 88 and 91.
- `PROVED`: all 93 retained Cycle 10--101 test modules ran 442 tests with no
  failures.
- `OBSERVED`: the deterministic Cycle-88 and corrected Cycle-91 discovery
  outputs replayed exactly.
- `OBSERVED`: combined replay wall time was `15.68s`, peak RSS
  `262852 KiB`; `git diff --check` passed and `HEAD..origin/main` was empty.

## Cycle 102 — exact cross-valuation inverse atlas (2026-08-02)

- `PROVED`: with `g0=(s,t)`, `s1=s/g0`, `t1=t/g0`,
  `x=(s1,R)`, and `y=(t1,N)`, writing
  `s1=x s2`, `R=x R2`, `t1=y t2`, `N=y N2` removes the exceptional gcd
  exactly. The primitive coefficient bases are
  `B0=t2 R2`, `C0=s2 N2`, and
  `|w|=g0(x s2+y t2)`.
- `PROVED`: the core obeys
  `(s2,R2)=(t2,N2)=(x,y)=(yN2,xR2)=1`. Every full prime power in `x`
  divides `s/g0` and `R` while dividing neither `t/g0` nor `N`; every full
  prime power in `y` has the reversed signature. This is the exact oriented
  valuation datum retained for E16.
- `PROVED`: for exceptional atoms of total nonnegative mass `E` and total
  mass at each distinct `w` at most `A`, some side/full-prime-power colour
  supports at least `E/(2P(2M)A)` distinct `w`. Retaining both cross-gcd
  dyadic indices gives `E/(2P(2M)L_M^2 A)`,
  `L_M=1+floor(log2(2M))`.
- Strategic correction: the former informal phrase “excess forces many
  distinct labels” omitted the colour-alphabet and per-`w` thresholds. Cycle
  102 makes them explicit. It proves no exceptional-mass estimate; a strong
  per-`w` cap or actual phase cancellation is the next analytic lock.
- `PROVED` replay coverage: exhaustive comparison with the Cycle-100 formula
  passed for all reduced `N/R` with `N,R<=18`, every `2<=|w|<=18`, and every
  split. Opaque stationary/anchor payloads are retained unchanged by the
  concentration representation, but no common-anchor conclusion is claimed.
- Claim boundary: no phase cancellation, common anchor, weak near-double or
  simple-root estimate, complete alias moment, density gain, or interval gain
  was proved.
- Artifact SHA-256:
  `1f4d27e5e1c269b04d3779634d6deaaa5ae21eb3f9352de781bc33b396c002ff`.
  Builder SHA-256:
  `b59de593dc611df2048883aae82e025572b099b393d2e1a384558e97c446666a`.
- Builder runtime: wall time `0.05s`, peak RSS `19968 KiB`.
- Gate:
  `CROSS_CORE_AND_COLOUR_THRESHOLD_BANKED_PER_W_PHASE_WEAK_SIMPLE_OPEN`.
- Replay:
  `python3 proof/build_cycle_102_cross_valuation_inverse_v1.py --check` and
  `python3 -m unittest tests/test_cycle_102_cross_valuation_inverse_v1.py`.

## Cycle 103 — critical-scale algebraic alias inverse (2026-08-02)

- `PROVED`: for one fixed Cycle-102 core, the critical label equation
  `r=C0 t/(B0 s)` gives `t*=log(r)/(s+t)`, independently of the coefficient
  scale. With
  `K=B0 r^(s/W)+C0 r^(-t/W)`, scaling `(B,C)=lambda(B0,C0)` yields the exact
  critical value `f(t*)=A-lambda K`.
- `PROVED`: `K` lies in `Q(r^(1/W))`, is positive algebraic, and has degree at
  most `W`. No useful height or irrationality measure is claimed.
- `PROVED`: Cycle 97's localized near-double estimate transfers at the actual
  critical point as
  `|A-lambda K|<=epsilon`,
  `epsilon=delta+2eta^2/ell+2Leta^2/ell^2`. Thus Cycle 100's raw `lambda`
  multiplicity consists only of near-integer hits of a fixed algebraic orbit.
- `PROVED`: if `J>=2` distinct scales in `[1,Lambda]` are hits, an adjacent
  gap gives
  `1<=q<=floor((Lambda-1)/(J-1))` and `||qK||<=2epsilon`. If
  `q_epsilon` is the least such denominator, then
  `J<=1+floor((Lambda-1)/q_epsilon)`; if it does not exist, `J<=1`.
- Implication: the strong exceptional scale multiplicity is now an exact
  dichotomy—one hit or a short algebraic alias. A short alias is E16
  structure, not cancellation; aggregation across core splits remains open.
- Containment event: the first test run exposed two incorrect fixture values.
  The Cycle-97 tolerance in that fixture is `1/20`, not `2/25`, and one
  alleged hit had residual `2epsilon` rather than at most `epsilon`.
  Correcting those examples changed no theorem formula.
- `PROVED` replay coverage: exact rational alias tests include repeated exact
  hits, no-alias support, boundary tolerance, false-hit rejection, and all
  small Cycle-102 core identities for `W,N,R<=12` in their registered ranges.
- Claim boundary: no irrationality measure, aggregate exceptional-web bound,
  signed phase cancellation, weak/simple-root estimate, complete moment,
  density gain, or interval gain was proved.
- Artifact SHA-256:
  `93514b9668c49beec4a11d3892af1ae6d4f0b80125bd927edb9f378c8eba5e15`.
  Builder SHA-256:
  `baa58b53166a4d47ea212c8a97ca8ef756dda236620adb26c11d81ea5069f45e`.
- Builder runtime: wall time `0.27s`, peak RSS `51088 KiB`.
- Full Cycle-103 test runtime: wall time `34.56s`, peak RSS `61812 KiB`.
- Gate:
  `CRITICAL_SCALE_ALIAS_BANKED_RADICAL_SEPARATION_AGGREGATION_WEAK_SIMPLE_OPEN`.
- Replay:
  `python3 proof/build_cycle_103_critical_scale_alias_v1.py --check` and
  `python3 -m unittest tests/test_cycle_103_critical_scale_alias_v1.py`.

## Cycle 104 — single-radical alias separation (2026-08-02)

- `PROVED`: at criticality the two terms in Cycle 103 are proportional. With
  `h=(s,t)`, `u=s/h`, `v=t/h`, and `d=u+v=W/h`, the scale number collapses
  exactly to
  `K=(W/t)B0 r^(s/W)=(d R2/y)(N/R)^(u/d)`.
- `PROVED`: `(u,d)=1` and
  `K^d=(d R2/y)^d(N/R)^u=P/S`. Prime valuations classify exact rational
  aliases: `K` is rational iff the reduced numerator and denominator are both
  perfect `d`th powers. This includes nontrivial classes such as `9/4` for
  `d=2`.
- `PROVED`: outside the perfect-power class, factoring
  `q^dK^d-m^d` over the `d`th roots of unity gives
  `|qK-m|>=1/(S(qK+|m|)^(d-1))`. For `q<=Lambda` and nearest-integer `m`,
  the exactly rational safe bound is
  `1/(S(2 Lambda U+1/2)^(d-1))`, `U=max(1,P/S)>=K`.
- `PROVED`: if `2epsilon` from Cycle 103 is strictly below the safe norm
  bound, no short alias exists and at most one coefficient scale survives on
  that core. For fixed radical degree this is polynomial in the height and
  scale ledgers; large degrees may remain too weak.
- Implication: the generic degree-`W` logarithmic-form obstruction has been
  replaced by a native single-radical dichotomy: norm-separated irrational
  cores versus exact powered rational rays, plus a large-degree aggregate
  branch.
- Containment event: the first test run found three fixture errors. The
  constructed `K^2` was `144`, not `324`; the grid expectation omitted
  nontrivial perfect-power labels; and one prose substring assertion was
  irrelevant. The corrected `9/4` row confirms rather than refutes the
  perfect-power classification. The theorem formulas were unchanged.
- Claim boundary: no all-degree or aggregate exceptional-web bound,
  weak/simple-root estimate, complete moment, density gain, or interval gain
  was proved.
- Artifact SHA-256:
  `be9acdb96e8d8708ccdc1625e273f9fd092ad505125b058f6162ceae0715ed5b`.
  Builder SHA-256:
  `5707467d1ef29ab3188ffb3c19c28621caff801f55803ffd336054abe0536308`.
- Builder runtime: wall time `0.06s`, peak RSS `20096 KiB`.
- Gate:
  `RADICAL_NORM_SECTOR_BANKED_POWERED_RAYS_LARGE_DEGREE_WEAK_SIMPLE_OPEN`.
- Replay:
  `python3 proof/build_cycle_104_radical_alias_separation_v1.py --check` and
  `python3 -m unittest tests/test_cycle_104_radical_alias_separation_v1.py`.

## Cycle 105 — perfect-power ray compiler and shared sealer (2026-08-02)

- `PROVED`: the Cycle-104 rational class has exact representation
  `(w,N/R)=(h d,(n0/r0)^d)`. Thus each exact rational alias is the `d`th
  power of an anchored base rational ray `(h,n0/r0)`.
- `PROVED`: the factorization of powers transfers the Cycle-99 error as
  `|n0/r0-exp(hx)|<=delta/[d min(n0/r0,exp(hx))^(d-1)]`. Under
  `|hdx|<=L` and `delta<=exp(-L)/2`, the minimum base has the explicit lower
  envelope `(exp(-L)/2)^(1/d)`.
- `PROVED`: for nonunit base height `Z`, the height and mode budgets give
  `d<=min(floor(log H/log Z),2M/|h|)`. Repeated bases retain their exact
  exponent set, arithmetic mode multiples, geometric labels, and unchanged
  stationary payloads. Missing exponents are not inserted.
- Workflow improvement: the versioned shared module `proof/cycle_seal_v1.py`
  now owns runtime checks, frozen-input verification, prior-status checking,
  deterministic rendering, and immutable write/check behavior. Cycle 105 is
  the first consumer; the helper and its tests are themselves frozen inputs.
  Existing sealed builders remain unchanged. Breaking helper changes require
  `cycle_seal_v2.py`.
- Repository memory was updated in root `AGENTS.md` (and therefore the
  `CLAUDE.md`/`GEMINI.md` symlinks) to require versioned scaffold reuse for
  future cycles and forbid mechanical refactoring of already sealed builders.
- Claim boundary: a powered ray is not yet a realized original packet seed;
  singleton and large-degree aggregation, weak/simple-root estimates, the
  complete moment, density gain, and interval gain remain open.
- Artifact SHA-256:
  `81a1e6b990f2ff0f869fc79b66afe1d73953def9882294faacb15c5c70c14c66`.
  Builder SHA-256:
  `1ce2861bc8ae258fa0c4fe92adb2fa00262911924f63b91e3e02424a4b4cfa16`.
- Shared sealer SHA-256:
  `96d404c0e493144d72e593b789062daeaa2bd2481ec8b84641a1e19f9cd646b9`;
  tests SHA-256:
  `5ae01d03653e8846b487869af99f9a1a4901e39570111e89495ddd27982f6427`.
- Builder runtime: wall time `0.07s`, peak RSS `19836 KiB`.
- Gate:
  `POWERED_RAY_COMPILER_BANKED_REALIZATION_SINGLETON_LARGE_DEGREE_WEAK_SIMPLE_OPEN`.
- Replay:
  `python3 proof/build_cycle_105_powered_ray_compiler_v1.py --check` and
  `python3 -m unittest tests/test_cycle_105_powered_ray_compiler_v1.py tests/test_cycle_seal_v1.py`.

### Current-chain replay through Cycle 105

- `PROVED`: the sealed artifacts for Cycles 102--105 replayed exactly after
  the shared-sealer extraction; Cycles 102--104 retain their original
  builders, while Cycle 105 freezes `cycle_seal_v1.py` and its tests.
- `PROVED`: all 27 registered tests for Cycles 102--105 and the common sealer
  passed with no failures.
- `OBSERVED`: combined replay wall time was `36.28s`, peak RSS `66560 KiB`;
  `git diff --check` passed.

## Cycle 106 — beta-free powered-ray saturation boundary (2026-08-02)

- `PROVED`: in the Cycle-104 perfect-power class the critical scale number
  simplifies to `K=d n0^u r0^v/(xy)=A0/S0` in lowest terms.
- `PROVED`: under the tight regime `0<=epsilon<1/S0`, the near-integer scale
  hits are exactly the multiples of `S0`. Their set is
  `{S0,2S0,...,floor(Lambda/S0)S0}`, with size `floor(Lambda/S0)`; every
  scale survives iff `S0=1`.
- `PROVED`: unsigned all-scale saturation occurs on an actual nontrivial
  cross core. The frozen example
  `(u,v,d,x,y,n0,r0)=(2,1,3,2,1,3,2)` has label `27/8` and `K=27`, so every
  coefficient scale is an exact critical-value hit.
- `PROVED`, scoped non-implication: powered-ray data is beta-free, whereas a
  Cycle-67 seed depends on `|j0+beta-h0 alpha|`. Holding all beta-free data
  fixed, `beta=h0 alpha-j0` is an exact seed while adding `1/2` gives a miss
  for strip radius below `1/2`. Therefore beta-free geometry alone cannot
  certify a genuine packet seed.
- Positive interface: a retained stationary payload which itself verifies
  the beta-dependent inequality may still invoke Cycle 67. The no-go does
  not cover payload-aware E16 or signed cancellation along the exact scale
  progression.
- `PROVED` replay coverage: the rational simplification agrees with Cycle 104
  on more than 100 frozen small perfect-power cores; exact integer and
  noninteger scale progressions and paired beta witnesses pass.
- Claim boundary: no payload-aware seed, signed phase cancellation,
  singleton/large-degree aggregation, weak/simple-root estimate, complete
  moment, density gain, or interval gain was proved.
- Artifact SHA-256:
  `0e681ebf90d531a9564677779016642afbb73cf6c0cc47760b4b17db4b2bf3d1`.
  Builder SHA-256:
  `80b40f1172b1110e8867d60985949bfefdef749cfaa5c08c721d0371037b79f2`.
- Builder runtime: wall time `0.06s`, peak RSS `20092 KiB`.
- Gate:
  `UNSIGNED_SCALE_SATURATOR_BANKED_ACTUAL_PHASE_PAYLOAD_SINGLETON_LARGE_DEGREE_WEAK_SIMPLE_OPEN`.
- Replay:
  `python3 proof/build_cycle_106_beta_free_saturation_v1.py --check` and
  `python3 -m unittest tests/test_cycle_106_beta_free_saturation_v1.py tests/test_cycle_seal_v1.py`.

## Cycle 107 — actual-scale geometric stationary phase (2026-08-02)

- `PROVED`: restoring `(A,B,C)=(p0n,p0n',q0m)` cuts the Cycle-106 rational
  scale orbit to `lambda=lambda0 ell`, where
  `lambda0=lcm(S0 p0/(p0,A0),p0/(p0,B0),q0/(q0,C0))`. The integral base
  indices are explicit and every actual `(n,n',m)` is their common multiple.
- `PROVED`: simultaneous scaling of `(H,Delta,n,n',m)` preserves both
  exponentiated Cycle-94 stationary equations. The entropy phase and fixed
  Poisson-mode linear terms are degree-one homogeneous, giving the exact
  identity `Phi_ell=ell Phi0`.
- `PROVED`: the unweighted actual scale sum satisfies
  `|sum_{ell<=L}e(ell Phi0)|<=min(L,1/(2||Phi0||))`. Abel summation multiplies
  the same factor by `|a_L|+sum|a_ell-a_(ell+1)|` for complex amplitudes.
- Implication: Cycle 106's unsigned all-scale saturator becomes a geometric
  phase sum. Failure to cancel now forces a near-integral base phase and
  retains `c0`, beta-bearing payload, modes, base indices, and stationary
  coordinates for E16.
- Containment event: SymPy did not normalize one complete cubic
  root-of-unity sum. Encoding the exact root order fixed the replay helper;
  no theorem identity or bound changed.
- Claim boundary: no actual B-process amplitude BV bound,
  phase-resonance-to-seed theorem, singleton/large-degree aggregation,
  weak/simple-root estimate, complete moment, density gain, or interval gain
  was proved.
- Artifact SHA-256:
  `189d2515ac835f25b14ff060604317c0a5210050b0c4ec06be567935caf28319`.
  Builder SHA-256:
  `69aa3945184a72adf1b3f385325b3445a72f978c7c4a878fa7c96e4fde21ac30`.
- Builder runtime: wall time `0.32s`, peak RSS `50780 KiB`.
- Gate:
  `ACTUAL_SCALE_GEOMETRIC_PHASE_BANKED_AMPLITUDE_RESONANCE_SINGLETON_LARGE_DEGREE_WEAK_SIMPLE_OPEN`.
- Replay:
  `python3 proof/build_cycle_107_actual_scale_phase_v1.py --check` and
  `python3 -m unittest tests/test_cycle_107_actual_scale_phase_v1.py tests/test_cycle_seal_v1.py`.

## Cycle 108 — triple-B leading Jacobian summability (2026-08-02)

- `PROVED`: the three frozen stationary amplitudes are
  `sqrt(c Delta)/m`, `sqrt(c H)/n`, and `sqrt(c(H-Delta))/n'`; their product
  is `c^(3/2)sqrt(Delta H(H-Delta))/(mnn')`.
- `PROVED`: along a Cycle-107 actual scale ray the stationary evaluation
  points `c c0 Delta/m`, `cH/n`, and `c(H-Delta)/n'` are invariant, while the
  Jacobian product scales exactly as `J_ell=ell^(-3/2)J0`.
- `PROVED`: `sum_{ell<=L}ell^(-3/2)<3`, and the finite BV norm of
  `ell^(-3/2)` telescopes exactly to one. Therefore
  `sum|omega_ell J_ell|<=3J0 sup|omega_ell|`.
- Implication: the raw coefficient-scale multiplicity disappears from the
  leading perfect-power stationary term under a subpower residual envelope,
  even at exact Cycle-107 phase resonance.
- Claim boundary: arithmetic payload weights, cutoff factors outside the
  invariant stationary coordinates, nonleading B-process remainders,
  aggregation across cores, weak/simple-root estimates, the complete moment,
  density gain, and interval gain remain open.
- Artifact SHA-256:
  `c030327447462241e056c593bc799e7fec472d6663faf17d5f8a9dbab8424813`.
  Builder SHA-256:
  `ececa237f6a367190e7262d8e36d5323230df8d9f4ced9fba9fcbb3974935f6e`.
- Builder runtime: wall time `0.27s`, peak RSS `50528 KiB`.
- Gate:
  `LEADING_SCALE_RAY_SUMMABLE_RESIDUAL_REMAINDER_SINGLETON_LARGE_DEGREE_WEAK_SIMPLE_OPEN`.
- Replay:
  `python3 proof/build_cycle_108_triple_b_jacobian_v1.py --check` and
  `python3 -m unittest tests/test_cycle_108_triple_b_jacobian_v1.py tests/test_cycle_seal_v1.py`.

## Cycle 109 — uniform full smooth triple-B scale ray (2026-08-02)

- `PROVED`: if a compactly supported one-dimensional amplitude is `C^1` and
  the phase curvature has fixed sign with magnitude at least `lambda`, then
  direct interval splitting and integration by parts give
  `|int w e(phi)|<=(4||w||_infinity+||w'||_1)lambda^(-1/2)`.
- `PROVED`: iterating that lemma for a joint smooth symbol with frozen mixed
  norm bounds the full separated three-variable logarithmic B-process
  integral by the product of the three inverse square-root curvatures. No
  asymptotic stationary expansion is used.
- `PROVED`: on a fixed compact actual-scale chart the three curvatures have
  fixed signs and magnitudes proportional to `ell`. Consequently the entire
  fixed-symbol kernel satisfies `|I_ell|<=C_W ell^(-3/2)` and
  `sum_ell |I_ell|<3C_W`, even when the Cycle-107 projective phase is exactly
  resonant.
- Implication: nonleading stationary-phase remainders no longer obstruct a
  fixed smooth perfect-power scale ray. The live issue is the dependence of
  `C_W` on the base core/chart and aggregation across primitive splits and
  distinct powered rays.
- Claim boundary: the theorem does not control nonsmooth arithmetic
  coefficient payloads, aggregate distinct cores, irrational large-degree
  cores, weak/simple roots, the complete signed moment, density gain, or an
  interval gain.
- Artifact SHA-256:
  `da481a16c7a9e027d53104282410e2bad73fcaf6157a9ea3fe61ffeb8d74f432`.
  Builder SHA-256:
  `8127a309b0e09e6ae07e19b33b737385cf4b562132cd74969206f48a0299f63f`.
- Builder runtime: wall time `0.30s`, peak RSS `50632 KiB`.
- Gate:
  `PERFECT_POWER_SCALE_RAYS_CLOSED_DISTINCT_CORE_LARGE_DEGREE_WEAK_SIMPLE_OPEN`.
- Replay:
  `python3 proof/build_cycle_109_uniform_triple_b_v1.py --check` and
  `python3 -m unittest tests/test_cycle_109_uniform_triple_b_v1.py tests/test_cycle_seal_v1.py`.

## Cycle 110 — perfect-power primitive-split summability (2026-08-02)

- `PROVED`: for a perfect-power label `(n0/r0)^d` and primitive split
  `u+v=d`, the exact cross factors are `x=(u,r0^d)`, `y=(v,n0^d)`, and
  `K B0 C0=d u v n0^(u+d) r0^(v+d)/(xy)^3`.
- `PROVED`: after factoring the common compact-chart/anchor normalization,
  the Cycle-109 Jacobian weight is
  `(xy)^(3/2)/sqrt(d u v n0^(u+d) r0^(v+d))`. Splitting into the unit base,
  the two one-sided unit cases, and the fully nonunit case proves that its
  sum over all primitive splits is `<4`, uniformly in `d,n0,r0`.
- `PROVED`: at fixed mode magnitude `W`, every primitive degree divides `W`;
  Cycle 99 gives one strong critical label per signed mode and each reduced
  rational has a unique positive `d`th root. Thus all perfect-power degrees
  and splits at that mode have normalized weight at most `4 tau(W)=W^o(1)`.
- `OBSERVED`: the frozen search over 7,189 triples with `d<=80` and
  `n0,r0<=12` has maximum `sqrt(2/3)=0.81649...` at `(d,n0,r0)=(3,1,1)`.
  This search has no proof role.
- Implication: neither raw coefficient-scale multiplicity nor the number of
  primitive cross-valuation splits causes a power loss in the smooth
  perfect-power branch.
- Claim boundary: the common compact-chart/anchor prefactor and nonsmooth
  coefficient payload remain unbounded across modes. Irrational large-degree
  cores, weak/simple roots, the complete moment, density gain, and interval
  gain remain open.
- Artifact SHA-256:
  `cfcedf8145cf6ef70fb88b1a722067460236dfb7a04061d75db325e093746c42`.
  Builder SHA-256:
  `dbb271018bfc988d0d2da51ccacf4ec5dffa28eb33fcda99725e589492a264be`.
- Builder runtime: wall time `0.04s`, peak RSS `18304 KiB`.
- Gate:
  `PERFECT_POWER_SPLIT_AND_SCALE_SUMMABLE_NORMALIZATION_LARGE_DEGREE_WEAK_SIMPLE_OPEN`.
- Replay:
  `python3 proof/build_cycle_110_perfect_power_split_sum_v1.py --check` and
  `python3 -m unittest tests/test_cycle_110_perfect_power_split_sum_v1.py tests/test_cycle_seal_v1.py`.

## Cycle 111 — versioned correction of the `k`-stationary point (2026-08-02)

- Correction: Cycle 108 displayed `k*=c c0 Delta/m`. Directly crossing the
  Cycle-81 columns gives `Phi_k=c Delta log(k c0)-mk`, hence
  `k*=c Delta/m`. The sealed Cycle-108 artifact was not edited; its location
  display is superseded by the Cycle-111 correction artifact.
- `PROVED`: the stationary Hessian remains `-m^2/(c Delta)` and the stationary
  value remains `c Delta[log(c c0 Delta/m)-1]`. Thus Cycle 94's entropy and
  central anchor relation are unchanged.
- `PROVED`: the corrected point is still invariant under the Cycle-107 common
  scale dilation. Cycle 108's Jacobian amplitude and `ell^(-3/2)` law,
  Cycle 109's curvature summability, and Cycle 110's normalized coefficient
  identity are unchanged.
- Containment event: any cutoff value or mixed-symbol norm evaluated using
  the old Cycle-108 point is withheld. The next normalization ledger must
  rederive it from `k*=c Delta/m`.
- `PROVED`: Cycles 94, 107, 109, and 110 replayed exactly after the correction.
- Claim boundary: no full outer-prefactor or anchor normalization, complete
  moment, density gain, or interval gain was proved.
- Artifact SHA-256:
  `22bb8d5a5d9eb581f66776b3fe9a88f9677e15173422c323ba4108138e7ae5c1`.
  Builder SHA-256:
  `a743c6de30078f46324252a379fa6739e794fefaac146efda9a83409256786fe`.
- Builder runtime: wall time `0.46s`, peak RSS `55748 KiB`.
- Gate:
  `K_LOCATION_CORRECTED_NORMALIZATION_CUTOFF_LARGE_DEGREE_WEAK_SIMPLE_OPEN`.
- Replay:
  `python3 proof/build_cycle_111_k_stationary_correction_v1.py --check` and
  `python3 -m unittest tests/test_cycle_111_k_stationary_correction_v1.py tests/test_cycle_seal_v1.py`.

## Cycle 112 — corrected full symbol and smooth perfect-power closure (2026-08-02)

- `PROVED`: multiplying the paired Cycle-81 amplitude `c^2/(rr')` by the
  three Hessian factors and substituting the corrected stationary points
  gives exactly `c^2 sqrt(k/(rr'))/sqrt(mnn')`.
- `PROVED`: the four inherited cutoffs become `V(n/Q)`, `V(n'/Q)` and two
  logarithmic `W` arguments. The anchor `c0` only translates the latter; it
  creates no multiplicative smooth-symbol norm loss.
- `PROVED`: with `c0=p0/q0`, actual indices satisfy
  `n'=lambda B0/p0`, `m=lambda C0/q0`. Since `B0,C0<=Q` and the fixed
  interior support has `n',m>=aQ`, every supported scale satisfies
  `lambda>=a max(p0,q0)`. This absorbs
  `p0 sqrt(q0)/lambda^(3/2)` uniformly.
- `PROVED`: combining the corrected full symbol with Cycle 110 gives
  `O(tau(|w|))` normalized weight per signed strong mode and total arithmetic
  multiplicity `M^(1+o(1))=X^(3/5+o(1))`. This is a strict `1/30` saving over
  the generic `X^(19/30+o(1))` strong branch.
- Implication: the registered smooth strong perfect-power branch is closed;
  neither scale rays, split entropy, rational-anchor height, nor smooth cutoff
  norms restore the lost power.
- Claim boundary: nonsmooth coefficient payloads, irrational large-degree
  cores, weak/simple roots, the complete signed moment, density gain, and
  interval gain remain open.
- Artifact SHA-256:
  `e6f890eaae72a99c53dbd07cea7bd69d050f4df5c93d40e27245f71503f6954c`.
  Builder SHA-256:
  `04fb6b71a79daebad3af2b015c20e13af56336b668b1956e0f5ff9cf384d7f54`.
- Builder runtime: wall time `0.44s`, peak RSS `56144 KiB`.
- Gate:
  `SMOOTH_PERFECT_POWER_STRONG_CLOSED_LARGE_DEGREE_WEAK_SIMPLE_OPEN`.
- Replay:
  `python3 proof/build_cycle_112_full_triple_b_symbol_v1.py --check` and
  `python3 -m unittest tests/test_cycle_112_full_triple_b_symbol_v1.py tests/test_cycle_seal_v1.py`.

## Cycle 113 — general weighted splits and Cycle-112 aggregate correction (2026-08-02)

- `PROVED`: for every reduced compact label and primitive split,
  `(K B0 C0)^d=(d u v)^d N^(d+u)R^(2d-u)/(xy)^(3d)`.
- `PROVED`: putting `Z=min(N,R)`, the small-height range `Z<=d^(1/3)` is
  bounded directly. In the complementary range, dyadically freezing
  `(u,v)` and exact divisors `(x,y)` leaves at most `1+d/(xy)` solutions;
  each cell is bounded and the number of cells is subpower. Hence the total
  normalized split weight is `(dNR)^o(1)`, uniformly for rational and
  irrational labels.
- `OBSERVED`: across 522,053 frozen rows with `d,N,R<=120` and
  `1/2<=N/R<=2`, the largest split sum is `0.986836...` at `(7,3,4)`.
  The scaled quantity `sqrt(d)` times the sum reaches `8.064...`, refuting
  the stronger discovery guess of uniform `d^(-1/2)` decay. The search has
  no proof role.
- Correction: Cycle 112's full-symbol and cutoff identities remain proved,
  but its `X^(3/5+o(1))` aggregate is withheld. If
  `lambda=lambda_BC ell` and `E` is the first supported `ell`, absolute scale
  summation retains
  `p0 sqrt(q0)/(lambda_BC^(3/2)sqrt(E))`; pointwise support absorption does
  not control a long support window.
- Implication: primitive-split entropy and irrational degree are no longer
  independent obstructions. The live strong-core problem is the coupled
  anchor-scale-label sum, which must not be factorized prematurely.
- Claim boundary: no strong-core aggregate closure, weak/simple-root bound,
  complete moment, density gain, or interval gain was proved.
- Artifact SHA-256:
  `2d29b2600e9b123ded335a2be83c656361c6ba46e3d74117d00bdf9253ebe393`.
  Builder SHA-256:
  `bdd421bb88e4c313f8da61ad93f516edbae000bf38e379200b95727debfc2850`.
- Discovery runtime: wall time `7.44s`, peak RSS `14836 KiB`.
  Builder runtime: wall time `0.05s`, peak RSS `18304 KiB`.
- Gate:
  `GENERAL_SPLIT_SUBPOWER_ANCHOR_SCALE_LABEL_WEAK_SIMPLE_OPEN`.
- Replay:
  `python3 proof/build_cycle_113_irrational_weighted_split_v1.py --check` and
  `python3 -m unittest tests/test_cycle_113_irrational_weighted_split_v1.py tests/test_cycle_seal_v1.py`.

## Cycle 114 — coupled anchor-scale-label closure (2026-08-02)

- `PROVED`: the original coefficient bounds `B=p0n'<=Q` and `C=q0m<=Q`,
  together with the fixed interior support `n',m>=aQ`, force
  `p0,q0<=1/a`. Thus the growing-anchor scenario isolated in Cycle 113 is
  impossible on an actual supported row.
- `PROVED`: simultaneous support makes `K,B0,C0` comparable to a coefficient
  height `Zc=Q/lambda`. A fixed core has `O(Q/Zc)` supported scales, each
  carrying coefficient kernel `O(Q^(-3/2))`; its scale sum is
  `O(1/(sqrt(Q)Zc))`.
- `PROVED`: coefficient comparability forces `u,v~d` and
  `Zc~dZ/(xy)`, `Z=min(N,R)`. The remaining split sum is a normalized gcd
  convolution. Expanding each gcd by Euler totients and treating the `+1`
  residue term separately for `Z<=d` and `Z>=d` proves
  `sum_u (u,R)(d-u,N)<=dZ(dNR)^o(1)`.
- `PROVED`: every degree at one smooth strong mode costs
  `Q^(-1/2)X^o(1)`. Since degrees divide `|w|` and strong labels inject,
  all registered smooth strong cores—rational and irrational—have weighted
  arithmetic factor `M Q^(-1/2)X^o(1)=X^(13/30+o(1))` after the common
  analytic chart factor.
- Implication: Cycle 113's containment is resolved by a genuinely coupled
  proof. Cycle 112's incorrect `X^(3/5)` route remains superseded; the
  licensed strong-core closure is the sharper Cycle-114 `X^(13/30)` route.
- Claim boundary: weak localization, simple roots, nonsmooth payload
  variants, complete moment assembly, density gain, and interval gain remain
  open.
- Artifact SHA-256:
  `bec19431e36affe22633ce2095db8537205b5dcd2525e29abb7a0ab79271d596`.
  Builder SHA-256:
  `18ad77e011ef5055116a6e07c7c94284e4a424ea7679eb5dbd92794c46b68d1e`.
- Builder runtime: wall time `0.04s`, peak RSS `17920 KiB`.
- Gate:
  `ALL_SMOOTH_STRONG_CORES_X13_30_WEAK_SIMPLE_OPEN`.
- Replay:
  `python3 proof/build_cycle_114_coupled_anchor_scale_v1.py --check` and
  `python3 -m unittest tests/test_cycle_114_coupled_anchor_scale_v1.py tests/test_cycle_seal_v1.py`.

## Cycle 115 — local weak-turnover trichotomy (2026-08-02)

- `PROVED`: on the local interval `[x/2,3x/2]`, the exact curvature satisfies
  `S2e^(-3Mx/2)<=|f''|<=S2e^(3Mx/2)`. This replaces Cycle 97's global
  `[x-1,x+1]` envelope and its artificial exponential-in-`M` loss.
- `PROVED`: if `eta>=max(4delta/x,2sqrt(L_x delta))`, a Newton sign change
  gives a real root within `2delta/eta`. If `eta<=ell_x x/2`, same-sign modes
  are excluded and strict concavity gives the unique critical point within
  `eta/ell_x`.
- `PROVED`: every remaining transition satisfies
  `delta>ell_x^2x^2/(16L_x)`. Consequently, below this explicit floor there
  is no weak middle: every row is either simple-root or locally strong.
- `PROVED`: for `x=2pi/D`, `M<=D`, the transition floor is at least
  `(pi^2e^(-9pi)/4)S2/D^2`; only an absolute constant is lost because
  `Mx<=2pi`.
- Claim boundary: the actual projective stationary tolerance has not yet
  been reconstructed and compared with this floor. Simple-root averaging,
  complete moment closure, density gain, and interval gain remain open.
- Artifact SHA-256:
  `cfc45ce92d0a986fca7d5708f1fd6a71befe47e07c1d6c95fe2a1059a72f029d`.
  Builder SHA-256:
  `d910c025fcb50422fb868cf1e94e02f8845a46a363f1599a6d7ef507b1f1afca`.
- Builder runtime: wall time `0.04s`, peak RSS `17792 KiB`.
- Gate:
  `STRONG_X13_30_LOCAL_TURNOVER_BANKED_TOLERANCE_SIMPLE_OPEN`.
- Replay:
  `python3 proof/build_cycle_115_local_turnover_v1.py --check` and
  `python3 -m unittest tests/test_cycle_115_local_turnover_v1.py tests/test_cycle_seal_v1.py`.

## Cycle 116 — projective tolerance and weak-mode cap (2026-08-02)

- `PROVED`: the two smooth height variables have length `H0~KQ/D`; with
  phase multiplier `c=D/(2pi)`, a surviving projective Poisson cell has
  gradient errors `|G1|+|G2|<<1/(KQ)`.
- `PROVED`: retaining both errors in the exact exponentiated elimination
  gives `A-Bg^u exp(G1)-Cg^(u+v)exp(G1+G2)=0`. Since `B,C<=Q`, the zero-error
  Laurent residual satisfies `delta<<1/K`.
- `PROVED`: comparison with Cycle 115 confines every weak transition to
  `S2=Ba^2+Cb^2<<D^2/K`. If `B,C>=Zc`, then
  `max(|a|,|b|)<<D/sqrt(KZc)`.
- `PROVED`: for `K=X^xi`, `Zc=X^zeta`, the weak-mode exponent is at most
  `3/5-xi/2-zeta/2`. Over the lower band `xi>=16/25`, its worst value is
  `7/25`, a reduction of `8/25` from the former `3/5` mode range.
- Claim boundary: the low-energy weak sector has not yet been summed with
  coefficient and stationary-kernel weights. Simple-root averaging, full
  moment closure, density gain, and interval gain remain open.
- Artifact SHA-256:
  `f40fb40708fb27d857f3c116dc8c1b7d76cb2291a4ad965e81f5cafe09a62dd2`.
  Builder SHA-256:
  `0cb4af42f249a21bd3a3cea641930cf18b541668a0920c3ba0ecded0a911ec60`.
- Builder runtime: wall time `0.04s`, peak RSS `18304 KiB`.
- Gate:
  `STRONG_X13_30_WEAK_MODE_7_25_SIMPLE_OPEN`.
- Replay:
  `python3 proof/build_cycle_116_projective_tolerance_v1.py --check` and
  `python3 -m unittest tests/test_cycle_116_projective_tolerance_v1.py tests/test_cycle_seal_v1.py`.

## Cycle 117 — weighted weak-sector closure (2026-08-02)

- `PROVED`: Cycle 114's bounded anchors and actual stationary support force
  `B,C~Q`; the coefficient-height exponent is not free on the weak branch.
- `PROVED`: for each coefficient pair, the Cycle-116 energy ellipse contains
  `O(1+D^2/(KQ))` integer mode pairs. For fixed `(B,C,a,b)`, the Laurent
  residual interval has length below one and therefore selects at most one
  integer `A`.
- `PROVED`: multiplying `O(Q^2)` coefficient pairs by the ellipse count and
  Cycle 112's corrected `Q^(-3/2)` kernel gives
  `Q^(1/2)+D^2/(KQ^(1/2))`.
- `PROVED`: the weak exponent is `max(1/6,31/30-xi)`. Its lower-band maximum
  is `59/150` at `xi=16/25`, a uniform `1/25` margin below Cycle 114's
  strong benchmark `13/30=65/150`.
- Implication: both registered smooth strong and weak near-double sectors are
  closed. The remaining smooth lower-band branch is the quantitative
  simple-root output.
- Claim boundary: simple-root averaging, nonsmooth payload variants, full
  moment assembly, density gain, and interval gain remain open.
- Artifact SHA-256:
  `2594773d6768fd46aa46da2e424cb2c06ab49fada984fd9b3c7315ff521b56ea`.
  Builder SHA-256:
  `8d33bb6c247aea42f2947f994334f457f5dca085f0d086b7fe91d78312465feb`.
- Builder runtime: wall time `0.04s`, peak RSS `18304 KiB`.
- Gate:
  `SMOOTH_STRONG_AND_WEAK_CLOSED_SIMPLE_ROOT_OPEN`.
- Replay:
  `python3 proof/build_cycle_117_weighted_weak_sector_v1.py --check` and
  `python3 -m unittest tests/test_cycle_117_weighted_weak_sector_v1.py tests/test_cycle_seal_v1.py`.

## Cycle 118 — derivative-resolved simple-root profiler (2026-08-02)

- `OBSERVED`: the frozen 80-decimal profiler retained 4,360, 9,584, and
  21,477 near rows at `D=24,36,48`; respectively 3,461, 7,400, and 16,128
  satisfy the Cycle-115 local simple-root threshold.
- `OBSERVED`: at `D=48`, the dominant signatures are
  `J0_NONZERO/J1_NONZERO/OPPOSITE` with 9,184 rows and
  `J0_NONZERO/J1_NONZERO/SAME` with 6,754 rows. The two zero-jet classes
  together contain only 190 rows.
- Falsifier: the discovery hypothesis that simple roots concentrate on
  `J0=0` or `J1=0` fails decisively on every frozen grid. This is not an
  asymptotic theorem or a universal negative.
- Implication: the simple branch must be treated as a genuine
  derivative-weighted discrepancy/covering problem for
  `A=B exp(2pi a/D)+C exp(2pi b/D)`, with same-sign and opposite-sign sectors
  retained separately. Representative rows preserve full coefficient,
  mode, jet, residual, and derivative payload.
- Claim boundary: no simple-root estimate, complete moment, density gain, or
  interval gain was proved.
- Artifact SHA-256:
  `5862998cc7811f79fee31301ae65ddcf55c93fb5455c38fa6627cb6f70b4065c`.
  Builder SHA-256:
  `7d4655cbf79719dc9b4a091ee1385e4f94c04e3d34ebe7e84dfb5672c1a95ef1`.
- Discovery runtime: wall time `7.96s`, peak RSS `17468 KiB`.
  Builder runtime: wall time `0.04s`, peak RSS `17920 KiB`.
- Gate:
  `SMOOTH_STRONG_WEAK_CLOSED_SIMPLE_DISCREPANCY_OPEN`.
- Replay:
  `python3 discovery/run_cycle_118_simple_root_profiler_v1.py` and
  `python3 proof/build_cycle_118_simple_root_profiler_v1.py --check`.

## Cycle 119 — simple-root absolute-volume limitation (2026-08-02)

- `PROVED`: a periodic Selberg majorant for
  `dist(B exp(2pi a/D)+C exp(2pi b/D),Z)<=c/K` has constant coefficient
  comparable to `1/K`. On the `Q^2D^2` coefficient-mode tuples, its zeroth
  Fourier mode is `Q^2D^2/K=X^(28/15-xi)`.
- `PROVED`: Cycle 112's corrected `Q^(-3/2)=X^(-1/2)` kernel turns this into
  weighted exponent `41/30-xi`. It exceeds the Cycle-114 benchmark `13/30`
  by exactly `14/15-xi`: `22/75` at `xi=16/25`, tending to `4/25` as
  `xi` approaches `58/75`.
- `PROVED`: on frozen sign sectors the nonzero Fourier mode factorizes as
  `hat(S)(h)T_sigma(h)T_tau(h)`, with
  `T_sigma(h)=sum_(B~Q,a in I_sigma)e(hB exp(2pi a/D))`. The two factors are
  not automatically conjugates.
- Structural no-go: any Selberg-majorant proof that bounds the nonzero modes
  termwise in absolute value retains the positive zeroth mode and cannot
  reach `13/30`. This is deliberately scoped: it does not exclude an
  unsigned discrepancy theorem proving cancellation against the mean.
- Implication: the simple branch must preserve the nonzero Fourier signs or
  restore the original stationary phase, and must supply the explicit saving
  `X^(14/15-xi)`.
- Claim boundary: no signed simple-root estimate, complete moment, density
  gain, or interval gain was proved.
- Artifact SHA-256:
  `d101504a18724dc79c143a0d485790584478e282c9544cfab8be2349212d50e9`.
  Builder SHA-256:
  `1b35b1aa3a8dedfc121ce72790a9e265638d512f3366dd3aeb28ad212dc9dcf6`.
- Builder runtime: wall time `0.04s`, peak RSS `18560 KiB`.
- Gate:
  `SIMPLE_ABSOLUTE_VOLUME_LIMIT_SIGNED_DISCREPANCY_OPEN`.
- Replay:
  `python3 proof/build_cycle_119_simple_root_volume_v1.py --check` and
  `python3 -m unittest tests/test_cycle_119_simple_root_volume_v1.py tests/test_cycle_seal_v1.py`.

## Cycle 120 — exact projective-radial phase normal form (2026-08-02)

- `PROVED`: with `Delta=zH`, the exact Cycle-94 entropy-Poisson phase becomes
  `H P_(u,v)(z)`. The former zero Hessian determinant is now localized: the
  phase is linear in the radial variable `H`, while
  `P''(z)=c/[z(1-z)]>0` in the projective variable.
- `PROVED`: for `(A,B,C)=(p0n,p0n',q0m)` the unique projective saddle is
  `z_v=Cg^v/(B+Cg^v)`, and its surviving radial frequency is exactly
  `P(z_v)=c log(A/(Bg^u+Cg^(u+v)))`.
- `PROVED`: if `R=A-Bg^u-Cg^(u+v)` and `|R|<=A/2`, then `P(z_v)` has the
  sign of `R` and lies between `(2c/(3A))|R|` and `(2c/A)|R|` in magnitude.
  Hence at `H0~KQ/D`, with `A~Q` and `c~D`, radial coherence is equivalent
  up to constants to the Cycle-116 window `|R|<<1/K`.
- Implication: the simple-root object is a signed radial Fourier profile at
  `H0P(z_v)`, with a positively curved projective saddle. Replacing it by a
  positive near-root indicator is exactly the Cycle-119 loss.
- Claim boundary: the uniform projective stationary amplitude, its remainder,
  cancellation in the radial-profile sum, complete moment, density gain, and
  interval gain remain open.
- Artifact SHA-256:
  `cd584128c1624c8ced2d91c71ff7cb370a7bab7a57f8441b7a8e7b994b5c66cd`.
  Builder SHA-256:
  `dbb52474c979bec85169df472ef8a8fedb9acd216bc25e43508b741072eeaa31`.
- Builder runtime: wall time `0.05s`, peak RSS `19320 KiB`.
- Gate:
  `PROJECTIVE_CURVATURE_RADIAL_SIGNED_KERNEL_OPEN`.
- Replay:
  `python3 proof/build_cycle_120_projective_radial_phase_v1.py --check` and
  `python3 -m unittest tests/test_cycle_120_projective_radial_phase_v1.py tests/test_cycle_seal_v1.py`.

## Cycle 121 — projective stationary-amplitude collapse (2026-08-02)

- `PROVED`: substituting `Delta=zH` into Cycle 112's corrected full symbol
  and multiplying by `dH dDelta=H dH dz` gives projective amplitude
  `c^(3/2)H^(1/2)sqrt(z/(1-z))/m`.
- `PROVED`: the positive-curvature stationary factor is
  `e(1/8)sqrt(z_v(1-z_v)/(Hc))`. Its product with the preceding amplitude is
  exactly `e(1/8)c z_v/m`, equivalently
  `e(1/8)c q0g^v/(B+Cg^v)`, with no remaining power of `H`.
- `PROVED`: all four corrected Cycle-112 cutoffs are independent of `H` in
  projective coordinates. A dyadic radial cutoff therefore gives the
  explicit profile `H0 hat(U)(-H0P(z_v))`.
- `PROVED`: on a fixed compact projective chart with fixed smooth norms, the
  stationary remainder is `O(1/(mH))`; integration over `H~H0` is `O(1/m)`.
- Implication: the smooth simple-root branch is now an explicit arithmetic
  sum of signed radial Fourier profiles. Because the original dyadic cutoff
  is supported away from zero, its continuous mean is expected to vanish;
  this is the next registered theorem rather than an assumed cancellation.
- Claim boundary: no arithmetic cancellation, simple-root closure, complete
  moment, density gain, or interval gain was proved.
- Artifact SHA-256:
  `5c003a1ce44fc5a87d7997fa80d71c18729ad3c89d857f09955a7baf0110317f`.
  Builder SHA-256:
  `610f4bdf245366a7aa31d86e601b70d4b523d2672337877af8177ed81d28dfb2`.
- Builder runtime: wall time `0.06s`, peak RSS `19188 KiB`.
- Gate:
  `PROJECTIVE_AMPLITUDE_COLLAPSED_RADIAL_OPERATOR_BOUND_OPEN`.
- Replay:
  `python3 proof/build_cycle_121_projective_amplitude_v1.py --check` and
  `python3 -m unittest tests/test_cycle_121_projective_amplitude_v1.py tests/test_cycle_seal_v1.py`.

## Cycle 122 — radial zero-mode removal and `K`-alias map (2026-08-02)

- `PROVED`: for `K_H0(y)=H0hat(U)(-H0y)`, every moment
  `int y^jK_H0(y)dy` vanishes because the frozen dyadic cutoff `U` is
  identically zero near zero.
- `PROVED`: after `y=c log(p0n/S)`, the corrected smooth symbol and nonlinear
  Jacobian have derivative scale `c^(-1)` on fixed supports. Taylor expansion
  against the vanishing moments, with the Schwartz tail treated before the
  support edge, bounds the zero `n`-Poisson mode by
  `O_N((Q/c)(cH0)^(-N))` for every fixed `N`. Since `cH0~KQ`, the continuous
  volume term is power-negligible.
- `PROVED`: a nonzero Poisson mode has phase
  `Phi_ell(n)=Hc log(p0n/S)-ell n`. Stationarity requires `ell>0` and gives
  `n*=Hc/ell`, value `Hc[log(p0Hc/(ell S))-1]`, curvature
  `ell^2/(Hc)`, and amplitude `sqrt(Hc)/ell~sqrt(Q/K)`.
- `PROVED`: support `n~Q`, `H~KQ/D`, and `c~D` forces `ell~K`.
- Implication: the Cycle-119 zeroth-volume obstruction disappears in the
  actual signed operator. The remaining simple branch is an explicit
  nonzero alias problem at the original frequency scale, not a near-root
  count.
- Claim boundary: no bound for the `ell~K` aliases, simple-root closure,
  complete moment, density gain, or interval gain was proved.
- Artifact SHA-256:
  `c419446735481e49ceef40c66296ad0ae6d0efe5bdef90cf4b3e173711a86a95`.
  Builder SHA-256:
  `045eb6ab35dd2d2ac910e65a439f7da48c0489e24d4b5b9f2a67b14a1583cc16`.
- Builder runtime: wall time `0.05s`, peak RSS `18372 KiB`.
- Gate:
  `RADIAL_ZERO_MODE_REMOVED_K_ALIAS_OPERATOR_OPEN`.
- Replay:
  `python3 proof/build_cycle_122_radial_mean_alias_v1.py --check` and
  `python3 -m unittest tests/test_cycle_122_radial_mean_alias_v1.py tests/test_cycle_seal_v1.py`.

## Cycle 123 — joint radial-alias saddle and phase factorization (2026-08-02)

- `PROVED`: for `S=p0n'g^u+q0mg^(u+v)`, the joint phase
  `Phi_ell(H,n)=Hc log(p0n/S)-ell n` has the unique interior saddle
  `n*=S/p0`, `H*=ell S/(p0c)`.
- `PROVED`: its Hessian is
  `[[0,c/n],[c/n,-Hc/n^2]]`, with determinant `-(c/n)^2` and one eigenvalue
  of each sign. The joint signature is therefore zero, the stationary value
  is `-ell S/p0`, and the joint amplitude is `S/(p0c)`.
- `PROVED`: multiplying the joint amplitude by Cycle 121's projective factor
  gives exactly `e(1/8)(q0/p0)g^(u+v)`. No power of `H,n,m,c` remains.
- `PROVED`: the corrected logarithmic cutoff arguments become
  `-(u+v)/D` and `-v/D`; the remaining smooth support is
  `V(n'/Q)V(S/(p0Q))U(ell S/(p0cH0))`.
- `PROVED`: the phase factors exactly as
  `e(-ell n'g^u)e(-ell(q0/p0)m g^(u+v))`. After rescaling, the fixed-chart
  joint remainder is smaller than its leading stationary scale by
  `O((KQ)^(-1))`.
- Implication: the live simple-root object is now a fully normalized weighted
  bilinear operator. Its possible self-duality with the original lower-band
  projector must be quantified before claiming a gain.
- Claim boundary: no bilinear estimate, simple-root closure, complete moment,
  density gain, or interval gain was proved.
- Artifact SHA-256:
  `e700c21a422413abb6f35882d8d5a67b4ae4095b23c157da6397417b08f4da79`.
  Builder SHA-256:
  `788d408cf6e7a66415358ff698a908581aaf4ce291fe5d5bd9348c96f11bfabf`.
- Builder runtime: wall time `0.05s`, peak RSS `19324 KiB`.
- Gate:
  `JOINT_ALIAS_NORMALIZED_BILINEAR_OR_SELF_DUAL_INVERSE_OPEN`.
- Replay:
  `python3 proof/build_cycle_123_joint_radial_alias_v1.py --check` and
  `python3 -m unittest tests/test_cycle_123_joint_radial_alias_v1.py tests/test_cycle_seal_v1.py`.

## Cycle 124 — scoped bilinear norm-self-duality (2026-08-02)

- `PROVED`: after `(a,b)=(u,u+v)` and `alpha=q0/p0`, the Cycle-123 phase is
  `e(-ell n'g^a)e(-ell alpha m g^b)`.
- `PROVED`: every fixed smooth coupled symbol in the normalized variables
  `(ell/K,n'g^a/Q,alpha m g^b/Q)` admits, for arbitrary fixed
  `epsilon,A>0`, a tensor expansion with rank and coefficient `l1` norm
  `O(X^epsilon)` and uniform error `O(X^(-A))`.
- `PROVED`: each separated term is
  `sum_(ell~K)T_1(ell)T_alpha(ell)`. If both sparse-exponential second moments
  have diagonal size `KDQX^epsilon`, Cauchy returns `KDQX^epsilon`, exactly
  the Cycle-87 target. The polynomial `T_alpha` is the original primal family
  with a bounded rational anchor, up to smooth shifts and sign.
- `PROVED`: if a separated bilinear term exceeds `LKDQ`, at least one factor
  has normalized second moment exceeding diagonal size by at least `L`, so
  it exports a labelled pair-collision energy witness.
- Structural no-go: the Cycle-119--123 transform followed by tensor
  separation, separate Cauchy, and diagonal second moments is norm-neutral.
  This is scoped and does not exclude correlated bilinear cancellation.
- Claim boundary: no simple-root closure, complete moment, density gain, or
  interval gain was proved.
- Artifact SHA-256:
  `d057acb6807a58be37e42a5bb1869de62e33e873dd0aebdb6033aad6b2e1f2b8`.
  Builder SHA-256:
  `91941f52702522eae07a327cf95b685febab2745bfa8b17f8339ef0b6459c937`.
- Builder runtime: wall time `0.05s`, peak RSS `18388 KiB`.
- Gate:
  `TENSOR_CAUCHY_SELF_DUAL_CORRELATED_OR_FREIMAN_WEB_OPEN`.
- Replay:
  `python3 proof/build_cycle_124_bilinear_self_duality_v1.py --check` and
  `python3 -m unittest tests/test_cycle_124_bilinear_self_duality_v1.py tests/test_cycle_seal_v1.py`.

## Cycle 125 — high-multiplicity Freiman ray web (2026-08-02)

- `PROVED`: a Cycle-92 dyadic ray class of multiplicity `M` has one injective
  reduced label `r_a=p_a/q_a` per occupied mode, with
  `|r_a-g^a|<<1/(KQ)` and `q_a<<Q/M`.
- `PROVED`: for `a1+a2=a3+a4`, the two rational products differ by
  `O((KQ)^(-1))`; if unequal, rational separation gives `>>M^4/Q^4`.
  Therefore `M^4K>>Q^3` forces
  `r_a1r_a2=r_a3r_a4` exactly.
- `PROVED`: with `M=X^mu`, the strict high-multiplicity threshold is
  `mu>(1-xi)/4`, equal to `9/100` at the lower endpoint and tending to
  `17/300` at the upper edge. The complementary branch retains the opposite
  cap.
- `PROVED`: for `R` occupied modes in a length-`D` interval,
  `E_plus(A)>=R^4/(2D-1)`. In the high branch every such additive quadruple
  is an exact multiplicative-label quadruple, so the vector
  `(nu_p(r_a))_p` is a Freiman `2`-homomorphism on `A`.
- Implication: a self-dual second-moment excess now exports exact valuation
  structure above the multiplicity threshold. Energy alone does not yet
  give the popular-difference depth and original phase anchor required by
  E16.
- Claim boundary: no low-multiplicity bound, seed realization, simple-root
  closure, complete moment, density gain, or interval gain was proved.
- Artifact SHA-256:
  `28112cb9c4e676719d1637b5ca650c49917b28ddcd2f43f04f93b54288802785`.
  Builder SHA-256:
  `c6702068f957891eb37dd6ba25074f1d802a1e610a405a4cb75b334dfbfd4b5f`.
- Builder runtime: wall time `0.05s`, peak RSS `18304 KiB`.
- Gate:
  `HIGH_MULTIPLICITY_FREIMAN_WEB_LOW_MULTIPLICITY_SEED_GATE_OPEN`.
- Replay:
  `python3 proof/build_cycle_125_freiman_ray_web_v1.py --check` and
  `python3 -m unittest tests/test_cycle_125_freiman_ray_web_v1.py tests/test_cycle_seal_v1.py`.

## Cycle 126 — common rational multipliers and chain-depth gate (2026-08-02)

- `PROVED`: for every represented nonzero difference `d`, Freiman
  multiplicativity applied to `(a+d)+b=a+(b+d)` makes
  `rho_d=r_(a+d)/r_a` independent of the edge base.
- `PROVED`: among `R` occupied modes in a length-`D` interval, some nonzero
  difference has at least `ceil(R(R-1)/(2D-2))` oriented edges.
- `PROVED`: the fixed-`d` graph is a disjoint union of paths. With `L_d`
  edges on `R` vertices, one path has at least
  `ceil(L_d/(R-L_d))` edges; `L_d>=ceil(JR/(J+1))` suffices for depth `J`.
  This quantifies why energy alone need not produce a long chain.
- `PROVED`: along a chain,
  `r_(a0+jd)=r_a0rho_d^j` exactly and
  `rho_d^J=g^(Jd)(1+O(J/(KQ)))`. For `J<=D`, the worst lower-band error is
  `X^(-28/75+o(1))`.
- Implication: the high-multiplicity branch now supplies exact rational
  recurrences with ample phase accuracy. E16 still needs sufficient chain
  depth and one vertex tied to the original packet anchor.
- Claim boundary: no long chain follows from energy alone; no seed
  realization, low-multiplicity bound, simple-root closure, complete moment,
  density gain, or interval gain was proved.
- Artifact SHA-256:
  `c228988b1549f129522a68f5b10698768ae3581b367166a9253048b67aeb92e5`.
  Builder SHA-256:
  `d7e9de1eb2dea7e2e8ddbd74af33bd66676cbcc1f0447cc0b973580f6b249968`.
- Builder runtime: wall time `0.04s`, peak RSS `18304 KiB`.
- Gate:
  `RATIONAL_RECURRENCE_COMPILED_CHAIN_DEPTH_LOW_MULTIPLICITY_OPEN`.
- Replay:
  `python3 proof/build_cycle_126_freiman_recurrence_v1.py --check` and
  `python3 -m unittest tests/test_cycle_126_freiman_recurrence_v1.py tests/test_cycle_seal_v1.py`.

## Cycle 127 — low-multiplicity logarithmic saddle and Mellin target (2026-08-02)

- `PROVED`: on multiplicity scale `M=X^mu`, reduced labels have denominator
  scale `L=Q/M` and satisfy
  `|a-(D/(2pi))log(p/q)|<<D/(KQ)`.
- `PROVED`: applying the checked order-three Huxley--Sargos theorem in `p`,
  summing over `q`, and restoring `M` gives weighted exponents
  `3/5-mu/2`, `34/45-mu-xi/3`, `5/9-mu-xi/3`, and `1/3`. The derivative term
  misses the target by `4/15-mu/2` and never closes the registered low branch.
- `PROVED`: the joint two-dimensional volume has exponent
  `14/15-xi-mu`, below target `1/3` by
  `xi+mu-3/5>=1/25`. The obstruction is not volume.
- `PROVED`: a Fejer majorant reduces volume-scale counting to the sampled
  Mellin estimate
  `sum_(h<=H)|P(hD)|^2<<HLX^epsilon`, where
  `P(t)=sum_(n~L)w(n)n^(it)` and `H=KQ/D`. This gives `O(LX^epsilon)` labels
  and hence `O(QX^epsilon)` weighted collisions.
- Structural no-go: a generic time large sieve sees span `HD` and loses the
  factor `D`; the arithmetic sampling or its logarithmic aliases must be used.
- Claim boundary: no sampled-Mellin estimate, low-multiplicity or simple-root
  closure, complete moment, density gain, or interval gain was proved.
- Artifact SHA-256:
  `0dc33bc38ac1e3edf85b98abeffcdcf162fe6c6f6f335c3cc0f9bf268d78955a`.
  Builder SHA-256:
  `cce2e02f13cb7e1eabd2b4ffed406dd8bcdc0a470e4e195c3b8eee49bcd63b0a`.
- Builder runtime: wall time `0.04s`, peak RSS `18304 KiB`.
- Gate:
  `LOW_MULTIPLICITY_MELLIN_DIAGONAL_OR_ALIAS_WEB_OPEN`.
- Replay:
  `python3 proof/build_cycle_127_low_multiplicity_log_saddle_v1.py --check` and
  `python3 -m unittest tests/test_cycle_127_low_multiplicity_log_saddle_v1.py tests/test_cycle_seal_v1.py`.

## Cycle 128 — sampled-Mellin alias profiler (2026-08-02)

- `OBSERVED`: the frozen 80-decimal profiler evaluated 18 grids from
  `D in {72,108,162}`, `xi in {16/25,7/10,23/30}`, and residual radii
  `1/K,4/K`.
- `OBSERVED`: the radius-one grids contain 16 hits on 16 occupied modes; the
  radius-four grids contain 48 hits on 48 occupied modes. Every observed ray
  has multiplicity one and no ray crosses its finite Cycle-125 threshold.
- `OBSERVED`: every reduced label is a continued-fraction convergent of
  `exp(2pi a/D)` before denominator `2Q`. All grid counts are below target
  `Q`; the largest hit/target ratio is `9/13`.
- `OBSERVED`: the longest chain for a most-popular nonzero difference has
  three edges. The data do not exhibit a finite-grid Freiman packet.
- Implication: the next low-multiplicity theorem should treat ordinary
  convergents as the bulk and large partial-quotient jumps as the labelled
  major-arc inverse. None of the observations has a proof role.
- Claim boundary: no asymptotic sparsity, continued-fraction classification,
  sampled-Mellin estimate, collision bound, density gain, or interval gain
  was proved.
- Artifact SHA-256:
  `ade56d2370748ecc7e0365e7134f11ec6775840a799f4b3e280b7d7a3ef01136`.
  Builder SHA-256:
  `915ff0ba9b5181f3a6248bd15f3dd9ba1b8ede6164144e6818f36c22ce0e7512`.
- Discovery runtime: wall time `0.10s`, peak RSS `18044 KiB`.
  Builder runtime: wall time `0.03s`, peak RSS `17920 KiB`.
- Gate:
  `MELLIN_ALIASES_PROFILED_CONTINUED_FRACTION_INVERSE_OPEN`.
- Replay:
  `python3 discovery/run_cycle_128_sampled_mellin_profiler_v1.py` and
  `python3 proof/build_cycle_128_sampled_mellin_profiler_v1.py --check`.

## Cycle 129 — continued-fraction jump compiler (2026-08-02)

- `PROVED`: for a multiplicity-`M` collision label `p/q`,
  `2q^2|g^a-p/q|<<Q/(KM^2)`. Its reciprocal has exponent
  `xi+2mu-1/3>=23/75`, so Legendre's criterion applies uniformly and `p/q`
  is a continued-fraction convergent of `g^a`.
- `PROVED`: the lower error bound
  `|g^a-p/q|>1/[q(q+q_next)]` forces `q_next>>KM`. The recurrence for
  convergent denominators then forces the next partial quotient
  `A_next>>KM^2/Q`, again with minimum exponent `23/75`.
- Implication: Cycle 128's convergent pattern is now proved and strengthened
  to a fixed-power jump. The exact remaining averaged theorem is that at most
  `(Q/M)X^epsilon` modes have such a convergent; this would close the dyadic
  class after multiplying by `M`.
- Claim boundary: no averaged jump theorem, collision or simple-root closure,
  complete moment, density gain, or interval gain was proved.
- Artifact SHA-256:
  `8be0a48187028ba3ca4ddf46a2c80d4e682207855cc86a1756b25c607de861bf`.
  Builder SHA-256:
  `6fd4beb6f5768f0da34316c0edfa369a226dcc9c17c9a3763f50687173ae2acb`.
- Builder runtime: wall time `0.04s`, peak RSS `18408 KiB`.
- Gate:
  `POWER_PARTIAL_QUOTIENT_JUMPS_AVERAGE_OPEN`.
- Replay:
  `python3 proof/build_cycle_129_continued_fraction_jump_v1.py --check` and
  `python3 -m unittest tests/test_cycle_129_continued_fraction_jump_v1.py tests/test_cycle_seal_v1.py`.

## Cycle 130 — broad continued-fraction cylinder closure (2026-08-02)

- `PROVED`: with `A0=KM^2/Q`, a convergent followed by partial quotient
  `>>A0` lies in an interval of length `O(1/(A0q^2))` about `p/q`.
- `PROVED`: consecutive targets `g^a` are separated by `asymp 1/D`. Summing
  `O(1+D|J|)` over the `O(q)` numerators and all
  `q<=q0=sqrt(D/A0)` gives `O((D/A0)X^epsilon)` occupied modes.
- `PROVED`: after restoring multiplicity, the broad-cylinder count is
  `DQ/(KM)X^epsilon`, with exponent `14/15-xi-mu`, below target `1/3` by
  `xi+mu-3/5>=1/25`.
- `PROVED`: the broad cutoff exponent
  `7/15-xi/2-mu` is uniformly at least `7/300`. The remaining denominator
  interval up to `Q/M` has exponent width `xi/2-2/15>=14/75`.
- Implication: a nonempty part of every low-multiplicity class is now closed
  unconditionally at volume scale. Only narrow cylinders
  `sqrt(DQ/(KM^2))<q<<Q/M` remain.
- Claim boundary: no narrow-cylinder, full low-multiplicity or simple-root
  closure, complete moment, density gain, or interval gain was proved.
- Artifact SHA-256:
  `07cbb17383fbc224b3a122540ce2c70ea15a01e0413a63f0b7018c2f882860ab`.
  Builder SHA-256:
  `69f263a6f1fb5fbf4ef30ffc3d83838a74fe31ff78ddd492a4baeb6208452bb2`.
- Builder runtime: wall time `0.04s`, peak RSS `18432 KiB`.
- Gate:
  `BROAD_CF_CYLINDERS_CLOSED_NARROW_ENDPOINT_OPEN`.
- Replay:
  `python3 proof/build_cycle_130_broad_cf_cylinder_v1.py --check` and
  `python3 -m unittest tests/test_cycle_130_broad_cf_cylinder_v1.py tests/test_cycle_seal_v1.py`.

## Cycle 131 — order-three denominator bridge (2026-08-02)

- `PROVED`: on `q~X^rho`, summing the checked order-three theorem over the
  denominator block and restoring `M=X^mu` gives exponents
  `mu+1/10+3rho/2`, `mu+2rho+4/45-xi/3`,
  `mu+2rho-xi/3-1/9`, and `mu+rho`.
- `PROVED`: all four meet the target through
  `rho_HS=7/45-2mu/3`. At that ceiling, the tube, ratio, and constant margins
  are positive throughout the registered lower band.
- `PROVED`: `rho_HS` exceeds the Cycle-130 broad cutoff by at least `2/225`.
  The only remaining denominator endpoint is
  `7/45-2mu/3<rho<=1/3-mu`, of width
  `8/45-mu/3>=133/900`.
- Implication: classical order three becomes useful after the continued-
  fraction denominator split, although it could not close the unsplit class.
- Claim boundary: no endpoint-denominator, full low-multiplicity or
  simple-root closure, complete moment, density gain, or interval gain was
  proved.
- Artifact SHA-256:
  `1fa3645c6cf6c59abc35604de076412cf413593ea49d5e5a214f9dee0aa99e55`.
  Builder SHA-256:
  `31542c9734ac4e7b9c6ec10896a4de46b3a57a2d368969490c20691118da27d7`.
- Builder runtime: wall time `0.04s`, peak RSS `18408 KiB`.
- Gate:
  `DENOMINATORS_CLOSED_TO_7_45_MINUS_2MU_3_ENDPOINT_OPEN`.
- Replay:
  `python3 proof/build_cycle_131_order_three_denominator_bridge_v1.py --check` and
  `python3 -m unittest tests/test_cycle_131_order_three_denominator_bridge_v1.py tests/test_cycle_seal_v1.py`.

## Cycle 132 — unimodular endpoint lift (2026-08-02)

- `PROVED`: if `p/q` is a collision convergent and `P/R` is its next
  convergent, then `s=Pq-pR` is `+1` or `-1`,
  `R=-s p^{-1} (mod q)`, and
  `1/[q(q+R)]<|g^a-p/q|<1/(qR)`.
- `PROVED`: for fixed `p/q` and orientation, consecutive denominator shells
  in a dyadic block `R~S` tile. Their union has logarithmic-mode width
  `O(D/(qS))`, so for `q~N` the natural bandwidth is `H=NS/D` and the
  candidate-label count is `O(N^2)`.
- `PROVED`: `R>>KQ/N` makes the restored zeroth mode `MDN/S`. Across the
  full Cycle-131 endpoint its exponent is at most `14/15-xi-mu`, below the
  target `1/3` by `xi+mu-3/5>=1/25`.
- `PROVED`: the remaining sufficient estimate is the nonzero logarithmic
  Fourier norm
  `H^{-1} sum_{1<=|h|<=H}|sum_V e(hD log(p/q)/(2pi))| << Q/M`.
  It is not proved.
- `PROVED`: failure produces a rational-ray cluster with edge tolerance
  `1/(NS)<=1/(KQ)`. Every vertex retains the consecutive matrix
  `[[P,p],[R,q]]` of determinant `+1` or `-1`; this is compatible with the
  Cycle-125/126 energy and recurrence compilers.
- Implication: there is no remaining endpoint volume obstruction. The live
  obstruction is modular clustering with an oriented unimodular label.
- Claim boundary: no nonzero Fourier norm, endpoint, full low-multiplicity or
  simple-root closure, complete moment, density gain, or interval gain was
  proved.
- Artifact SHA-256:
  `aeab0475962728918ab08c2b78e87dcef4bed7840c57e376557bcdcdfb434cee`.
  Builder SHA-256:
  `66a074daf5d7882709ca44e4d36c65c860229f641cb4ba513e420d47cfd0a13d`.
- Builder runtime: wall time `0.04s`, peak RSS `18548 KiB`.
- Gate:
  `ENDPOINT_VOLUME_CLOSED_DETERMINANT_CLUSTER_NORM_OPEN`.
- Replay:
  `python3 proof/build_cycle_132_unimodular_endpoint_lift_v1.py --check` and
  `python3 -m unittest tests/test_cycle_132_unimodular_endpoint_lift_v1.py tests/test_cycle_seal_v1.py`.

## Cycle 133 — determinant-cluster energy compiler (2026-08-02)

- `PROVED`: an additive mode quadruple in a Cycle-132 block has rational-
  label product error `O(1/(NS))`, while distinct products have separation
  `>>N^(-4)`. Hence `S>>N^3`, equivalently `tau>3rho`, forces exact
  multiplicative rational-label equality.
- `PROVED`: since `S>>KQ/N`, exactness is automatic for
  `rho<(xi+1/3)/4`. This extends the Cycle-131 exact structured range by at
  least `79/900` in exponent.
- `PROVED`: the nonexact width between this ceiling and `rho=1/3-mu` is
  exactly `(1-xi)/4-mu`; it vanishes at maximal low multiplicity. Equality at
  the exponent boundary is not included.
- `PROVED`: at the excessive threshold `|A|=Q/M`, additive energy is at
  least `|A|^4/(2D-1)`, of exponent `11/15-4mu`. In the exact region, every
  prime valuation of the rational labels is a Freiman `2`-homomorphism.
- `PROVED`: the consecutive matrices `U_a=[[P_a,p_a],[R_a,q_a]]` yield
  integral transitions `T_(a,b)=U_b U_a^(-1)` satisfying the exact cocycle
  law and `det T_(a,b)=s_a s_b`.
- `PROVED` scoped data-class no-go (licensed explicitly by Cycle 134): energy,
  determinant labels, and the cocycle identity alone leave shear freedom and
  do not supply repeated-difference transition concentration. A phase-
  anchored edge invariant is needed for Cycle-126 chain depth.
- Claim boundary: no transition concentration, recurrence seed, endpoint or
  lower-moment closure, density gain, or interval gain was proved.
- Artifact SHA-256:
  `c837c041cc796ec2553a97074d66707ad6fb339bcc6530beddc242eb06d56427`.
  Builder SHA-256:
  `aa6347bb04b3cb48d1522ce86981f410b58e9b7aa46b4fc4aa95aace151c0083`.
- Builder runtime: wall time `0.04s`, peak RSS `18420 KiB`.
- Gate:
  `EXACT_DETERMINANT_FREIMAN_SUBRANGE_TRANSITION_CONCENTRATION_OPEN`.
- Replay:
  `python3 proof/build_cycle_133_determinant_cluster_energy_v1.py --check` and
  `python3 -m unittest tests/test_cycle_133_determinant_cluster_energy_v1.py tests/test_cycle_seal_v1.py`.

## Cycle 134 — transition entropy and the tail anchor (2026-08-02)

- `PROVED`: for a fixed primitive column `(p,q)` and sign `s`, all solutions
  of `Pq-pR=s` are `(P0+tp,R0+tq)`. Equivalently, every lift is a right
  integral shear of one base unimodular matrix.
- `PROVED`: a nonempty interior dyadic block `q~N`, `R~S` contains order
  `S/N` formal lifts. The entropy exponent is `tau-rho`; at the full endpoint
  its minimum is `xi+2mu-1/3>=23/75`.
- `PROVED`: if `delta=|g^a-p/q|`, the actual consecutive shell defines
  `theta=(1/(q delta)-R)/q in (0,1)` and recovers
  `delta=1/[q(R+theta q)]` exactly.
- `PROVED` scoped no-go: rational labels, determinant signs, and dyadic sizes
  alone retain fixed-power shear entropy, so a determinant-only compiler
  cannot prove subpower transition concentration. It must retain `theta`,
  the signed residual, or equivalent full phase data.
- Claim boundary: this does not obstruct the phase-coupled operator and
  proves no transition concentration, recurrence seed, endpoint, moment,
  density gain, or interval gain.
- Artifact SHA-256:
  `02141cd02825052f2de39cb1edff0499f9d073c1f7c00e748eaa7d3f98722202`.
  Builder SHA-256:
  `cdeecbe1e412f4c0d771f30ca8b42f559ab9b0e7a8b941ce7db9dd8d890117ed`.
- Builder runtime: wall time `0.04s`, peak RSS `18384 KiB`.
- Gate:
  `DETERMINANT_ONLY_SHEAR_ENTROPY_TAIL_PHASE_REQUIRED`.
- Replay:
  `python3 proof/build_cycle_134_transition_entropy_v1.py --check` and
  `python3 -m unittest tests/test_cycle_134_transition_entropy_v1.py tests/test_cycle_seal_v1.py`.

## Cycle 135 — tail-coupled transition operator (2026-08-02)

- `PROVED`: writing `Y=1/(q|g^a-p/q|)` and `R=r+tq`, the shell condition is
  `R<Y<R+q`. Consecutive shear shells tile exactly, leaving only the two
  outer boundaries of a complete block.
- `PROVED` scoped no-gain: Fourier projection in `theta=(Y-R)/q` alone only
  cancels those internal boundaries and reproduces the Cycle-132
  logarithmic-center discrepancy. It gives no independent transition-
  entropy saving.
- `PROVED`: for an edge `b=a+d`, the two exact tails obey
  `x_b-g^d x_a=g^d s_a/[q_a(R_a+theta_a q_a)]
  -s_b/[q_b(R_b+theta_b q_b)]`.
- `PROVED`: the normalized residual
  `Omega_d(a)=NS(x_(a+d)-g^d x_a)` has tail variation `N/S`; its natural
  resolving frequency is `L=S/N`, equivalently raw residual frequency
  `S^2`.
- `CONJECTURED`: the next analytic target is the paired-tail diagonal norm
  `sum_(|ell|<=L)|sum_(a in E_d)w_a e(ell Omega_d(a))|^2
  <<L|E_d|X^epsilon`.
- Claim boundary: no paired-tail bound, transition concentration, recurrence
  seed, endpoint, moment, density gain, or interval gain was proved.
- Artifact SHA-256:
  `fa5dcd292a3076e865ffaf7b40f7bef595b803688c37bcc6df7d65be83a76464`.
  Builder SHA-256:
  `8c888b2bcd2c3f3005a85fad78087838973aa4a95c22eccbec27749bbc1e08e8`.
- Builder runtime: wall time `0.04s`, peak RSS `18304 KiB`.
- Gate:
  `TAIL_MARGINAL_SELF_DUAL_PAIRED_EDGE_NORM_OPEN`.
- Replay:
  `python3 proof/build_cycle_135_tail_coupled_transition_v1.py --check` and
  `python3 -m unittest tests/test_cycle_135_tail_coupled_transition_v1.py tests/test_cycle_seal_v1.py`.

## Cycle 136 — common-multiplier scalar dichotomy (2026-08-02)

- `PROVED`: in the strict exact region `S>>N^3`, every edge of one nonzero
  represented difference `d` shares a reduced rational multiplier
  `r_d=x_(a+d)/x_a`.
- `PROVED`: the paired residual factorizes exactly as
  `x_(a+d)-g^d x_a=(r_d-g^d)x_a`.
- `PROVED`: with `kappa_d=NS(r_d-g^d)` and `L=S/N`, the separated rational-
  label large sieve bounds the paired second moment by
  `(L+N^2/|kappa_d|)|E_d|X^epsilon`. Thus the diagonal target holds unless
  `|kappa_d|<<N^3/S`.
- `PROVED`: an exceptional multiplier satisfies
  `|r_d-g^d|<<N^2/S^2`. Its reduced denominator is `<<N^2`; Legendre's
  criterion applies with margin `S^2/N^6`.
- `PROVED`: every exception is a convergent of `g^d` whose next denominator
  is `>>S^2/N^4` and whose next partial quotient is `>>S^2/N^6`.
- Implication: the paired-tail norm is closed away from one explicit scalar
  class per difference. The remaining task is an edge-weighted average of
  power partial-quotient jumps across `g^d`.
- Claim boundary: no averaged exclusion of exceptional multipliers, full
  paired norm, endpoint, moment, density gain, or interval gain was proved.
- Artifact SHA-256:
  `d3af0383df6754f59fb0515c0f0811e116c772b441868d1ad41c13360cfcf52f`.
  Builder SHA-256:
  `0f12ce1d922b1e483c40cdbb48e5eebff8c1934e6074c427fb037b7008b9861b`.
- Builder runtime: wall time `0.04s`, peak RSS `18412 KiB`.
- Gate:
  `PAIRED_NORM_SCALAR_DICHOTOMY_EXCEPTIONAL_MULTIPLIER_AVERAGE_OPEN`.
- Replay:
  `python3 proof/build_cycle_136_common_multiplier_scalar_v1.py --check` and
  `python3 -m unittest tests/test_cycle_136_common_multiplier_scalar_v1.py tests/test_cycle_seal_v1.py`.

## Cycle 137 — exceptional-multiplier weighted average (2026-08-02)

- `PROVED`: exceptional multipliers lie in intervals of width `N^2/S^2`
  around `g^d` and have height at most `N^2`, giving
  `B_exc<<X^epsilon(N^4+DN^6/S^2)` exceptional differences.
- `PROVED`: on the edge class `|E_d|~J`, the correct diagonal allowance is
  `B_exc J^2<<(Q/M)^2X^epsilon`, not an unweighted difference count.
- `PROVED`: writing `J=X^j`, the elementary average closes exactly when
  `j<min(1/3-mu-2rho,1/30-mu+tau-3rho)`.
- `PROVED`: at `(xi,mu,rho,tau)=(16/25,0,7/45,184/225)`, every fixed
  `j<1/45` closes. This is a nonempty edge-weighted subrange.
- `PROVED` structural obstruction: outside that range, the first loss across much of
  the upper exact region is the `N^4` Farey-discretization term rather than
  the volume term.
- Claim boundary: no high-edge or full exceptional average, paired norm,
  endpoint, moment, density gain, or interval gain was proved.
- Artifact SHA-256:
  `305d9dfe39e0f3c2b18d7969eecc2e6b8f898aefe8565f03bcd7925cf4cf4359`.
  Builder SHA-256:
  `4e2c2f62b550b2514dcf42f8681bce0798c3042a04614bb63b5863a2e63a734e`.
- Builder runtime: wall time `0.04s`, peak RSS `18396 KiB`.
- Gate:
  `LOW_EDGE_EXCEPTION_AVERAGE_CLOSED_FAREY_DISCRETIZATION_OPEN`.
- Replay:
  `python3 proof/build_cycle_137_exceptional_multiplier_average_v1.py --check` and
  `python3 -m unittest tests/test_cycle_137_exceptional_multiplier_average_v1.py tests/test_cycle_seal_v1.py`.

## Cycle 138 — multiplier-fiber height descent (2026-08-02)

- `PROVED`: for coprime pairs `(A,B)` and `(p,q)`, the cancellation divisor
  satisfies `gcd(Ap,Bq)=gcd(A,q)gcd(B,p)`.
- `PROVED`: a compact reduced multiplier of height `H` has at most
  `N^2 H^(-1)X^epsilon` primitive realizations `x -> rx` with both labels at
  height `N`.
- `PROVED`: an edge class `|E_d|~J` therefore forces
  `height(r_d)<<N^2/J X^epsilon`. The exceptional count improves to
  `N^4/J^2+DN^6/(J^2S^2)`.
- `PROVED`: after restoring the coherent cost `J^2`, edge multiplicity
  cancels exactly. Every `J` meets the exceptional-average diagonal budget
  when `rho<1/6-mu/2` and `tau-3rho>mu-1/30`.
- `PROVED`: the new all-multiplicity ceiling exceeds the Cycle-131 ceiling by
  `1/90+mu/6>=1/90`.
- Implication: low-edge closure has become all-edge closure on a strict
  regional band. The remaining upper Farey range requires denominator
  curvature or a high-height multiplier inverse.
- Claim boundary: no full paired norm, endpoint, moment, density gain, or
  interval gain was proved.
- Artifact SHA-256:
  `d1eacac468da23239faa829ec6fb509dbba083dafbd2855ee55b84f8174029a6`.
  Builder SHA-256:
  `8df8ac8e7276542978d9edc0af40f7425f3ad576cca78d0c7c4e5d2c7ce7fefd`.
- Builder runtime: wall time `0.04s`, peak RSS `18304 KiB`.
- Gate:
  `ALL_EDGE_MULTIPLICITIES_TO_1_6_MINUS_MU_2_UPPER_FAREY_RANGE_OPEN`.
- Replay:
  `python3 proof/build_cycle_138_multiplier_fiber_height_v1.py --check` and
  `python3 -m unittest tests/test_cycle_138_multiplier_fiber_height_v1.py tests/test_cycle_seal_v1.py`.

## Cycle 139 — multiplier-denominator curvature (2026-08-02)

- `PROVED`: with descended height `H=N^2/J` and tube
  `delta=DN^2/S^2`, the checked order-three theorem gives pre-weight terms
  `D^(1/6)H^(3/2)`, `H^2delta^(1/3)`,
  `H^2(delta/D)^(1/3)`, and `H`.
- `PROVED`: after restoring `J^2`, their exponents are
  `1/10+3rho+j/2`, `1/5+14rho/3-2tau/3`,
  `14rho/3-2tau/3`, and `2rho+j`.
- `PROVED`: the derivative and constant terms require respectively
  `j<17/15-4mu-6rho` and `j<2/3-2mu-2rho`.
- `PROVED`: low-edge closure extends through
  `rho<17/90-2mu/3`. Its gain beyond the Cycle-138 all-edge ceiling is
  `1/45-mu/6`, uniformly at least `13/1800`; all secondary margins remain
  positive there.
- `PROVED` structural limitation: order three does not extend the all-edge frontier,
  because the derivative term grows with `j/2` and the constant term with
  `j`.
- Claim boundary: no high-edge or all-multiplicity extension, full paired
  norm, endpoint, moment, density gain, or interval gain was proved.
- Artifact SHA-256:
  `7f78a648ef0126918ab4487c9947d84fc04c51bdd7fe459d9b04ef7ab55776ca`.
  Builder SHA-256:
  `8a992e05c2afc5806b355e549e237afb1fa64d4c195b192a86240170be9f98cc`.
- Builder runtime: wall time `0.04s`, peak RSS `18304 KiB`.
- Gate:
  `LOW_EDGE_CURVATURE_TO_17_90_MINUS_2MU_3_HIGH_EDGE_OPEN`.
- Replay:
  `python3 proof/build_cycle_139_multiplier_curvature_v1.py --check` and
  `python3 -m unittest tests/test_cycle_139_multiplier_curvature_v1.py tests/test_cycle_seal_v1.py`.

## Cycle 140 — multiplier-fiber saturation inverse (2026-08-02)

- `PROVED`: writing the actual multiplier height as `H=N^2/(JZ)`,
  `Z=X^zeta`, changes the weighted discretization and volume exponents to
  `4rho-2zeta` and `3/5+6rho-2tau-2zeta`.
- `PROVED`: a block closes when `zeta` exceeds both
  `2rho-1/3+mu` and `3rho-tau+mu-1/30`. Survivors therefore have a quantified
  fiber-saturation deficit.
- `PROVED`: the actual height amplifies the Legendre margin to
  `2tau+2j+2zeta-6rho`, the next-denominator exponent to
  `2tau-4rho+j+zeta`, and the next-partial-quotient exponent to
  `2tau-6rho+2j+2zeta`.
- `PROVED`: one cross-gcd class `u|A`, `v|B`, `uv~H` carries at least
  `JX^(-epsilon)` edges, on which
  `x_a=vp0/(uq0)` and
  `x_(a+d)=(A/u)p0/((B/v)q0)`. Original orientations, next-convergent
  matrices, and signed tails remain attached.
- `PROVED` conditional interpretation: when `zeta=o(1)`, this class occupies
  an `X^(-o(1))` fraction of its capacity and is a genuine saturated divisor
  seed. The theorem does not force subpower slack for every survivor.
- Claim boundary: no recurrence, full paired norm, endpoint, moment, density
  gain, or interval gain was proved.
- Artifact SHA-256:
  `a02aa56b0a79c95baff74e0088b08caaf5ad4d9c5e956eec4dd1da62c140f5d8`.
  Builder SHA-256:
  `a7d1b1406d1c83e8e33b005e7783c951e22aa49c376a83e6423f209f68f35442`.
- Builder runtime: wall time `0.04s`, peak RSS `18412 KiB`.
- Gate:
  `HEIGHT_SLACK_CLOSED_DIVISOR_FIBER_SEED_RECURRENCE_OPEN`.
- Replay:
  `python3 proof/build_cycle_140_fiber_saturation_inverse_v1.py --check` and
  `python3 -m unittest tests/test_cycle_140_fiber_saturation_inverse_v1.py tests/test_cycle_seal_v1.py`.

## Cycle 141 — divisor-seed recurrence correction (2026-08-02)

- `PROVED`: in one class, the rational input/output columns are
  `(vp0,uq0)^T` and `((A/u)p0,(B/v)q0)^T`.
- `PROVED` structural no-go: if one linear transition maps two distinct core
  ratios between those columns, it is forced to be
  `diag(A/(uv),B/(uv))`. Integral unimodularity then gives
  `A=B=uv=1`, hence `d=0`. For nonzero `d`, a fixed `GL_2(Z)` transition
  labels at most one edge.
- `PROVED`: a class with `L` edges on `R` vertices remains a path forest. Its
  longest guaranteed chain has `ceil(L/(R-L))` edges; it has at least
  `max(0,2L-R)` length-two starts, and depth `k` requires
  `L>=ceil(kR/(k+1))`.
- `PROVED`: fiber saturation compares `L` with `N^2/H`, while continuation
  compares `L` with `R`. Neither ratio controls the other.
- `PROVED` correction: equal transition matrices must not be used as the recurrence
  invariant. The replacement is the changing-color continuation profile,
  retaining signed tails on consecutive edges.
- Claim boundary: no positive continuation density, recurrence, full paired
  norm, endpoint, moment, density gain, or interval gain was proved.
- Artifact SHA-256:
  `eb030677c760ea337daadaf326bfec568f5328e5d87b0d820834753309ef11a8`.
  Builder SHA-256:
  `295fd5cacdfdb256749cb2a08ff7a8d48a221b948365a27b78f4adc32cffb253`.
- Builder runtime: wall time `0.04s`, peak RSS `18304 KiB`.
- Gate:
  `TRANSITION_REPETITION_IMPOSSIBLE_CONTINUATION_PROFILE_OPEN`.
- Replay:
  `python3 proof/build_cycle_141_divisor_seed_recurrence_v1.py --check` and
  `python3 -m unittest tests/test_cycle_141_divisor_seed_recurrence_v1.py tests/test_cycle_seal_v1.py`.

## Cycle 142 — changing-color valuation walk (2026-08-02)

- `PROVED`: for successive reduced labels under `A/B`, the exact update is
  `z_t=gcd(Ap_t,Bq_t)=gcd(A,q_t)gcd(B,p_t)`,
  `p_(t+1)=Ap_t/z_t`, and `q_(t+1)=Bq_t/z_t`.
- `PROVED`: primewise divisor colors are deterministic functions of the
  current numerator/denominator valuations; they are not an independent
  recurrence parameter.
- `PROVED`: Cycle 78's rational-height bound applies to every complete chain,
  giving depth `O(log N)` for each nontrivial fixed multiplier.
- `PROVED` scoped saturation: a path forest forces a forbidden chain only
  when its edge density is `1-O(1/log N)`. Therefore the divisor/continuation
  compiler yields no fixed-power gain without an independent near-complete
  density theorem.
- Implication: sparse path components must return to the paired Fourier norm,
  retaining component starts, `r_d-g^d`, and signed tails. Analytic
  cancellation across components remains open.
- Claim boundary: no paired norm, endpoint, moment, density gain, or interval
  gain was proved.
- Artifact SHA-256:
  `7533463448df762879b9113901489f584b8ae76d47ca9b51a046b9ab984aab76`.
  Builder SHA-256:
  `9ec93ce68a483545562581f7ff58a4a59fda64c36a1e895882a2672c216f7d8a`.
- Builder runtime: wall time `0.05s`, peak RSS `17920 KiB`.
- Gate:
  `RECURRENCE_LOG_DEPTH_SATURATION_SPARSE_COMPONENT_NORM_OPEN`.
- Replay:
  `python3 proof/build_cycle_142_changing_color_walk_v1.py --check` and
  `python3 -m unittest tests/test_cycle_142_changing_color_walk_v1.py tests/test_cycle_seal_v1.py`.

## Cycle 143 — sparse-path Fourier compiler (2026-08-02)

- `PROVED`: decomposing a fixed-difference graph into its `O(log N)` paths
  and layering by path position gives separated height-`N` rational labels
  on every layer.
- `PROVED`: the layerwise large sieve plus Cauchy gives
  `M2<<Lambda(L+N^2/|kappa_d|)sum|w_a|^2`, with
  `Lambda=O(log N)=X^(o(1))`.
- `PROVED` scoped self-duality: path decomposition leaves the Cycle-136
  power threshold `|kappa_d|>>N^3/S` unchanged.
- `PROVED` scoped sharpness: arbitrary one-sign weights remain coherent when
  `L|kappa_d|` is small and give second moment of order `L|E_d|^2`. This is
  not yet a saturator for the actual coefficient vector.
- `PROVED`: the first coefficient-sensitive invariants are the signed moments
  `M_m(d)=sum_a w_a x_a^m`, beginning with `M_0(d)=sum_a w_a`.
- Claim boundary: the actual signed moments remain unbounded; no paired norm,
  endpoint, complete moment, density gain, or interval gain was proved.
- Artifact SHA-256:
  `364083fc16cfa7591afd69dd3df6c83c292f4efcea9f1077db3531ee61330937`.
  Builder SHA-256:
  `d67dec7bfa961a2e1932dd04b0bfca971fc24b04b12cf9b9653060197eb85442`.
- Builder runtime: wall time `0.04s`, peak RSS `18432 KiB`.
- Gate:
  `SPARSE_PATH_NORM_SELF_DUAL_SIGNED_MOMENT_HIERARCHY_OPEN`.
- Replay:
  `python3 proof/build_cycle_143_sparse_path_fourier_v1.py --check` and
  `python3 -m unittest tests/test_cycle_143_sparse_path_fourier_v1.py tests/test_cycle_seal_v1.py`.

## Cycle 144 — actual edge-coefficient interface (2026-08-02)

- `PROVED`: if
  `T(ell)=sum_j c_j(ell)e(-ell z_j)`, an oriented collision edge
  `(j,j')` has coefficient
  `c_(j')(ell) conjugate(c_j(ell))`; this coefficient generally depends on
  `ell`.
- `PROVED` correction: Cycle 124 records coefficient functions
  `w_alpha(a,n;ell)`, but the Cycle-132--134 inverse retains only support,
  multiplicity, rational centers, next-convergent matrices, orientations,
  and tails. No sealed coefficient-preserving pushforward identifies these
  functions with the scalar `w_a` introduced in Cycle 135.
- `PROVED`: Cycle 143's scalar signed moments are exact for a
  frequency-independent scalar edge vector, but are not yet identified with
  the actual alias coefficients. The actual formal hierarchy is
  `M_m(d;ell)=sum_e c_(e,+)(ell)conjugate(c_(e,-)(ell))x_e^m`.
- `PROVED`: before tensor separation, all displayed algebraic/Jacobian
  factors in the Cycle-123 leading amplitude are positive and its only
  explicit stationary phase is `e(1/8)`. Any real smooth symbol nonzero at
  an interior point has a smaller fixed-sign chart, so the saddle itself
  forces no zeroth-moment cancellation.
- `PROVED`: Cycle 122's global continuous-moment vanishing eliminates the
  zero Poisson mode; it supplies no vanishing identity for the surviving
  nonzero-alias edge moments.
- Implication: the minimal next object is the complex, frequency-dependent
  measure
  `nu_(d,ell)=sum_e c_(e,+)(ell)conjugate(c_(e,-)(ell))delta_e`, retaining
  tensor, anchor, orientation, and tail labels. The next theorem must
  transport it through a weighted collision inverse or prove a controlled
  factorization to one scalar vector.
- Claim boundary: no actual signed-moment estimate, coefficient-faithful
  saturator, paired norm, endpoint, complete moment, density gain, or interval
  gain was proved.
- Artifact SHA-256:
  `c8260b7152a02b9d2b61ee1f60340b79c4eea40542311c64057af88c7a5ebf3c`.
  Builder SHA-256:
  `71049cd6c0924889ac846ca9314e1f2f2f90f05fb242b8474c83e49ce1d3a59b`.
- Builder runtime: wall time `0.04s`, peak RSS `17920 KiB`.
- Gate:
  `COEFFICIENT_PRESERVING_WEIGHTED_COLLISION_INVERSE_OPEN`.
- Replay:
  `python3 proof/build_cycle_144_actual_edge_coefficient_v1.py --check` and
  `python3 -m unittest tests/test_cycle_144_actual_edge_coefficient_v1.py tests/test_cycle_seal_v1.py`.

## Cycle 145 — vector-valued autocorrelation compiler (2026-08-02)

- `PROVED`: for edge coefficient functions `C_e(ell)`, the exact moments are
  vectors `M_m(ell)=sum_e C_e(ell)x_e^m`. If `D_ell` denotes multiplication
  by `ell`, the paired sum has the componentwise expansion
  `F=sum_(m<R)(2pi i kappa)^m D_ell^m M_m/m!+Rem_R`.
- `PROVED`: when `|x_e|<=B`, `|ell|<=L`, and
  `z=2pi|kappa|LB`, the remainder satisfies
  `||Rem_R||_2<=exp(z)z^R/R! ||(sum_e|C_e(ell)|)_ell||_2`.
  Thus every higher moment retains its exact `ell^m` multiplier.
- `PROVED`: for a complete mode-difference class, the zeroth moment is the
  autocorrelation
  `R_ell(d)=sum_a c_(a+d)(ell)conjugate(c_a(ell))`, and
  `sum_d R_ell(d)e(-d theta)=|sum_a c_a(ell)e(-a theta)|^2>=0`.
- `PROVED`: the actual continued-fraction inverse inserts a selection mask
  `chi_(a,d,ell)`. An arbitrary mask destroys the complete positive-definite
  identity; it survives only after a separately proved Gram or convolution
  factorization of `chi`.
- `PROVED` adverse local model: on any block where the atom coefficients
  have one common phase and nonnegative magnitudes, every unweighted selected
  zeroth product is nonnegative. Smooth local amplitude alone cannot supply
  the needed cancellation.
- Implication: the live analytic object is the vector-valued selected
  autocorrelation for the actual collision/tail mask. The next engine should
  reconstruct its signed high-pass kernel rather than replace it by a
  positive incidence majorant.
- Claim boundary: no selected-autocorrelation saving, paired norm, endpoint,
  complete moment, density gain, or interval gain was proved.
- Artifact SHA-256:
  `5989739fe7de6e80782e98d38b60226b0eb5aa95e630a10587427dc12a77d41a`.
  Builder SHA-256:
  `a386c7fe79ccb9d5cb4de2143ebf9bcbef679a169ffb471fdcb7abca5d715918`.
- Builder runtime: wall time `0.04s`, peak RSS `17920 KiB`.
- Gate:
  `ARITHMETIC_SELECTION_MASK_AUTOCORRELATION_OPEN`.
- Replay:
  `python3 proof/build_cycle_145_vector_autocorrelation_v1.py --check` and
  `python3 -m unittest tests/test_cycle_145_vector_autocorrelation_v1.py tests/test_cycle_seal_v1.py`.

## Cycle 146 — balanced high-pass mask (2026-08-02)

- `PROVED`: the exact Cycle-87 pair kernel is
  `Psi_K(t)=sum_k U(k/K)e(kt)=K sum_m hat U(K(m-t))`, with circle mean
  `U(0)=0` because the frequency block is supported away from zero.
- `PROVED` conditional Gram form: under the additional standard choice
  `U>=0` (not frozen by Cycle 87), the pair quadratic form is
  `sum_k U(k/K)|sum_j c_j e(kz_j)|^2`; its missing `k=0` feature is exactly
  the removed volume mode.
- `PROVED`: `Re Psi_K` has equal positive and negative `L1` mass. The
  negative halo is part of the cancellation mechanism, not a remainder.
- `PROVED` scoped majorant cost: any nonnegative replacement of height one
  on a circle core of width `w` has mean at least `w`; at the natural
  `w~1/K` scale, multiplication by `K` restores a constant zero-mode cost per
  pair.
- `PROVED`: if a deterministic partition into `P` arithmetic cells is made
  before absolute values and its real signed cell contributions sum to `E`,
  one cell has contribution at least `E/P`. The factor `P` must be charged.
- `PROVED`: this signed cell can retain the original Fourier frequency,
  oriented correlation coefficient, phase residual, rational centers,
  next-convergent matrices, orientations, anchors, and tails without changing
  the partition equality.
- Implication: the next step is one actual signed-cell estimate with a
  minimal, affordable hierarchy. Positive incidence and further interface
  compilers are not the active route.
- Claim boundary: no arithmetic-cell estimate, paired norm, endpoint,
  complete moment, density gain, or interval gain was proved.
- Artifact SHA-256:
  `f78ab979c956af5932e5998d635d0844156fa9158169bb4294f453bd6f8f6d28`.
  Builder SHA-256:
  `a75642eda982618c70b8dd7a41046a99b98364c81b1178d71a558dcfb35ff2cc`.
- Builder runtime: wall time `0.04s`, peak RSS `17920 KiB`.
- Gate:
  `SIGNED_HIGH_PASS_CELL_ENTROPY_OPEN`.
- Replay:
  `python3 proof/build_cycle_146_balanced_highpass_mask_v1.py --check` and
  `python3 -m unittest tests/test_cycle_146_balanced_highpass_mask_v1.py tests/test_cycle_seal_v1.py`.

## Cycle 147 — strict-core signed-cell estimate (2026-08-02)

- `PROVED`: for an additionally chosen nonnegative dyadic cutoff supported on
  `0<k<=bK`, every endpoint residual
  `||t_e||<=1/(12bK)` has Fourier phase of absolute argument at most `pi/6`.
- `PROVED`: if all atom coefficients lie within phase `phi` of one common
  ray, the oriented products lie within `2phi`. For `phi<=pi/12`, the real
  signed strict-core contribution is at least one half of the total frequency
  weight times the pair-magnitude mass.
- `PROVED` actual-chart scope: Cycle 123's leading coefficient has common
  phase `e(1/8)` and positive algebraic/Jacobian factors. Any real smooth
  symbol nonzero at an interior point has a smaller fixed-sign chart fitting
  the theorem with `phi=0`.
- `PROVED`: for exact common-phase coefficients, the kernel remains
  nonnegative throughout `||t||<=1/(4bK)`. A negative contribution capable
  of cancelling the strict core must lie outside this collar, which is three
  times wider than the frozen core.
- Structural implication: an isolated continued-fraction endpoint cell is
  positively coherent and cannot supply its own signed saving. The next
  analytic unit must retain a coefficient-faithful core--halo bundle.
- Claim boundary: no lower bound was proved for the strict chart's share of
  the original excessive quadratic form. No paired norm, endpoint, complete
  moment, density gain, or interval gain was proved.
- Artifact SHA-256:
  `95671bb99fb4f070b15e8c8210d7c69a6f9c4241d6ec5bd17434a3ab1e5116b8`.
  Builder SHA-256:
  `600fdf02f96fa3d8428e1e82d9c18ef62e458782055fbfabcab475b15aa04c4b`.
- Builder runtime: wall time `0.04s`, peak RSS `18048 KiB`.
- Gate:
  `COEFFICIENT_FAITHFUL_CORE_HALO_BUNDLE_OPEN`.
- Replay:
  `python3 proof/build_cycle_147_strict_core_signed_cell_v1.py --check` and
  `python3 -m unittest tests/test_cycle_147_strict_core_signed_cell_v1.py tests/test_cycle_seal_v1.py`.

## Cycle 148 — endpoint major-arc comb (2026-08-02)

- `PROVED`: for a bounded reduced rational anchor `c0=A/B`, the reduced
  denominator `h` of `c0p/q` satisfies `q/A<=h<=Bq`; bounded anchors preserve
  the endpoint denominator exponent.
- `PROVED`: on a strict endpoint band
  `|c0g^a-r_a/h_a|<<1/(KQ)`, `h_a~N<=QX^(-delta)`, exact Poisson summation in
  the length-`Q` coefficient variable makes every nonmultiple
  `h_a` not dividing `k` smaller than `Q(Q/N)^(-J)` for arbitrary fixed `J`.
- `PROVED`: when `h_a|k`, the rational phase is integral and the strict
  endpoint buffer puts the residual coefficient sum in a common phase wedge,
  giving real part `>>Q` for positive interior-chart weights.
- `PROVED`: for any such endpoint mode set `C`, the divisor-incidence comb
  satisfies
  `sum_(k~K)|T_C(k)|^2>>KQ^2N^(-1)sum_(a in C)u_a^2`.
  Its diagonal energy is `asymp KQ sum_a u_a^2`, so the isolated endpoint
  excess is exactly `Q/N=X^(1/3-rho+o(1))`.
- `PROVED` structural no-go: decomposing into strict endpoint operators and
  summing their second-moment norms cannot reach diagonal strength in any
  fixed `rho<1/3` band. Cancellation must occur between endpoint combs or
  through the full common coefficient vector before endpoint norms are taken.
- Claim boundary: no endpoint class was proved to carry target-sized mass,
  and cross-cell cancellation in the full fixed polynomial was not excluded.
  No full second moment, endpoint, complete moment, density gain, or interval
  gain was proved.
- Artifact SHA-256:
  `9549454a2cefd60d37673ecd9b7f012bb8d18bcb24ff7f439c99005e99604cbb`.
  Builder SHA-256:
  `2f7a09acc2c38f857b92a476006b34a2d2754eccae3cd050857e97f0038a9061`.
- Builder runtime: wall time `0.05s`, peak RSS `18396 KiB`.
- Gate:
  `CROSS_ENDPOINT_COMB_CANCELLATION_OR_INVERSE_OPEN`.
- Replay:
  `python3 proof/build_cycle_148_endpoint_major_arc_comb_v1.py --check` and
  `python3 -m unittest tests/test_cycle_148_endpoint_major_arc_comb_v1.py tests/test_cycle_seal_v1.py`.

## Cycle 149 — target-mass comb anti-alignment inverse (2026-08-02)

- `PROVED`: a strict endpoint population of `R_C` modes has comb-to-global
  diagonal ratio `Lambda=(R_C/D)(Q/N)`. Its exact critical occupation is
  `R_C/D=N/Q`.
- `PROVED`: writing the full fixed polynomial as `F=C+R`, if
  `||F||_2^2<=C_diag KDQ` but `||C||_2^2>=Lambda KDQ`, then
  `||R+C||_2/||C||_2<=sqrt(C_diag/Lambda)` and
  `| ||R||_2/||C||_2-1 |` obeys the same bound.
- `PROVED`: if `Lambda=X^(omega+o(1))`, diagonal full moment forces the
  complement to be `X^(-omega/2+o(1))`-close to the negative endpoint comb.
  This retains one common coefficient vector rather than an unsigned support
  witness.
- `PROVED`: writing the ideal comb as
  `C_comb=Q sum_h A_h 1_(h|k)`, one actual endpoint denominator `h` satisfies
  a negative-correlation bound of magnitude at least
  `(1-epsilon)||C_comb||_2^2/sum_h A_h`.
- Structural implication: a supercritical strict-endpoint population can
  coexist with a diagonal full moment only through near-perfect
  cross-endpoint or core--halo anti-alignment on a retained divisor comb.
- Claim boundary: the theorem did not exclude that anti-alignment. No full
  second moment, endpoint, complete moment, density gain, or interval gain
  was proved.
- Artifact SHA-256:
  `2e7b318892e5ee0807d30a2d548b515a837a54757a3596223df5097c86564a48`.
  Builder SHA-256:
  `d3392c0cf00dd6892ea469d5b1d66a349d2ef171c47a951305ba33f3c328a298`.
- Builder runtime: wall time `0.04s`, peak RSS `18392 KiB`.
- Gate:
  `DIVISOR_COMB_ANTIALIGNMENT_EXCLUSION_OR_MODEL_OPEN`.
- Replay:
  `python3 proof/build_cycle_149_target_mass_comb_inverse_v1.py --check` and
  `python3 -m unittest tests/test_cycle_149_target_mass_comb_inverse_v1.py tests/test_cycle_seal_v1.py`.

## Cycle 150 — divisor-comb sign test (2026-08-02)

- `PROVED`: on the sampled frequencies `k=h ell` from Cycle 149, every other
  strict positive endpoint mode is either resonant and contributes real part
  `>>Q`, or nonresonant and is power-negligible by the Cycle-148 Poisson
  estimate.
- `PROVED`: strict positive endpoint combs with denominators
  `<=QX^(-delta)` reinforce rather than cancel one another on every retained
  modulus.
- `PROVED`: if the full complement has negative divisor-comb correlation
  `-M`, its exact residual escape class `H` has correlation at most
  `-(M-eta)` and norm at least
  `(M-eta)/(Q sqrt(K/h))`.
- `PROVED`: after inserting the Cycle-149 witness with bounded endpoint
  weights and `h~N`, the forced escape norm squared is at the one-ray comb
  scale `KQ^2/N`, again `Q/N` above one-mode diagonal.
- `PROVED` scoped exhaustion: every anti-aligner leaves the strict class via
  at least one of `HALO`, `BOUNDARY_DENOMINATOR`, `PHASE_CHANGE`, or
  `NONSMOOTH_PAYLOAD`.
- Claim boundary: none of the four escape classes was bounded or excluded.
  No full second moment, endpoint, complete moment, density gain, or interval
  gain was proved.
- Artifact SHA-256:
  `1039725acb7e764e1d352a7506756f5c6b620b232bfddeaf6c0cb1b0e73f1269`.
  Builder SHA-256:
  `d0b36de26a9675b4f7fe3e60226fe602b9145f8adbfb31e8500e761e1c1e36d1`.
- Builder runtime: wall time `0.04s`, peak RSS `18392 KiB`.
- Gate:
  `HALO_BOUNDARY_DIVISOR_COMB_ESTIMATE_OPEN`.
- Replay:
  `python3 proof/build_cycle_150_divisor_comb_sign_test_v1.py --check` and
  `python3 -m unittest tests/test_cycle_150_divisor_comb_sign_test_v1.py tests/test_cycle_seal_v1.py`.

## Cycle 151 — sampled-comb double Poisson (2026-08-02)

- `PROVED`: on the Cycle-149 sample `k=h ell`, a reduced halo denominator
  `h_b` resonates exactly on multiples of
  `L_b=lcm(h,h_b)=h h_b/gcd(h,h_b)`.
- `PROVED`: for `h_b<=QX^(-delta)`, all nonmultiples are power-negligible by
  Cycle 148. If `L_b` exceeds the upper frequency support, the entire smooth
  halo mode is negligible.
- `PROVED`: when `L_b` lies in support and
  `tau_b=KQ(c0g^b-r_b/h_b)` is bounded, the sampled correlation is
  `KQ^2L_b^(-1) B(tau_b)` with relative smooth Riemann error
  `O(L_b/K+1/Q)`, where
  `B(tau)=int int U(x)V(y)e(tau xy)dxdy`.
- `PROVED`: relative to the one-witness scale `KQ^2/h`, one halo mode has
  capacity `gcd(h,h_b)/h_b`. Target negative mass therefore forces a weighted
  gcd sum of order one.
- `PROVED`: positive weights can contribute negatively only when
  `Re B(tau_b)` lies below the explicit discretization error. Cycle 147
  excludes a fixed neighborhood of `tau=0`.
- Structural implication: a smooth halo anti-aligner simultaneously needs
  `lcm(h,h_b)<=K`, large aggregate gcd capacity, and tail parameters in
  negative transform lobes.
- Claim boundary: the gcd-weighted negative-lobe population and denominators
  within a fixed power of `Q` were not bounded. No full second moment,
  endpoint, density gain, or interval gain was proved.
- Artifact SHA-256:
  `9a7cff91d70b5d7d9da91f7f718fd0e8ee68808b81f8e3ee89d9d5ecdda6245c`.
  Builder SHA-256:
  `fc8a8dcbf58392b2ce4ed9e9346a0cb610c5f46be69e19652e71c3d36654e4c4`.
- Builder runtime: wall time `0.04s`, peak RSS `18396 KiB`.
- Gate:
  `GCD_WEIGHTED_NEGATIVE_TAIL_LOBE_OR_BOUNDARY_OPEN`.
- Replay:
  `python3 proof/build_cycle_151_sampled_comb_double_poisson_v1.py --check` and
  `python3 -m unittest tests/test_cycle_151_sampled_comb_double_poisson_v1.py tests/test_cycle_seal_v1.py`.
