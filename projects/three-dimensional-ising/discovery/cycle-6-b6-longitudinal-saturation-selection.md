# Cycle 6 / B6.2 selection: longitudinal saturation

## Decision question

At fixed transverse widths `w=3` and `w=4`, what are the exact growth and
saturation values of the twist-tensor ranks at cuts between complete
symplectic handles and cuts inside one handle?  In particular, does the rank
at `w=3` stop at the ordinary carrier dimension `256`, or does the locally
coupled twist data require the proved extra factors `4` and `8`?

## Question the questioning

The raw central ranks `8` and `32` at `n=4` only show that the earliest twist
bits do not cancel.  They do not measure saturation.  Likewise, reaching rank
`256` at `w=3,n=9` reaches the ordinary physical carrier but does not prove a
plateau: the Cycle 4 factorization permits ranks `1024` between handles and
`2048` inside a handle.  Therefore the decisive invariant is not the first
carrier crossing, but an exact lower bound meeting an all-size factorization
upper bound.

## Exclusion map

- Former question: is the 256-state homology frontier a new topological
  carrier?  Outcome/falsifier: `QH=2^(w^2)HK` proves it is the conventional
  zero-field flip-even slice transfer.  Delta: factor out that ordinary
  carrier and measure only simultaneous twist propagation.
- Former question: do `n=4,w=3,4` full ranks imply area-exponential growth?
  Outcome/falsifier: two widths and one longitudinal size cannot imply an
  asymptotic law.  Delta: determine `R_infinity(w)` before comparing widths.
- Former question: should the next width be `w=5`?  Outcome: excluded by the
  user until B6.2 saturation is resolved.  Delta: all current compute increases
  `n`, not `w`.

## Selected mechanism and alternatives

Selected: expose the Cycle 4 repeated-handle MPS bond at a central cut and
certify its two boundary maps.  This seeks a full-rank factorization witness
using matrices no larger than the asserted bond, instead of first forming the
entire exponentially large twist tensor.

Materially different alternatives considered:

1. Dense construction of all `2^(2n-2)` twist values followed by Gaussian
   elimination.  It is the clearest control for `n<=10` but wastes both time
   and memory near the predicted `1024/2048` plateaus.
2. A determinant recurrence in `n`.  This could prove saturation uniformly,
   but no recurrence has yet been derived; it remains a theorem-development
   route if factorized boundary maps reveal repeated blocks.
3. Randomized numerical SVD.  Rejected for closure because it cannot certify
   a nonzero symbolic minor.

## Frozen experiment

- Input state: the Cycle 5 frozen embedding, homology labels, bit ordering,
  intersection form, and three weight regimes.
- Map/invariant: finite-field rank of the `F(lambda)` flattening, tagged as a
  pair cut or handle-internal cut; compare it to the exact Cycle 4 MPS bond
  bound and to `d_w=2^(w^2-1)`.
- Smallest verifier: continue `w=3` from `n=9` through `n=12`; retain prime,
  weights, labels, order, pivots or an equivalent replayable full-minor
  transcript, and invertibility of every normalization.
- Advance condition: for each cut type, a nonzero minor whose size equals the
  explicit all-size upper bound, thereby proving `R_infinity`; or a smaller
  exact factorization proving a lower plateau.
- Stop criterion: one optimized run below 30 minutes and aggregate memory
  below 8 GiB.  If that cap prevents closure, record the last exact rank and
  leave saturation unresolved.
- Falsifier: a zero proposed full-size minor, disagreement between dense and
  factorized routes on overlapping sizes, or a later rank exceeding a claimed
  plateau.

## Claim discipline

Finite-field nonzero minors establish that the corresponding symbolic
determinants are not identically zero when all reductions and denominators are
valid.  They do not establish nonvanishing at every physical temperature.
No result at `w=3,4` alone is an area-exponential theorem or a solution of the
three-dimensional Ising model.
