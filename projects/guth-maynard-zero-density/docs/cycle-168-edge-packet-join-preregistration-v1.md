# Cycle 168 preregistration: cross-edge/local-packet join

## Question and claim boundary

Starting from the `PROVED` Cycle-167 reduced-rational cross-label edge
classifier, determine whether a retained beta-anchored edge can be joined,
label-faithfully, to an independently retained *target-local* rational packet.
If it can, the target edge endpoint is a genuine beta seed for that local
packet and may invoke the exact Cycle-67 propagation identity.  If it cannot,
preserve the first complete support-separation obstruction.

No overlap, recurrence, E7/E9 skeleton, density, or interval gain is
preregistered.  A global count of edges and a global count of packets is not
an incidence theorem.

## Frozen records and join schema

An eligible Cycle-167 edge retains

```text
E=(beta, ell, L=ell+u, a_E, q_E, K_E, h, j, h^+, j^+),
```

where its target is a genuine strip hit

```text
|j^+ + beta-h^+ alpha_L| <= C_E/X,    h^+ in [H,2H]. (1)
```

Independently, a target-local packet record retains

```text
P=(L, a_P, q_P, K_P, C_P),
|q_P alpha_L-a_P| <= C_P/(K_P X),     q_P K_P<=H.    (2)
```

The packet need not carry beta; its entire purpose is to be seeded by (1).
Retain the complete edge and packet records; their compatibility is a relation,
not equality of one over-refined key.  In particular, an edge need not have
the packet's denominator or depth.  For an edge record `e` and packet record
`p`, freeze

```text
Comp(e,p) = [L_e=L_p, h^+_e in I_p,
             q_P K_P<=H, C_E+C_P<=C_join,
             K_P>=K_crit].                           (3)
```

Here `C_join` and `K_crit` are frozen output-interface constants.  Retain all
source labels of `E` and construction labels of `P`.  Do not quotient either
side by label, fraction, depth, strip constant, or target range before the
compatibility ledger is frozen.

## Gates

1. **Exact composition.**  For each compatible `(E,P)`, prove that
   `h_k=h^+ + k q_P`, `j_k=j^+ + k a_P` are beta-anchored target-strip hits
   for the Cycle-67 admissible one-sided range.  Retain every source and
   packet label.
2. **Weighted support ledger.**  Define weights on complete edge records and
   complete packet records.  Derive the exact compatibility bilinear form
   `J=sum_(e,p) E_e P_p 1_Comp(e,p)`, rather than multiplying global totals
   or taking a diagonal product on a fictitious common key. Preregister the
   rule that a support-only count is non-progress unless it retains a fixed
   labelled fibre or supplies a proved lower bound for `J`.
3. **Separation alternative.**  If the required overlap is absent, retain
   the first reason-labelled cut: target-label separation, target-range
   separation, subcritical-depth/packet-admissibility, or strip-constant
   incompatibility.  It must
   carry its full edge and packet supports, not merely their cardinalities.
4. **Loop containment.**  A closed cross-edge loop is not a substitute join.
   The affine update telescopes to
   `(h_L-h_0)(1+alpha_ell)=O(X^-1)`, so at a common label it has trivial
   integer holonomy for large `X`; it cannot by itself create a nonzero
   Cycle-67 packet step.

## Advance condition and falsifier

Advance if an exact labelled join produces a genuine seeded local packet with
its complete depth/range ledger, or if the listed support cuts are proved
exhaustive for the frozen join architecture.

The registered falsifier is a legal massed edge bank and legal local-packet
bank with disjoint complete supports, or with every intersection losing target
range or critical depth. Preserve it as a typed incidence obstruction. Do not
infer an overlap from two separate mass bounds.
