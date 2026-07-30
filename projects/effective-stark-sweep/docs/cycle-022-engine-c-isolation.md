# Cycle 022 — Engine-C packet isolation

Distinct primitive quartic fields are deduplicated within each case.
Every packet is processed in a fresh PARI process.  This isolates tool
failures and prevents a failed packet from erasing completed results
from the same case.
