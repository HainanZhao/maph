# Cycle 014 — full verified production prime schedule

Date: 2026-07-29

Status: `G2 PASSED`

## Schedule

`data/primes-schedule-v1.json` contains 3,740 ordered primes:

- 3,738 work primes, covering the conservative worst-cell budget;
- two universal overflow primes;
- deterministic descending coefficients \(c<2^{30}\);
- \(p=c2^{32}+1\) for every record.

The schedule is 5,779,087 bytes with SHA-256
`22fadf04ddc70749a5c340483d457590dbe445fbf87883f4875f0ccf71331697`.
The first prime is `4611685941117976577`; the last work prime is
`4611341355891818497`; the overflow primes are
`4611341321532080129` and `4611341278582407169`.

## N−1 certificates

Each record contains the complete factorization of the at-most-30-bit
coefficient \(c\), the induced complete factorization of \(p-1\), and a
single witness \(a\) satisfying:

\[
 a^{p-1}\equiv1\pmod p,\qquad
 \gcd(a^{(p-1)/q}-1,p)=1
\]

for every distinct prime \(q\mid p-1\).  With the complete
factorization, this is the Lucas/Pocklington N−1 criterion; it proves
primality.  The same checks prove that \(a\) has exact order \(p-1\), so
it is the certified primitive root.  Each record also carries the
2-adic valuation and transform capacity.

## Independent verifier

`scripts/verify_prime_schedule_v1.py` imports no project arithmetic
helper.  It independently:

1. proves every coefficient factor is prime by deterministic trial
   division;
2. reconstructs \(c\) and \(p-1\);
3. replays every modular power and gcd;
4. recomputes every 2-adic valuation;
5. checks role, index, family, ordering, and primitive-root identity.

All 3,740 records passed.  The verifier then ran the generator twice in
fresh temporary locations.  Both outputs were byte-identical to each
other and to the banked schedule.

The replay manifest is
`certificates/cycle-014-prime-schedule-manifest.json`, tagged
`VERIFIED_FULL_N_MINUS_ONE_PRIME_SCHEDULE`.

## Exit gate

- worst-cell schedule plus two overflow primes: complete;
- independent N−1 certificate replay: 3,740/3,740;
- overflow certificates: 2/2;
- deterministic byte-identical regeneration: passed.

Cycle 015 may begin.  The frozen production kernel is unchanged.
