# Cycle 160 preregistration: phase-anchored colored four-cycle condenser

Date frozen: 2026-08-02 UTC.

## Frozen regime and objects

Freeze

```text
xi in [39/50,83/75],
eta_*=2(39/50-58/75)=1/75,
theta_*=eta_*/2=1/150.
```

Use the actual Cycle-87 atoms

```text
u=(d,q),        z_u=c0 q exp(2pi d/D),
S_k=sum_u a_u e(k z_u),
M4=sum_k U(k/K)|S_k|^4,
```

with frozen `D,Q,K,c0`, actual coefficient normalization, a nonnegative
cutoff `U`, and a smooth `K^(-1)`-scale circle partition. Retain every grid
shift/overlap constant, ordered-pair orientation, diagonal rule, coefficient,
denominator shell, Mellin-alias label, and boundary row.

## Target theorem

Expand `M4` as the second moment of the coefficient-faithful ordered
pair-difference polynomial. Define coefficient-weighted codegree for each
frozen pair-difference cell using that exact expansion.

Prove that, if every frozen cell has codegree at most
`X^(1/150+o(1))`, then

```text
M4 << K(DQ)^2 X^(1/150+o(1)).                      (1)
```

Hence a Cycle-89 forced excess

```text
M4 >= K(DQ)^2 X^(1/75-o(1))                        (2)
```

must produce a labelled cell of codegree at least `X^(1/150-o(1))`, giving a
phase-anchored colored four-cycle inverse.

The `o(1)` budget and every overlap/boundary error must be frozen strictly
below `1/150`; no unregistered loss may consume the margin.

## Registered falsifier

An explicit admissible coefficient family with the excess (2) while every
frozen cell stays below `X^(1/150+o(1))` refutes the condenser target and is
preserved as an inverse falsifier. Inability to prove (1) is not itself a
falsifier.

## Boundary and decision record

This is an upper-band structural theorem search, not a fourth-moment estimate,
large-value theorem, density gain, or interval theorem.

The persistent companion `/root/guth_maynard_session_mentor` was reactivated
under its stable identity on 2026-08-02 UTC. It timeboxed E14D-L at the
Cycle-159 multiplier information loss and selected this Cycle-160 target.
The primary adopts it; E14D-L may reopen during Cycles 160--162 only if an
upstream coefficient-preserving source retaining `t` or ordered atoms is
identified.
