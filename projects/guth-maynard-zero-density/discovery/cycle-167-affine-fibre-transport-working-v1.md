# Cycle 167 working decision summary v1

`SEALED`: the canonical record is
`artifacts/cycle-167-affine-fibre-transport-v1.json`. The frozen question is
in `docs/cycle-167-affine-fibre-transport-preregistration-v1.md`.

## Session checkpoint

`OBSERVED` mentor recommendation: attack one canonical massed shift fibre by
the gate `AFFINE_FIBRE -> BETA_PRESERVING_MULTIPLICATIVE_TRANSPORT OR EXACT
DIVISIBILITY/RANGE/BALANCE OBSTRUCTION`.  Do not use parent multiplicity as a
proxy for distinct `h` values.  First retain the actual parameter set `N`.

Its concrete falsifier is a legal massed state with primitive parents but no
eligible residue/range anchor, or `aK=o(H)`, and no secondary loop restoring
the condition.  That is a labelled obstruction, not failed bookkeeping.

## First derivation targets

- `CONJECTURED`: deconvolution is exactly `P(N)<=binom(|N|,4)`; therefore a
  parent count forces distinct parameters only after taking a fourth root.
- `CONJECTURED`: for `h=h0+r n`, eligibility has the congruence
  `r n=-h0 (mod a)`, soluble iff `gcd(a,r)|h0`; a solution is one class
  modulo `a/gcd(a,r)`, subject also to two exact row intervals.
- `CONJECTURED`: with `h^+=qh/a`, `j^+=j+h-h^+`, the beta-preserving error is
  the old error minus `h y(qE_u-a)/a`.  Its true cost is `H/(aKX)`, so
  `qK<=H` alone says nothing about the required balance. This creates a
  cross-label hit, not a Cycle-67 local AP packet: `qE_u≈a` does not imply
  `q alpha_(ell+u)≈a`.

The first finite exact prototype must test all three failure modes before any
attempted E7/E9 interpretation.

## First finite probe

`OBSERVED`: `cycle_167_affine_fibre_transport_probe.py` verifies the exact
transport identity and the deconvolution inequality.  It also constructs two
finite legal affine models with primitive four-parent multiplicity but no
eligible anchor: one misses the unique divisibility residue despite both row
ranges being valid, and one has every source anchor divisible but misses the
transformed range.  A separate balance example has `H/(aK)=100`.

These are discriminating countermodels to any claim that mass alone forces
transport.  They do not yet establish the exhaustive alternative for actual
Cycle-166 fibres, whose geometry may supply an additional loop or invariant.

`PROVED` interface correction: even an eligible transported hit is only a
beta-preserving edge from `ell` to `ell+u`.  It becomes a Cycle-67 recurrence
seed only if a separately retained target-local packet joins it, or if a
closed transport loop yields that local relation.  No such join is claimed in
this cycle.

## Seal outcome

`PROVED`, within the reduced rational ansatz `h^+=(q/a)h`,
`j^+=j+(1-q/a)h`: the direct map is unique, `a|h` is exactly its integrality
condition, `N_elig` is the necessary and sufficient residue/range classifier,
and its extra strip constant is exactly controlled by `2HY/(aK)`. The exact
finite countermodels show residue, transformed-range, and balance failures
are independent within that architecture.

`OBSERVED` companion seal checkpoint: `APPROVE SEAL` after the theorem was
narrowed from arbitrary real multipliers to the frozen reduced rational
approximant. Its falsifier is a nonunique `A`, a wrong integrality/range
classification, or a residual-bound violation. Adoption reason: replayed
exact convention and five focused tests cover those conditions.

Next: choose one new bridge at a strategic checkpoint—either join a retained
cross-label edge to a target-local packet, or build a labelled closed loop
that itself yields a local packet relation. Neither route is implied yet.
