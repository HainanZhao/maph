# Cycle 52 idea selection: exact local graphon variation

## Evidence that fixes the question

- `PROVED` Cycle 51: the frozen finite conjugacy corpus has no route
  countermodel, but it is too structured to justify extrapolation.
- `PROVED` literature boundary: the Möbius graph is not weakly norming, so
  convexity/norming cannot be assumed as a local certificate.
- `CONJECTURED`: if Sidorenko fails for this graph, a low-complexity,
  fixed-density step graphon may exhibit its first detectable negative local
  direction before a global optimizer does.

## Serious candidates

### A. Exact symmetric step variation

At (p=1/2), enumerate primitive symmetric zero-mean two- and three-step
matrices with entries in {-1,-1/2,0,1/2,1}.  Expand
\(t_H(p+\varepsilon U)-p^{15}\) exactly, classify its first nonzero
coefficient, and turn any negative one into a bounded rational graphon.

- Preserves: graphon symmetry, fixed edge density, and a literal rational
  realization.
- Falsifier: one negative leading coefficient plus exact negative evaluation
  at a permitted dyadic epsilon.
- Information: direct counterexample potential; otherwise a finite local
  stability theorem with no global extrapolation.

### B. Extend the conjugacy corpus to larger symmetric groups

- Falsifier: a larger finite countermodel.
- Rejected: it is a census treadmill after C51 and has no new invariant.

### C. Representation-theoretic proof of conjugacy monotonicity

- Falsifier: a non-PSD representation block.
- Rejected for now: C51 equality/gap data are too structured to safely infer
  the needed universal block form.

## Question the questioning

Why use only (p=1/2)?  The sign of the *first* nonzero coefficient is
independent of the positive factor (p^{15-k}); (1/2) makes a bounded
dyadic realization transparent.  This does not make the finite direction
family universal.

Why require a graphon realization after a negative coefficient?  A formal
Taylor sign is insufficient unless a positive rational epsilon keeps all block
values in [0,1] and makes the full polynomial negative.  The exact
evaluation is the counterexample certificate.

Why not restrict directions by (D_{10}) symmetry?  The target graph has that
symmetry, but an asymmetric direction could be the first negative one.
Symmetry is used only to canonicalize matrix representatives, never to omit
directions without proof.

## Choice

Choose A.  Freeze equal two- and three-block partitions, the primitive entry
alphabet, coefficient rule, and dyadic realization search.  A finite all
nonnegative result closes this local family only; a negative exact graphon is
a Sidorenko counterexample candidate requiring independent replay.
