# Cycle 069 — R-13, RQ-007500 recovery, and paper fork

**RQ-007500 RE-PASSES under GENUINE reconstruction.** The case is
\(\mathbb Q(\sqrt{185})\), modulus
\(\left[\begin{smallmatrix}30&6\\0&3\end{smallmatrix}\right]\infty_2\)
of finite norm \(90\), with support order \(8\). The contaminated
generic route had treated the two-place field at the original,
conjugation-unstable finite modulus as the actual normal closure.
Starting instead from the one-place degree-eight ray field and applying
`nfsplitting` gives a degree-32 normal closure with group `[32,38]`.
Its polynomial is exactly the historical polynomial. Independent
ray-field reconstruction over \(\mathbb Q(\sqrt{-3})\) and
\(\mathbb Q(\sqrt{-555})\) matches that field on both routes. The
effective tag is `VERIFIED_W2_GENUINE_RECOVERY`; W3 remains pending,
and the completed B-closure count returns from 50 to 51.

## R-13 provenance correction

Every deciding predicate is now GENUINE or PROXY; mixed aggregate
artifacts are recorded as MIXED. Historical artifacts remain immutable,
but `artifacts/predicate-provenance-ledger-r13-v1.json` is authoritative
for effective tags. Of the 51 historical individual W2 certificates,
50 are GENUINE and the original RQ-007500 artifact is
`SUPERSEDED_PROXY_W2`; the separate recovery certificate restores the
case through a GENUINE path. No PROXY or MIXED record has an effective
`VERIFIED_*` tag.

The root cause and joint responsibility are recorded in
`docs/methods-proxy-root-cause-r13.md`. The proxy represented
conjugated ideals in one ray group before proving modulus stability. It
entered five load-bearing paths. The implementation confused agreement
with provenance, and the human verifier made the same
architecture-implies-genuine assumption when banking the earlier
246-for-246 attestation.

## Genuine battery gate

The new Engine-B battery constructs the one-place field and its
conjugate-modulus field, selects their normal compositum, computes the
actual derived subgroup, and independently reconstructs every surviving
imaginary-base route. It passed all three Engine-B structural anchors.
A fresh full theorem-level replay passed 7/7 anchors. These gates close
before any of the 241 proxy-exposed rows can affect census counts.

The first degree-40 recovery row exposed a multi-minute, multi-gigabyte
tail. The one-node-hour per-case cap remains active; a cap produces a
named FRONTIER result rather than an infrastructure project. The
pre-registered estimate is 13–21 total case-cycles for tracks a–c, or
10–16 wall-clock research cycles with the index pass in the background.
The estimate will be reported against realized tranche timings, never
silently rewritten.

## Claim boundary

Genuine reconstruction may change B eligibility and closure counts,
the FRONTIER total and taxonomy, exact C completeness, the
FRONTIER-versus-norm trend, and the odd-index landscape. It cannot
change the seven anchors, any of the 25 promoted theorem cases, the
order-six and order-ten headlines, the RQ-000458 dual route,
RQ-000129, RQ-002057, the \(\mathbb Q(\sqrt{35})\) generic C theorem,
the uniform Engine-A theorem, or the absolute-abelian no-go lemma.

The old 9.93%, 21.60%, 27.26%, 31.65% norm-quartile trend is
`PROVISIONAL_WITHDRAWN` until census v5 and may not appear unflagged.

## Paper fork

`paper/effective-stark-results-paper.md` is now assembled and
scope-sealed. It contains only proxy-clean theorem results and is
independent of recovery outcomes. The census draft is visibly withheld
pending v5. Its revision history remains part of the data-methods
record, but no population count or W4 statistic is promoted meanwhile.

The containment cost the census its statistics but not one of its
theorems: case-level promotion held while an intermediate
classification layer leaked.
