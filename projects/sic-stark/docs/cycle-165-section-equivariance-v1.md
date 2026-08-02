# Cycle 165: pointwise section-equivariance obstruction

## Outcome

`PROVED`: no deterministic target action on the oriented `C6` makes the
preregistered pointwise section pushforward intertwine the frozen period-one
Shintani action. The exhaustive census checked all (6^6=46{,}656) set maps
(u:C_6\to C_6) and found zero compatible actions.

This falsifies only the stated pointwise label-respecting operation class. It
does not rule out non-pointwise, nonlinear, fibre-resolved,
characteristic-dependent, or analytically regularized operations, and it says
nothing directly about AFK, Stark, fusion, or TCC.

## Exact witness and criterion

Let (X=(\mathbb Z/6\mathbb Z)^2), let
\(T(a,b)=(5a+b,-a)\pmod6\), and let \(\lambda:X\to C_6\) be the
sealed Cycle-164 section. The operation class is
\(A(\delta_x)=\delta_{\lambda(x)}\). For a target set map (u), write
\(U_u(\delta_e)=\delta_{u(e)}\). Exact compatibility requires

\[
A\,T_*=U_u\,A
\]

on every basis vector. Hence equal section labels must have equal successor
labels. The first frozen lexicographic counterexample is

\[
\lambda(0,0)=\lambda(0,1)=0,
\qquad
\lambda(T(0,0))=0,\quad\lambda(T(0,1))=3.
\]

Thus no function (u)—not merely no affine or group-automorphic one—can
meet the identity. All six source labels have non-singleton successor sets;
the output records every witness. The deterministic principal replay took
0.05 seconds and 13,312 KiB peak RSS.

## Claim boundary and decision

The obstruction identifies the loss caused by quotienting the 36-characteristic
module through the finite section fibres. It does not establish that a valid
coefficient-to-logarithm map must be pointwise, fibrewise, linear, or
Shintani-equivariant in this exact form.

The session companion `/root/decision_companion_2` recommends sealing this
strictly scoped falsifier. That recommendation is adopted. Its stated
falsifier is any replay/census disagreement, transform-direction error,
invalid collision witness, or broader interpretation.

## Next authorized action

Cycle 166 / `B004` must preregister a fibre-resolved (C_6)-torsor state
space, a frozen multiplier law, both preserved orientation anchors, and the
smallest exact intertwining-or-falsifier test. It must retain the coordinate
discarded by the pointwise quotient rather than rename its failed pushforward
as an interface.
