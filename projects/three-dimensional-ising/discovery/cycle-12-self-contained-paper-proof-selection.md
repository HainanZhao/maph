# Cycle 12 — self-contained separator-paper proof revision

## Decision question

Can the two grid-strip headline claims be verified from the manuscript
without treating scripts, finite-width tables, or sealed JSON as the
arbitrary-width proof?

## Question the questioning

The prior question was whether exact certificates and proof sketches were
consistent with the claimed rank bounds.  That audit succeeded at the level
of frozen computations but did not establish that the exposition contains
all geometric and combinatorial arguments.  The new question is therefore
not another rank computation.  It is whether the proof interfaces are
complete and human-verifiable.

## Exclusion map

| Former mechanism | Outcome/falsifier | Required state delta |
|---|---|---|
| infer polynomial-ring TT from cut ranks | invalid over a general integral domain | either construct compatible mask cores or retain only a fraction-field TT |
| infer dual connectivity from BFS layer sizes | layer counts do not specify edges | print a parent map or complete contracted quotient edge set |
| cite encoder scripts/JSON | finite checks do not prove all widths | give a symbolic odd/even shell induction and readable bases |
| say characters are behind/ahead | does not exhibit H1–H3 | define relative chains, cocycles, zero-cochains, trace functions, and quadratic split |
| use “cap boundary walks” as geometry proof | hides rotation/cellularity | define dart permutations and trace face orbits |

## Selected mechanism

Input state: the integrated manuscript, the frozen Cycle 7/8/10 proof
documents, and their conventions.

Invariant: at every promotion step, a referee can reconstruct the finite
mathematical object and check the universal argument from printed formulas.
Computation is labeled as an audit only.

Smallest direct verifier: compile the manuscript and check that every
headline dependency points to an explicit lemma whose proof contains its
objects and maps.  For finite witnesses, print the complete specialization
and minor.

Stop criterion: do not restore PROVED labels until (i) the co-core/collar
topology, (ii) H1–H3 after triangular correction, (iii) compatible
polynomial-ring cores or an explicit weakening, and (iv) both encoder
quotient trees are self-contained.

Falsifier: any step that still requires an undisclosed program output,
unprinted base case, or a layer count without an edge/parent description.

## Brainstormed alternatives

1. Keep a short paper and move all constructive proofs to a formally included
   supplement.
2. Replace the explicit encoder induction by a matroid-intersection theorem
   with a symbolic min–max proof.
3. Retain only the abstract separator theorem and publish the grid statements
   later.

The current choice is (1), with immediate claim weakening wherever the
included proof is not yet complete.

## Contained proof-text discrepancy

Exact reconstruction of the opposite-phase contracted dual quotient found
that the frozen working proof's breadth-first counts were transcribed
incorrectly.  The quotient remains a tree, but its layers are

- `1, 2W-3, W-2, W-1` for odd `W>=5` (including `1,7,3,4` at `W=5`);
- `1, 2W-4, W-2, W-2, 3` for even `W>=6`.

The former formulas undercounted the second layer by one for every `W>=7`
and gave a different, nonmatching `W=5` decomposition.  The revised
manuscript prints complete symbolic parent families.  The scratch audit
`discovery/diagnose_g1_opposite_quotient.py` reconstructs the quotient edge
set from the declared rotations and recurrences and matches those families
through width 20; this finite check is an audit, not the arbitrary-width
proof.

Both normal and opposite width-four base traces are now included in the
compiled manuscript.  Each prints a 79-edge primal parent witness, all 16
terminal-forest components, and an 89-edge parent tree reaching all 90 dual
faces.  This closes the finite base-trace obligation.  The encoder lemma
remains `PROOF INCOMPLETE` only because the exceptional homology relations
and their terminal-cut coordinates have not yet been derived from those
printed cuts in the text.

## Publication state

Zenodo version DOI `10.5281/zenodo.21845273` was reserved on 2026-08-08 in
draft deposition `21845273`.  The draft is unsubmitted and contains no files.
The DOI is not registered or public.  It will be inserted into the working
source so that the eventual deterministic archive is DOI-bearing, but no
upload or publication occurs until the proof, extracted-replay, inventory,
checksum, and default-preview gates pass.
