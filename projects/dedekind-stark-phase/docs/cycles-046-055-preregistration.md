# Cycles 046--055: ray-class cocycle bridge preregistration

Frozen: 2026-07-31 UTC, before extracting a non-SIC phase feature.

## Target

Determine whether the exact SIC multiplier machinery contains a
convention-preserving construction

\[
(K,\mathfrak m,\chi,\infty_2)
\longmapsto
(Q,A,\boldsymbol r,\mathcal L,\mu),
\]

where \(Q\) is an oriented primitive indefinite form, \(A\) its positive
level stabilizer, \(\boldsymbol r\) a characteristic, \(\mathcal L\) the
positive-lift data, and \(\mu\in\mu_4\) the Dedekind--Rademacher cocycle
phase. The output must be covariant under character inversion and under
the dominant-embedding gauge.

## Convention freeze

- Matrices act on column characteristics from the left.
- The classical Dedekind sum and `rademacher_phi` convention are those
  in `src/dedekind.py`.
- An oriented quartic character has \(\chi(\gamma)=i\); replacing
  \(\gamma\) by \(\gamma^{-1}\) conjugates both analytic and cocycle
  phases.
- The distinguished place is the negative-square-root embedding used
  throughout the Stark papers.
- A successful phase prediction must be invariant after converting the
  weak solution to the dominant-embedding gauge.

## Frozen anchors

1. dimension 4, discriminant 5, modulus 4;
2. dimension 5, discriminant 5, modulus 5;
3. dimension 7, discriminants 8 and 32, modulus 7;
4. dimension 8, discriminants 5 and 45, modulus 8.

Every extracted universal formula must replay its source anchor exactly.
No convention is repaired case by case after seeing a failed replay.

## Non-SIC gate

RQ-000129 is the first and only non-SIC control opened in this block.
Its input is limited to its already banked field, modulus, oriented
quartic character, ray labels, and independent weak solution. Its phase
label is not used while attempting the construction.

## Outcomes

- `GENERAL_BRIDGE`: ray data canonically determines the complete tuple
  and passes every anchor plus RQ-000129.
- `RESTRICTED_SIC_BRIDGE`: a universal arithmetic evaluator exists once
  form/characteristic/lift data are supplied, but ray data alone does
  not canonically supply those data.
- `NO_BRIDGE`: even the supplied-tuple arithmetic fails to unify the
  anchors.

Coefficient fitting and a 50-row holdout remain forbidden in all three
outcomes. A general bridge requires a theorem, not a numerical match.
