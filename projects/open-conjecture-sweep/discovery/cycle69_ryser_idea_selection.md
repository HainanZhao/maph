# C69 creative selection: intersecting Ryser at r=6

Status: `EXPLORATORY`; no claim or executable experiment is implied.

Candidate A — critical-cover kernel.  Freeze a minimal counterexample with
\(\tau\ge6\), delete redundant edges and vertices, and seek a forced small
degree/part profile whose local cover exchange lowers \(\tau\).  Falsifier:
an exact critical finite system satisfying every proposed profile inequality
without a five-cover.

Candidate B — fractional dual obstruction.  Turn the absence of a five-cover
into a normalized fractional matching certificate and try to use pairwise
intersection plus the six-part partition to force total weight at most five.
Falsifier: an explicit feasible fractional matching on an intersecting
6-partite system whose mass defeats the proposed inequality.

Candidate C — 13-edge extremal interface.  Use the known exact extremal
construction scale as a bounded SAT/isomorph-free classification target and
look for a theorem that every minimal counterexample has an edge bound placing
it in that interface. Falsifier: a rigorously derived critical system outside
the bound, or no structural route to the bound.

Question the questions: A can mistake a local degree profile for a global
cover mechanism; B may only recover the weaker fractional transversal bound;
C risks becoming another blind census.  The sharper first question is A:
does minimality plus intersecting 6-partite incidence force a cover-exchange
reduction that is not visible in the fractional relaxation?  It has a direct
countermodel, can absorb known extremal examples as controls, and—unlike C—can
yield a theorem without a finite-size assumption.  B is retained as the main
rejected alternative because it may expose a dual invariant if A collapses.
