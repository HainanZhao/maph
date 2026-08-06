# C95 selection: Bollobás--Meir Boolean four-cube gate

## Historical reconstruction

Oracle independently read the C80--C94 program summaries, sealed artifact
headers, and selection/overlap records. C81--C83/C93 close the LEM families;
C84/C93 close the composite-LRC bridge; C85/C89/C90/C94 close the listed
Sidorenko interfaces; C86/C92 and C91 close the Frankl alternatives; and
C87/C88/C91 close the Ryser alternatives. The Boolean \(Q_4\) TSP gate changes
the target, state space, invariant, and falsifier; none of those boundaries
contains a Hamiltonian-cycle optimization on Hamming-cube subsets. This proves
distinctness from the local program history, not novelty.

## Decision

`CONJECTURED` Oracle selection: test the source-defined \(k=4\) Boolean
restriction of the adjusted Bollobás--Meir conjecture. The target is all
nontrivial \(X\subseteq Q_4=\{0,1\}^4\), with cost
\(c(x,y)=d_H(x,y)^2\) and threshold \(32\).

The exact invariant is the rooted Held--Karp value
\[
 D_X(S,v)=\min\{c\text{-cost of a path from }r_X\text{ through }S
 \text{ ending at }v\},
\]
where \(r_X\) is the least labelled member of \(X\). Closing the path to
\(r_X\) gives the cycle optimum. The two-vertex convention counts the sole
edge twice, matching the source's diameter-pair lower bound.

The primary and Oracle reject a cube-automorphism quotient: it would create a
second canonicalization theorem before the first gate. Enumerate all 65,519
labelled subsets directly.

- **Falsifier:** a labelled \(X\) whose exact optimum exceeds 32. Preserve
  its cycle lower certificate and require an independent exact confirmation.
- **Advance condition:** every subset has a directly checked cycle of cost at
  most 32, and the exact DP has no internal inconsistency. This proves only
  the Boolean \(Q_4\) subclass.
- **Stop:** a pass without a source-clear orbit/metric explanation seals the
  finite subclass and stops; do not move to \(Q_5\), rational grids, random
  points, or another dimension.
- **Strongest flaw:** a complete pass may be a low-information finite census
  already implicit in the 2024 extremal work.
