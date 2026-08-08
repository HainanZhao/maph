# Denominator-free mask tensor train from one global phase gauge

## Status and scope

`PROVED` below is an algebraic statement under the explicitly stated
filtration hypotheses.  Its grid corollary is `PROVED` only after the
checkerboard collar construction supplies those hypotheses.  No matrix
factorization over a fraction field is used.

All chains, masks, phases, and cochains in the proof are over `F_2`.  Edge
weights remain independent indeterminates over `Z`.

## 1. A cellular filtration and its path space

Let

    P_0 subset P_1 subset ... subset P_N = G

be a filtration of the physical edge set.  Put `E_j=P_j\P_(j-1)` and assume
that the only vertices incident to both `P_j` and its complement are the
labelled separator `Gamma_j`.  Thus the `E_j` are pairwise disjoint and their
union is `E(G)`.

For `S subset E_j`, let `partial_- S` and `partial_+ S` denote its parity
defect on `Gamma_(j-1)` and `Gamma_j`, after requiring even parity at every
vertex strictly inside the block.  A compatible path is

    (m_0,S_1,m_1,...,S_N,m_N),

where `m_0=m_N=0` and the two displayed defects of `S_j` are
`m_(j-1),m_j`.  Taking the disjoint union of its `S_j` gives an even subgraph.
Conversely, restriction of an even subgraph to the disjoint blocks gives one
and only one compatible path.  This is a bijection, not a weighted identity.

Choose on every `Gamma_j` the same rooted labelled tree transported through
the collar isotopy.  Write `c_j(m)` for its unique `m`-join.  At an elementary
co-core move the transported tree differs by the single displayed edge
exchange; choosing the new edge lexicographically in the only ambiguous
boundary case fixes the transport.  Hence all `c_j` belong to one global
system.  The locally closed chain

    z_j(S,m,m') = c_(j-1)(m) + S + c_j(m')

is a cycle in the ribbon collar with its cap intervals.  In the sum of all
`z_j`, every internal completion occurs twice, so

    sum_j z_j = disjoint_union_j S_j = A.                 (1)

This is the chain-level gauge telescoping identity.

## 2. The phase-potential lemma

Let `theta(A)` be a binary phase on complete compatible paths.  Suppose that
at every cut `j` there are functions `L_j`, `R_j`, and `kappa_j` with

    theta(A) = L_j(A_<=j,m_j) + R_j(A_>j,m_j) + kappa_j(m_j).   (2)

The decompositions in (2) are not selected independently.  Fix one global
phase `theta`, the transported completions above, and one canonical right
reference continuation `r_j(m)` for every reachable mask.  Normalize
`L_j(p,m)` as the phase difference between `p+r_j(m)` and the zero reference
path with the same right continuation.  Equation (2) says precisely that
this difference is independent of any other right continuation.

Define

    Q_j(S,m,m') = L_j(p+S,m') + L_(j-1)(p,m),             (3)

