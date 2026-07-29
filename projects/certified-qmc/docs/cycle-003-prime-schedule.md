# Cycle 003 — deterministic NTT/CRT prime schedule

Date: 2026-07-29

The prototype schedule scans coefficients downward from \(2^{30}-1\)
and admits exactly those signed-63-bit integers

\[
p=c\,2^{32}+1
\]

that pass deterministic Miller–Rabin for unsigned 64-bit inputs.
The small coefficient \(c\) is completely factored by deterministic
trial division.  The least primitive root passing the complete
prime-divisor order test is then recorded.  Every schedule entry is
re-audited from its full factorization.

The first 16 primes are frozen in
`certificates/cycle-003-prime-schedule.json`.  Every one supports at
least \(2^{32}\)-point radix-two transforms; entries with even \(c\)
support more.  The first entry reproduces the proposal's previously
audited prime and primitive root.

This is a verified prototype schedule, not yet a claim about an
optimized Montgomery/NTT implementation.  More entries can be generated
by the same rule when a reconstruction bound requires them.

Decision: **CONTINUE**.

Tag: `VERIFIED`.
