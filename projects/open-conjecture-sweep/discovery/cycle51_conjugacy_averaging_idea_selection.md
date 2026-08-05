# Cycle 51 idea selection: conjugacy averaging for the Möbius graph

## Evidence that fixes the question

- `PROVED` from the Cycle 51 eligibility reading: (H=K_{5,5}\setminus
  C_{10}) has 15 edges; it is not weakly norming and the ordinary SOS route
  is excluded.  Neither statement resolves Sidorenko.
- `PROVED` from Zhao, Theorem 1.3: if
  \(t_{\rm Cay}(H;\Gamma,a)\ge t_{\rm Cay}(H;\Gamma,a^{\rm cl})\) for all
  finite groups and nonnegative functions, then (H) is strong Sidorenko.
- `PROVED` from the same source: the positive 1-subdivision theorem does not
  apply to this 3-regular, non-subdivision (H).

## Serious candidates

### A. Exact finite-group conjugacy comparison

Evaluate the theorem's comparison exactly for a frozen small group corpus and
for subgroup-product connection sets in (S_3,S_4).  Use the Cayley identity
to sum over four normalized left variables and independent right fibers.

- Preserves: exact (15)-edge labeling, edge density under class averaging,
  and the comparison appearing in Zhao's theorem.
- Falsifier: one exact nonnegative indicator function with
  \(t_{\rm Cay}(H;a)<t_{\rm Cay}(H;a^{\rm cl})\).
- Information: a counterexample destroys the universal comparison route; a
  finite pass establishes only a reusable exact corpus result.

### B. Dihedral-equivariant local variation about constant graphons

Derive the fixed-density Taylor form of (t_H(W)-p^{15}) and decompose it by
the (D_{10}) action.

- Falsifier: an exact negative variation direction.
- Information: useful local geometry, but positive semidefiniteness would not
  access the known global difficulty.

### C. Certified low-step graphon search

Optimize rational two- and three-step graphons at fixed density.

- Falsifier: a rigorously evaluated counterexample.
- Information: direct but potentially a broad numerical search without a
  structural bridge.

## Question the questioning

Why test a finite corpus when Theorem 1.3 is universal?  Because the new
comparison is strong enough that a *single* exact violation is decisive for
that route, and the smallest nonabelian groups expose the representation
theory absent in abelian controls.  A pass is explicitly non-promotional.

Why include (S_3,S_4) subgroup products?  Szegedy's reduction requires
symmetric groups and such connection sets, whereas arbitrary (D_8,Q_8)
indicator functions test only the stronger universal hypothesis.  The two
families answer different failure questions and must not be conflated.

Why not first chase a local Hessian?  The weak-norming obstruction already
shows convexity-based reasoning is structurally unsafe here.  The new theorem
offers an exact global comparison with a sharp countermodel criterion.

## Choice

Choose A.  Freeze the graph labeling, exact finite groups, all indicator
functions on (S_3,D_8,Q_8), and every distinct subgroup-product connection
set in (S_3,S_4).  Verify the density evaluator against direct enumeration
on the small groups.  If a comparison violation occurs, seal it as a route
falsifier; otherwise classify the finite corpus and decide whether its
representation signatures justify a distinct next engine.
