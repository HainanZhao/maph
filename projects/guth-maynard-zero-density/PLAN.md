# PLAN: Beyond Guth--Maynard Zero Density

## Purpose, boundary, and status

- Project horizon: August 2026 through July 2028.
- Objective: obtain either (i) an explicit improvement on the `30/13`
  zero-density coefficient that survives the complete density and
  short-interval ledger, (ii) a sharp saturation/inverse theorem for a
  materially larger, coefficient-sensitive Guth--Maynard architecture, (iii)
  a direct zero-cluster route to a better prime-interval theorem, or (iv) a
  conductor-accounted transfer of a proved mechanism to one specified
  L-function family.
- Claim boundary: no improved density coefficient, uniform prime-interval
  endpoint, almost-all endpoint, or family transfer is proved yet.
- Stop condition: a strict gain survives the full ledger, or a sharp theorem
  covers an architecture materially larger than `EO-LF4`.
- Review policy: use lightweight source, algebra, replay, and consistency
  checks during research. Hostile referee simulation begins only once a
  manuscript theorem is frozen.

## Memory model

`PLAN.md` is strategic state, not a laboratory notebook. The canonical
committed record of each cycle is its immutable JSON artifact and linked
preregistration, proof document, convention, builder, and test. `STATUS.md`
is generated from those records. `.research/index.duckdb` is an ignored,
rebuildable query index. The historical aggregate ledger is frozen at
`archive/RESEARCH_LOG-through-cycle-151.md`; do not append to it.

Rebuild and inspect the local index:

```sh
cd /root/projects/maph/projects/guth-maynard-zero-density
source ../../tools/dev-env.sh
research rebuild
research check
research cycle 151
research search negative-tail
research db tables
```

## Critical-decision companion

Every research session for this project starts one mentor companion alongside
the primary worker, before calculations or path selection. It remains the
same session companion across all Cycle 152+ branches and decisions; do not
replace it with a fresh per-cycle reviewer. Where a more capable model is
available, use it; otherwise use an independent agent with a fresh brief. The
companion is not a second proof engine and does not run a hostile audit. Its
narrow job is to track the preregistered checkpoint: frozen premise,
alternatives, tagged decisive evidence, recommendation, and unexamined
assumptions. Consult it before changing this plan, choosing or dropping an
engine, revising a gate/advance criterion, preregistering a cycle, or deciding
the next authorized action. Put its recommendation and the primary worker's
adopt/reject reason in the relevant readable session/cycle decision record.
Before each such decision, check the companion's live task status. If it is
idle or completed, reactivate that same task identity with the frozen decision
brief; if it is running, deliver the brief and await its response. Record the
liveness check and response alongside the decision. If the companion cannot
be invoked, defer the critical decision while routine reversible exploration
continues.

## Frozen baseline

- `PROVED`: the checked baseline density coefficient is `30/13`; the stated
  uniform and almost-all prime-interval endpoints are respectively `17/30`
  and `2/15`. At `sigma=7/10`, the baseline branches meet at `30/13`.
- `PROVED`: for the actual phase-lattice extremizer, Base compatibility is
  equivalent to the product gate `lambda*Xi`, requiring
  `lambda=v^(12-o(1))` and `Xi=v^(-o(1))`.
- `PROVED`: within `EO-LF4` (actual reduced Farey labels, frozen row geometry,
  tolerance-one energy, and no Base/RationalMass/PositiveCubic input), the
  exponent `20` is sharp up to a constant factor. This is the scoped input
  licensing the preceding reduction, not a field-wide impossibility theorem.
- `PROVED`: retaining the Ingham-side branch fixes the global supremum at
  `30/13`; a right-only improvement cannot move it.
- `PROVED`: the E13 critical transport reduction has raw target below
  `X^(31/25)` and needs an anchored seed before packet propagation; removing
  that anchor costs `17/75`.

## Headline findings

- `PROVED`: unsigned incidence closes all critical Fourier blocks
  `xi<16/25`; above this it is volume-obstructed. The remaining signed range
  is `16/25<=xi<=83/75`.
- `PROVED`: below `58/75`, diagonal-strength `M2` is sufficient; above it,
  diagonal-size `M2` plus raw `L1` forces fourth-moment excess
  `2xi-116/75`. The upper task is an inverse concentration problem.
- `PROVED`: the lower alias analysis banks strict sub-alias removal,
  exact central and noncentral projective-mode structure, a strong-core
  closure, weak-sector closure, and several inverse compilers. It does not
  close the full signed moment.
