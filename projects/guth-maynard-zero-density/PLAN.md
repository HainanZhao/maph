# PLAN: Beyond Guth--Maynard Zero Density

## 0. Control and claim boundary

- Project: `guth-maynard-zero-density`; selected 2026-08-01 UTC.
- Status: research Objective 2 is complete for the precisely defined EO-LF4
  energy-only actual-log-Farey subarchitecture. P1R-CRR remains open at the
  stronger common-Base bridge; P6 retains its primitive envelope gap; P7
  retains its detector/discrepancy gap over `Q(i)`.
- Program horizon: a 24-month extension runs from August 2026 through July
  2028, with `PL-BASE-BRIDGE` as the primary bet and gated alternatives below.
- This file is the concise strategic state. Chronological findings,
  corrections, failed paths, artifact hashes, and replay details live in
  `RESEARCH_LOG.md`.
- `PROVED`: EO-LF4 has sharp central exponent `20`; the checked Guth--Maynard
  `RL4` upper is attained in exponent by actual-label equal-weight
  phase-lattice row sets. This is the scoped saturation theorem required by
  Objective 2.
- `OBSERVED`: the project has not proved a new zero-density estimate, a
  smaller short-interval exponent, full-method or full-CRR saturation, or an
  extension to a new L-function family.
- Research-stage review policy: use lightweight source, algebra, replay, and
  consistency checks. Preserve adverse evidence, but do not use hostile
  audits as research continuation or route-selection gates. Hostile promotion
  audits occur when a result enters a manuscript/paper stage.
- Claim stop: contain an affected claim if independent exact derivations
  disagree, a theorem hypothesis is unchecked, or a claimed strict gain has
  no rigorous positive margin. Continue safe independent research elsewhere.
- Program review outcome: the precisely delimited EO-LF4 saturation/no-go
  theorem satisfies the stated alternative. Stronger branches remain
  authorized research extensions rather than conditions for this objective.

## 1. Objective

Extend the Guth--Maynard method by accomplishing at least one of:

1. prove, for explicit `eta>0`, a uniform estimate
   `N(sigma,T) <<_epsilon T^((30/13-eta)(1-sigma)+epsilon)` on the range
   needed for a new uniform short-interval prime-number theorem;
2. prove a saturation theorem for a precisely defined Guth--Maynard
   architecture, identifying its sharp inequality or extremizer;
3. translate any proof-grade density gain into explicit uniform and
   almost-all short-interval consequences;
4. complete one source-checked extension to a specified L-function family.

Out of scope without revision: RH, polylogarithmic intervals, a generic claim
for all automorphic L-functions, and promotion of empirical optimization as
proof.

`PROVED` current outcome: item 2 is `COMPLETE` only for EO-LF4 as defined
below; it is not a claim about the full Guth--Maynard method.

## 2. Frozen conventions and baseline

- Count multiplicity and use
  `N(sigma,T)=#{rho=beta+i gamma: beta>=sigma, |gamma|<=T}`.
- Distinguish uniform PNT asymptotics, almost-all asymptotics, and mere prime
  existence. The primary downstream target is the uniform asymptotic.
- `PROVED` from checked published sources: the baseline uniform density
  coefficient is `30/13`; the uniform short-interval endpoint is `17/30`;
  the stated almost-all endpoint is `2/15`.
- `PROVED`: at `sigma=7/10`, the coefficients `3/(2-sigma)` and
  `15/(3+5sigma)` both equal `30/13`.
- `OBSERVED`: Chen--Gupta--Li, arXiv:2507.08296v2, is prior Dirichlet-L work
  whose overlap and remaining hypotheses must be conceded and reconstructed.

Primary source identities and theorem/page mappings are frozen in the source
ledger and replay artifacts indexed by `RESEARCH_LOG.md`.

## 3. Working thesis and falsifiers

- `CONJECTURED`: the `30/13` loss is caused by an implemented cubic-trace,
  additive-energy, or zero-detection step rather than by general Dirichlet
  polynomials alone.
