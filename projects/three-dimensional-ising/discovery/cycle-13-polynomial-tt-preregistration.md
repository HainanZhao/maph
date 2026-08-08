# Cycle 13 / B13 preregistration: denominator-free all-sector tensor train

## Claim boundary

Decision question: does the checkerboard filtration admit one coherent
chain-completion gauge for which the complete pre-Arf sign is a sum of local
block phases, so that the mask-carrier tensor train exists over
`Z[t_e : e in E]`, rather than only over its fraction field?

The intended result is only a finite-strip representation.  It would not
compress the carrier below `2^(w^2-1)`, establish homogeneous-weight
minimality, or control the three-dimensional thermodynamic limit.

## Question -> question the questioning -> selected mechanism

The existing cut-by-cut H1--H3 factorization proves fraction-field ranks but
does not make independently selected completions at adjacent cuts compatible.
The missing issue is therefore not another rank estimate: it is whether the
phase factorizations form one cocycle along the whole filtration.

Two mechanisms were considered.

1. **Selected mechanism: swept completion chains and a phase potential.**
   Transport one rooted completion tree with the labelled separator through
   every elementary collar move.  For each mask `m`, its unique join gives a
   coherent completion `c_j(m)`.  Closing a block by the completions at its
   two ends produces a local cycle.  Consecutive auxiliary completions cancel
   in `F_2`.  Character cocycles are gauged once, globally, to the block at
   which their coordinate is emitted.  The quadratic phase is assigned by
   the canonical handle order; the only cross-block `a_i b_i` term is reduced
   to the shared mask by H3.  The proposed local exponent is the difference
   of this single global phase potential across one elementary move.

2. **Falsifying alternative: a residual junction cocycle.**  If the swept
   trees cannot be made compatible, the discrepancy at a junction defines a
   mask-dependent or history-dependent residual phase.  A mask-only residual
   can be absorbed by a gauge transition without increasing the carrier.  A
   residual whose value differs for two partial chains with the same mask is
   a genuine obstruction to the proposed polynomial cores, even though the
   fraction-field rank theorem can remain true.

The selected mechanism advances only if the local phase is well defined from
`(S_j,m_{j-1},m_j)` and the current spin-structure bit.  Merely factoring the
already assembled tensor is excluded.

## Frozen conventions and input state

- Graph and edge order: `src/conventions.py::cubic_box`, lexicographic
  undirected edge order.
- Embedding and canonical handles: the rotation system and nested basis in
  `paper/canonical-spin-structure-compression/main.tex`, with the affine
  quadratic-origin correction retained.
- Coordinate order:
  `(lambda_a1,lambda_b1,...,lambda_ag,lambda_bg)`.
- Separator labels: the same `w^2` longitudinal strands at every elementary
  cut; attainable states are even masks, rooted at label zero.
- Completion rule: the lexicographically first rooted tree in the initial
  collar, transported by the explicit collar isotopy; at a co-core move use
  the unique local edge exchange that preserves the rooted labelled tree.
  Any nonuniqueness is resolved lexicographically and recorded.
- Arithmetic audits: Python 3.11; primes `1,000,000,007` and
  `1,000,000,009`; two deterministic independent nonzero edge-weight
  specializations per prime and case.  No modular division is permitted in
  core construction.

## Mathematical acceptance criteria

The proof must supply all of the following before promotion.

1. Explicit separators `Gamma_j` and disjoint physical edge blocks `E_j`
   whose union is `E(G_{n,w})`.
2. A single transported completion family `c_j(m)` and a proof that the
   auxiliary chains cancel at every gluing.
3. Global character representatives and their one-time gauge transformation
   to local functions `H_j(S_j,m_{j-1},m_j)`.
4. Local quadratic functions `Q_j` and the identity, for every even subgraph
   `A = disjoint_union S_j`,

       q_0(pi A) + sum_j epsilon_j h_j(pi A)
       = sum_j (Q_j + epsilon_j H_j)  (mod 2).

   The internal-handle `a_i b_i` contribution must be displayed separately
   and reduced using the explicit H3 frontier function.
5. A bijection between even subgraphs and compatible local subsets with
   zero endpoint masks.  This must show that multiplying the polynomial
   cores counts each monomial exactly once.
6. Hence an exact TT/MPS identity with entries in `Z[t_e]` and bond at most
   `2^(w^2-1)` before any Arf sum.

## Computational firewall

After the arbitrary-width algebra is written, construct the local cores
directly from edge blocks (never by TT factorization of the final tensor) and
compare their contraction with an independent literal/cycle-transfer
evaluation of the defining sum at:

- `(n,w) = (6,3), (7,3), (4,4)`;
- both declared primes;
- two deterministic weight evaluations per prime;
- all spin structures when feasible, otherwise a preregistered set consisting
  of zero, every unit vector, every within-handle pair, and 64 deterministic
  full-coordinate vectors.

For each case also test the local telescoping identity on every reachable
transition and on deterministic random compatible block sequences.  The
replay must report the first failing block, masks, local subset, and residual
phase.

## Kill and escalation criteria

- If transported completions differ only by a mask function, incorporate the
  corresponding diagonal transition and prove its telescoping explicitly.
- If two compatible partial chains with the same incoming/outgoing masks and
  local subset give different residual junction phases, kill the naked-mask
  polynomial-core claim.  Record whether an enlarged carrier repairs it; do
  not hide the extra state.
- If the edge blocks overlap or omit a physical edge, or if one even subgraph
  has two compatible block decompositions, kill the proposed construction.
- A finite-width failure is not patched locally.  Name the false global-gauge
  step in the failure ledger and retain the fraction-field theorem only.
- Passing finite computations without the arbitrary-width telescoping proof
  is `CERTIFIED_NUMERICAL`, not acceptance.

## Resource stop

First prove or falsify the phase-potential identity on the symbolic
elementary collar types.  Only then run the three dense cases.  Stop a dense
case before exceeding 32 GiB RAM or four hours wall time; optimize the local
transition representation rather than substituting final-tensor
factorization.  Keep one CPU free.

