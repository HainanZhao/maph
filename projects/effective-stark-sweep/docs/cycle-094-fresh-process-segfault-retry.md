# Cycle 094 — fresh-process segmentation-fault retry

The user authorized one direct retry before assigning the four
PARI/GP 2.15.4 `bnrclassfield` segmentation faults to the newer-PARI
route.  The target is RQ-002397, packet 2, because it is the first
recorded failure.  The run is a fresh GP process using the unchanged
exact geometry screen, the historical 4 GB GP stack, and a 1,200-second
wall-time cap.  It runs concurrently with, but independently of,
RQ-005298.

A crash, timeout, or successful completion changes only the tool-status
record.  A successful positive geometry predicate must still pass the
Cycle-093 independent exact replay before changing the H taxonomy.
All earlier failure artifacts remain preserved.
