# Cycle 2 — Stream C two-route reconciliation v1

Claim boundary: `OBSERVED` for the full independent-route status. `PROVED`
applies to the exact agreement and the source-authority mismatch below. This
does not edit or supersede either route.

## Outcome

`PROVED`: Routes A and B agree exactly on the published boundaries
\(17/30\) (uniform) and \(2/15\) (almost all). Their preserved arithmetic
also agrees on the upper range \(y\le Z^{0.99}\), the truncations, epsilon
absorption, VK weakening, and the exceptional-set arithmetic.

`PROVED`: Route A v3 is not an independent archival formula closure. Its
replay pins only the old access ledger v1 and `errorbounds.pdf`; it does not
pin access ledger v2 or the `von-mangoldt.pdf` proof unit. Ledger v1 itself
labels archival source access `OBSERVED`. Route B v4's later CC/OCW closure
cannot retroactively change Route A v3's dependency chain.

`OBSERVED`: full independent-route Stream-C PASS is therefore **NOT PASS**.
The six Route-A formula/convention labels below remain open. This is a
source-authority coverage mismatch, not a disagreement of exponents or
secondary arithmetic.

## Preregistered coverage map

| Label | Route A v3 | Route B v4 | Reconciliation |
|---|---|---|---|
| Formula theorem, arbitrary-\(T\) range, remainder | `OBSERVED` | `PROVED` | A v3 pins v1 rather than the licensed v2 source chain. |
| Endpoint/half-weight, multiplicity, \(|\rho|\)/\(|\gamma|\) | `OBSERVED` | `PROVED` | A v3 does not pin the proof unit that proves residue multiplicity. |
| Huxley theorem/range/log\(^{44}\) loss | `PROVED` | `PROVED` | Exact common branch: \(4/5\le\sigma\le1\). |
| Ford+Platt all-height VK and \(5/7\) weakening | `PROVED` | `PROVED` | Common finite- and high-height completion. |
| Local pair kernel | `PROVED` | `PROVED` | HSW+Bui multiplicity-inclusive unit-strip path. |
| Uniform \(T\), epsilon, density supremum, upper range, error, prime conversion | `PROVED` | `PROVED` | Preserved A v1 and B v2 arithmetic agree. |
| Almost-all \(\delta,T\), epsilon, \(L^2\), remainder, Chebyshev, exceptional set, upper range, prime conversion | `PROVED` | `PROVED` | Preserved A v1 and B v2 arithmetic agree. |

`PROVED`: the exact machine record expands this table to all 28 individual
preregistration labels; every item other than the six Route-A formula labels
is closed on both paths.

## Required correction

`OBSERVED`: issue Route A v4 before reconsidering a route-level PASS. It must
pin `cycle-2-stream-c-explicit-formula-source-closure-v2.json`, both frozen
Kedlaya course PDFs, and the v2 formula-source check; its source hashes and
convention transfer must be replayed without importing Route B's closure
artifact.

## Replay

```sh
python3 projects/guth-maynard-zero-density/proof/reconcile_cycle2_stream_c_two_routes_v1.py --check projects/guth-maynard-zero-density/artifacts/cycle-2-stream-c-two-route-reconciliation-v1.json
python3 -m unittest projects/guth-maynard-zero-density/tests/test_cycle2_stream_c_two_route_reconciliation_v1.py
```
