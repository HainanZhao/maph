# SIC--Stark research cycle 47: dimension-seven closure inventory

## North-star alignment

The long-term target is a dimension-independent proof of the Twisted
Convolution Conjecture for the AFK ghost-SIC construction.  Dimensions four
and five supply closed examples; dimension six identifies a primitive
character obstruction; dimension eight retains a quartic obstruction.
Dimension seven is currently the cleanest test of whether the
Shintani-algebraicity route can scale beyond the small examples.

Cycle 46 closed the conductor-two absolute-value bridge.  The remaining
dimension-seven proof was separated into four independently auditable gates:

1. exact roots of unity in the AFK/Kopp phase;
2. exact ray-unit fields and chosen real roots;
3. exact reconstruction of both twisted ghost matrices; and
4. vanishing of their rank-two minor ideals.

The first gate is finite and unconditional.  The second is algebraic and is
the principal bottleneck.  The third and fourth are finite once the second is
certified.

## Canonical data

\[
 d=7,\quad r=1,\quad
 Q=\langle1,-6,1\rangle,\quad
 \Delta=32,\quad K=\mathbb Q(\sqrt2),\quad f=2.
\]

For \(K\), the AFK fundamental positive-norm unit is
\(\epsilon=3+2\sqrt2\).  Its first conductor is \(f_1=2\), so the tuple is
\((K,j,m,Q)=(K,1,1,Q)\), and \(f_{jm}/f=1\).

The associated matrices are

\[
 L=\begin{pmatrix}6&-1\\1&0\end{pmatrix},\qquad
 A=L^3=
 \begin{pmatrix}204&-35\\35&-6\end{pmatrix}.
\]

This inventory removes the ambiguity about which order, form, stabilizer,
and phase formula the next cycles must use.

## Decision

Proceed phase-first.  Exact unit recognition performed before the phase
normalization would merely reproduce the convention problems encountered in
dimension four.

