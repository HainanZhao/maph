# Cycle 7 exact residual-translate feasibility argument

## Claim boundary

This is a finite pre-emission cut under the frozen cyclic-cover conventions.
It does not prove a Lonely Runner statement, a lift, or an equivalence with
the Cycle-6 triple hypergraph.

For residual uncovered times (W) and (r) remaining centers, define
\(\operatorname{FEAS}(W,r)\) to mean that there are centers
\(x_1,\ldots,x_s\), with \(s\le r\), such that

\[
W\subseteq (B-x_1)\cup\cdots\cup(B-x_s).
\]

**Lemma.** If a partial cyclic-cover state has a completion using its
remaining \(r\) centers, then \(\operatorname{FEAS}(W,r)\) is true.

**Proof.** The remaining centers in the completion define at most \(r\)
translates of \(B\). Each currently uncovered time must lie in at least one
of those translates, exactly giving the displayed containment. ∎

The exact solver selects an uncovered time, branches over every center whose
translate covers it, subtracts that translate from the residual mask, and
decrements \(r\). It returns true at the empty mask and false at positive mask
with \(r=0\). This exhausts every possible first covering center; deterministic
memoization preserves the result for an identical \((W,r)\) subproblem.
Therefore only an exact false result is a sound prune. A cap, cache anomaly,
or unverified result retains the state.
