# C78 reinstatement timestamp correction

## Correction — PROVED metadata only

The sealed C78 reinstatement v2 contains
`recorded_at_utc = 2026-08-05T19:05:00Z`, which is ahead of the actual
write time. This is a deterministic metadata error only: it does not affect
the theorem, source dependency, frozen hashes, replay, or gate decision.

This v3 correction supersedes the v2 reinstatement status record and records
the actual bounded write timestamp. The v1 theorem, v1 withdrawal, and v2
reinstatement records remain immutable historical artifacts.
