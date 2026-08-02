# Cycle 156: exact divisor-comb norm majorant

## Claim boundary

`PROVED`: for the exact sampled comb

```text
w_h(k)=Q 1_(h|k),      k in Z cap [K,2K],
```

with positive integers `K,h` and a frozen fixed `C_h>0` satisfying
`h<=C_hK`,

```text
||w_h||_2^2
=Q^2(floor(2K/h)-ceil(K/h)+1)
<=Q^2(K/h+1)
<=(1+C_h)KQ^2/h.                                  (1)
```

Thus the Cycle-154 norm condition holds with `A=1+C_h`; for the explicitly
frozen subregime `h<=K`, it holds with `A=2`.

This does not produce an actual finite coefficient-escape partition, an
escape projection, positive transport, a bounded fan, a moment, density, or
prime-interval result.

## Derivation

The multiples of `h` in the inclusive interval are precisely the integers
`jh` with `ceil(K/h)<=j<=floor(2K/h)`, so their number is the first equality
in (1).  Any interval of length `K` contains at most `K/h+1` members of a
spacing-`h` progression.  Finally `h<=C_hK` gives `1<=C_hK/h`.

## Cycle-154 interface

Cycle 154 had made the one-ray conclusion conditional on
`||w_h||_2^2<=AW_h`, `W_h=KQ^2/h`.  Equation (1) discharges that condition
for the selected comb once its frozen anchor ratio is supplied.  The separate
Cycle-155 task remains indispensable: no actual escape class is localized
until the exact finite reason-labelled coefficient partition is constructed.

## Decision record

The persistent session companion `/root/guth_maynard_session_mentor` was
reactivated and recommended this exact-count result as an immediate, separate
lemma, while retaining Cycle 155 as the substantive next action. The primary
adopts that recommendation.
