# C85 selection: a completely-positive triple-kernel route for the Möbius ladder

## Creative comparison

`CONJECTURED` candidates after C84 were: a height-four optimal-element
extension for Frankl, a global inverse/dual construction for intersecting
Ryser at \(r=6\), and a tensor-representation reduction for
\(K_{5,5}\setminus C_{10}\).  The first has a new height-three source but no
nontrivial height-four invariant yet; the second has no small exact interface
after C72's blocker saturation.  The third has a concrete Fubini reduction to
a nonnegative completely-positive tensor and is distinct from C68's
fixed-\(S_3\) conjugacy comparison.

## Question the target

The Sidorenko target is a graphon inequality, not a finite-group comparison.
The inherited C68 vocabulary could make a representation calculation look
like a universal proof.  The proposed inequality below is deliberately
**stronger** than Sidorenko; a counterexample therefore rejects only this
tensor mechanism, not the graph conjecture.

## Question the critique

The stronger statement might be so strong that a small counterexample merely
records an obvious loss of information in passing from \(W\) to its
triple-kernel.  That is still high information gain: it tells us whether the
kernel is a viable proof state space before any Fourier or polarization work.

## Oracle selection

Oracle selected the following mechanism.  For a nonnegative graphon \(W\),
set
\[
 K(a,b,c)=\int W(a,y)W(b,y)W(c,y)\,dy.
\]
Relabeling the bipartition of \(K_{5,5}\setminus C_{10}\) and applying
Fubini gives
\[
 t_H(W)=\int\prod_{i\in\mathbb Z_5}K(x_i,x_{i+1},x_{i+2})\,d\boldsymbol x.
\]
The selected `CONJECTURED` strengthening is
\[
 t_H(W)\ \ge\ \left(\int K\right)^5. \tag{C5-K}
\]
Since \(\int K=\int d_W(y)^3dy\ge t_{K_2}(W)^3\), (C5-K) would imply the
Sidorenko inequality for \(H\).

The first gate is a complete rational two-atom **bigraphon** packet (a control
superset of symmetric graphons).  A negative
exact difference in that packet falsifies (C5-K).  A pass is only a control;
continue only with an explicit tensor factorization or polarization identity,
not a larger grid.  The main rejected alternative is a height-four Frankl
search, because its intended contraction is presently not specified beyond
known height-three and irreducible-deletion results.

## Post-control Oracle decision

`PROVED` exact packet routes agreed on 729 rows with no negative defect; this
does not promote (C5-K).  Oracle authorized one final C85 gate: compute the
two-atom completely-positive defect polynomial
\(K=\lambda u^{\otimes3}+(1-\lambda)v^{\otimes3}\) exactly and seek a
factorization/SOS with visibly nonnegative cone factors.  A rational negative
specialization falsifies (C5-K).  If neither outcome occurs under the frozen
symbolic cap, seal this finite-method boundary rather than add a grid.
