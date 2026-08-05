# Cycle 29 idea selection: semantic primal lift

## Candidate engines and decision questions

1. **Ownership-blocker hypergraph.** For each time, choose a labeled owning
   coordinate. A coordinate's ownership cell is legal exactly when one of its
   allowed digits covers the entire cell; equivalently, the cell contains no
   minimal subset that is missed by every allowed digit. Decision question:
   is this an exact direct-cover equivalence, does a complete H11 control
   reproduce direct feasibility, and does the representation distinguish raw
   masks inside one Cycle-13 divisor color on a frozen p199 leaf?
2. **Rational primal reconstruction.** On one near-one Cycle-28 LP, reconstruct
   an exact rational primal or dual optimum. Decision question: can a fixed
   geometry receive a narrow exact lower-bound certificate? This has a sharp
   verifier but does not itself close a survivor and stays inside the
   audit-sensitive LP family.
3. **Non-class-constant characters.** Give every individual or cyclotomic
   character its own coefficient and derive a direct-CNF interpretation.
   Decision question: does the refined character space escape the Cycle-24--25
   one-class collapse? The direct semantic map is currently absent, so a
   numerical prototype would have a weak claim boundary.

## Questioning the questioning

Why ask for equivalence before searching survivors? A semantic engine that
does not preserve coordinate labels, full-cover feasibility, and exclusion
status can manufacture apparent progress. The smallest exact control is more
discriminating than another 60-row search.

Why might the ownership question mislead? The representation can be a verbose
restatement of choosing one digit per coordinate. Its full minimal-blocker
family may be exponentially large, and low-rank blocker truncations may repeat
Cycle 5--6's weak incompatibility mechanisms. Exact equivalence alone is not
an advance toward LRC unless the representation exposes a tractable invariant.

What framing would hide a collapse? Checking only divisor colors would repeat
Cycle 13. The p199 control must exhibit two allowed digits of the same 2/7
color with different raw-time masks and preserve the distinguishing time in
the semantic local-admissibility relation.

Why reject the simpler rational-LP question now? It can classify one fixed
geometry but has low leaf-closing information after Cycles 22--28 and cannot
repair C28's incomplete audit. Why reject characters now? Their missing exact
direct interface makes the first result likely observational rather than a
new proof mechanism.

## Choice and falsifier

Choose the ownership-blocker hypergraph. It changes the state space from digit
assignments and proof-core embeddings to labeled time ownership with exact
coordinate-local blockers. The main rejected alternative is rational primal
reconstruction because its verifier is stronger but its expected strategic
information is lower.

Before implementation, question the apparent blocker explosion itself. For a
fixed coordinate, a time is characterized locally by its digit-support
signature (D_t=\{d:t\in M_{i,d}\}). A cell is legal exactly when its
signatures have nonempty intersection. A minimal blocker cannot repeat a
signature, so the complete time hypergraph has an exact quotient on support
signatures, with concrete blocker multiplicities recovered from signature
class sizes. This quotient is the intended implementation; enumerating raw
time subsets would preserve the old representation's accidental scale.

The branch is falsified by any finite interface where a direct full cover has
no legal ownership coloring, a legal ownership coloring cannot reconstruct a
direct full cover, minimal-blocker enumeration disagrees with direct local
admissibility, or the frozen p199 same-color distinction disappears. A proved
equivalence that yields only the original full blocker family with no
compressible invariant is a containment outcome, not evidence of progress.