- `CONJECTURED`: on the actual phase-lattice extremizers, either the
  distinct-phase sampling norm and all-row efficiency jointly attain the
  Base threshold, or one has a fixed-power deficit that can be propagated
  into a Base-aware incompatibility theorem.
- F1: an explicit coefficient/set family simultaneously saturates every
  proposed improvement in the critical cell.
- F2: exact optimization proves that an available local gain cannot reduce
  the combined density envelope.
- F3: a universal theorem proves that a precisely defined cubic-trace/current-
  energy architecture has optimum `30/13`.

A surviving falsifier is a headline result, not a row to discard.

## 4. Research-path graph

```text
P0/G0 exact published-method reconstruction [COMPLETE]
  |
  +-- P1/G1 critical atlas [COMPLETE: NO_SELECTION]
        |
        +-- P1R-FS fixed-splice obstruction [COMPLETE]
        |
        +-- P1R-CRR critical compatibility
              |-- EO-LF4 energy-only saturation [COMPLETE: OBJECTIVE 2]
              |-- PL-BASE-BRIDGE [OPEN]
              |-- explicit compatible family --> P2B/P4
              `-- universal incompatibility --> P2B/P4

P2A higher trace ----\
P2B energy refinement +--> P3 density propagation --> P5 short intervals
P2C zero detection ---/          [all unselected/pending]

P6 Dirichlet-L reconstruction [REPAIRS RECONCILED; CORE ENVELOPE OPEN]
  `-- P7 finite-order Hecke over Q(i) [P7-1/2 COMPLETE; P7-3B ACTIVE]
        `-- P8 low-degree automorphic families [DEFERRED]
