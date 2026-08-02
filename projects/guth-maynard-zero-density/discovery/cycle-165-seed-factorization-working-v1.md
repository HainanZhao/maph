# Cycle 165 working ledger: seed-predicate factorization

`CONJECTURED` question: does the Cycle-164 retained-label map `pi` determine
the Cycle-67 seed predicate, including the original beta payload and an
admissible packet of depth `L_pkt>=X^(6/25-o(1))`?

## Frozen source interfaces

- Cycle 164 retains common-wrap labels `(d,q,c0)`, coefficient, wrap,
  orientation, atom, and phase-sector data. Its stated valuation relation is
  beta-free.
- Cycle 67 requires the original inequality
  `|j0+beta-h0 alpha|<=C0/X`, together with
  `|q alpha-a|<=C1/(L_pkt X)`, `qL_pkt<=H`, and the stated depth.
- Cycle 106 proves only a beta-free non-implication. It cannot be imported as
  a Cycle-165 theorem until all Cycle-164 labels are checked against its
  paired-payload witness.

## Dependent tasks (not separately sealed)

1. `OPEN`: reconstruct the exact original-row-to-Cycle-164-label map,
   including whether `beta`, `j0`, `h0`, `alpha`, and packet data are retained,
   derived, or forgotten at each Cycle 160--164 map.
2. `OPEN`: attempt a deterministic reconstruction of the seed predicate from
   the complete retained label tuple.
3. `OPEN`: if reconstruction fails, construct a same-complete-label pair of
   admissible original rows with opposite seed predicates. Varying a retained
   label invalidates the witness.
4. `OPEN`: independently check the packet inequalities using `L_pkt` (not
   Fourier scale `K`) and preserve the first unresolved pi-fiber if neither
   outcome closes.

## First schema audit

`OBSERVED` from the immutable Cycle 160--164 preregistrations and proof
documents: the declared surviving tuple contains atom/anchor/denominator/tail
data, then `(d,q,c0)`, coefficient, phase-sector, orientation, cell, and wrap
data. None declares `beta`, `j0`, `h0`, `alpha`, or `L_pkt` as a retained
coordinate. Cycle 163 explicitly says its coordinate pullback is not yet a
transport seed; Cycle 164 likewise labels its web beta-free.

This is not yet `PROVED` information loss: the next task is to check whether
one of the retained coordinates deterministically reconstructs the omitted
seed data in the actual original-row map. Cycle 106's paired beta witness is
only an analogue until that map is explicit.

## Variable disambiguation

`PROVED` source reading: Cycle 63's transport census is
`|j+beta-h alpha_ell|<=C/X`, with `alpha_ell=exp(2pi ell/Delta)-1`; this
`beta` is a row phase shift and disappears only after differencing two
original hits. The `2pi` in the Cycle-87/160--164 coordinate
`z_(d,q)=c0 q exp(2pi d/D)` is instead a fixed analytic constant. It is not a
retained transport-beta payload. Thus a notation match cannot supply the
missing Seed coordinate.

`OPEN` bridge: establish the exact map (or lack of a map) from the Cycle-164
`(d,q,c0)` atom ancestry to Cycle-63's `(h,ell,j,beta)` transport row. Until
then neither a payload-aware compiler nor a complete-label no-go is licensed.

## Typed ancestry subproblem

Freeze distinct types: `TransportRow63=(alpha,beta,h0,j0,L_pkt,q,a,...)`,
`UpperAtom87=(c0,d,q,a_(d,q),z_(d,q),...)`, and `WebLeaf164` with its wrap,
valuation, coefficient, tail, and orientation labels. Transport `beta` and
the fixed circle constant `2pi` are distinct typed objects.

`OPEN`: build a provenance DAG using only sealed constructors. Each edge must
list input/output fields, exact formula, branch hypotheses, retained and
discarded fields, and coefficient/phase normalization. Test the composition
`TransportRow63 -> UpperAtom87 -> WebLeaf164` by an exact commutative phase
identity.

If the path exists, test seed-predicate constancy on each actual source fiber.
If beta is free on a nonempty fiber, make the same-complete-label opposite-
seed witness. If no composable sealed path exists, preserve a finite cut
certificate naming its first absent interface and the contract it needs. The
latter is only a `PROVED relative to sealed artifact interfaces` statement;
an overlooked sealed constructor falsifies it.

## Provenance-DAG audit

`PROVED relative to sealed builders`: `Cycle63` has frozen predecessors
`Cycle48,Cycle58`; `Cycle87` has predecessors `Cycle81,Cycle86`; `Cycle89`
uses `Cycle86,Cycle87`; and the present upper inverse continues through
`Cycle160 -> Cycle163 -> Cycle164`. The checked builder inputs contain no
edge with input `TransportRow63` and output `UpperAtom87`. The first finite
cut is therefore the absent typed constructor

```text
TransportRow63(alpha,beta,h,j,L_pkt,...) ->
UpperAtom87(c0,d,q,a_(d,q),z_(d,q),...).
```

Required contract: an exact phase identity, branch hypotheses, coefficient
normalization, and an explicit record of beta/payload retention. Cycle 89's
statement that a future inverse *should* produce transport structure is
`CONJECTURED`, not such a constructor. An overlooked sealed builder edge is
the preregistered falsifier of this cut certificate.

## New-engine attempt: beta-payload completion

`CONJECTURED`: replace each scalar upper coefficient `a_(d,q)` by a finite or
Hilbert-valued coefficient carrying the original transport payload
`(beta,h,j,ell,L_pkt)`, or its beta-Fourier character. Define a lifted atom
whose scalar projection is the Cycle-87 atom and whose phase keeps the seed
strip visible. The target is a fibered Cycle-160--164 inverse: fourth-moment
mass must either concentrate in one payload fiber sufficiently to test the
seed predicate, or expose an explicit payload-dispersion obstruction.

Falsifier: an admissible lifted model with the Cycle-162 mass scale but every
payload fiber below the frozen concentration threshold, after all exact
orthogonality/Parseval accounting. This is a new bridge-engine attempt, not a
claim that the present scalar records already carry beta.

No claim is promoted from this ledger. It is the working record for one
substantive Cycle-165 block.
