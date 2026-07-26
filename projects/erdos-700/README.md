# Erdős Problem 700 exploration

This project studies

\[
f(n)=\min_{1<k\le n/2}\gcd\left(n,\binom{n}{k}\right)
\]

for composite \(n\), with emphasis on exact computation, prime-power and
two-prime-factor cases, Lucas-theorem carry structure, and possible infinite
families satisfying \(f(n)>\sqrt n\).

## Layout

- `src/erdos700.py`: exact valuation and factorization routines.
- `tests/test_erdos700.py`: independent exact tests.
- `scripts/`: searches, falsifiers, and certificate generators.
- `data/`: reproducible finite scans.
- `docs/progress.md`: dated claim ledger.
- `docs/mathematics.md`: definitions and proved lemmas.
- `docs/roadmap.md`: open proof targets and standards.
- `docs/brainstorm-stage*.md`: the iterative research record.

## Quick start

Run commands from this directory:

```bash
python3 -m unittest discover -s tests -v
python3 scripts/explore.py --limit 500
python3 scripts/explore.py --limit 5000 --csv data/f_values_5000.csv
python3 scripts/scan_squarefree_triples.py --prime-limit 200
python3 scripts/analyze_2qr.py --q-limit 1000
python3 scripts/analyze_primary_pseudoperfect.py 52495396602
python3 scripts/search_power5_near_witnesses.py --max-exponent 100
python3 scripts/search_supercritical_boxes.py --max-exponent 12
python3 scripts/scan_lucas_helly.py --limit 10000
```

The Python code uses only the standard library.  The C falsifiers in
`scripts/` can be compiled independently when needed.

## Claim standard

Unbounded statements require proofs.  Finite searches are recorded as
computational observations, not extrapolated into theorems.
