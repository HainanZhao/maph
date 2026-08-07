# Cycle 4 failure ledger

## Direct symplectic-basis extension

- Proposed claim: appending a new symplectic pair to the Cycle 3 ordered basis
  preserves its rank-seven relation.
- Result: `CERTIFIED_NUMERICAL` (exact modular nonzero minors at two rational
  evaluations).  The profile is maximal `(2,4,8,16,8,4,2)` and the old row
  equality fails coefficientwise.
- Disposition: **KILLED** for this exact ordered-basis extension.  No claim is
  made about all symplectic bases.

## Naive closed-homology inclusion

- Proposed claim: deletion-compatible rotations automatically give
  `B_4 subset B_5`, so old closed-surface homology embeds without refinement.
- Result: `CERTIFIED_NUMERICAL` (exact GF(2), radius zero).  For the pinned
  compatible rotation, `dim(B_4 intersect B_5)=33<34`; one old facial
  boundary maps to a nonzero new homology line.
- Disposition: **KILLED**.  It is replaced by the derived relative-sector
  identity, not by assuming away the missing dimension.

## Zero-defect compatible-rotation search

- Proposed claim: another rotation in the exact deletion-compatible ansatz
  might have genus four and zero facial-boundary defect.
- Result: `OBSERVED`.  A deterministic simulated-annealing run with seed
  `20260811` tested 5,000,000 mutations, repeatedly reached the 45-face
  genus-four census, and found best defect one, never zero.
- Disposition: unresolved bounded search only.  This is not a no-go theorem
  for the ansatz and is not used to prove that the defect is necessary.

## Adapted-label description correction

- Earlier live prose described the two adapted label-`96` added edges as
  carrying `d` alone.
- `CERTIFIED_NUMERICAL`: in the declared adapted coordinate basis, `d` is
  coordinate `64`; label `96=32+64` is the last old coordinate plus `d`.
- Disposition: corrected in the live relative-theta note before sealing.  The
  exact label counts, three-bit support, sector identity, and replay output
  were unchanged; only the semantic description was wrong.
