# Certifying branch-and-bound

## Node relaxation

A search node partitions the pools into included \(I\), excluded \(E\), and
free \(F\).  The binary activation cost is already fixed for pools in
\(I\), absent for pools in \(E\), and relaxed independently for pools in
\(F\).  Its Lagrangian upper bound is

\[
B_{I,E}(\lambda)
=\lambda Q
+\sum_{i\in I}\left(h_i(\lambda)-q_i\right)
+\sum_{i\in F}\max\{0,h_i(\lambda)-q_i\},
\tag{1}
\]

where

\[
h_i(\lambda)=\sup_{x\geq0}\{f_i(x)-\lambda x\}.
\]

Every completion of the node's activation assignment is bounded by (1).
An included pool pays \(q_i\) even when its relaxed input is zero; this is
essential for validity after branching on its activation binary.

For an included pool, the analytic conjugate changes formula at its initial
marginal output \(b_i\gamma_i/a_i\).  For a free pool, its truncated net
conjugate changes formula at the gas-adjusted activation threshold.  Between
these breakpoints, (1) has the same
\(D-C/\sqrt{\lambda}\) derivative as the root relaxation.  The exact-real
node minimum is therefore found by enumerating breakpoints and the one
possible stationary point per interval.

## Search

The implementation keeps the open node with the largest upper bound in a
priority queue.  At each node it:

1. evaluates the water-filled route suggested by the relaxed support and
   updates the global incumbent;
2. branches on the free pool with the largest relaxed allocation;
3. computes analytic bounds for the include and exclude children;
4. prunes a child when its bound is within the requested tolerance of the
   incumbent.

A node limit may stop the search early.  The maximum bound among open and
closed nodes is retained, so the returned route still has a valid
a posteriori gap.  With no node limit, the method either exhausts or prunes
the finite binary tree.

As elsewhere in this prototype, the reported bound has a floating-point
roundoff cushion but is not a formal interval-arithmetic certificate.

## Seeded prototype result

`scripts/benchmark_branch_and_bound.py` compares the method with exhaustive
enumeration.  On the default heterogeneous generator, a strong initial
route and the root dual bound often close the instance immediately.  A
local run on 2026-07-27 explored a median of one node for 8, 10, and 12
pools; exhaustive enumeration took progressively longer.

The structured SUBSET-SUM reduction is harder and exposes the expected
weak-hardness boundary.  In the same run, the 16-pool reduction explored
1,243 nodes.  This was still below the full binary tree, but the result is
one seeded instance, not a scalability claim.

Timing is machine-dependent.  Node counts, oracle agreement, and certified
gaps are the primary reproducible outputs.
