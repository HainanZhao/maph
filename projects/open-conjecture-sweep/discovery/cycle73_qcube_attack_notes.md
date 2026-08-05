# C73 Q7 attack notes

## Exact reformulation

`PROVED`: A subgraph of \(Q_n\) is \(C_4\)-free exactly when its omitted-edge
set meets every two-dimensional face. Thus
\(\operatorname{ex}(Q_7,C_4)\le304\) is equivalent to saying that every edge
transversal of the 672 square faces has at least \(448-304=144\) edges.

The canonical enumeration uses one variable for each pair
\((u,u\oplus e_i)\) with bit \(i\) of \(u\) zero. It therefore has
\(7\cdot2^6=448\) edge variables. A face is uniquely indexed by directions
\(i<j\) and a base with both bits zero, giving
\(\binom72 2^5=672\) clauses. Each clause forbids selecting all four boundary
edges.

## Exhaustive maximum-degree symmetry split

`PROVED`: Any C4-free graph with at least 305 edges belongs, up to an
automorphism of \(Q_7\), to one of three branches \(\Delta=5,6,7\) encoded by
the generator.

Proof. Its average degree is at least \(610/128>4\), so its maximum degree is
at least five and at most seven. XOR translation maps a maximum-degree vertex
to zero. A coordinate permutation then maps its incident selected directions
to \(0,\ldots,\Delta-1\). Requiring every vertex to have degree at most
\(\Delta\), fixing those \(\Delta\) incident edges present, and fixing the
others absent loses no orbit. The three maximum-degree values are disjoint and
exhaustive.

## Certificate boundary

The SAT sequential counter asserts that at most 143 edge variables are absent.
Its auxiliary variables do not alter the cube-edge model. A SAT model is
checked using only the first 448 variables and an independently generated list
of all faces. An UNSAT result is promoted only if the DRAT proof is accepted by
the pinned independent checker for every one of the three maximum-degree
branches. Solver status or a timeout alone has no epistemic force.

The independent SciPy/HiGHS formulation uses the 448 original binary
variables and 672 inequalities \(\sum_{e\in F}x_e\le3\). It is corroboration,
not a proof certificate for the upper bound.

