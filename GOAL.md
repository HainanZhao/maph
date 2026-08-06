# Research goals

The user has selected every research topic in this file. Following this goal
means carrying all three topics to mathematical resolution, not merely
screening them, running bounded searches, proposing approaches, or preparing
a shortlist.

**Overall status:** `OPEN (0/3 resolved)`.

The overall goal is complete only when each numbered topic has one of these
outcomes:

1. a proof of its stated universal claim with all hypotheses checked;
2. an exact counterexample independently verified against the statement; or
3. a verified prior result that already resolves precisely the same claim.

A finite search without a counterexample, a resource limit, a method-family
no-go, or a publishable partial result does not resolve a topic and does not
permit removing or replacing it. Work may proceed in the order below, but all
three completion conditions are conjunctive.

## Execution order

| Order | Target | Topic status | First exact gate |
| --- | --- | --- | --- |
| 1 | covering number \(C(23,6,2)\) | `OPEN` | 20-block witness or SAT/DRAT no-go |
| 2 | q-analog Conjecture 5.4 at \(k=4,r=4\) | `OPEN` | exact coefficient-difference sign |
| 3 | q-Fibonomial unimodality at width 4 | `OPEN` | exact coefficient-difference sign |

## 1. The exact covering number \(C(23,6,2)\)

- **Claim:** `CONJECTURED`. Decide whether 20 six-subsets of a 23-set cover
  all pairs. The current La Jolla tables give lower bound 20 and a 21-block
  construction, hence the exact value is 20 or 21.
- **Direct verifier:** check all \(\binom{23}{2}=253\) pairs in a proposed
  20-block family. A no-go requires a symmetry-broken SAT encoding and an
  independently checked DRAT certificate.
- **Proposed mechanism:** derive pair-degree and block-intersection constraints
  before SAT to reduce the incidence patterns. This is a finite decision
  problem, not a heuristic search.
- **Stop rule:** a 20-block witness or a checked UNSAT certificate is complete;
  an unverified solver status is not a result.
- **Sources:** [La Jolla upper-bound table](https://ljcr.dmgordon.org/cover/table.html)
  and [lower-bound table](https://ljcr.dmgordon.org/cover/low_tab.html), both
  current in 2026.

## 2. q-analog Conjecture 5.4: the \(k=4,r=4\) slice

- **Claim:** `CONJECTURED`. For all positive integers
  \(a_1,a_2,a_3,a_4,b\), if one \(a_i\) is divisible by four or
  \[
  b\le1+\sum_{i=1}^{4}\left\lfloor a_i/4\right\rfloor,
  \]
  then \([a_1]_q[a_2]_q[a_3]_q[a_4]_q[b]_{q^4}\) is unimodal.
- **Status:** this is the source's named Conjecture 5.4. The authors checked
  their general conjecture through \(k\le5,r\le6\), with parameters at most
  15. A separate exact local sweep found no counterexample in this slice for
  every nondecreasing \(a_i,b\le20\): 143,440 admissible tuples. This is
  `OBSERVED`, not proof; replay it with
  `python3 discovery/goal_qanalog_k4r4_sweep.py --limit 20`.
- **Direct verifier:** multiply the five finite geometric series in exact
  integer arithmetic and inspect successive coefficient differences. Any
  descent followed by an ascent refutes the claim.
- **Proposed mechanism:** each coefficient counts bounded solutions of
  \(x_1+x_2+x_3+x_4+4y=d\). Prove an injection or interval dominance between
  consecutive degree fibers under the displayed inequality.
- **Stop rule:** an exact counterexample disproves the slice; a uniform fiber
  injection or coefficient-difference proof settles it.
- **Primary source:** Connelly--Ito--Martinez--Shevchenko--Yang, Conjecture
  5.4, <https://arxiv.org/html/2605.12822>.

## 3. Fixed-width q-Fibonomial unimodality: the \(n=4\) slice

- **Claim:** `CONJECTURED`. For every \(m\ge1\), prove or refute the
  unimodality of
  \[
  \left[\!\begin{matrix}m+4\\4\end{matrix}\!\right]_{\mathcal F}.
  \]
- **Status:** the current primary source proves the full conjecture only for
  widths \(n\le3\). An exact local sweep for \(m=1,\ldots,10\) found no
  counterexample: `OBSERVED`, not proof; replay it with
  `python3 discovery/goal_qfibonomial_width4_sweep.py --limit 10`.
- **Direct verifier:** form the exact quotient
  \[
  \frac{[F_{m+1}]_q[F_{m+2}]_q[F_{m+3}]_q[F_{m+4}]_q}
       {[2]_q[3]_q}
  \]
  and inspect successive coefficient differences.
- **Obstacle / proposed mechanism:** the source explicitly says that its
  available q-analog factorization does not cover width four. First supply a
  new factorization or a tiling recurrence; only then seek periodic
  coefficient inequalities.
- **Stop rule:** a proof or counterexample settles this fixed-width slice; a
  computation-only range extension does not.
- **Primary source:** same paper, Conjecture 1.1 and §5.2,
  <https://arxiv.org/html/2605.12822>.

## Out of scope

- Alon--Jaeger--Tarsi nowhere-zero mappings, finite-cyclic Fuglede,
  projective planes of order 12, HRT, and strong Littlewood lack a small,
  discriminating first gate for this program. They are not part of this goal.
