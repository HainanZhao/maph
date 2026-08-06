# C89 source and convention audit: rank-one escape geometry

## Source boundary

`PROVED` from Lee--Schülke, *Convex graphon parameters and graph norms*,
pp. 1--2 (Theorem 1.3): \(K_{5,5}\setminus C_{10}\) is not weakly norming;
the paper explicitly says the Sidorenko status of this graph remains
undetermined.  Their Hessian criterion is for convexity/weak norming, so it
does not settle C89's fixed-base deficit Hessian.

`PROVED` from Blekherman--Raymond--Singh--Thomas, Corollary 1.6 (pp. 3--4):
\(H-e^{15}\) is neither SOS nor admits an \((1+\mathrm{SOS})\)-multiplier
SOS certificate.  This excludes those global certificate forms, not a local
step-bigraphon calculation.

`PROVED` from Zhao, arXiv:2606.15368v1, Theorem 1.3: a conjugacy comparison
for every finite group and nonnegative function implies strong Sidorenko.
Theorem 1.4 concerns 1-subdivisions only.  C89 is neither a universal
finite-group comparison nor a subdivision result.

`PROVED` from C53's sealed record: the constant symmetric base \(W\equiv
1/2\) has a directional local-stability theorem.  C89 instead uses
nonconstant rank-one **bipartite** bases, density tangents, a stationarity
restriction, and a full feasible-line crossing check; it does not repeat
C53's theorem.

`PROVED` from Lovász, *Subgraph densities in signed graphons and the local
Sidorenko conjecture*, arXiv:1004.3026, abstract and local expansion setup:
the established local question is a perturbation of a constant random base.
For every bipartite graph it supplies a local constant-base inequality; it
does not state a stationary Hessian theorem at a nonconstant rank-one
**bigraphon** base.  The Lee--Schülke paper also studies Hessians for
convexity/weak-norming, rather than this constrained deficit at such a base.

`OBSERVED`: after reading the reachable Lovász local-Sidorenko source and
Lee--Schülke Hessian source, the bounded primary search found only
constant-base local theory and weak-norming convexity Hessians, not this
precise nonconstant rank-one step-bigraphon mechanism.  This is not a
novelty proof.

## Frozen conventions for the proposed gate

Let left/right vertices both be \(\mathbb Z_5\), with right vertex \(j\)
adjacent to left vertices \(j,j+1,j+2\) (indices modulo 5).  Thus \(H\) has
ten vertices and 15 edges.  For positive rational atom weights
\(\alpha_i,\beta_j\) summing to one and a matrix \(W\), use
\[
t_H(W)=\sum_{f:L\to[3],\,g:R\to[3]}
 \prod_i\alpha_{f(i)}\prod_j\beta_{g(j)}
 \prod_{(u,v)\in E(H)}W_{f(u),g(v)},\qquad
d(W)=\sum_{ij}\alpha_i\beta_jW_{ij}.
\]
The deficit is \(\Delta(W)=t_H(W)-d(W)^{15}\).  These conventions will be
implemented and independently enumerated before any claim.

## Claim boundary

The source interfaces above are `PROVED` only to their quoted scopes.  The
bounded no-overlap search remains `OBSERVED`: it does not establish universal
openness or novelty.  C89's subsequently derived stationary-Hessian identity
is a separate exact algebraic result, not an attribution to any source here.