- `PROVED`: scalar collision inverses are not coefficient-faithful. The real
  object has frequency-dependent oriented edge coefficients; the selected
  vector autocorrelation and signed high-pass kernel are now explicit.
- `PROVED`: strict endpoint cells contribute a major-arc comb of relative
  size `Q/N`; isolated endpoint norm aggregation therefore cannot attain
  diagonal strength in a fixed `rho<1/3` band.
- `PROVED`: any smooth halo anti-aligner must have an admissible lcm,
  gcd-weighted capacity of order one, and a negative tail-transform lobe.
- `PROVED`: conditional on normalized strict smooth-halo negative mass, that
  mass has a bounded-multiplier labelled divisor-fan inverse. The actual
  complement-to-strict-halo mass bridge remains open; this is not a density
  theorem.
- `PROVED`: every post-error forced negative divisor-comb correlation routes
  either to labelled strict-halo negative mass or, if that branch is below its
  fixed threshold, to a quantitative labelled escape obligation.
- `PROVED`: a finite reason-labelled escape partition with a fixed comb-norm
  bound localizes its negative projection to one retained class, with a
  one-ray `L2` lower bound. The actual partition and its anchor-constant
  instantiation are not yet proved.
- `PROVED`: the selected divisor comb has exact squared norm at most
  `(1+C_h)KQ^2/h` under a frozen anchor ratio `h<=C_hK` (and constant `2`
  when `h<=K`). Instantiating its actual anchor constant and constructing the
  finite coefficient partition remain open.

## Research-path graph

```text
published reconstruction P0 [complete]
  +-- EO-LF4 sharpness [complete, scoped] -- lambda*Xi [diagnostic]
  `-- E13 critical transport [principal]
        +-- E14 unsigned incidence [volume limit; inverse input]
        +-- E14D-L signed Mellin aliases [principal]
        |     `-- actual strict antecedent -> bounded fan / escape control [active]
        +-- E14D-H fourth-moment condenser <--- E17 extremizer foundry
        +-- E15 anchored shifted-ratio spectrometer
        `-- E16 alias-to-seed compiler --> E7/E9 prime skeleton
  +-- E11/E12 autocorrelation--ANOVA [co-primary]
  `-- E5/E6 feedback/direct zero cancellation [incubation]
        `-- P3/P5 intervals; P6/P7 L-function transfer
