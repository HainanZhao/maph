# C83 triangle-tip reduction

## Statement and boundary

Let \(D(P)\) be the strict linear-extension-majority digraph of a finite
poset, and let \(D_{\mathrm{inc}}(P)\) retain its edges between incomparable
vertices.  `PROVED`: a simple directed four-cycle of \(D(P)\) using a
comparable pair is equivalent, after cyclic relabelling, to vertices
\(x,y,z,w\) such that
\[
 x<y,\qquad x\to z\to w\to x,\qquad y\to z\to w\to y.
\]
Every pair among these four other than \(x,y\) is incomparable.  In
particular, the two directed triangles are in \(D_{\mathrm{inc}}(P)\) and
share the edge \(z\to w\).

This is a structural reduction, not a solution of Gupta Question 14.  The
configuration might exist while a restricted directed four-cycle exists
elsewhere; a counterexample additionally requires that no such restricted
four-cycle occur anywhere in \(D(P)\).

## Proof

Suppose first that a full directed four-cycle contains a comparable edge.  A
strict majority edge on a comparable pair is directed from the lower to the
upper element, so rotate to write it as
\[
 x\to y\to z\to w\to x,\qquad x<y.
\]
The event \(y\prec z\) implies \(x\prec z\), hence \(x\to z\).  Likewise
the event \(w\prec x\) implies \(w\prec y\), hence \(w\to y\).  Therefore
\(x\to z\to w\to x\) and \(y\to z\to w\to y\) are directed triangles.
By Gupta Proposition 7 (as checked in C81), no directed majority triangle can
use a comparable pair.  Thus all their edges join incomparable vertices;
together they cover every pair except \(x,y\).

Conversely, the displayed two triangles and \(x<y\) give the deterministic
edge \(x\to y\).  Hence \(x\to y\to z\to w\to x\) is a full directed
four-cycle using the comparable pair \(x,y\).

## Consequence for the first C83 gate

The C81 35-weight ranking model already realizes all five nontrivial majority
arrows in the display with every ranking satisfying \(x<y\).  Thus neither
rank-pattern inequalities nor C81's common-pivot XYZ correlations can exclude
ordered tips.  Any C83 proof must use a property specific to the uniform
linear-extension measure, such as an order-ideal fiber identity or an
extension-preserving injection.  An exact poset with the displayed
configuration and no restricted 4-cycle would instead falsify that proposed
bridge and resolve the target negatively.