where `p` is any reachable left path ending at `m`.  This is well defined.
Indeed, if `p'` is another such path and `r` is any common continuation from
`m'`, apply (2) at cuts `j-1` and `j` to `p+S+r` and `p'+S+r`.  After adding
the two identities, every right and mask term cancels and gives

    L_j(p+S,m')+L_j(p'+S,m')
      = L_(j-1)(p,m)+L_(j-1)(p',m).

This is exactly independence in (3).  Summing (3) along a compatible path
telescopes.  With the endpoint normalizations `L_0=0` and `L_N(A,0)=theta(A)`,

    theta(A) = sum_j Q_j(S_j,m_(j-1),m_j).                (4)

The proof used one phase and one reference-completion system; it did not
splice unrelated two-cut factorizations.

For the grid application, take `theta(A)=q_0(pi A)` including the fixed
affine-origin correction.  H2 at every pair and internal cut is exactly (2).
At an internal cut, its proof must use H3 to make the current cross term a
mask function.  Therefore (3) gives the required local quadratic phase.

## 3. Localizing every linear character once

Let `gamma_j` be the fixed global cocycle representing the homology
coordinate paired with the `j`-th spin-structure bit.  The two separators on
the sides of its elementary handle block have the following two-sided H1
property:

- on the earlier prefix, `gamma_j` is a coboundary plus a trace functional
  `phi_j^-`;
- on the later suffix, it is a coboundary plus a trace functional
  `phi_j^+`.

The coboundaries are restrictions of the one global cellular representative,
with the vertex potential pinned at the transported root.  Discrete Stokes
then gives, for every complete path,

    <gamma_j,A>
      = phi_j^-(m_(j-1)) + <gamma_j,S_j> + phi_j^+(m_j)
      =: H_j(S_j,m_(j-1),m_j).                           (5)

Thus the `j`-th global character is emitted exactly once.  A change of
representative `gamma_j -> gamma_j+delta s` changes the three terms in (5)
by two endpoint traces and the block coboundary; Stokes makes their total
zero.  Hence (5) is gauge invariant even though its three summands are not.

For a cut between `a_i` and `b_i`, the later character has one exposed half.
H3 identifies its trace contribution explicitly as

    rho_i(m)=<s_i,m>.

This is the same term used in the internal-cut instance of (2).  Consequently
the `a_i b_i` part of `q_0` is assigned by (3) without retaining either bit as
an additional virtual state.  The triangular symplectic correction only adds
earlier meridian cocycles supported in the same newly attached collar; their
pinned potentials add to `phi_j^+` and `rho_i`, so (5) and the mask-only H3
term are unchanged in form.

Combining (4) and (5), for every spin structure `epsilon` and every even
subgraph `A`,

    q_0(pi A) + sum_j epsilon_j <gamma_j,A>
      = sum_j [Q_j(S_j,m_(j-1),m_j)
               + epsilon_j H_j(S_j,m_(j-1),m_j)].        (6)

This is the required global telescoping identity.

## 4. Polynomial cores

For the reachable even-mask set `V_j` at `Gamma_j`, define

    A_j(epsilon)[m,m']
      = sum over S subset E_j with defects (m,m')
          (-1)^(Q_j(S,m,m')+epsilon H_j(S,m,m'))
          product_(e in S) t_e.                          (7)

Every entry of (7) is in `Z[t_e]`; no division has occurred.  Expanding

    e_0^T A_1(epsilon_1)...A_N(epsilon_N)e_0

chooses one compatible path.  The path/even-subgraph bijection counts each
monomial exactly once, while (6) supplies its defining pre-Arf sign.  Hence
the contraction equals the complete pre-Arf tensor entry.  Padding every
reachable mask set by the even masks on `w^2` labels gives bond at most
`2^(w^2-1)`.  Empty geometric blocks are identity transitions with the
corresponding local phase and do not alter the statement.

The construction is valid over the polynomial ring itself.  The earlier
fraction-field rank theorem is a corollary, not an input.

## 5. Boundaries

Free longitudinal boundaries use `m_0=m_N=0`.  An antiperiodic seam changes
the unique block containing it by a fixed linear edge sign.  A periodic seam
identifies the endpoint mask and takes the trace of the same polynomial
cores.  Fixed-spin boundaries require transforming their boundary vector
with the same pinned gauge; no invariance is asserted for an untransformed
fixed-spin vector.

## 6. Falsifier

The proof would fail at the first cut for which either (i) the phase
rectangular identity implied by (2) is false for two prefixes with the same
mask, or (ii) a character in (5) has a nonzero period on one of the two
outside relative-cycle spaces.  Such a failure would produce two partial
chains with identical boundary data but different residual junction phase.
It cannot be repaired by changing `Q_j` on one row; it requires additional
virtual memory or abandonment of the polynomial-core claim.

