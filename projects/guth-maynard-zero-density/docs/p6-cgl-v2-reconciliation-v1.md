# P6 CGL-v2 Route A-v1 / Route B-v2 reconciliation

## Outcome and claim boundary

`OBSERVED`: both independent reconstructions retain the preregistered 46
canonical rows and both mandatory L12 branches. The combined disposition is
`OPEN_ANALYTIC_INPUT`, not validation or repair of Chen--Gupta--Li v2 and not
a new zero-density or short-interval theorem.

The authority is Route A-v1 and Route B-v1 together with the narrow
Route B-v2 exact-margin correction. Route B-v1 remains immutable: its
assertion `7 * 13 - 30 == 61` was true but irrelevant to the displayed
\(7/3-30/13=1/39\) margin. Route B-v2 checks
`7 * 13 - 30 * 3 == 1` without changing any row or open input.

`PROVED`, conditional only on the displayed source formulae: the reconciled
\(q_1=q\) rational/radical comparisons give margins \(1/12\),
\((\sqrt{10}-3)/3>0\), and \(1/39\). This exact algebra does not close the
source theorem.

## Retained differences and open obligations

- Route A leaves `L12.two_power` open because its source details are not
  expanded; Route B records its analogous two-power decomposition. The
  disagreement is preserved and is not promoted.
- Every preregistered open analytic obligation remains: external-input
  hypotheses, the X/T tail scope, primitive Euler-factor and conductor-sum
  transfer, and undefined `T`-smoothness. Route B additionally retains the
  unstated multiplicity convention.
- Each row stores both raw formula descriptions. Only the F09 crossings and
  F10 \(q_1=q\) comparison are string-independent exact algebra checks; no
  unproved prose normalization is claimed for the other source-trace rows.
- S01 is a whole-source identity record rather than a numerical TeX-line
  comparison; its nonnumeric locator is explicitly retained as a follow-up,
  not a source mismatch.

Paper-stage hostile audit remains deferred.

## Replay

```sh
python3 proof/p6_cgl_v2_route_b_v2_correction.py --check
python3 proof/reconcile_p6_cgl_v2_routes_v1.py --check
python3 -m unittest tests/test_p6_cgl_v2_route_b_v2_correction.py tests/test_p6_cgl_v2_reconciliation_v1.py -v
```
