# Lane B report — first growing-genus experiment

## Claim boundary first

The three-dimensional Ising model is **not solved**.  No size-uniform
bounded-rank representation, recurrence in box size, or controlled
thermodynamic limit has been found.  The result below is an exact finite-graph
homology-frontier identity plus a genuine finite-size spin-structure
compression: after recovering the physical intersection form, one explicit
symplectic basis has exact generic TT profile `(2,4,7,4,2)` instead of the
generic maximum `(2,4,8,4,2)`.  No claim is made that rank seven persists as
the box grows.

Research-status vocabulary in this report follows the user's required
`PROVED / COMPUTATIONALLY VERIFIED / CONJECTURED / SPECULATIVE` labels.  Under
the repository promotion taxonomy, the new computer-assisted claims remain
`OBSERVED` until a separate proof audit promotes them.

## 1. Exact proposed identity

Let `G=(V,E)` be a graph cellularly embedded in an orientable surface and let
`B_1` be the span over `F_2` of its facial boundaries.  For an even edge set
`A` define its homology class `[A]` in `H_1=Z_1/B_1` and

\[
 W_h(\{t_e\})=
 \sum_{\substack{A\subseteq E\\ \partial A=0,\ [A]=h}}
 \prod_{e\in A}t_e .
\]

Then the finite zero-field partition function is

\[
 Z_G=2^{|V|}\prod_{e\in E}\cosh K_e
       \sum_{h\in H_1}W_h(\{\tanh K_e\}).
\]

For any quadratic refinement `q` of the surface intersection form, define

\[
 F(q)=\sum_h(-1)^{q(h)}W_h.
\]

The Arf identity reconstructs the physical sum as its Arf-weighted Fourier
coefficient.  The new computational mechanism is the following exact edge
recurrence.  Give each edge a six-bit label `ell_e` whose sum on a cycle is
its quotient coordinate.  If `P_i(p,h)` is the polynomial after the first `i`
edges, with live vertex parity `p` and accumulated homology `h`, then

\[
 P_{i+1}(p,h)=P_i(p,h)+t_e
 P_i(p\mathbin\oplus\partial e,h\mathbin\oplus\ell_e).
\]

When the last incident edge of a vertex has been processed, states with odd
parity there are deleted and the even bit is forgotten.  The terminal states
are exactly `W_h`.

**Status: PROVED.** This recurrence follows by the disjoint choice “exclude
or include the next edge”; the forgetting rule is exactly the even-subgraph
constraint.  It is multivariate and does not assume isotropy.

## 2. Why it escapes the Stage 1 obstruction

The recurrence never assigns pairwise crossing signs and never asks surfaces
to be free fermions.  All topology seen so far is accumulated locally in the
finite label `h`, while vertex parity is carried only across the current
frontier.  Intersections and genus are represented collectively by the
quotient `Z_1/B_1`; spin-structure signs are applied only after the positive
sector polynomials have been computed.

This is not yet an asymptotic escape.  The frontier and the `2^(2g)` homology
labels may both grow.  No bound proving subexponential cost for cubic
`L x L x L` boxes has been obtained.

## 3. Auxiliary complexity

For the free `4 x 3 x 3` box, direct cycle enumeration has `2^40` terms.  The
exact recurrence computed all 64 homology-sector polynomials with at most
16,384 live `(parity,homology)` states and about 101 MiB peak resident memory.
The replay took 8.4 seconds including two independent rational controls and
rank calculations.

**Status: COMPUTATIONALLY VERIFIED.** This is a finite-instance reduction by
a factor of `2^26` in peak combinatorial state count, not a general complexity
theorem.

## 4. Smallest decisive experiments and results

### Genus-one calibration

On the pinned free `3 x 3 x 2` slab, the frontier recurrence reproduces all
four sector polynomials from the sealed `2^16` direct enumeration,
coefficient-for-coefficient, after swapping the two quotient generators.  A
character-wise signed transfer followed by exact Walsh inversion agrees at
`t=1/2` and `t=1/3`.

**Status: COMPUTATIONALLY VERIFIED.** Maximum live states: 64.

### A certified growing-genus cubic embedding