```

| Gate | State | Advance condition |
|---|---|---|
| E14 | `UNSIGNED_VOLUME_LIMIT_REACHED` | Use only for inverse structure. |
| E14D-L | `EXACT_DIVISOR_COMB_NORM_MAJORANT_LEMMA_BANKED_ACTUAL_PARTITION_OPEN` | Instantiate the frozen anchor ratio and derive an actual fixed finite coefficient-escape partition, or expose a quantified coefficient-complexity inverse; separately prove positive transport to activate the bounded fan. |
| E14D-L mask cone | `ACTUAL_SELECTION_MASK_GRAM_FACTORIZATION_OR_COEFFICIENT_COMPLEXITY_INVERSE_OPEN` | Prove a bounded positive-Gram transport in actual coefficient geometry or extract a labelled weighted dual/negative-spectral witness. |
| E14D-H | `MOMENT_CONCENTRATION_OR_SATURATION_INVERSE_OPEN` | Classify/exclude excess `2xi-116/75` with its phase anchor. |
| E15 | `ANCHOR_REQUIRED` | Classify anchored almost-eigenfunctions. |
| E16 | `EXACT_VALUATION_WEB_BANKED` | Compile relation-rich structure to a genuine transport seed. |
| E11/E12 | `AUTOCORRELATION_ANOVA_OPEN` | Save `>3/50` in complete form or force enough recurrence. |
| E7/E9 | `SKELETON_RECURRENCE_OPEN` | Prove the `X^(21/25+o(1))` skeleton bound. |
| P3/P5 | `PENDING_GAIN` | Reinsert only a strict proof-grade analytic margin. |
| Paper audit | `DEFERRED` | Start after a manuscript theorem freezes. |

## Principal engines and falsifiers

- `CONJECTURED` E14D-L: Cycles 152--154 bank a conditional fan, an exact
  actual-mass router, a conditional finite-class escape localizer, and an
  exact anchor-bounded comb-norm lemma. Cycle 155 must derive the actual fixed
  finite coefficient partition or expose its quantified complexity inverse.
  Cycle 157 attacks that latter alternative in the actual Hermitian selection
  mask rather than the smooth-model taxonomy. Positive strict transport still
  needs its normalized weights and uniform complete capacity bound before
  spacing/order-three curvature can attack an actual bounded fan.
- `CONJECTURED` E14D-H: encode required `M4` excess as a colored four-cycle
  problem. Low codegree should exclude excess; high codegree should expose an
  anchored rational web. A raw-target example without either output enlarges
  the inverse class.
- `CONJECTURED` E15/E16: classify anchored shifted-strip almost-eigenfunctions
  and turn high-codegree alias structure into a seed with an explicit phase
  error budget. A seedless target-sized anchored graph is itself structural
  output.
- `CONJECTURED` E17: search exact finite alias operators for adversarial
  extremizers. All numerical output remains discovery-only.

## Two-year execution plan

| Dates | Deliverable | Decision rule |
|---|---|---|
| Aug--Oct 2026 | E14D-L negative-tail theorem; E17 finite extremizer atlas. | Bank a compact signed theorem or preserve its explicit saturator. |
| Nov 2026--Apr 2027 | Widest lower-band `M2` closure; narrow-band E14D-H concentration theorem. | Promote only a proved band closure or a real inverse class. |
| May--Jul 2027 | E16 compiler from the strongest structured output. | Year-one target: lower band closure plus upper inverse theorem, or complete signed-projector saturation. |
| Aug 2027--Jan 2028 | Glue across the atlas; test E7/E9, E11/E12, E5, and E6 ledgers. | Freeze only a complete raw-form, skeleton, density, or direct-interval candidate. |
| Feb--Jul 2028 | Propagate a surviving margin; then conduct source review, independent derivation, hostile audit, replay, and paper preparation. | Transfer only with strict conductor/occupancy margin. |

## Open questions and next action

1. Can the gcd-weighted negative-tail population be bounded below the
   anti-alignment threshold away from boundary denominators?
2. Can a denominator near `Q` contribute a coherent negative lobe without
   yielding a new explicit divisor-fan model?
3. Does the coefficient-faithful vector autocorrelation produce a fixed-power
   lower-band saving, or only a larger saturation theorem?
4. Can forced upper-band fourth-moment excess be converted to colored
   four-cycles retaining the phase anchor?
5. Can a relation-rich web produce a genuine transport seed and then the
   `X^(21/25+o(1))` prime skeleton?

Cycle 154 banks only the conditional finite-class localization compiler.
Cycle 155 is preregistered at
`docs/cycle-155-actual-coefficient-escape-partition-preregistration-v1.md`.
Cycle 157 is preregistered at
`docs/cycle-157-selection-mask-cone-preregistration-v1.md`. Next authorized
action: derive a bounded positive-Gram factorization of the actual Hermitian
selection mask in coefficient-weighted geometry, or a labelled weighted dual,
rectangle, or negative-spectral complexity witness. The older Cycle-155
partition remains a parallel output only if it is actual and fixed-size; an
`X^(o(1))` class count is not fixed localization. Only after an actual
partition may Cycle 154 identify a real high-projection class. Cycle 156
supplies its norm constant once the actual frozen anchor ratio is
instantiated. Positive transport and the Cycle-152 bounded fan remain
unclosed.

## Crash recovery

```sh
cd /root/projects/maph
git status --short --branch
cat projects/guth-maynard-zero-density/PLAN.md
cat projects/guth-maynard-zero-density/STATUS.md
cd projects/guth-maynard-zero-density
research check
research cycle 151
python3 proof/build_cycle_144_actual_edge_coefficient_v1.py --check
python3 proof/build_cycle_145_vector_autocorrelation_v1.py --check
python3 proof/build_cycle_146_balanced_highpass_mask_v1.py --check
python3 proof/build_cycle_147_strict_core_signed_cell_v1.py --check
python3 proof/build_cycle_148_endpoint_major_arc_comb_v1.py --check
python3 proof/build_cycle_149_target_mass_comb_inverse_v1.py --check
python3 proof/build_cycle_150_divisor_comb_sign_test_v1.py --check
python3 proof/build_cycle_151_sampled_comb_double_poisson_v1.py --check
python3 proof/build_cycle_152_bounded_multiplier_divisor_fan_v1.py --check
python3 proof/build_cycle_152_bounded_multiplier_divisor_fan_scope_correction_v1.py --check
python3 proof/build_cycle_153_actual_mass_routing_v1.py --check
python3 proof/build_cycle_154_coefficient_escape_localization_v1.py --check
python3 proof/build_cycle_156_divisor_comb_norm_majorant_v1.py --check
```
