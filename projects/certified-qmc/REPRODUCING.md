# Reproducing one certified entry

This walkthrough verifies one exact fidelity-table entry without
trusting a printed decimal merit. It authenticates the run metadata and
chunk manifest, reads only the residue chunks covering the selected
dimension, performs bounded balanced CRT reconstruction, and checks
both universal overflow primes.

The release does not redistribute the upstream UNSW generating
vectors. Each table entry is instead keyed by the upstream citation,
the frozen source-file SHA-256, the entry index, and the
generator-prefix SHA-256.

## 1. Build the frozen evaluator and verify the prime schedule

From the released source directory:

```bash
make -C production
python3 scripts/verify_prime_schedule_v1.py \
  --schedule data/primes-schedule-v1.json \
  --output /tmp/certified-qmc-prime-verification.json \
  --skip-regeneration
```

The schedule verifier independently checks all 3,740 N−1
certificates. The production binary must link only the system C runtime;
the release graph contains no FFTW.

## 2. Authenticate and reconstruct one entry

Assuming the fidelity dataset archive was extracted as
`tables/fidelity-v2`, run:

```bash
bin/verify-entry \
  --dataset tables/fidelity-v2 \
  --table unsw-fixed-29102-n1024-j2 \
  --N 1024 \
  --d 16
```

A successful result has:

- `status: VERIFIED`;
- the frozen generator-prefix SHA-256;
- the proved integer-numerator bound;
- the uniquely reconstructed scaled and reduced exact rational;
- two overflow checks with `equal: true`; and
- the exact fraction of dataset payload touched.

The command does not turn the merit into an error bound for an arbitrary
integrand. It certifies the selected lattice rule’s squared
shift-averaged worst-case error in the frozen product-weight,
Bernoulli-\(B_2\) convention.

## 3. Check the keyed upstream vector

For the example above, retrieve the vector from its cited publisher and
verify its frozen hash:

```bash
curl -fL \
  https://web.maths.unsw.edu.au/~fkuo/lattice/lattice-29102-1024.3600 \
  -o lattice-29102-1024.3600
sha256sum lattice-29102-1024.3600
```

The required digest is recorded in `table-index.json` and
`run-manifest.json`. The first 16 components, serialized as canonical
compact JSON, must hash to the `generator_prefix_sha256` reported by
`verify-entry`.

## 4. Replay the release tests

The Arb-dependent tests use the pinned environment:

```bash
python3 -m venv .venv
.venv/bin/pip install -r requirements-arb.txt
.venv/bin/python -m unittest discover -s tests -v
```

Tags retain their strict meanings:

- `VERIFIED`: exact arithmetic or replayed hash/certificate predicate;
- `ENCLOSED`: rigorous Arb ball;
- `NUMERICAL`: floating-point measurement or cross-check;
- `CONJECTURAL`: unproved research claim.