The free `4 x 3 x 3` graph has 36 vertices and 75 edges.  A pinned orientable
rotation system has 35 faces—34 quadrilaterals and one 14-gon—so its genus is
three.  Genus two would force exactly 36 length-four facial walks and one
length-six facial walk.  Minimum degree three forbids immediate reversal in a
face walk; a reduced closed walk of length four or six in this bipartite graph
cannot repeat a vertex, because repetition would split it into two reduced
even closed walks of length at least four.  Thus the faces would be elementary
squares and one simple six-cycle.  The verifier exhausts all 52 squares and
all 250 simple six-cycles and finds no edge-twice face cover.  As a positive
control, the same exact-cover engine accepts the pinned 34-square plus
14-gon census.

**Status: COMPUTATIONALLY VERIFIED.** Subject to ordinary code-audit risk, the
minimum orientable genus is exactly three.

### Exact sectors

The cellular embedding has face-boundary rank 34 and homology dimension six.
All 64 sector polynomials were computed.  Every sector contains exactly
`2^34` even subgraphs, so together they account for all `2^40` cycles.  At
both `t=1/2` and `t=1/3`, independent character-wise transfer and Walsh
inversion reproduce every sector value exactly.

**Status: COMPUTATIONALLY VERIFIED.** Positivity is manifest in every `W_h`;
signs occur only in the finite Fourier/Arf post-transform and are harmless.

Summing the sectors gives the checkable high-temperature coefficients

\[
1+52t^4+250t^6+2488t^8+18078t^{10}+129351t^{12}
+844020t^{14}+\cdots+211100t^{58}+1364t^{60}.
\]

Their total at `t=1` is `2^40=1099511627776`.  The coefficients of `t^4`
and `t^6` independently equal the exhaustive counts of elementary squares
and simple six-cycles.  **Status: COMPUTATIONALLY VERIFIED.** Novelty of the
higher coefficients has not been audited, so they are offered as replayable
data rather than a priority claim.

### Tensor-train rank

For the reference symplectic quadratic form
`q_0(h)=h_0h_1+h_2h_3+h_4h_5`, the TT ranks are

\[
 (2,4,8,4,2),
\]

the maximum possible profile.  The same profile occurs for all 48 handle
permutations and within-handle reversals, at both exact rational controls.

**Status: COMPUTATIONALLY VERIFIED; RESTRICTED NO-GO.** This provisional
reference-ordering result motivated, but is superseded in scope by, the
physical symplectic search below.

### Physical intersection form

Two independent labeled constructions recover the same mod-two homology
intersection matrix in the pinned six-bit quotient basis:

\[
J=\begin{pmatrix}
0&1&1&0&0&1\\
1&0&0&1&1&0\\
1&0&0&0&0&0\\
0&1&0&0&0&0\\
0&1&0&0&0&1\\
1&0&0&0&1&0
\end{pmatrix}.
\]

Route A fans every cellular face to a new center, constructs cohomology
classes dual to the pinned homology cycles, evaluates the
Alexander--Whitney cup product on every triangle, and inverts the dual cup
matrix. Route B chooses deterministic primal and dual spanning trees, reduces
the map to a one-vertex/one-face chord word, computes the cohomology
interlacement matrix, inverts it to obtain the bouquet homology intersection
matrix, and transports that matrix to the pinned labels. The genus-one slab
independently returns the standard matrix `[[0,1],[1,0]]`.

The matrix is alternating and has rank six. The explicit transport whose
columns form `(a1,b1,a2,b2,a3,b3)` is stored by row masks

`[9, 6, 36, 24, 16, 32]`,

and is checked exactly to satisfy `S^T J S = diag(J2,J2,J2)`.

**Status: COMPUTATIONALLY VERIFIED.** Both routes agree with the actual six
labels, not merely up to an unspecified basis change.

### Physical quadratic refinements and exhaustive symplectic search

In the transported basis the verifier derives all 64 refinements

\[
q_\lambda(h)=h_0h_1+h_2h_3+h_4h_5+\lambda\cdot h
\]

from the polarization identity. Exact Gauss sums independently give 36 even
and 28 odd spin structures, and the Arf-weighted sum reconstructs the physical
sector polynomial at both rational controls.

