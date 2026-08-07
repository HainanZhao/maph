# Cycle 3 selection — Lane B growing-genus falsification

## Decision question

For the first certified minimum-genus cubic graph with genus at least two,
does the exact spin-structure tensor

\[
F(q)=\sum_{h\in H_1(\Sigma;\mathbf F_2)}(-1)^{q(h)}W_h(t)
\]

admit a nonmaximal tensor-train cut rank in some symplectic handle ordering,
or an exact recurrence inherited from a smaller slab?

## Question the questioning

The sealed genus-one computation cannot test collective compression: every
four-entry spin-structure table has only one nontrivial matrix cut.  Nor does
the existence of an Arf Fourier formula itself reduce complexity.  The useful
object is therefore the homology-resolved even-subgraph polynomial `W_h`, and
the falsification target is its induced rank under every admissible handle
ordering, not a visually suggestive factorization in one basis.

## Brainstorm and engine comparison

1. **Direct homology-frontier propagation.** Process edges in a path-like
   order, retain only live vertex parities and four homology bits, and forget a
   vertex exactly after its final incident edge.  This computes all `W_h`
   simultaneously.  Its predicted cost is exponential in frontier width and
   genus, not in the full cycle-space dimension.
2. **Character-twisted transfer plus Walsh inversion.** For each character of
   `H_1`, evaluate the signed even-subgraph polynomial independently and apply
   the exact Walsh transform.  This is an independent reconstruction route;
   it duplicates transfer work but gives a label-sensitive check.
3. **Deletion–contraction with labeled-minor memoization.** Carry homology
   labels through graph minors.  This is structurally different, but the state
   key is expected to proliferate on the `4 x 3 x 3` control.  It remains the
   fallback if frontier width exceeds the declared cap.

The direct frontier engine is provisionally preferred because it computes all
sectors in one pass.  It is selected only if it exactly reproduces the sealed
`3 x 3 x 2` sector polynomials and remains below the resource cap on the
genus-two control.  Character-wise reconstruction supplies the independent
route on the calibration graph and at two exact rational specializations on
the genus-two graph.

## Exclusion map

- Former question: does a genus-one cubic slab already show handle
  factorization? Outcome: the four spin-structure entries have exact matrix
  rank two. Delta: this is maximal at genus one and therefore neither evidence
  for nor against growing-genus compression.
- Former question: can unrestricted spin-structure enumeration count as a
  reduction? Outcome: no; the sector count is `2^(2g)`. Delta: Cycle 3 requires
  a measured rank/recurrence reduction or records a falsifier.
- Former method: enumerate the full cycle space. Outcome: exact but
  `2^40` subsets for the free `4 x 3 x 3` box. Delta: that enumeration is
  excluded by the resource stop.

## Frozen experimental contract

- **Input state:** the pinned cellular `3 x 3 x 2` genus-one embedding, then a
  rotation system for the free `4 x 3 x 3` cubic box with 37 faces.
- **Invariant/map:** face-boundary space `B_1`, quotient
  `H_1=Z_1/B_1`, exact polynomials `W_h(t)`, and the Arf-weighted transform over
  quadratic refinements.
- **Smallest direct verifier:** reproduce all four sealed genus-one sector
  polynomials; independently reconstruct them character by character; then
  agree on all sixteen genus-two sectors at `t=1/2` and `t=1/3`.
- **Resource-bounded stop:** never enumerate `2^40` cycles; stop or change
  engine if a frontier pass exceeds 2,000,000 live algebraic states, 8 GiB
  resident memory, or 30 minutes on the `4 x 3 x 3` control.
- **Advance condition:** a provably submaximal TT cut rank in at least one
  symplectic ordering, an exact recurrence surviving a held-out sector/size,
  or a proved frontier-state reduction beyond generic pathwidth times
  `2^(2g)`.
- **Falsifier:** maximal TT cut ranks for every symplectic ordering at two exact
  rational specializations, together with failure of every proposed recurrence
  on a held-out exact sector or box.

## Claim boundary

This note selects a finite exact falsification experiment.  It proves no
compression and makes no thermodynamic claim.