```

## 5. Current gate states

| Gate/path | State | Strategic meaning |
|---|---|---|
| G0/P0 | `COMPLETE` | `PROVED` conditional reconstruction of published `30/13`, `17/30`, and `2/15`; not a new theorem. |
| G1/P1 | `NO_SELECTION` | `OBSERVED` bounded searches selected none of P2A/P2B/P2C; none is refuted. |
| P1R-FS | `COMPLETE` | `PROVED` fixed-splice obstruction only; the unchanged left branch has supremum `30/13`. |
| P1R-CRR | `EO_LF4_COMPLETE_BASE_OPEN` | `PROVED`: the energy-only actual-log-Farey fourth-moment exponent is sharply `20`, with an actual phase-lattice extremizer. Full Base remains open at the exact `lambda*Xi` common-coefficient bridge, with RationalMass and PositiveCubic additionally required for full CRR. |
| P2A/B/C | `NOT SELECTED` | May be opened only by new affirmative evidence and a recorded route decision. |
| P3/P5 | `PENDING` | Exact conditional endpoint formulas are banked, but propagation still requires a proof-grade analytic gain. |
| P6 | `REPAIRS_RECONCILED_CORE_OPEN` | S06 polynomial growth, local multiplicity, and primitive fourth moment are now supplied, as are conductor transfer/reset and detector/smooth repairs. The primitive large-value/comparator/energy envelope remains open, so no general `7/3` theorem is promoted. |
| P7 | `OPEN_DETECTOR_OCCUPANCY` | Selected Gram pinching and fixed-ray transfer are exact, but fibrewise separation and individual zero counts permit the sharp colour loss `D_Delta=mP`. A source-scale result needs a common ideal detector or a higher-moment bypass. |
| Paper audit | `DEFERRED` | Hostile promotion audit begins only when manuscript claims are proposed. |

## 6. Banked headline results and corrections

- `PROVED`: independent reconstructions recover published `30/13`, `17/30`,
  and `2/15`. Retaining the left Ingham branch forces the fixed-splice
  supremum `30/13`; right-only or endpoint-only changes cannot lower it.
- `PROVED` conditional CRR reduction: the Montgomery large-values conjecture
  rules out the frozen Base sequence throughout every fixed
  `3/5<sigma<7/10`; saving only one of the two tied `v^8` terms is
  insufficient in this architecture.
- `PROVED`: generic alias models cannot yield a spacing/energy-only saving.
  On actual Farey cells, RationalMass and global L2/L4-energy meet at bundle
  exponent `26`; CFARI and AFARI are fixed-power equivalent. These are scoped
  saturation results, not full-method saturation.
- `PROVED` EO-LF4 saturation: for the class retaining the actual reduced
  Farey union, frozen row geometry, and tolerance-one energy but discarding
  Base/RationalMass/PositiveCubic, `RL4` gives `v^(20+o(1))` and actual
  phase-lattice sets give at least `v^20/30` in logarithmic measure. Thus the
  sharp exponent is `20` and every fixed-power energy-only saving fails.
- `PROVED`: exact rational aliases on the extremizing phase lattice have
  classes of size at most four. Base compatibility is equivalent to the
  product gate `lambda*Xi`; any compatible lattice must have
  `lambda=v^(12-o(1))` and `Xi=v^(-o(1))`. Neither compatibility nor
  exclusion is proved.
- `PROVED`: Base has an exact capped max-phase/min-probability formulation.
  Its leading-vector certificate isolates eigenvalue, coefficient
  delocalization, and all-row flatness. `OBSERVED`: both bounded CRR probes
  missed; neither miss licenses an asymptotic negative.
- `PROVED` P6 repair package: primitive-to-all transfer, conductor-level
  `q1` reset, the `qT` detector tail, multiplicity transfer, corrected
  smooth-divisor chain, polynomial growth, local multiplicity, and the
  primitive discrete fourth moment hold in their stated scopes. `CONJECTURED`:
  the central primitive large-value/comparator chain is still missing.
- `PROVED` P7 map: common-ideal/ray projectors and L2 transfer exactly, while
  naïve completion and per-character fallback can cost `Q` and `Q^2`.
  PSD pinching gives `0<=X_cross<=G(K)<=3||K||V2(K)`; class averaging removes
  completion and leaves a ray discrepancy over time differences.
- `OBSERVED` corrections and superseded branches are preserved in
  `RESEARCH_LOG.md`; no failed path is erased from project memory.

## 7. Twenty-four-month research program

North star: lift EO-LF4 to a coefficient-sensitive theorem—either an explicit
gain that lowers the density envelope, or a Base-aware saturation theorem
with a sharp inequality or extremizer. Frozen central scales remain
`T=v^13, H=v^12, L=v^10, R=v^8, Q=v^4, V=v^7`.

Planned effort: roughly 65% on `PL-BASE-BRIDGE` and full CRR coupling, 20% on
the higher-trace/zero-detection contingency, and 15% on P6/P7 transfer. These
shares are planning defaults, not resource caps.

| Months | Primary question and deliverable | Decision gate |
|---|---|---|
| 0–3 | Replace the definitional `lambda*Xi` identity by two independently estimable formulations: a distinct-phase spectral criterion and a capped all-row dual/minimax criterion. Freeze model families and falsifiers before computation. | Bank at least one analytic estimate with an explicit exponent budget; bounded probes remain discovery only. |
| 4–6 | Attack the actual phase-lattice Base bridge in both directions: construct one common capped coefficient attaining the product threshold, or prove a uniform fixed-power deficit in `lambda` or `Xi`. | `COMPATIBLE`, `INCOMPATIBLE`, or `UNRESOLVED`. If unresolved, preserve the branch and move 25% of main effort to higher trace rather than declaring failure. |
| 7–9 | On compatibility, verify RationalMass and PositiveCubic for the same `(b,W)`. On incompatibility, propagate the deficit through the actual `S3` argument and a left neighborhood of `sigma=7/10`. | Require one proof-grade coupling lemma or a precisely scoped non-implication theorem. Otherwise activate P2A quartic trace as a co-primary route. |
| 10–12 | Recompute the full piecewise density envelope. If a strict margin survives, derive uniform and almost-all interval endpoints; otherwise formulate the strongest Base-aware saturation statement justified by the first-year work. | Year-one outcome must be a density gain, a Base-aware saturation/no-go theorem, or a recorded pivot to P2A/P2C with an exact missing lemma. |
| 13–15 | Pursue only the affirmative contingency selected at month 12: quartic/higher trace, altered zero detection, or coefficient-sensitive energy. Keep P6/P7 as transfer tests, not substitutes for the main theorem. | Continue a route only with a theorem-scale exponent budget or a surviving explicit witness. |
| 16–18 | Close the principal analytic chain and obtain an independent derivation where the mechanism permits. If no density gain survives, stop optimizing the old envelope and consolidate the sharpest Base-aware obstruction. | Freeze the main theorem statement and every remaining hypothesis; no priority claim yet. |
| 19–21 | Test the successful mechanism on primitive Dirichlet characters and the selected finite-order `Q(i)` Hecke family. For P7, require a common ideal detector or a higher-moment bypass of the sharp `mP` occupancy loss. | Promote an L-family extension only after every conductor, detector, and archimedean hypothesis is source-checked. |
| 22–24 | Consolidate the theorem, independent checks, source/novelty ledger, and replay archive. Begin hostile audit only now, when concrete manuscript claims exist. | Paper-ready result requires a replayable proof archive; final circulation still requires an immutable DOI. |

Two-year success hierarchy:

1. stretch outcome: `PROVED` explicit `eta>0`, a lower uniform density
   coefficient, and the resulting short-interval endpoints;
2. main outcome: `PROVED` Base-aware/full-CRR saturation with a sharp
   inequality, extremizer, or universal incompatibility theorem;
3. companion outcome: one source-checked Dirichlet or `Q(i)` L-family
   extension of the mechanism established in outcomes 1 or 2.

Outcome 3 alone does not replace the primary year-two decision between a
density gain and a Base-aware saturation theorem.

## 8. Open questions

1. Does the phase-lattice extremizer satisfy the exact `lambda*Xi` Base gate,
   or does distinct-phase sampling force a fixed-power loss in one factor?
2. If incompatible, does the quantitative saving survive the actual `S3`
   argument and a left neighborhood of `sigma=7/10`?
3. Is the leading energy term sharp for the frozen coefficient class?
4. Can a quartic trace exploit structure invisible to the cubic trace without
   a larger off-diagonal loss?
5. Does any local gain survive the complete zero-detection optimization and
   lower the global envelope?
6. Can the critical short-interval contribution be improved without passing
   solely through a uniform density envelope?
7. Can the `Q(i)` ray-class discrepancy over the uncoloured difference
   multiset be bounded at source scale from a conductor-safe sampling input?

## 9. Immediate authorized actions and pivot rules

1. Derive a non-tautological spectral/dual formulation of `PL-BASE-BRIDGE`
   whose inputs can be bounded independently of `Gamma`; keep the exact iff
   only as the target identity.
2. Preregister compatibility and exclusion attempts separately, including
   exponent margins, phase-lattice families, and rules for inconclusive rows.
3. Keep the actual-log probe, RFDI surgery, P6, and P7 at their exact scopes;
   none currently supplies the common Base/CRR witness.
4. A failed research check contains its claim but does not kill the broader
   idea. Formal route termination occurs only at the scheduled gates and is
   preserved in `RESEARCH_LOG.md`.
5. Do not propagate to density or short intervals without a strict analytic
   margin, and do not initiate hostile audit before paper-stage promotion.

## 10. Crash recovery

From the repository root:

```sh
cd /root/projects/maph
git status --short --branch
cat projects/guth-maynard-zero-density/PLAN.md
tail -n 160 projects/guth-maynard-zero-density/RESEARCH_LOG.md
find projects/guth-maynard-zero-density -maxdepth 3 -type f -print | sort
git log -5 --oneline --decorate
```

Before release or publication:

```sh
git fetch
git log HEAD..origin/main --oneline
```

Preserve unrelated worktree changes, especially existing
`projects/effective-stark-sweep/` work.
