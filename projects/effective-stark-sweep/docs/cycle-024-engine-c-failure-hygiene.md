# Cycle 024 — Engine-C failure hygiene

The first full driver retained results only in memory and lost the
active failing record.  That run is preserved as failed v0.  Subsequent
versions use per-packet processes and append transcripts as results
arrive.  Later crashes and interruptions are individually versioned;
none is interpreted as a mathematical obstruction.
