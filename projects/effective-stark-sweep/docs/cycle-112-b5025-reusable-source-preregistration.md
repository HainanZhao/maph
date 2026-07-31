# Cycle 112 — B5-025 reusable-source transport batch

The RQ-000195 attempt established that the source Arb replay, not the
target arithmetic, is the time bottleneck.  This amendment freezes a
different proof organization for B5-025: validate RQ-000190's already
sealed direct certificate once by its frozen data, transcript, and
program hashes; then run fresh exact transport gates for every target.

The source certificate is not recomputed and hash validation is not
called an independent numerical route.  Every target must still pass
the finite-modulus, exact ray-map/sign, Euler-deletion, and positivity
gates.  Any failed target remains unpromoted.  The batch consists of
all eight noncanonical B5-025 members, ordered by finite norm then RQ
identifier.