All `|Sp(6,2)|=1,451,520` ordered physical symplectic bases were exhausted
modulo the prime `1000000007`. Full modular rank proves exact full rank of the
corresponding integer specialization. At both `t=1/2` and `t=1/3`, the profile
counts are:

- `1,313,280` bases with `(2,4,8,4,2)`;
- `138,240` bases with `(2,4,7,4,2)` modulo the prime.

The first survivor has ordered columns `[1,34,4,8,17,32]`. For this basis the
middle flattening obeys the coefficientwise polynomial identity

\[
\operatorname{row}_4(t)-\operatorname{row}_6(t)=0.
\]

Thus its middle rank is at most seven over `Q(t)`. Exact nonzero `7 x 7`
minors at both rational controls prove rank at least seven. The other four
cuts have exact maximal modular witnesses, hence the generic profile is
exactly

\[
(2,4,7,4,2).
\]

The identity is explained, rather than merely recognized, by the box
automorphism `(x,y,z) -> (x,z,y)`. Its induced action preserves the pinned
facial-boundary space, the physical intersection form, the reference
quadratic refinement, and every sector polynomial. On the selected tensor
cut its dual action sends every entry of row 4 to the corresponding entry of
row 6.

**Status: COMPUTATIONALLY VERIFIED.** This is an exact finite-size TT bond
reduction from eight to seven and completes the positive branch of Gate 2.
It is not a size-uniform rank bound.

## 5. Candidate-report fields

1. **Exact proposed identity:** the homology-resolved frontier recurrence for
   `W_h`, followed by the quadratic Fourier transform `F(q)`.
2. **Stage 1 escape:** topology is accumulated as a quotient label without a
   local fermionic crossing sign.
3. **Auxiliary dimension/sectors:** 64 sectors and at most 16,384 live states
   on the genus-three control; no size-uniform bound is proved.
4. **Smallest decisive experiment:** sealed genus-one replay, then the
   minimum-genus free `4 x 3 x 3` box.
5. **Result:** exact finite reduction survives; the physical exhaustive search
   finds and certifies a symmetry-derived rank-seven basis.
6. **Status:** **SURVIVES — LEVEL 2 FINITE-INSTANCE SUCCESS**. The original
   reference handle ordering remains a restricted no-go, not the lane.
7. **Unproved assumptions/open bridges:** test the symmetry-aligned basis on a
   held-out growing-genus box; determine whether a compatible family of
   minimum-genus embeddings exists; derive or falsify a recurrence in box
   size; bound the asymptotic frontier-plus-genus state count.

## Failure ledger additions

- `F301`: genus-one factorization was not probative. Contained by moving to a
  certified genus-three graph.
- `F302`: the genus-two simple-face construction is impossible on the free
  `4 x 3 x 3` box. This becomes part of the minimum-genus certificate, not a
  universal embedding no-go.
- `F303`: low TT rank fails for the reference quadratic form under all 48
  handle permutations/reversals. General symplectic changes remain open.
- `F304`: `2^(2g)` sector growth remains explicit. The finite frontier saving
  does not establish a controlled thermodynamic limit.
- `F305`: the apparent conflict between the cup and tree-cotree routes came
  from treating chord interlacement as homology intersection. It is the cup
  matrix in the dual cohomology edge basis; inversion repairs the convention,
  after which both labeled routes agree. The genus-one control was blind to
  this because the standard `2 x 2` symplectic matrix is self-inverse.
- `F306`: the conjecture that every physical symplectic basis is maximally
  ranked is killed. An exact coefficientwise row identity gives generic
  middle rank seven in the displayed basis.

## Replay

```bash
cd projects/three-dimensional-ising
python3 proof/verify_lane_b_genus3.py > /tmp/lane-b-genus3.json
python3 proof/verify_lane_b_intersection.py > /tmp/lane-b-intersection.json
python3 proof/verify_lane_b_physical_ranks.py > /tmp/lane-b-physical-ranks.json
```

The immutable Cycle 3 artifact freezes these verifiers, their tests, this
report, and the exact gate decision. Use its `--check` replay before relying
on the result.
