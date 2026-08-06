# C95 candidate screen: Bollobás--Meir Boolean four-cube gate

This is source/selection scratch only. It authorizes no computation.

## Current source scope

`OBSERVED` from Gordeev, *Bollobás--Meir TSP Conjecture Holds
Asymptotically*, arXiv:2603.22010v1, Introduction / Conjecture 1.6:
the adjusted conjecture remains open for every \(k>2\). It asks that every
finite \(X\subseteq[0,1]^k\) have a Hamiltonian cycle \(H\) with
\[
 \sum_{e\in H}|e|^k\leq 2k^{k/2}\quad(k\ne3),
\]
and with the revised \(2^{7/2}\) bound at \(k=3\). The source states that
the original bound is false at \(k=3\), so that original formulation is not
a target. URL: <https://arxiv.org/abs/2603.22010>.

`PROVED` from Balogh--Clemen--Dumitrescu, *On a Traveling Salesman Problem
for Points in the Unit Cube*, Algorithmica 86 (2024), Theorem 1.4 and the
discussion of \(k=4\): for all sufficiently large \(k\) (with the source's
bound \(k_0<30\)), every subset of cube vertices meets the original cycle
bound. It records two \(k=4\) vertex subsets attaining cost \(32\), but that
theorem does not cover all \(k=4\) subsets. URL:
<https://link.springer.com/article/10.1007/s00453-024-01257-w>.

`OBSERVED`: the official OpenAI mathematics announcement checked in this
discovery pass concerns the planar unit-distance problem, not this TSP
conjecture. This is bounded eligibility evidence only.

## Candidate gate, not yet selected

Let \(Q_4=\{0,1\}^4\). For \(X\subseteq Q_4\) with \(|X|\ge2\), use the
complete graph on \(X\) with integer edge cost
\[
 c(x,y)=|x-y|_2^4=d_H(x,y)^2.
\]
The candidate decision question is whether every such \(X\) has a Hamiltonian
cycle of total cost at most \(32=2\cdot4^{4/2}\). The opposite pair already
has cost \(32\), so the threshold is sharp within this class.

- **State:** a subset of the sixteen labelled Boolean four-cube vertices and
  a rooted Hamiltonian-cycle DP state \((S,v)\), modulo only a frozen cube
  automorphism if that quotient is independently checked.
- **Smallest direct verifier:** exact integer Held--Karp minimization for all
  \(2^{16}-17\) nontrivial subsets, with a separately implemented direct
  cycle evaluator on every emitted extremal witness.
- **Falsifier:** one labelled subset with certified optimum greater than \(32\);
  it would disprove the adjusted \(k=4\) conjecture outright.
- **Pass boundary:** a pass proves only the Boolean-vertex \(k=4\) subclass,
  not arbitrary points of \([0,1]^4\), another dimension, or the general
  conjecture. It merits continuation only if an orbit/metric argument
  explains the extremal bound; otherwise it is a finite control, not a new
  census ladder.
- **Stop:** a counterexample ends the global target; a pass without a
  source-clear structural lemma ends this gate without moving to \(Q_5\),
  rational grids, or random point sets.

## Historical-risk note

This is a new target vocabulary and must not be selected merely because it is
small. Oracle must compare it against every relevant C80--C94 boundary and
identify a genuine information gain beyond a brute-force finite census.
