# C79 endpoint-foundation idea selection

## Decision question

Can the weighted compatible three-qubit (Q=I/2) endpoint be established
from published, exactly scoped ingredients (or directly by an independently
replayable derivation), so that C78's interpolation is no longer conditional
on the Song--Chen preprint?

## Question the question

The tempting question is whether the C78 interpolation is correct.  Its exact
target algebra is already checked; that reframing hides the real blocker:
the endpoint's authority.  A numerical search or another interpolation cannot
replace a proof of the endpoint.  Conversely, merely finding that the
Song--Chen argument looks sound would still leave the repository's published-
theorem requirement unmet.

## Question the questioning

The certification rule might cause us to overvalue reconstructing the
preprint's proof verbatim.  The useful question could instead be whether an
earlier published result already has the exact endpoint scope, or whether a
short direct Ky Fan proof can eliminate a cited black box.  A reconstruction
that imports an unverified corollary is not independent; a literature match
with different tensor support or freely chosen rather than compatible
marginals is not a bridge.

## Distinct candidate mechanisms

1. **Published-source route.** Search for a peer-reviewed theorem exactly
   covering the weighted compatible (Q=I/2), three-qubit, pair-support
   endpoint.  Falsifier: every candidate leaves at least one of compatibility,
   arbitrary weights, or all three supports outside its hypotheses.
2. **Three-prefix majorization reconstruction.** Independently prove the
   ordered prefix bounds (X_j\preceq T_j): the one-term case is elementary,
   the two-term case is checked against published Alhejji--Knill Corollary
   4.10, and the three-term case follows from the published Higuchi--Sudbery--
   Szulc polygon theorem plus the qubit spin-flip identity and exact Ky Fan
   algebra.  Falsifier: a prefix inequality cannot be derived under its exact
   stated hypotheses, or an exact compatible state violates it.
3. **Direct variational route.** Maximize each of the first three Ky Fan sums
   of (X_3) over pure states with a projector variational form, then reduce
   to one-qubit spectra.  Falsifier: the variational reduction retains
   unbounded two-body correlation data, making it no shorter or more
   independent than mechanism 2.

## Choice

Run mechanisms 1 and 2 as independent light-compute source/proof checks.
Mechanism 2 is the leading candidate because the published components have
clear, separately checkable hypotheses and it produces a replayable proof
rather than reliance on a recent preprint.  Mechanism 3 is the main rejected
alternative for now: it is a genuinely different backup but has no smaller
rigorous interface than the prefix route.  No executable proof or test runs
are authorized until the C79 preregistration freezes the exact cited theorem
statements, the pure-state reduction, and the finite symbolic checks.
