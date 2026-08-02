# Cycle 170 preregistration: projective packet lift through a cross edge

## Question and claim boundary

Starting from a compatible beta-anchored cross-edge and a source-local packet
at its source label, determine whether the exponential identity lifts them to
a seeded deep target-local packet. The permitted alternative is an exact
projective content, error-load, depth, or admissibility obstruction with all
labels retained. No mass lower bound, E7/E9 skeleton, density, or interval
gain is preregistered.

## Frozen signed data and identity

Retain a source packet and a reduced-rational cross edge:

```text
d alpha_ell-b = delta,       |delta|<=C_S/(K_S X),
q E_u-a = e,                 |e|<=C_E/(K_E X),
1+alpha_L=E_u(1+alpha_ell),  L=ell+u.                (1)
```

Require the transported seed from Cycle 167 to be integral and in its frozen
target range. Define signed projective data

```text
D=q d,
N=a(d+b)-q d,
g=gcd(|D|,|N|),
Q=|D|/g,  A=sgn(D)N/g.                                  (2)
```

The exact target identity is

```text
D alpha_L-N = a delta + e(d+b+delta).                 (3)
```

Freeze the conservative error load

```text
Lambda = a C_S/K_S + (|d+b|+1) C_E/K_E,               (4)
K_err=floor(g/Lambda) when Lambda>0, and infinity
when Lambda=0;
K_T=min(K_err, floor(H/Q)).                            (5)
```

The `+1` is permitted only after separately checking
`C_S/(K_S X)<=1`. The classifier retains `Lambda` rather than replacing it
by a denominator-only heuristic.

## Gates

1. **Exact lift.** Prove (3), including all signs, and the reduced relation
   `|Q alpha_L-A|<=Lambda/(gX)`.
2. **Seeded target-packet gate.** If `K_T>=1`, prove the transformed edge
   endpoint is a genuine beta seed for this target packet. A deep handoff
   additionally requires both

   ```text
   K_T>=X^(6/25-o(1)),       Q K_T<=H.                (6)
   ```

3. **Exhaustive obstruction classifier.** If the lift is not a deep usable
   packet, retain the first of: nonintegral/out-of-range seed, zero/low
   projective content, error-supported subcritical depth, or denominator
   capacity/subcritical admissible depth. A large `g` alone is non-progress.
4. **Mass deferral.** Only after this finite classifier is proved may a later
   block seek a lower bound for compatible joined pairs in actual banks.

## Falsifier and advance condition

The registered falsifier is a fully compatible beta-retaining joined pair
with high projective content but failed depth or `QK_T<=H`, not assigned to
one of the frozen obstruction labels; or a critical joined bank supported on
low-content states without a bounded-complexity retained web.

Advance if the exact classifier is exhaustive within this projective-lift
architecture, or if it yields a labelled seeded deep target packet.
