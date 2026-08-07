# Lane B candidate report — bounded relative-theta transfer

## Outcome and claim boundary

**Status: SURVIVES.**

`PROVED`: for the free minimum-genus family

```
G_L = P_L square P_3 square P_3,  L>=4,
```

the complete tensor of `4^(L-1)` Walsh sector transforms—and therefore the
complete tensor of Cimasoni quadratic-refinement values `F(q)`—has an exact
handle-site tensor-train representation with rank at most `1024`, uniformly
in `L`.  In the earlier binary-coordinate convention, the uniform bound is
`2048` because a cut may pass through a two-bit handle.

This is a genuine collective compression and exact recursive closure in one
box dimension.  It does not treat growing transverse dimensions, periodic or
antiperiodic boxes, or the full three-dimensional thermodynamic limit.  It is
not an exact solution of the three-dimensional Ising model.

## 1. Exact proposed identity

Let `R_L` be the period-two minimum-genus rotation in
`src/lane_b_recursive_family.py`, and let `ell_L` be its nested homology label.
For every dual character `mu`, define

```
G_L(mu) = sum_(partial A=0) (-1)^mu(ell_L(A)) product_(e in A) t_e.
```

Let `P` be the 256 even-parity patterns on a transverse `3 x 3` slice.  The
explicit matrices in `proof/lane_b_bounded_theta_transfer_proof.md` satisfy

```
G_L(mu) = e_0^T M_0(mu) ... M_(L-1)(mu) e_0.
```

Every entry is a finite polynomial sum over the 4096 subsets of twelve
transverse edges with a prescribed boundary.  Each edge appears exactly once,
so the formula is coefficientwise valid for arbitrary edge variables.

The nonlinear reference quadratic sign factorizes by symplectic handle.  Its
one-handle transform is an invertible signed `4 x 4` Hadamard matrix.  Applying
these local transforms to `G_L` gives exactly the tensor `F(q)` and preserves
all TT flattening ranks.

## 2. Why this escapes the Stage 1 obstruction

The construction does not seek a single three-dimensional Pfaffian.  It keeps
the surface topology but organizes successive handles relatively.  Each
minimum-genus extension has:

- a one-dimensional old-boundary defect;
- one new orthogonal symplectic pair;
- edge labels supported only on the last old coordinate and the new pair.

Thus global genus is not discarded; it is converted into a one-dimensional
chain of finite character interactions.  The intermediate signs are exact
Walsh/Arf characters and disappear under the final inverse transform.

## 3. Auxiliary dimension and complexity reduction

`PROVED`: a `3 x 3` slice has 256 even boundary-parity states.  Across a cut
in handle variables, only one character bit from each adjacent side crosses.
Therefore

```
handle-site TT rank <= 2 * 2 * 256 = 1024,
binary-site TT rank <= 2 * 1024 = 2048.
```

for every `L`.  Direct tabulation requires `4^(L-1)` polynomial entries.  The
TT representation uses `O(L)` bounded cores for arbitrary inhomogeneous edge
weights.  For translation-invariant anisotropic weights, the bulk cores have
period two.

This compresses the full spin-structure family collectively.  It is not the
ordinary statement that one partition function can be computed by a
fixed-width spin transfer matrix.

## 4. Smallest decisive experiments

1. `4 x 3 x 3`: two independent intersection constructions agree; exhaustive
   `Sp(6,2)` search finds the finite rank-seven relation.
2. Independent `5 x 3 x 3`: the naive basis extension has maximal profile
   `(2,4,8,16,8,4,2)` and is killed.
3. Compatible `4->5`: exact one-defect relative splitting produces 128
   refined sectors; all 64 reunion identities hold coefficientwise with the
   same 16,384-state frontier peak.
4. Compatible `5->6`: the one-defect, three-bit pattern repeats.  Exact genus
   five is independently checked by 13,978,722 excluded face-cover candidates,
   and is also an instance of the published all-size genus theorem.
5. Both local parity templates: generated lengths `4` through `12` have the
   proved face census; cup and tree-cotree routes agree at each exercised
   transition.
6. Independent transfer: the homology-frontier Walsh values and the 256-state
   slice transfer agree modulo `1,000,000,007` at `t=2,3`, exhaustively for all
   64 length-four characters and for 38 declared length-five characters.

The modular checks are `CERTIFIED_NUMERICAL / COMPUTATIONALLY VERIFIED`; the
all-size multivariate identity and rank bound are `PROVED` algebraically.

## 5. Topology, signs, and assumptions

- **Intersections:** `PROVED` by the nested orthogonal decomposition, with
  cup-product and tree-cotree checks on both local transition types.
- **Topology:** `PROVED` minimum genus `L-1` by Millichap--Salinas Theorem 4,
  after matching their path convention exactly.
- **Signs:** `PROVED` local signed-Hadamard Arf/Walsh transform; intermediate
  negative values are Fourier coefficients, while the physical high-
  temperature sum remains positive for ferromagnetic real couplings.
- **Free boundary conditions:** included exactly.
- **Periodic/antiperiodic boundaries:** unproved for this recursive family.
- **Growing transverse dimensions:** unproved; the handle-site bound `1024`
  depends on the fixed `3 x 3` section.
- **Thermodynamic free energy:** no three-dimensional limit is claimed.

## 6. Failure ledger

- **KILLED:** direct extension of the Cycle 3 symplectic basis.
- **KILLED:** assumption that deletion-compatible closed homology embeds
  without a relative boundary bit.
- **CORRECTED:** label `old_last+defect` was briefly described as `defect`
  alone; the exact data and three-bit support were unchanged.
- **NOT A NO-GO:** bounded searches that found no zero-defect rotation.

Full details are in `discovery/failure-ledger-cycle4.md`.

## 7. First point where the surviving candidate may fail

The bound is constant only while the transverse section is fixed.  For an
`L x M x N` family, the parity space has dimension at most
`2^(MN-1)`.  Nothing here proves subexponential behavior as `M,N` grow, nor
that periodic closures preserve the period-two relative labels.  Those are
the exact next obstructions, not hidden assumptions in the present theorem.
