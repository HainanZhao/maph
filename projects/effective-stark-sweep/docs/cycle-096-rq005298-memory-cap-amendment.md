# Cycle 096 — RQ-005298 memory-cap amendment

The unchanged Cycle-093 run reached 3,601,164 KiB resident memory after
57 minutes under the historical 4,000,000,000-byte GP stack ceiling.
The host had approximately 11 GiB available.  Under the user's explicit
memory authorization, preserve this partial resource observation and
restart the same exact geometry calculation with a 10,000,000,000-byte
GP stack ceiling and the unchanged 10,800-second wall-time cap.

This changes only a preregistered resource cap.  The base geometry code,
target, predicates, and output interpretation are unchanged.  The
partial stopped run has no mathematical verdict.
