# PLAN: SIC--Stark companion-paper series

## Purpose, boundary, and status

- Objective: preserve and publish the proved formal Twisted Convolution
  Conjecture (TCC) cases in dimensions 4, 5, 7, and 8, while developing a
  falsifiable dimension-six analytic interface if one exists.
- Claim boundary: `PROVED` certificate suites close the documented dimension
  4, 5, 7, and 8 scopes. No dimension-six TCC identity, coefficient-to-ray
  map, or boundary-limit theorem is proved. `OBSERVED` growth in the audited
  boundary packets is not a nonexistence theorem.
- Status: Cycle 162 establishes the current-format record system and records
  the dimension-six formulation gate. Cycles 1--161 and the four
  `artifacts/tcc-*.json` files are preserved legacy evidence; they are not
  retrofitted with manifests or altered.
- Stop condition: do not reopen the dimension-six boundary-packet route, or
  prepare Paper III as a theorem paper, until the active interface gate has a
  replayable positive result. The whole program stops only by explicit user
  direction or after a scoped no-go for a precisely defined interface class.

## Frozen baseline

- `PROVED`: the dimension-seven discriminant-8 and discriminant-32 packets
  are both closed; together with the dimension-eight packets this supports the
  archived universal dimensions-seven-and-eight paper scope. See legacy Cycle
  161 and `certificates/dimension-seven-cycle161-discriminant-eight-closure.json`.
- `PROVED`: Cycle 157 verified the ordinary Fourier gauge and finite-frequency
  descent but found no supplied map from 36 additive coefficients to the three
  ray-class logarithms or AFK cocycle values.
- `CERTIFIED_NUMERICAL`: the Cycle-157 audited finite ladder has stable
  high/low-precision agreement while the tested transformed coefficients grow;
  this constrains the retired componentwise route only.

## Research-path graph and gates

```text
closed certificate packages: dimensions 4, 5, 7, 8 [preserved]
  `-- publication maintenance [only scope-accurate archive/DOI work]
dimension 6 [active formulation gate]
  `-- coefficient-to-cocycle/ray-logarithm interface [OPEN]
       +-- smallest finite-frequency prototype [authorized after interface]
       +-- analytic boundary/periodization estimate [blocked]
       `-- exact downstream TCC algebra [conditional, preserved]
```

| Gate | State | Advance condition | Disallowed pseudo-progress |
|---|---|---|---|
| D6 interface | `OPEN_DESIGN_PROBLEM` | A convention-pinned formula specifies characteristic selection, additive-to-logarithmic operation, branches, finite part, and AFK-cocycle identification; a minimal finite-frequency prototype can falsify it. | More raw/gauged packet numerics, an asserted BF_6=>MFC_6 implication, or downstream algebra without the map. |
| D6 boundary estimate | `BLOCKED_BY_INTERFACE` | The new interface passes the prototype and makes a concrete boundary quantity operationally testable. | Treating numerical growth as a no-go for TCC. |
| Paper III | `RESEARCH_NOTE_ONLY` | A proved theorem with a replayable interface-to-TCC chain and scope-accurate manuscript/archive gates. | Theorem or Zenodo metadata claims exceeding the paper's stated scope. |
| Papers I--II | `PRESERVED_PROOF_PACKAGES` | Only a scope correction, replay failure, or release action changes this gate. | Rewriting legacy evidence to fit the new record format. |

## Headlines, questions, and next action

- `PROVED`: the missing bridge is a named construction problem, not evidence
  that only existing boundary-packet machinery is legitimate.
- `CONJECTURED`: a viable interface may require a new finite-characteristic
  selector or a cocycle-level completion; it must preserve pinned Fourier and
  ray-class labels and be falsified by the smallest finite-frequency model.
- Falsifier: a candidate interface is rejected if it cannot define all five
  frozen components above, changes a pinned label/branch convention, or fails
  its preregistered prototype exactly.
- Next authorized action: open one preregistered substantive cycle for the
  interface state space and smallest falsifiable prototype. Read Cycle 162,
  then legacy Cycles 157 and 161 before changing mathematics.

## Recovery

```sh
source ../../tools/dev-env.sh
research rebuild
research check
research cycle 162
python proof/verify_cycle_162_workflow_migration.py
python -m unittest tests.test_research_workflow_migration -v
```
