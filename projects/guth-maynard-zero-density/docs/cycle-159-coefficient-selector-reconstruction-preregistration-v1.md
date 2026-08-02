# Cycle 159 preregistration: coefficient-preserving selection-kernel reconstruction

Date frozen: 2026-08-02 UTC.

## Objective

Starting with the actual Cycle-124 polynomial

```text
T_alpha(ell)=sum_x c_x(ell)e(-ell z_x),
```

and the deterministic Cycle 132--136 continued-fraction maps, attempt to
construct an exact selector `chi_lambda(x,x',ell)` in `{0,1}`. Its label
`lambda` must retain fixed difference, collision cell, denominator, rational
center, continued-fraction tail, orientation, tensor frequency, anchor, and
the ordered coefficient-atom identity. It must satisfy

```text
sum_lambda chi_lambda(x,x',ell)=1
```

on the registered selected branch, with every excluded/ambiguous pair sent to
an explicitly labelled residual, and must push forward

```text
nu_(lambda,ell)=sum_(x,x') chi_lambda(x,x',ell)
c_(x')(ell)conjugate(c_x(ell)) delta_(retained labels)
```

exactly to `R^chi_ell(d)`.

## Registered information-loss alternative

If reconstruction fails, identify the **first** Cycle 124--136 map that
lacks enough retained data and prove the loss by two coefficient atoms or
coefficient assignments with the same retained metadata but different
oriented product. State the minimal missing label needed to repair it.

For the ray map, test explicitly whether the multiplier
`(n',n)=t(p,q)` is discarded when only the primitive ray `p/q` and
continued-fraction decorations are retained. A general statement that
``coefficients vary'' without a pair of equal-metadata inputs is not enough.

## Success and boundary

Success is either an executable exact selector/reconstruction or a `PROVED`
information-loss theorem. Neither output proves spectral concentration,
positive transport, a full moment, density, or intervals. If the loss output
is sealed, timebox E14D-L and activate E14D-H rather than add further
untyped selection scaffolding.

## Companion checkpoint

The persistent companion `/root/guth_maynard_session_mentor` was reactivated
under its stable identity and selected this single non-conditional cycle on
2026-08-02 UTC. The primary adopts it.
