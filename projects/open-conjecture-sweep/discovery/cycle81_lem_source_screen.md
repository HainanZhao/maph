# C81 LEM 4-cycle source and eligibility screen

## Exact target

For a finite poset \(P\), let \(D(P)\) have the strict majority edge
\(x\to y\) when \(\Pr[x\prec y]>1/2\), and let \(D_{\mathrm{inc}}(P)\)
retain only edges between incomparable elements. Question 14 of Anish Gupta,
*Balance Constants, Majority Cycles, and the Gold Partition Conjecture through
Fourteen Elements*, arXiv:2607.23926v2, asks whether these two digraphs have
the same simple-cycle spectrum for every finite \(P\).

- `PROVED` source scope: Proposition 7 proves that no directed triangle in
  \(D(P)\) can use a comparable edge.
- `OBSERVED` bounded evidence: the source's exact census finds equal spectra
  for every poset through order 14 (Observation 11); it explicitly labels
  every longer-cycle assertion as Question 14, not a theorem.
- `OBSERVED` eligibility: refreshed exact-title/identifier searches and the
  official OpenAI-result screen on 2026-08-05 found no announced resolution
  or OpenAI overlap. This is not a universal novelty claim.

Source locations: Section 4.1, Proposition 7 and its proof; Section 4.2,
Observation 11; Section 8, Question 14. The primary paper is a recent
preprint, so it is an exact problem statement and evidence source, not
authority for a new theorem.

## First exact gate

Every comparable edge is a dominance edge: if \(x<y\), then
\[
 z\to x\quad\Longrightarrow\quad z\to y,
\]
because the event \(z\prec x\) is contained in \(z\prec y\). The same
monotonicity holds for threshold probabilities but does not by itself shorten
a directed 4-cycle to a directed triangle.

The first C81 question is therefore deliberately weaker and falsifiable:
does this dominance axiom alone force every directed 4-cycle in
\(D_{\mathrm{inc}}\cup <\) to have a directed 4-cycle in
\(D_{\mathrm{inc}}\)? Construct the smallest abstract digraph satisfying the
axiom and a full 4-cycle but no incomparable-only 4-cycle, or prove this
finite implication at the frozen small size.

- **Falsifier of the proposed mechanism:** a valid abstract dominance
  countermodel. It does not refute Question 14, but it rejects a proof using
  dominance alone.
- **Advance condition:** if dominance survives, identify one genuinely
  poset/linear-extension-specific invariant absent from the abstract model;
  otherwise pivot rather than enumerate posets.
- **Main rejected alternative:** a fresh finite poset census merely repeats
  the published order-14 evidence and cannot prove the universal statement.
