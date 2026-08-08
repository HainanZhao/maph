# Encoder boundary-incidence proof

**Status: PROVED** for the cellular-boundary identities. The width `4..8`
face-walk calculation is an independent exact audit, not the arbitrary-width
proof. No finite-field arithmetic enters this result.

Use the edge convention `e_a(p)=[p,p+e_a]` and let `(a;p)` be the unit square
whose fixed coordinate is `a`. If `b<c` are the other axes, then over
`F_2`

```text
partial(a;p) = e_b(p)+e_b(p+e_c)+e_c(p)+e_c(p+e_b).
```

This identity proves the tables because summing consecutive squares cancels
every repeated interior edge.

## Normal islands

- For `I_3={(0;0,y,2):0<=y<=2}`, the two shared `z` edges are internal;
  the six `y` side rails and lower endpoint `e_z(0,0,2)` lie in `T_W^0`;
  the upper endpoint is `e_z(0,3,2) in X_W^+`.
- For `I_5={(0;0,y,0):0<=y<=4}`, valid for `W>=6`, the four shared `z`
  edges are internal; the ten `y` rails and lower endpoint are gauge edges;
  the upper endpoint is `e_z(0,5,0) in X_W^+`.
- For `I_{2,r}`, `3<=r<floor(W/2)`, the two squares share
  `e_z(0,2r,0)`; their four `y` rails are gauge edges; the two endpoints are
  exactly `e_z(0,2r-1,0),e_z(0,2r+1,0) in X_W^+`.

Deleting the duals of `T_W^0 union X_W^+` therefore isolates precisely these
paths. The symbolic parent tree in the manuscript shows that deleting these
leaf paths leaves the unique large component.

## Opposite cut

For even `W>=6`, sum the seven face families defining `C_W`. Applying the
unit-square identity and cancelling repeated edges leaves exactly

```text
e_z(0,0,0),
e_y(0,y,0)                         0<=y<=W-2,
e_y(0,y,1)                         odd 1<=y<=W-3,
e_x(x,y,1)                         0<=x<=3, 0<=y<W,
e_z(0,W-1,0),
e_y(4,2j,1)                        0<=j<W/2.
```

The first four rows lie in `T_W^0`, the fifth is the unique `X_W^-` chord,
and the last row lies in `P_W^-`. Before deleting `X_W^-*`, the printed
opposite quotient parent map is a tree. Since `X_W^-*` is the only remaining
dual edge crossing this face chain, its deletion produces exactly `C_W` and
its connected complement.

At width four the separate printed base trace applies. At odd width
`X_W^-` is empty, so there is no exceptional cut.

## Independent firewall

`proof/generate_encoder_incidence_tables.py` constructs these boundaries from
the square formula and independently reconstructs them from actual face walks
of the fixed normal and translated-opposite rotations. Widths `4..8` agree,
every selected normal island is an entire dual component, and the opposite
cut is one of exactly two components after exceptional-edge deletion.

Falsifier: an unclassified edge, a selected square absent from the declared
rotation, or an extra dual component invalidates the decomposition. The
firewall reports the first width and edge family rather than fitting a repair.
