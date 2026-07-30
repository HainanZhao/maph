# Effective-Stark results-paper companion

This archive accompanies *Effective Archimedean Stark Theorems over
Real Quadratic Fields: Quadratic Support, Shintani Transfer, and CM
Descent*.

Public record: <https://doi.org/10.5281/zenodo.21708121>.

The paper contains the mathematical arguments. This archive exposes
the exact case data, Arb certificate transcripts, correction records,
and compact proof-checking programs used for the selected computational
theorems. It is not a replacement for the written proofs.
The separate
`paper/effective-stark-results-supplement.pdf` contains the complete
certificate-record map, Artin-label interval table, and queue-level
statistics omitted from the main mathematical narrative.

## One-command verification

From the archive root:

```bash
python3 scripts/verify_results_companion.py all
```

The expected final lines are recorded in
`companion/EXPECTED_OUTPUT.txt`. Individual surfaces can be checked
with `engine-a`, `engine-b`, `engine-c`, or `structural` in place of
`all`.

The complete manuscript-level consistency audit is:

```bash
python3 scripts/audit_results_paper_full.py
```

## Proof checking versus discovery

The two programs above and
`scripts/certify_engine_b_archimedean_places.gp` are proof-checking
entry points. The case-specific cone, recognition, selection, and
bridge programs included under `scripts/` generated or independently
recomputed the underlying certificates. They are retained for full
reproduction but are not needed merely to check the frozen records.

Failed transcripts remain present when they document a correction or
gate. No failed record is accepted by either verifier.

## Claim boundaries

- The natural \(e=8\) route proves the selected
  \(\mathbb Q(\sqrt6)\) CM packet.
- Its \(e=12\) auxiliary-prime route is a cross-check, not a proof.
- RQ-000458 is proved through Engine B. Its Engine-C computation is a
  normalization diagnostic only.
- The three corrected \(e=6\) polynomials are primitive packets. The
  earlier larger polynomials are preserved as powered representatives.
- The Engine-C forward-character convention gives
  \(L'_S(0,\psi)=-(4/e)(\ell_1+i\ell_\sigma)\) and
  \(Y_{\bar s^r}=N_{E/E^+}(\sigma^r u)^{-1}\).  The earlier
  minus-sign normalization prose is superseded; packet polynomials and
  case tags are unchanged.
- Census completeness and conductor trends are outside this archive.
- Roblot's sextic weak-Stark theorem applies to four selected
  order-six ray fields; RQ-002057 is excluded by wild ramification
  above \(3\).  The exact hypothesis audit is included in
  `artifacts/roblot-sextic-overlap-audit-v1.json`.

## Integrity

`MANIFEST.sha256` hashes every other file in the archive. Verify it
with:

```bash
sha256sum -c MANIFEST.sha256
```

The public record must cite the archive SHA-256 and immutable DOI.
