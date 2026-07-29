# Cycle 015 — chunked replay and run hygiene

Date: 2026-07-29

Status: `G3 PASSED`

## Preserved failed attempt

The first attempt is not part of the passing evidence.  It failed when
the selected-entry verifier demanded that a table-level max-dimension
prime count equal the smaller prefix's minimal prime count.  Extra work
primes are valid and remain sufficient.  The attempt also revealed that
the manually entered preregistration timestamp postdated execution, so
it was independently ineligible for promotion.

Both defects are recorded in
`certificates/cycle-015-demo-failed-v1.json`.  A v2 preregistration was
frozen before rerun.  It retained the same kill points, sample seed,
sample count, block size, and 1% ceiling, and permitted only:

- acceptance of sufficient extra work primes;
- deterministic normalization of `ldd` load addresses;
- correction of the prospective timestamp.

## Chunk contract

The production driver emits per-table, per-prime residue streams split
into contiguous blocks of at most 512 prefix dimensions.  Chunk words
are unsigned 64-bit little-endian.  Every chunk has a SHA-256 entry in
`manifest.jsonl`.

The manifest is append-only.  Each canonical JSON line includes the
previous line hash and its own hash.  Appends are flushed and synced
before the next task.  A final `SEAL` binds:

- total chunk count and payload bytes;
- table-index hash;
- run-manifest hash;
- terminal hash-chain state.

The table index contains source citations, snapshot/file hashes, and
every generator-prefix hash, but no vector components.  It therefore
implements the Cycle-013 keyed-vector policy.

## Forced-kill resumability

The preregistered pilot contains 128 project-authored synthetic tables,
938 chunks, and 120,064 payload bytes.  Three independent runs were
sent literal `SIGKILL` immediately after manifesting chunks 17, 211,
and 503.  Each resumed from its next chunk boundary and sealed.

Every resumed artifact tree had the same 941 files, 878,327 total bytes,
and tree digest
`e0e99b511791bf585f7075370292f879f719ac7645e2c551a76bfda4aec0d148`
as the uninterrupted run.

## Selected-entry replay

`bin/verify-entry --dataset D --table T --N n --d k`:

1. verifies run-manifest and table-index self-hashes;
2. replays the append-only manifest chain and seal;
3. reads only the dimension block for every required work and overflow
   prime;
4. authenticates those chunks;
5. reconstructs the unique bounded integer numerator;
6. checks both universal overflow residues;
7. returns the exact reduced rational and keyed generator-prefix hash.

Ten entries selected with frozen seed 15019 all returned `VERIFIED`,
matched the independent Python scaled-integer oracle, and passed both
overflow primes.  The largest touched payload fraction was
0.008528785, below the frozen 0.01 ceiling.

## Run manifest

The run manifest records GCC 13.3.0, exact flags, AMD EPYC 9354P CPU,
platform, production and pilot kernel hashes, binary hash, normalized
dynamic libraries, full prime-schedule and verifier-manifest hashes,
every input source hash, and all preregistration hashes.  The required
schema is frozen in `data/run-manifest-template.json`.

The production evaluator retains plain `__int128` reduction and no
optimization changes.  It matches the independent Python oracle on all
ten replay samples.

## Exit gate

- three forced-kill resumes byte-identical: passed;
- ten selected entries: 10/10 `VERIFIED`;
- independent exact oracle: 10/10 equal;
- universal overflow primes: 20/20 equal;
- selected-entry payload ceiling: passed;
- complete run-manifest template: passed.

G3 is closed.  Cycles 016–017 may start only after their pre-run freeze.

## Post-gate batch replay extension

The Cycles 016–018 audit path now accepts a JSON array of selected
entries through the same `verify-entry` executable.  It authenticates
the sealed manifest, run manifest, table index, and prime schedule once,
then performs the unchanged bounded CRT reconstruction and two
universal overflow checks separately for every requested entry.

On the banked pilot, dimensions 7 and 13 replay together and the
dimension-7 result is field-identical to an independent single-entry
invocation.  Single-entry CLI behavior and the 1% contract are
unchanged.  This is verifier orchestration only: it does not modify the
frozen production kernel, data layout, threshold, or certificate
meaning.

Artifacts:
`certificates/cycle-015-batch-replay-extension-v1.json` preserves the
original batch transcript;
`certificates/cycle-015-batch-replay-extension-v2.json` banks the
bounded-memory streaming verifier/audit extension.

The v2 extension authenticates `manifest.jsonl` one record at a time,
extracts only requested 64-bit residues, and discards each selected
chunk payload immediately.  Shared chunks are read once per batch;
only residues plus path/hash metadata survive the scan.  File hashes
are likewise accumulated in fixed 1 MiB blocks.
The extension replayed the original single and batched exact results,
rejected truncation and hash-link tampering, and reproduced a
chunk-boundary stop/resume tree byte-for-byte.  It changes no chunk
bytes, CRT result, threshold, production input, or frozen native
kernel.

Downloaded chunk references are constrained to regular files beneath
the dataset's `chunks/` directory; absolute paths, `..` traversal, and
symlinks fail closed.  Full-dataset audits additionally require an
exact match between manifested paths and files present in the chunk
tree, so unmanifested payloads cannot enter a release archive silently.
