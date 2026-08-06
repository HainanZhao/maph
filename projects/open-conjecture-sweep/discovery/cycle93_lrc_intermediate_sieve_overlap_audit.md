# C93 LRC intermediate-sieve overlap audit

`PROVED` from Sungkawichai--Trakulthongchai (2026), Section 3 and Section 4:
the intermediate lift/projection operations preserve the relevant upper-bound
inclusion, but their eventual-properness route still requires a lift with
\(c=k+1\).  The paper states this explicitly before its polynomial argument.
That argument assumes \(k+1\) is an odd prime and works in the field
\(\mathbb Z_{k+1}\).

For the program target \(k=13\), \(k+1=14\) is composite.  The proposed
“intermediate-sieve bridge” therefore collapses to the same missing
composite-modulus step that C84 tested: a verbatim \(\mathbb Z_{14}\)
target-box extension has an exact zero-divisor obstruction.  The source does
not supply a replacement projection invariant that avoids that field step.

## Decision

Reject LRC intermediate-sieve continuation before preregistration.  Do not
reuse the C50 p=199 local engine, C84 target box, or a staged \(2\)-then-\(7\)
lift merely as a computational variation.  A future LRC selection needs a
source-clear composite replacement for the field argument, not another lift
schedule.
