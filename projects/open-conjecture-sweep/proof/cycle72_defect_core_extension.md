# Exact closure of one C71 defect-five equality core

**Theorem (`PROVED`, scoped).** Let (C) be the 11-line six-partite
hypergraph reconstructed from the satisfying `pairs` and `maps` witness of
`cycle71_defect5_core_csp.cpp`.  It has (D(C)=5) and
(	au(C)=3).  If (L) is any further six-partite line for which
(C\cup\{L\}) remains intersecting and has defect five, then (L) is one
of exactly two explicit lines.  The two lines are compatible with one another,
and the maximal resulting 13-line extension has defect five and transversal
number four.

**Proof.** Since every pair of lines in (C) intersects and (D(C)=5),
preserving defect five gives

\[
 0=D(C\cup\{L\})-D(C)=\sum_{E\in C}(|L\cap E|-1).
\]

Every summand is nonnegative, so (L) meets each of the 11 core lines in
exactly one vertex.  In a fixed part, a vertex outside the core has empty
incidence trace on those 11 lines; hence all such outside vertices have the
same role for this one-line condition.  It is enough to enumerate the core
vertices in each part plus one `fresh` representative: (7\cdot6^5=54,432)
six-tuples.

The exact enumeration in `cycle72_defect_core_extension.py` leaves precisely
the following two lines (part labels begin at zero):

\[
\begin{aligned}
L_0={}&\{(0,f0),(1,b0\_1),(2,b1\_5),(3,r2),(4,b3\_4),(5,b4\_3)\},\\
L_1={}&\{(0,f0),(1,b0\_3),(2,b1\_4),(3,b2\_5),(4,r3),(5,b4\_2)\}.
\end{aligned}
\]

Neither uses `fresh`; therefore the representative argument covers arbitrary
ambient vertex sets, not only a bounded vertex universe.  The two lines meet
once (at ((0,f0))), and exhaustive cover search gives

\[
 \tau(C\cup\{L_0,L_1\})=4,
\]

with an explicit four-cover printed by the replay.  The independent checker
reconstructs the core separately, re-enumerates all 54,432 tuples, and checks
the cover lower bound by exhaustive subsets. \(\square\)

**Boundary.** This closes only the extension family containing this particular
locally satisfiable C71 equality core while keeping (D=5).  It neither
classifies all (D=5) equality cores nor proves the intersecting (r=6)
Ryser conjecture.
