# Cycle 64 preregistration: primitive Farey packets

## Question

Compress the Cycle-63 beta-free pair census into primitive rational packets.
Use only the frozen inequalities `H^2=o(X)` and `X^(-1)=o(Delta^(-1))`, and
derive the exact weighted packet-mass target.

## Frozen setup

- `alpha_ell=exp(2pi ell/Delta)-1`, `ell<=cDelta`.
- A hit is `(d,ell,j)` with `1<=d<=H` and
  `|d alpha_ell-j|<=C/X`.
- Reduce `j/d=a/q`, so `d=kq` and `j=ka`.
- `Delta=X^(3/5)`, `H=X^(11/25)`.
- The Cycle-63 weighted pair target is exponent strictly below `17/25`.

## Outcomes

- `UNIQUE_PACKETS`: for large `X`, each `ell` has at most one reduced
  approximant `a/q`, and each reduced approximant serves at most one `ell`.
  The weighted pair census is at most `O(H^2 sum_packets 1/q)`.
- `PACKET_COLLISION`: either uniqueness assertion fails under the frozen
  scales.

No harmonic packet-mass bound, pair census, powered saving, density gain, or
interval gain is asserted by the first outcome.
