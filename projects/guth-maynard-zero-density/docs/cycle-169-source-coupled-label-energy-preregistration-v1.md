# Cycle 169 preregistration: source-coupled target-label energy

## Question and claim boundary

Starting from the `PROVED` Cycle-168 compatibility calculus, determine whether
the actual fixed-beta source witness structure forces target-label overlap
between cross-edge landings and target-local packets.  The first output is
only a positive lower bound for the *label energy*, or a source-provenanced
target-label separation certificate. It is not yet a full compatible join.

No edge/packet overlap, recurrence, E7/E9 skeleton, density, or interval gain
is preregistered. Separate marginal bank sizes must never be multiplied.

## Frozen common-source ledger

Freeze a labelled fixed-beta source witness space `Omega` with nonnegative
weight `w(omega)`.  Edge extraction and local-packet extraction retain their
own labels and define unnormalized target pushforwards

```text
E_L = sum_(omega in Omega) w(omega) e(omega) 1_[L_E(omega)=L],
P_L = sum_(omega in Omega) w(omega) p(omega) 1_[L_P(omega)=L].  (1)
```

Here `e,p` are frozen selection multiplicities, not normalized conditional
probabilities. The primary mixed quantity is

```text
M = sum_L E_L P_L.                                    (2)
```

Keep the complete source provenance of every summand in (1).  `M>0` means
same-target-label support only; it does not assert the finer Cycle-168
compatibility form is positive.

## Gates

1. **Exact mixed identity.**  Derive (2) as the pair sum over two labelled
   source copies, before any branchwise normalization, deduplication, or
   data-dependent choice.
2. **Source-coupled lower-bound attempt.**  Use the actual Cycle-165--167
   fixed-beta fibre maps to seek a power-relevant lower bound for `M`.
   Every use of a common source label or target map is explicit.
3. **Label-separation inverse.**  If this fails, retain the complete
   partition of source labels into edge-only and packet-only target supports,
   with their weights and first separation reason. A statement merely that
   supports differ is insufficient.
4. **Finer-cut deferral.**  Only a retained same-`L` mass may enter the
   target-range, packet-admissibility, depth, and strip-constant cuts from
   Cycle 168. `M>0` alone is not a recurrence claim.

## Falsifier and advance condition

The registered falsifier is a legal common-source configuration carrying both
marginal masses but with `E_L P_L=0` for every `L`, or with positive `M` and
zero full Cycle-168 compatibility mass. Preserve the first case as a
label-separation inverse and the second as a finer-cut obstruction.

Advance if a proved positive lower bound for `M` retains full source labels,
or if the source-provenanced target-label separator is exact and exhaustive
for this frozen architecture.
