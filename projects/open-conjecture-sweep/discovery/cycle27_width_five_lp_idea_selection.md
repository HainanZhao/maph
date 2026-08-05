# Cycle 27 idea selection scratch

Candidate A — **fresh width-five time-weight LP (chosen).**  Retain the
restriction-selected 5+4+4 geometry but optimize a nonnegative direct time
weight rather than transferring Cycle 22's sparse witness.  Validate the
engine first by separating all options on the known Cycle-22 width-four
certificate, then use deterministic cutting-plane separation and direct
integer replay on every survivor.

Candidate B — a semantic primal assignment lift.  Rejected for now: without
an exact lift-equivalence theorem it can repeat the earlier semantic collapse
and cannot certify a leaf from its own output.

Candidate C — individual/cyclotomic character dual.  Rejected: the complete
quadratic refinement still collapsed, so another aggregate refinement is
lower-information unless it demonstrably escapes class-constant weights.

Questioning the choice: a single fixed geometry can miss a contradiction in
another width-five partition, and a floating LP may yield a non-integer
pseudo-certificate.  It is selected because it changes the witness state
space while retaining a complete direct-CNF verifier; all option separation,
source-mode recovery, bounded rounds, fixed denominators, and direct U/W
replay make failure informative and a success checkable.

Chosen question: does a fresh direct time-weight LP on the frozen 5+4+4
partition produce a new integer deficit among the 60 survivors?  Main
rejected alternative: semantic primal lift.  Falsifier: source-mode,
separation, integerization, or direct replay mismatch.
