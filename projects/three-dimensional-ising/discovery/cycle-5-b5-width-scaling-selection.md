# Cycle 5 / Gate B5 selection

## Decision question

Does Lane B contain topological compression beyond ordinary fixed-frontier
transfer when the cross-section of
`G_(n,w)=P_n square P_w square P_w` grows, or is the exact result only a strip
algorithm whose rank is exponential in `w^2`?

## Question the questioning

The equality `256=2^(9-1)` may have been misread as independent topology.  A
zero-field spin slice modulo global spin flip and an even connector-parity
slice are finite Pontryagin duals.  The first attack must therefore seek the
explicit Walsh intertwiner before interpreting any rank reduction as new.

Conversely, ordinary bounded pathwidth does not automatically explain why an
entire exponentially large spin-structure component has bounded rank in the
length direction.  After quotient equivalence is settled, the remaining
question is whether locality of the homology labels yields rank growth in `w`
that is smaller than the physical frontier `2^(w^2-1)`.

## Brainstorm and selected mechanism

Alternatives considered:

1. compute larger fixed-width TT tensors directly;
2. derive a general Fourier duality between quotient spins and even masks;
3. search new minimum-genus rotations independently for each width;
4. use arbitrary cellular embeddings and separate genus from transfer rank.

The selected order is (2), then a hybrid of (3) and (4).  It has the smallest
direct falsifier and prevents expensive width-four work from certifying only a
standard transfer-matrix fact.

## Exclusion map

| Former question | Outcome/falsifier | State or invariant delta |
|---|---|---|
| Does fixed `3x3` genus growth destroy collective compression? | No: Cycle 4 proves bounded handle-site TT rank. | Replace fixed-width survival by width scaling. |
| Is the 256-state homology frontier intrinsically topological? | Open; an invertible Walsh intertwiner would refute that interpretation. | Compare full transition operators, not state counts. |
| Does the `3x3` result imply a cubic-box route? | Explicitly excluded. | `w` is now a variable and area scaling is the gate invariant. |

## Exact protocol

- Input state: Cycle 4 conventions, rotations, and character transfer.
- Map: character table between `F_2^(w^2)/<1>` and the even-mask subspace.
- Smallest verifier: exact symbolic `w=2`, exact finite-field `w=3`.
- Advance condition: a proved `R(w)` plus exact/certified ranks at `w=2,3,4`
  that distinguish physical-frontier and spin-structure contributions.
- Stop condition: 8 GiB resident memory or 30 minutes for one optimized run;
  use nonzero-minor certificates rather than dense `w=4` matrices.
- Falsifier: failure of the operator intertwining identity, or an exact minor
  forcing area-exponential rank in the purported topological component.
