# Cycle 2 — Stream C explicit-formula v2 adversarial audit

Claim boundary: `OBSERVED` for archival license and mirror provenance. The
mathematical formula and transfer statements are `PROVED` only conditional on
the exact theorem text in the two pinned PDFs. This audit preserves ledger v2
and Route B v4; it does not declare G0 PASS.

## Outcome

`PROVED` conditional on the pinned theorem text: the formula unit states
\(x\ge2\), \(T>0\), half weights at integral prime powers, and the needed
remainder. The proof unit explicitly counts every zero with multiplicity and
ends with a completed proof. Both Guth--Maynard truncation choices therefore
meet the theorem's displayed height condition.

`PROVED` conditional on that formula and the HSW+Bui local-count node: the
integer-endpoint transfer, nearest-other-prime-power bound, and boundary-strip
bridge are mathematically sound. The subtraction cancels the constant term;
the elementary logarithm varies harmlessly. A literal
\(|\rho|\le T\)/\(|\gamma|<T\) disagreement lies in unit strips around
\(\pm T\), and costs \(O(x\log T/T)\).

`OBSERVED`: the current evidence does not prove that the *frozen author-hosted
bytes* are licensed OCW copies of the official DSpace materials. The official
license is CC BY-NC-SA 4.0 and the official indexed `errorbounds.pdf` path was
identified, but DSpace returned 405/403; byte identity could not be checked.
No official OCW/DSpace locator for the frozen `von-mangoldt.pdf` proof byte
was located in this audit. The author calendar establishes course association,
not byte-level OCW provenance.

`OBSERVED`: Route B v4's formula-source promotion consequently has an
archival-source-authority gap under a strict reading of the preregistration.
This does not refute the formula, the endpoint conversion, multiplicity, or
the two exponents. It blocks treating the v4 source closure itself as a
standalone `PROVED` archival node.

## Exact blockers

- `OBSERVED`: obtain an official retrievable OCW/DSpace proof-unit URL or
  manifest connecting `von-mangoldt.pdf` to course handle `1721.1/101679`.
- `OBSERVED`: establish byte identity, or an official hash, for the frozen
  author formula mirror and the inaccessible DSpace object.
- `OBSERVED`: pin the PDF text-extraction tool version. The checker invokes
  `mutool`; this run observed version 1.23.10, but v2 does not record it.

## Replay

```sh
python3 projects/guth-maynard-zero-density/proof/audit_cycle2_stream_c_explicit_formula_v2_v1.py --check projects/guth-maynard-zero-density/artifacts/cycle-2-stream-c-explicit-formula-v2-adversarial-audit-v1.json
python3 -m unittest projects/guth-maynard-zero-density/tests/test_cycle2_stream_c_explicit_formula_v2_adversarial_audit_v1.py
```
