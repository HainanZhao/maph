# Cycle 65 exact density and scope note

For left masses `(p,1-p)`, right masses `(q,1-q)`, and normalized kernel
`[[1,w01],[w10,w11]]`, the search evaluates the fixed 15-edge graph in the
preregistration.  Conditioning first on its five left vertex classes leaves
32 assignments.  Each right vertex then contributes the weighted sum of the
two products over its three incident edges.  This is algebraically identical
to the direct 1,024 assignments of all ten vertex classes.

For rational coordinates with common denominator `D`, let `T` be the integer
numerator produced by that conditional sum and `M` the integer numerator of
the edge density.  Their denominators are `D^25` and `D^3`, respectively, so
the exact sign of `t_H-m^15` is the sign of

```text
T * D^20 - M^15.
```

The proof executable uses arbitrary-precision integers for this expression
and checks its conditional evaluator against an independently coded direct
1,024-assignment evaluator at an interior point, a boundary point, and a
constant equality point.  It exhausts the frozen denominator-4 grid and
replays every retained search candidate after coordinatewise rounding to
denominator `10^9`.

`PROVED`: the named finite exact rows have the signs reported by the packet.
`OBSERVED`: the three frozen differential-evolution streams found no exactly
negative candidate.  The latter is bounded falsifier evidence only and is not
a positivity theorem for the continuous family.
