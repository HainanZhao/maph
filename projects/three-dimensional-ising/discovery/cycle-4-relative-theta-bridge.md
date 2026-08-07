# Cycle 4 live result — relative theta bridge

## Claim boundary first

`CERTIFIED_NUMERICAL` (exact GF(2), radius zero): the pinned compatible
`4 x 3 x 3 -> 5 x 3 x 3` rotation step has a one-dimensional relative
boundary defect, preserves the old six-dimensional intersection form
label-by-label, and confines every topological label changed by the new slice
to three adapted bits.  This is one finite step.  It is not yet a recurrence,
a bounded-genus compression, a theta-function identity, or a thermodynamic
calculation.

## Exact relative-sector identity

Let `C_4` be the cycle space of the old graph, `B_4` its facial-boundary
space, and `ell_5` the homology label induced by the compatible genus-four
embedding.  Exact elimination gives

```
dim B_4 = 34,
dim B_5 = 44,
dim(B_4 embedded intersect B_5) = 33.
```

Put `K = B_4 intersect ker(ell_5)`.  There is a facial boundary `delta` with
`B_4 = K direct-sum <delta>` and `ell_5(delta) = d`, where `d=96` in pinned
coordinates.  The six pinned old homology representatives map to
`1,2,4,8,16,32`, and their full intersection matrix is unchanged.  The
defect `d` is orthogonal to all six and pairs once with `c=128`; hence `(d,c)`
is the new symplectic pair after an adapted basis change.

For fixed representatives `r_h`, define

```
W_rel[h,epsilon](t)
  = sum over k in K of t^|k + epsilon*delta + r_h|.
```

Then, in the group algebra of the new homology space,

```
sum over A in C_4 of t^|A| X^ell_5(A)
  = sum over h [W_rel[h,0](t) X^h + W_rel[h,1](t) X^(h+d)],

W_4[h](t) = W_rel[h,0](t) + W_rel[h,1](t).
```

`CERTIFIED_NUMERICAL`: all 128 refined polynomials were computed exactly;
each contains `2^33` cycles, and all 64 coefficientwise reunion identities
hold.  The refined computation has the same peak frontier-state count
`16384` as the ordinary 64-sector computation, so this refinement costs no
additional peak state complexity on this instance.

Walsh transformation in `epsilon` gives two exact relative theta channels

```
Theta_h^+(t) = W_rel[h,0](t) + W_rel[h,1](t),
Theta_h^-(t) = W_rel[h,0](t) - W_rel[h,1](t).
```

The new conjugate bit `c` makes four character choices for the newly created
handle.  This is the finite Heisenberg/Weil analogy being tested; no modular
or q-series transformation law is assumed.

## Locality and the next falsifier

`CERTIFIED_NUMERICAL`: on old edges the correction cochain is supported on
exactly two boundary-slice edges (indices 69 and 71), both with value `d`.
Among the 21 added edges, adapted homology labels are distributed as
`0:13, old-bit-5:2, old-bit-5+d:2, c:4`.  Thus the step touches only the last old
coordinate and the new pair: three topological bits rather than all eight.

`CONJECTURED`: compatible embeddings can be chosen at every length so that
each slice touches only a bounded window of adjacent handle characters.  If
true, the Arf-weighted spin-structure sum becomes a fixed-width transfer in
handle space rather than a `4^g` unrestricted sector sum.

The smallest decisive falsifier is the next `5 x 3 x 3 -> 6 x 3 x 3` step:
either the image dimension of old facial boundaries or the number of prior
handle coordinates touched by the added-edge labels grows.  The prior direct
symplectic-basis extension is already falsified and is not being repaired by
this relative construction.

Replay:

```
python3 proof/verify_lane_b_recursive.py
python3 -m unittest tests/test_lane_b_recursive.py -v
```
