# Cycle-009 premature target-scale smoke-test quarantine

Recorded at: 2026-07-29T08:36:42Z

Disposition: `QUARANTINED_NUMERICAL`; excluded from every Cycle-009 gate,
performance projection, target transcript, and paper result

## What happened

During implementation validation, the compiled scorer was invoked once
at the frozen target modulus \(N=65{,}536\), for the first verified
prime and prefix `[1]`.  This was intended only to check the executable
interface and output length, but it crossed the Cycle-019 release
boundary for target-scale arithmetic.

The command was equivalent to:

```text
compiled_candidate_scores(
    65536,
    4611685941117976577,
    3,
    [1],
)
```

The transient output contained 16,384 residues.  Its temporary file was
automatically deleted.  The console exposed:

```text
length = 16384
first residue = 2009055809193980723
elapsed = 0.17 seconds
maximum RSS = 20480 KiB
```

Source SHA-256:
`c314aa42befe7f06d5e6da636b7808fc0f8147182eeab6631083420fe59bfbe9`.

Transient binary SHA-256:
`97f0910667e874872b9638b08aa801692a14dfa586c9079b0f537c746fad6f80`.

## Contamination boundary

The invocation did **not**:

- construct or inspect any Arb score ball;
- execute a tournament comparison;
- select or record a winning component;
- measure an overlap or exact-CRT escalation;
- produce an escalation histogram;
- alter a threshold, kernel, compiler flag, or prime schedule; or
- write into the future manifested Cycle-009 target directory.

Therefore the frozen predicate
`exact_crt_resolved < 803` over 802,767 comparisons has not been
sampled.  Nevertheless the residue and timing are target-scale data and
are quarantined rather than silently relabeled as a preflight.

## Corrective action

The actual target experiment remains blocked in code on an authenticated
published-DOI certificate.  It will start after release in a fresh
directory with a new run manifest, all 40 primes, per-stage hash-chained
checkpoints, the complete Arb tournament, and exact-CRT overflow
checks.  No value or timing above may be used for capacity decisions or
reported as a Cycle-009 result.
