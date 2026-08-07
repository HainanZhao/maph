# Cycle 8 decision: generic nonuniform G1

## Outcome

`PROVED`: for the explicit canonical checkerboard embedding and every
transverse width `w>=3`,

```
R_infinity(w)=2^(w^2-1)
```

over the fraction field of independent nonuniform edge weights.  A uniform
sufficient longitudinal length is `n_0(w)<=11`.  The nonzero-minor locus also
meets the strictly positive ferromagnetic orthant.

The universal upper bound is the previously sealed G0 theorem.  The new
lower bound is a reachability/observability proof: a normal five-layer
encoder gives full left separator rank, an opposite-phase five-layer encoder
gives full right separator rank, and a two-slab buffer has an invertible
diagonal specialization on the even-mask carrier.  The two encoder trees are
not glued into one sparse graph.

## Exact boundary

The result is for generic independent nonuniform weights.  It does not prove
homogeneous anisotropic or isotropic tightness, and it does not prove
nonvanishing at any particular physical temperature.  For `w=L`, the exact
carrier remains `2^(L^2-1)`; no cubic thermodynamic limit or critical point is
obtained.

## Falsifiers retained

The following stronger constructions are false and remain in the failure
ledger:

- reflection of one prefix encoder into the same global canonical labeling;
- replacement by a locally full opposite-phase encoder without a buffer;
- two fixed endpoint trees joined by a one-layer connector;
- freezing both endpoint chord bases and optimizing only the remaining
  edges.

These failures expose the difference between one simultaneous sparse
specialization and separate full-rank polynomial factors.  G1 needs only the
latter.

## Replay

```
python3 proof/verify_g1_buffered_factorization.py \
  --maximum-symbolic-width 20 --maximum-global-width 6
python3 proof/verify_g1_lifted_widths.py
python3 -m unittest \
  tests.test_g1_arbitrary_width_generic_tightness \
  tests.test_g1_buffered_factorization -v
```

The first command checks the explicit parity recursions, even-width
rank-one relation, and their simultaneous placement in `G_(11,w)`.  The
second is an independent finite-width route through connected lifted-matroid
specializations at `w=3,...,7`.
