# Cycle 010 — bounded W1 pilot preregistration

Frozen before execution: 2026-07-29 UTC

This pilot covers every Galois-deduplicated ideal case in the already
frozen census satisfying \(D\le13\) and
\(\operatorname{N}(\mathfrak f)\le12\).  The subset is selected by
parameters alone, before any structural verdict is computed.

The pilot validates exact ray-group construction, the sign-class
Fourier support, Engine-A selection, the two-place projective
Engine-C screen, and the operational Engine-B unit/index predicates.
It is not the Phase-1 yield checkpoint: its yield cannot authorize the
census-paper framing.

Acceptance requires:

1. every field passes `bnfcertify`;
2. every selected case terminates without a PARI error;
3. every case receives exactly one of `ROUTE_CANDIDATE` or `FRONTIER`;
4. every `ROUTE_CANDIDATE` case has exactly one provisional engine;
5. every `FRONTIER` case has exactly one obstruction;
6. the frozen Paper-I/II structural anchor moduli that lie in the
   pilot range are separately checked against their historical
   ray-group data before any W1 code is reused for the full census.

`ROUTE_CANDIDATE` is not `PROVED` and is not counted at the Phase-1
yield gate.  It records that the exact W1 structural predicates point
to an engine; the engine-specific packet, exponent, and identification
gates remain due.

The pilot has no minimum-yield threshold. Unexpectedly high or low
candidate yield is a research finding, not grounds to amend the screen.
