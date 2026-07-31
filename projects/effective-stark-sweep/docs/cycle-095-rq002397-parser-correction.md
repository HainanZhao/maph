# Cycle 095 — RQ-002397 retry parser correction

The Cycle-094 fresh-process retry reproduced the documented PARI/GP
2.15.4 `bnrclassfield` segmentation fault in 0.017 seconds.  GP exited
with status zero, so the generic process-status field in the preserved
v1 observation incorrectly says `COMPLETED`.  The stderr diagnostic and
missing geometry verdict show that this is a tool failure.  A versioned
v2 successor corrects the compute status to `TOOL_FAILURE_REPRODUCED`.

No mathematical verdict changes.  The result confirms that more wall
time on PARI/GP 2.15.4 is not a remedy for this target.
