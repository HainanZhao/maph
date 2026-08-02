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

## Research-block cadence

Cycles are substantive research blocks: one preregistered question, several
dependent lemmas/counterexamples, and one bound-or-obstruction gate. Keep
intermediate bookkeeping in a compact working ledger; seal, rebuild status,
and commit only when the block's advance condition is resolved. Early seals
are reserved for corrections, falsifiers, externally useful theorems, or
irreversible strategy/gate changes.

When a sealed-interface cut is found, treat it as a design problem, not a
terminal barrier: the next block must attempt a new payload-preserving bridge,
invariant, lift, or discriminating countermodel before any saturation claim.
The program is expressly authorized to invent the missing engine from the
ground up; known theorems constrain and test that engine, rather than defining
the boundary of permissible ideas. Each proposed engine starts as the smallest
falsifiable prototype with a stated invariant and failure signature.

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
- `PROVED`: conditional upper-band fourth-moment excess has a
  coefficient-weighted off-diagonal pair-cell inverse. Its local refinement
  gives positive-real four-distinct-atom mass or a consistently oriented,
  labelled high-effective-degree star; the required global mass retention is
  now the active Cycle-162 question.
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
| E14D-L | `TIMEBOXED_AT_SCALE_LABEL_INFORMATION_LOSS` | Reopen only by restoring `t`/ordered atoms in a coefficient-preserving selector or proving a genuinely `t`-independent factorization. |
| E14D-L mask cone | `RAW_ZERO_DIAGONAL_GRAM_OBSTRUCTION_BANKED_COEFFICIENT_NEGATIVE_SPECTRAL_ALIGNMENT_OPEN` | Concentrate actual negative spectral energy in a fixed labelled block family or prove a robust labelled block-complexity inverse. |
| E14D-H | `MASS_ALIGNED_FOUR_CYCLE_OR_GLOBALLY_MASSED_COMMON_WRAP_LOG_WEB_OR_INTEGER_WRAP_COMPLEXITY_OPEN` | Compile the labelled common-wrap web or bound the labelled wrap-complexity inverse without discarding the four-cycle arm. |
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
  Cycle 157 rules out exact raw-mask Gram transport and Cycle 159 proves that
  primitive-ray compression loses the multiplier needed by coefficient
  products. E14D-L is timeboxed for Cycles 160--162. Positive strict
  transport still needs its normalized weights and uniform complete capacity
  bound before spacing/order-three curvature can attack an actual bounded fan.
- `CONJECTURED` E14D-H: Cycles 160--163 turn conditional upper-band `M4`
  excess into a globally massed four-atom/star inverse, then classify the
  star by literal wrap complexity or an aggregate common-wrap logarithmic
  web. The next step must compile one labelled output or preserve an
  admissible obstruction. A raw-target example without either output enlarges
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
action is Cycle 159, preregistered at
`docs/cycle-159-coefficient-selector-reconstruction-preregistration-v1.md`:
reconstruct the actual coefficient-preserving selection kernel through the
Cycle 124--136 maps, or prove the first information-loss map and its minimal
missing label. It ended in the primitive-ray multiplier-loss alternative.
E14D-L is therefore timeboxed through Cycles 160--162. Next authorized
action: execute Cycle 160, preregistered at
`docs/cycle-160-colored-four-cycle-condenser-preregistration-v1.md`, proving
the `1/150` low-codegree condenser bound or preserving an actual high-codegree
pair-cell inverse/falsifier. Cycle 161 is preregistered at
`docs/cycle-161-high-cell-refinement-preregistration-v1.md`: refine the high
cell into coefficient-weighted phase-aligned disjoint four-atom mass or a
labelled effective-degree star; it is now sealed. Next authorized action is
Cycle 162, preregistered at
`docs/cycle-162-mass-sensitive-high-cell-preregistration-v1.md`, is sealed:
it retains a fixed share of the conditional forced excess in a dyadic
high-codegree layer and exports either globally massed positive-real
four-cycle mass or literal weighted labelled oriented-star mass. Next
authorized action is Cycle 163, preregistered at
`docs/cycle-163-star-wrap-fiber-preregistration-v1.md`: pull back the
weighted star family through `z_(d,q)=c0q exp(2pi d/D)` by the exact
wrap/fiber effective-degree factorization, producing a common-wrap log web
or explicit wrap-complexity inverse; it is now sealed. Next authorized action
is Cycle 164, preregistered at
`docs/cycle-164-wrap-valuation-sidon-preregistration-v1.md`: retain high
common-wrap fibers and prove an exact valuation-web versus weighted-Sidon
classification. Cycle
158's concentration theorem remains deferred until a selector
is real rather than formal. The older
Cycle-155 partition remains a parallel output only if it is actual and
fixed-size; an `X^(o(1))` class count is not fixed localization. Cycle 156
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
python3 proof/build_cycle_157_selection_mask_negative_spectral_v1.py --check
python3 proof/build_cycle_159_coefficient_selector_information_loss_v1.py --check
```
