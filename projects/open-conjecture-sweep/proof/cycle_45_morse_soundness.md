# Cycle 45 soundness boundary: distinguished-owner Morse flow

## Generic operator theorem

`PROVED`: let \(K\) be any finite simplicial complex with ordered vertices,
and fix an ordered list of vertices.  Process those vertices in order.  At a
stage \(v\), pair every still-unmatched cell \(\sigma\) not containing
\(v\) with \(\sigma\cup\{v\}\) when the latter is a still-unmatched cell of
\(K\).  The union of these pairs is an acyclic partial matching.

For one vertex, every reversed matched arrow inserts that vertex and every
other arrow deletes a vertex other than the inserted one; a closed gradient
path is impossible.  For several vertices, the standard stagewise patchwork
argument applies: after the first stage, later matchings use only cells left
critical by the preceding stages.  If a closed gradient path existed, its
earliest-stage reversed arrow could not return through the later-stage
critical subgraph.  Removing that stage inductively gives a closed path in a
single-vertex matching, a contradiction.  The executable additionally
constructs the complete reversed-arrow graph and checks its topological order
on every instantiated complex.

Orient every matched incidence by its simplicial sign.  Define the degree-one
operator \(V\) on a matched lower cell \(\sigma<\tau\) by

\[
  V\sigma=-\langle d\tau,\sigma\rangle^{-1}\tau,
\]

and let it vanish on other basis cells.  Put

\[
  \Phi=I+dV+Vd.
\]

`PROVED`: acyclicity makes every nonstationary term of an iterate of \(\Phi\)
follow a finite directed gradient path, so \(\Phi^N\) stabilizes for finite
\(N\).  Write \(\pi=\Phi^N\) and
\(S_N=I+\Phi+\cdots+\Phi^{N-1}\).  Since \(d\Phi=\Phi d\),

\[
  \pi-I=(\Phi-I)S_N=(dV+Vd)S_N=d(VS_N)+(VS_N)d.
\]

Thus with \(h=-VS_N\),

\[
  dh+hd=I-\pi,
\]

and \(\pi\) is a chain map chain-homotopic to the identity.  In particular,
for a cycle \(z\), \(\pi z=0\) gives the explicit fill \(hz\).  A nonzero
\(\pi z\) is a residual chain, not automatically a nonzero homology class.

This proof is characteristic-zero only because the project uses rational
chains; every matched incidence is \(\pm1\), so the operator itself is also
defined integrally.

## Frozen actual-corpus result

`PROVED` by primary and independent exact routes: the first
four-stage matching uses the frozen delta owner of each part.  Across all
5,954 serialized Cycle 43/44 interfaces, every matching is acyclic and every
cycle satisfies the exact homotopy identity.  The projection vanishes on all
3,954 Cycle 43 interfaces and on 1,530 of 2,000 Cycle 44 interfaces.  It is
nonzero on 470 Cycle 44 interfaces, with support at most 76.

The classification is exact: every Cycle 44 explicit-cone row has zero
projection, including all 29 rows with positive GF(2) H2.  Of the 472
non-cone H2-zero rows, two also have zero projection and 470 retain a nonzero
projection.  Hence the first Morse layer recovers the cone mechanism almost
exactly and isolates the acyclic remainder.

The independent route derives every rank-two and rank-three deletion directly
from the local signature patterns, enumerates cells and Hasse arrows in
reverse order, checks acyclicity by depth-first search rather than the
primary topological queue, and recomputes both exact flows.  It agrees on all
30,212,057 interface-weighted allowed simplices, all 5,954 initial and
extended projections, their maximum supports, and their step counts.

Appending every other support vertex in lexicographic part/owner order is a
second valid stagewise matching.  It kills 13 of the 470 residuals and leaves
457.  This refutes complete annihilation by the naive layered schedule.  The
remaining chains are nevertheless rational boundaries: the homotopy identity
makes them homologous to the original cycles, whose boundaries were sealed in
Cycles 43/44.  No repeated exact fill solve is needed.

## Abstract falsification and the missing state

`PROVED` finite search: among 41,641 admissible models from 48,037
deduplicated arbitrary-deletion descriptors, 3,083 have nonzero initial
projection and 2,647 are genuinely nonboundary.  The extended schedule leaves
2,838 nonzero, including the same 2,647 nonboundary classes.  A valid chain
homotopy cannot erase those classes.

Removing every rank-three deletion does not repair the abstract axioms: 96
rank-three-free models still have a nonboundary projection.  Thus Cycle 41's
proved absence of rank-three blockers with two small supports is necessary
but not sufficient.

The next lift restores local ownership data.  At an actual owner, every type
has a digit-signature set.  Rank-two blockers are disjoint signature pairs;
rank-three blockers are minimal empty triple intersections, so all three pair
intersections are nonempty.  Deletions cannot be chosen independently.

`PROVED` finite search: the signature lift generated 31,204 deduplicated
models from 50,000 frozen counters after rejecting 18,796 models whose selected
pair was deleted.  Of 31,160 face-admissible models, 649 still have a
nonboundary projection under both schedules.  Therefore local signature-set
realizability is also insufficient.  The exact discriminator is global:
every actual first-layer residual in the frozen corpus has H2 zero, whereas
the abstract and signature-lift families admit nonzero critical homology.
The missing theorem must use the global p199 type corpus and marginal-selection
closure, not only local blocker geometry.

## Control boundary

The generic proof is independent of finite controls.  Exact basis checks have
passed the complete 81-cell undeleted two-owner join and 200 deterministic
deleted two-owner complexes.  A pre-execution exact count found 2,836,566 raw
two-owner support/deletion descriptors, exceeding the frozen 2,000,000-model
control cap before quotienting.  The raw exhaustive control is therefore a
`CAP`, not evidence against the theorem; no universal empirical claim is made
from that branch.

## Claim boundary

Cycle 45 proves the generic operator identity and finite classifications
above.  It does not prove that every actual four-type interface is cone or
H2-zero, that the layered matching annihilates every actual moment cycle, or
that local signature realizability characterizes the p199 corpus.  It is not
the complete degree-four functional, a leaf certificate, or LRC(13).
