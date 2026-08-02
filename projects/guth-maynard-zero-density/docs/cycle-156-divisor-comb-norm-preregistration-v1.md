# Cycle 156 preregistration: exact divisor-comb norm majorant

Date frozen: 2026-08-02 UTC.

## Objective

Replace the Cycle-154 comb-norm hypothesis by an exact count for the frozen
Cycle-150 witness

```text
w_h(k)=Q 1_(h|k),     k in Z cap [K,2K].
```

Freeze integer `K,h`, positive `Q`, and a fixed real constant `C_h>0` with
`h<=C_h K`.  The special endpoint regime `h<=K` is recorded by `C_h=1`.

## Required conclusion

Prove exactly

```text
||w_h||_2^2
= Q^2 (floor(2K/h)-ceil(K/h)+1)
<= (1+C_h) KQ^2/h.                                (1)
```

This gives the Cycle-154 constant `A=1+C_h`; in particular `A=2` when
`h<=K`.  The lemma must not replace `C_h` by an unregistered bounded factor.

## Boundary

This is a property of the already selected divisor comb only. It does not
prove the actual finite coefficient-escape partition, its negative
projection, positive coefficient transport, a bounded divisor fan, a moment,
density, or prime-interval result.

## Companion checkpoint

The persistent companion `/root/guth_maynard_session_mentor` was reactivated
under its stable identity on 2026-08-02 UTC. It recommends banking this exact
lemma immediately while leaving Cycle 155's actual coefficient-partition
objective unchanged. The primary adopts that recommendation.
