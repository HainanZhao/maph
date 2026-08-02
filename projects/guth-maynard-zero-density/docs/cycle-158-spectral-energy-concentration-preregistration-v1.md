# Cycle 158 preregistration: labelled negative-spectral energy concentration or complexity

Date frozen: 2026-08-02 UTC.

## Frozen inputs

Freeze a fixed `kappa_*>0`, `epsilon_*=1/4`, and

```text
J_*=ceil(8/kappa_*).
```

Starting from Cycle 157, freeze the exact nonnegative external weights,
the no-extra-factor-of-two Hermitianization convention, and a finite-resolution
block map. Each block retains: escape reason, anchor, tail/lobe, orientation,
fixed difference and frequency shells, tensor term, and coefficient-vector
identity. Fix deterministic descending energy order with a lexicographic label
tie-break.

For every block `B`, set

```text
E_B=sum_((ell,d) in B) q_(ell,d)||H_(ell,d),-^(1/2)c_ell||_2^2,
E=sum_B E_B >= kappa_* W_h.                        (1)
```

## Required dichotomy

Prove one of the following for the actual coefficient object.

1. **Finite concentration.** At most `J_*` labelled blocks carry at least
   `(1-epsilon_*)E`; consequently one retained block has

   ```text
   E_B >= (1-epsilon_*)kappa_*/J_* W_h.            (2)
   ```

2. **Robust block-complexity inverse.** Every collection of at most `J_*`
   frozen blocks leaves at least `epsilon_*E>=epsilon_*kappa_*W_h` outside it.
   Record

   ```text
   C_(epsilon_*)(E)>J_*,
   ```

   where `C_epsilon(E)` is the minimum number of frozen blocks that capture
   `1-epsilon` of the negative spectral energy.

Merely defining a partition, sorting blocks, or observing that a raw rank is
large is not a result. The energy must be attached to the actual coefficient
object with all labels retained.

## Boundary and decision record

This search does not prove an individual negative eigenspace aligns with the
coefficient vector until one branch is actually established. It proves no
selected-autocorrelation bound, full moment, density, or intervals.

The persistent companion `/root/guth_maynard_session_mentor` was reactivated
under its stable identity and fixed this advance criterion on 2026-08-02 UTC.
The primary adopts it.
