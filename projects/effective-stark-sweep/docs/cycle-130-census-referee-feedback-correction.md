# Cycle 130 — census referee-feedback correction

Recorded: 2026-08-01 UTC, before editing the published-paper source.

## Claim boundary

Zenodo version 1.0 at DOI `10.5281/zenodo.21729947` is immutable. This
cycle prepares a local version 1.1 correction candidate; it does not
alter the public record or claim that the corrected bytes are already
archived.

## Audited feedback

1. The source and rendered PDF both display
   `2461 + 11478/2 = 8200`, with the fraction bar visibly covering only
   11,478. Thus the published mathematical equality is correct.
   `OBSERVED`: linear text extraction can nevertheless invite the false
   reading `(2461+11478)/2`. The correction will print the equivalent
   integer sum `2461+5739=8200`.
2. Theorem 3 uses Arabic condition numbers while its proof also cites
   displayed equations (2) and (3). This is a genuine notation
   collision. The conditions will become (i)--(iv).
3. The nonvanishing of the relative logarithm is load-bearing and is
   asserted too tersely. The corrected proof will cite the companion
   paper's Proposition 4 and regulator identity (9), and will spell out
   that a primitive generator of the rank-one kernel is non-torsion,
   the logarithmic embedding is injective modulo torsion, and the
   chosen orientation makes its nonzero first coordinate positive.
4. Table 2 is a partition by the frozen v5 assignment sets. The v5
   declaration checks their pairwise intersections are empty, and the
   H artifact contains 232/881/1,591 rows in the three assignments.
   This is an exact finite-corpus fact, not a theorem that Shintani and
   cyclic-quartic predicates can never overlap in another range. The
   correction will state that a future overlap would require an
   explicit overlap category rather than silent priority filing.
5. The phrase “residual 73” after the 382 field-certificate keys is
   arithmetically correct but does not explicitly say that 73 is a
   subset of 382. The field inventory splits the 382 exactly into 309
   direct completions and 73 strong-class-certificate cases. The 309
   comprise 48 reused full `bnfcertify` certificates and 261 quotient
   certificates from computed prime-to-three class groups. The paper
   will print this complete partition.

No T/Q/H count or theorem conclusion changes.

## Local gate outcome

The correction candidate builds deterministically in two independent
two-pass PDF builds under `SOURCE_DATE_EPOCH=1785542400`. The result is
nine pages. Pages 2--5, containing every affected display and paragraph,
were visually inspected. There are no overfull-box, undefined-reference,
LaTeX-warning, or error matches. The manuscript, referee-boundary, and
deleted-prime theorem audits pass. The full suite passes 175 tests in
33.18 seconds wall time with peak RSS 75,108 KiB.

Status: `BANKED_LOCAL_V1_1_CORRECTION_CANDIDATE`. No Zenodo mutation or
new-version reservation occurred.
