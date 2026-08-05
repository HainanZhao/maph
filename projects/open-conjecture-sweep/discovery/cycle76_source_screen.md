# C76 corrected source screen

## Purpose and claim boundary

This is the first selection screen after C75's `OBSERVED` eligibility loss.
It is a bounded literature check, not a proof that a candidate is open or
novel.  No attack code is authorized by this document.

## Required three-part check

Every finalist was screened on 2026-08-05 by: (1) an exact-statement search,
(2) an arXiv-ID/title search, and (3) a current primary-source and citation
check.  A null result is tagged only `OBSERVED`.

### Gupta: LEM cycle-spectrum question

- **Exact statement / source:** Question 14 of Anish Gupta,
  *Balance Constants, Majority Cycles, and the Gold Partition Conjecture
  through Fourteen Elements*, arXiv:2607.23926v2 (30 July 2026), asks whether
  the full LEM digraph \(D(P)\) and its incomparable-edge subdigraph
  \(D_{\rm inc}(P)\) have the same cycle spectrum for every finite poset.
- **Known scope:** Proposition 7 excludes comparable edges only from
  3-cycles.  The source explains why its shortening argument does not
  preserve a 4-cycle and reports exhaustive agreement through order 14.
- **Current check — OBSERVED:** exact-question and arXiv-ID/title searches
  found no later resolution by 2026-08-05.  The paper is too recent for this
  null citation signal to carry much weight.
- **Small rigorous gate:** settle the length-4 implication, or give an exact
  finite poset witnessing a full-majority 4-cycle absent from
  \(D_{\rm inc}(P)\).  A triangle created by shortening is not enough.

### Song--Chen: compatible-marginal spin alignment

- **Exact statement / source:** Conjecture 2 of Zhiwei Song and Lin Chen,
  *A counterexample to the strong spin alignment conjecture*,
  arXiv:2603.25410, asserts majorization for the compatible marginals of one
  global \(n\)-partite state.
- **Known scope:** Proposition 3 establishes the three-qubit, two-body
  support case only for \(Q=I/2\), with arbitrary nonnegative weights.  The
  unrestricted strong conjecture is already false because its independently
  chosen marginals are incompatible.
- **Current check — OBSERVED:** exact-statement and arXiv-ID/title searches,
  followed by a current record/citation check, found no later proof or
  refutation by 2026-08-05.  An official OpenAI search for the exact name and
  formula returned no announcement; the current First Proof list is also
  disjoint from this target.
- **Small rigorous gate:** with three qubits, uniform two-body weights and
  \(Q=\operatorname{diag}(q,1-q)\) for rational \(q>1/2\), seek a rational
  global state violating a Ky Fan inequality; certify any candidate by exact
  characteristic-polynomial and root-isolation calculations.  A null search
  is not positive evidence.

### Post-C72 Ryser \(r=6\)

- **Current project fact — PROVED:** C72 establishes \(D(H)\ge6\) for an
  intersecting six-partite six-uniform hypergraph with \(\tau(H)=6\).  It
  does not prove Ryser's conjecture or eliminate \(D=6\) cores.
- **Current check — OBSERVED:** no current primary source was found that
  closes the general \(r=6\) case.  This is retained as a candidate only;
  neither a direct enumeration nor a defect ladder is a default next step.
- **Small rigorous gate:** formulate a new global dual certificate or a
  falsifiable structural classification of a \(D=6\) equality core.  A raw
  finite census has no credible bridge and therefore fails this gate.

## Selection discipline

Question: which target has the shortest route from a rigorous first gate to a
durable theorem or counterexample?  Question the questioning: C75 shows that
apparent low dimension is useless if the problem is already closed; freshness
can also disguise a shallow citation record rather than tractability.  The
selection must therefore value a discriminating exact gate and a credible
bridge more than familiar vocabulary or small matrices.

Oracle receives this packet and independently proposes and ranks mechanisms.
The ensuing selection must record its main rejected alternative, strongest
flaw, falsifier, expected information gain, and 50-cycle pivot test before an
attack preregistration is written.
