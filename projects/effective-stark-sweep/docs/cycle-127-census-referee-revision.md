# Cycle 127 — census manuscript referee revision

## Outcome and containment

`PROVED` — The frozen enumerator has always formed orbits of finite
ideals under field conjugation and then attached the pinned
`infinity_2` place.  From 2,461 self-conjugate raw ideals and 11,478
nonself-conjugate raw ideals it obtains

\[
  2461+11478/2=8200.
\]

The prior manuscript description instead invoked conjugation of
pointed one-place moduli.  That wording does not justify the implemented
quotient.  The 8,200 rows and every downstream certificate are
preserved, but the paper is narrowed to the implemented canonical
selected-modulus universe.  It makes no completeness claim for all
pairs consisting of a finite ideal and a distinguished real place.

`PROVED` — The sentence “empty support is exactly the trivial packet
condition” is false in the frozen range.  Empty support is sufficient
for the value-one packet, but 346 nonempty quadratic-support rows also
give `X-1` because all supported derivatives vanish through
imprimitive Euler factors.  The structural T/Q/H partition remains
unchanged.

`OBSERVED` — The H taxonomy has 2,699 rows with complete registered
mechanism status and five preserved incomplete quartic constructions.
The revised paper must not call all 2,704 eligibility decisions
complete.

`OBSERVED` — The local correction gates now pass.  The manuscript was
built twice with pdfTeX 1.40.25 into a seven-page PDF; its log contains
no warning, overfull-box, undefined-reference, or error match.  Both
census manuscript audits pass, and the full suite reports 173 tests
passing in 33.273 seconds (33.43 seconds wall time, 75,064 KiB peak
RSS).  Exact file hashes and replay results are frozen in
`artifacts/census-paper-referee-revision-v1.json`.

Publication and final-circulation status remain contained because the
corrected census manuscript and its archive are still local and have
no immutable census-paper DOI.

## Revision tasks

1. State the implemented finite-ideal-orbit/pinned-place universe and
   its exact count formula.
2. Replace the false support/value-one biconditional and expose the
   346-row evaluated degeneracy.
3. Replace the overlapping H list by an explicit route-by-Roblot
   cross-table and isolate the five incomplete rows.
4. Define the packet polynomial as the squarefree polynomial of the
   distinct effective Artin orbit and state the label-recovery data.
5. Add proof paragraphs for the finite trichotomy and exhaustive Q
   synthesis.
6. Print the numerical radius cap and preserved initial precision
   failure.
7. Replace the transport paragraph by a complete twelve-target table.
8. Add the exact prior-theorem boundary and the local replay command.

## Falsification gates

- Any revised sentence that again identifies the 8,200 rows with the
  full pointed-modulus quotient fails the range gate.
- Any revised sentence that makes empty support necessary for a
  value-one packet fails the 346-row Euler-degeneracy gate.
- Any revised sentence that assigns a complete mechanism verdict to
  the five legacy quartic failures fails the H-status gate.
- Any packet-polynomial theorem that omits the effective Artin-image
  degree and label-recovery data fails the Q-deliverable gate.

The controlling amendment is
`data/census-paper-preregistration-amendment-v18.json`.

## Completion record

All eight revision tasks are complete.  The range and support errors
are corrected without changing or dropping any frozen row; the five
incomplete H rows remain explicit; the packet-polynomial theorem is
narrowed to distinct effective Artin value orbits; the twelve proved
transports and the prior-theorem boundary are printed in full.  The
local correction is therefore `BANKED_LOCAL_CORRECTION`, not a
publication claim.
