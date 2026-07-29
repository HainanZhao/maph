# Cycle 018 packaging preflight: preserved failed run v1

- Status: `FAILED`, not promoted
- Preserved at: `2026-07-29T09:08:14Z`
- Command:
  `.venv/bin/python scripts/audit_release_packaging_preflight.py`
- Git revision under test: `84f1573`
- `package_release_v1.py` SHA-256:
  `768dfdba5496221ae0bc4e66aa8e226ad43da99f79cfaecd2ddf453deb17bd0c`
- `audit_release_packaging_preflight.py` SHA-256:
  `dc509315f947fc8310bc827a6d9e7ad841b0ae28abd034429425ae98c83af744`
- zstd: `v1.5.5`

The first paired source-archive regeneration terminated with:

```text
Traceback (most recent call last):
  ...
  File "scripts/audit_release_packaging_preflight.py", in paired
    raise ArithmeticError("archive regeneration is not byte-identical")
ArithmeticError: archive regeneration is not byte-identical
```

The temporary archives were intentionally deleted when the failed
preflight unwound, so their individual hashes are unavailable.  No
release artifact or verification tag was produced.

An initial hypothesis attributed the failure to the compressor's
automatic worker count.  A second, unpromoted run at
`2026-07-29T09:09:00Z` used zstd's explicit `--single-thread` mode and
failed at the same source-archive comparison.  Direct diagnostics then
showed:

- two raw archives made from the commit object were byte-identical;
- two compressed copies of the same raw archive were byte-identical;
- archives made through the release command's
  `HEAD:projects/certified-qmc` tree object had changing tar mtimes.

The actual defect was therefore the source tree object's missing commit
timestamp, not compressor concurrency.  The corrected source-archive
command pins every member mtime to the selected revision's committer
timestamp, and compression remains in explicit `--single-thread` mode
to eliminate another unnecessary environmental degree of freedom.  The
corrective version must pass the same two-run, byte-identical preflight
before packaging can proceed.

These changes affect only release archiving and compression; the frozen
production arithmetic kernel, compiler flags, inputs, and running
production process are unchanged.
