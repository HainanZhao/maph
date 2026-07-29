# Cycles 016–017 fidelity production

## Pre-run freeze

The production grid is fixed in
`data/cycles-016-017-fidelity-spec-v2.json`: the UNSW fixed `29102`
and extensible `39102` families, \(N=2^{10},\ldots,2^{20}\), every
prefix \(d=1,\ldots,3600\), and \(\gamma_j=j^{-2}\). The evaluator
uses prime-major streaming and updates each within-column running
product once per dimension.

All twelve external input files were re-hashed before computation. The
fixed \(N=1024\) file equals the Phase-0 hash. Because the UNSW
redistribution terms remain `UNCLEAR`, vectors are not embedded in the
output; merits are keyed by source citation, source-file hash, and
generator-prefix hash.

The exact ordered schedule requires 2,517 work primes at \(N=1024\)
and rises to 3,678 at \(N=2^{20}\), plus the two universal overflow
primes. These are the shortest verified schedule prefixes satisfying
the corrected numerator bounds. The exact fidelity count is
53,767,080,345,600 modular updates.

## Preserved v1 pause

The first production attempt correctly fired its prospectively frozen
25% VPS drift alarm after 5,013,504,000 updates:

- observed aggregate throughput: 3.653536617902369 ns/update;
- frozen ceiling: 3.1034289290573425 ns/update;
- exit code: 76 (`PAUSED_THROUGHPUT_DRIFT`);
- authenticated partial chunks: 10,880;
- authenticated partial payload: 39,168,000 bytes.

No partial merit is promoted. The partial dataset remains at
`artifacts/fidelity-v1`, and its hash-chain endpoints and diagnostic
runs are banked in
`certificates/cycles-016-017-throughput-pause-v1.json`.

Same-host single-process diagnostics measured medians of 1.9371
ns/update at \(d=256\) and 2.0992 ns/update at \(d=3600\), both below
the original ceiling. This localizes the observed excess to the
production orchestration/VPS measurement rather than the frozen
modular-reduction kernel. The diagnosis is `NUMERICAL`, not a portable
performance claim.

## Human-authorized v2

After the VPS variance was identified, the user authorized relaxing
the drift rule. The amendment is versioned rather than applied in
place:

- the alert moves from +25% to +75%, or
  4.3448005006802795 ns/update;
- its boundary projects 2.704 node-days for the exact fidelity count;
- the hard seven-node-day budget is unchanged;
- the five-billion-update enforcement floor is unchanged;
- every arithmetic, input, schedule, overflow, manifest, replay, and
  oracle gate is unchanged;
- the v1 output is not resumed; v2 starts in a clean dataset.

The v2 preregistration predates its first computation. The production
run is in progress at `artifacts/fidelity-v2`. It must not be tagged
complete until the dataset is sealed, 100/100 selected-entry replays
pass, and all three frozen independent oracle checks agree.

## Claim boundary

The frozen plain `__int128` remainder kernel, compiler flags, and prime
schedule are unchanged. Throughput remains `NUMERICAL`. Chunk hashes,
manifest-chain replay, exact bounded reconstruction, and overflow-prime
agreement become `VERIFIED` only through the post-run audit.
