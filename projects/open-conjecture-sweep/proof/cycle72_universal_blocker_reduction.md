# Universal-blocker reduction at defect five

**Theorem (`PROVED`, conditional interface).** Let \(H\) be a finite simple
intersecting six-partite six-uniform hypergraph with \(D(H)=5\). Suppose every
rooted C71 equality core \(C\) has a set \(B\subseteq V(C)\), \(|B|\le5\),
that meets all 11 lines of \(C\) and every trace

\[
 T=L\cap V(C)
\]

of a six-partite line \(L\) satisfying \(|L\cap E|=1\) for every \(E\in C\).
Then \(\tau(H)\le5\). Consequently, proving the stated blocker property for
all rooted equality cores upgrades the C71 conclusion for a hypothetical
\(\tau=6\) counterexample from \(D(H)\ge5\) to \(D(H)\ge6\).

**Proof.** Assume for contradiction that \(\tau(H)=6\). C71 and the published
maximum-degree inequality give a vertex \(v\) of degree \(d\ge6\). Equality in

\[
 D(H)\ge \sum_{r\ne v}\binom{k_r}{2}\ge |R|\ge5
\]

forces \(|R|=5\), with every \(r\in R\) on exactly two \(v\)-star lines. For
each \(r\), the five vertices \(\{v\}\cup(R\setminus\{r\})\) do not cover
\(H\), so there is a non-star witness \(W_r\) with \(W_r\cap R=\{r\}\).
The witness meets two star lines at \(r\); its other four noncentral
coordinates lie outside \(R\) and meet at most one star line each. Hence
\(d\le2+4=6\), and therefore \(d=6\).

The six star lines and five singleton witnesses form a rooted 11-line core
\(C\). Equality gives \(D(C)=D(H)=5\). All excess-pair terms are nonnegative,
so every line \(L\in H\setminus C\) meets every \(E\in C\) exactly once.
Thus \(L\cap V(C)\) is an individually compatible trace. The assumed set
\(B\) hits the core and every such trace, hence every line of \(H\),
contradicting \(\tau(H)=6\). \(\square\)

**Finite-interface boundary.** A trace has at most one core vertex per part;
an absent coordinate represents an arbitrary fresh vertex. One fresh symbol
per part is exact because blockers are restricted to \(V(C)\). No simultaneous
compatibility among trace types is needed for the forward implication. A core
without a universal blocker refutes only this stronger sufficient mechanism:
its troublesome traces may not coexist in any full defect-five hypergraph.

**Enumeration obligation.** “All rooted cores” must include arbitrary parts
of the five repeated vertices, arbitrary identifications of witness vertices
in the central part, all star-pair choices, and every exact-intersection map,
up to proved relabellings of parts, star lines, and witnesses.

