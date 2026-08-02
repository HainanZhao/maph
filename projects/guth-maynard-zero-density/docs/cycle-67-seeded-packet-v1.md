# Cycle 67: deep packets become recurrence only after a seed

## Claim boundary

`PROVED`: a beta-free packet of depth `K` supplies possible resonant
differences, not actual transport hits. If one genuine hit is supplied, the
packet propagates it to at least `1+floor(K/2)` hits on a single
`q`-arithmetic progression, with strip constant enlarged from `C0` to
`C0+C1` and no exponent loss.

Consequently, a seeded packet with `K>=X^(6/25-o(1))` creates a realized
transport recurrence of the critical Cycle-19 degree. No theorem bounding
the number of seeds or such packets is proved, and no powered, density, or
interval gain follows.

## Propagation identity

Assume

```text
|j0+beta-h0 alpha| <= C0/X,                         (1)
|q alpha-a|       <= C1/(KX),                       (2)
```

where `h0 in [H,2H]`, `(a,q)=1`, and `qK<=H`. For every integer `k` with
`|k|<=K`, put

```text
h_k=h0+kq,   j_k=j0+ka.
```

Then

```text
j_k+beta-h_k alpha
 =(j0+beta-h0 alpha)-k(q alpha-a),
```

so (1)--(2) give

```text
|j_k+beta-h_k alpha| <= (C0+C1)/X.                  (3)
```

This retains the numerator labels as well as the row progression.

## Boundary count

The distances from `h0` to the two endpoints of `[H,2H]` sum to `H`.
Therefore one direction from `h0` admits at least

```text
floor(H/(2q)) >= floor(K/2)
```

steps of size `q`. Along that direction, (3) supplies at least
`1+floor(K/2)` actual hits. Endpoint location cannot remove a fixed power of
the recurrence.

At `K=X^(kappa+o(1))`, the realized degree exponent is `kappa`. Hence the
Cycle-65 dangerous threshold `kappa=6/25` is exactly the degree exponent
already isolated in the critical synchronization graph. If the packet is
maximally deep, admissibility `qK<=H=X^(11/25)` gives
`q<=X^(1/5+o(1))`.

## Scope correction and route

The Cycle-65 phrase “deep packet recurrence” is valid only for a packet
carrying at least one original triple-census seed. Without a seed, the
packet records values of `d` for which recurrence is arithmetically allowed;
it does not assert that any `h` satisfies the beta-dependent strip.

`CONJECTURED`: after the primitive Poisson form is split into minor and major
arcs, a major-arc contribution large enough to obstruct `X^(31/25)` should
either contain a seeded deep packet or be bounded by the same phase
alignment argument that supplies the seed. The enlarged constant in (3)
must be retained in that proof.

## Gate effect

The structured E13 branch is now
`SEEDED_X6_25_AP_RECURRENCE_OPEN`; beta-free depth alone is not a completed
handoff to E7/E9/E10.
