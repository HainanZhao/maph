# P1R-FS two-route reconciliation v1

## Claim boundary

`PROVED`, conditional on the hash-pinned published Ingham estimate as recorded
through Huxley's restatement: two independent exact routes agree that the
frozen strict left branch has supremum \(30/13\). Consequently, within the
architecture that changes only \(\sigma\geq7/10\), no right-only replacement
can certify a strict global coefficient below \(30/13\).

This is a theorem about a deliberately narrow envelope assembly. It is not a
lower bound for the actual zero count, not saturation of the Guth--Maynard
method, not a new zero-density estimate, and not a short-interval theorem.

## Independent routes

Route A works directly in \(\sigma\), proves the positive-difference identity,
and gives an exact epsilon witness. Route B substitutes
\(\sigma=7/10-h\), clears all denominators, and uses inclusion of the retained
left image in the full spliced image. Neither route reads or names the other
route's files.

Both prove

\[
\sup_{1/2\leq\sigma<7/10}\frac3{2-\sigma}=\frac{30}{13}.
\]

The reconciled result still requires a final hostile audit before promotion
in `PLAN.md`.

## Replay

```sh
python3 proof/reconcile_p1r_fs_routes_v1.py --check
python3 -m unittest tests/test_p1r_fs_route_reconciliation_v1.py -v
```
