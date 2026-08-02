# Cycle 58 correction: exact `3/50` ties and does not trigger

## Correction boundary

`PROVED` correction: after `s-1` ordinary contractions and the Cycle-48
powered saving, the trigger-minus-selected gap is `3/50`. If a hybrid saves
`gamma`, the adjusted gap is

```text
3/50-gamma.
```

The off-diagonal condition is strict, so exponent closure requires
`gamma>3/50`. Exact `gamma=3/50` merely ties. It can close only if accompanied
by a separately proved logarithmic or constant margin that makes the
underlying inequality strict.

Equivalently, if E13 replaces the entire powered-coordinate input, its
standalone saving must exceed `1/5`; exact `1/5=7/50+3/50` again ties.

This corrects the phrases “at least `3/50`” and target `1/5` in the strategic
interpretation of Cycles 54--57. Their proved gap, centered-trace boundary,
prime-edge covariance identity, and constant-cost support-collapse theorem
are unchanged.

## Affected claims

- Cycle 54: the proved signed gaps `3/50` and `-47/50` are correct. The
  conjectural hybrid target must read `>3/50`, not `>=3/50`.
- Cycle 55: scalar centered traces remain abstractly sharp. The proposed
  prime cumulant must supply `>3/50` or an explicit endpoint margin.
- Cycle 56: the PSD edge kernel and its signed expansion are unchanged. Its
  analytic dichotomy inherits the strict target.
- Cycle 57: the Hilbert-valued coefficient norm and collision bound are
  unchanged. Its restriction target inherits the strict target.

No artifact is overwritten. This document and its replay artifact are the
versioned correction record.

## Gate effect

The live gate is
`HILBERT_EDGE_CUMULANT_RESTRICTION_GT_3_50_OR_ENDPOINT_MARGIN_OPEN`.
